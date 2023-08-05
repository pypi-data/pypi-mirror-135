# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_terraform']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=0.10.0',
 'portalocker>=1.7.0',
 'pytest-xdist>=1.31.0',
 'pytest>=6.0']

entry_points = \
{'pytest11': ['terraform = pytest_terraform.plugin']}

setup_kwargs = {
    'name': 'pytest-terraform',
    'version': '0.6.1',
    'description': 'A pytest plugin for using terraform fixtures',
    'long_description': '# Introduction\n\n[![CI](https://github.com/cloud-custodian/pytest-terraform/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/cloud-custodian/pytest-terraform/actions?query=branch%3Amaster)\n[![codecov](https://codecov.io/gh/cloud-custodian/pytest-terraform/branch/master/graph/badge.svg)](https://codecov.io/gh/cloud-custodian/pytest-terraform)\n\npytest_terraform is a pytest plugin that enables executing terraform\nto provision infrastructure in a unit/functional test as a fixture.\n\nThis plugin features uses a fixture factory pattern to enable paramterized\nconstruction of fixtures via decorators.\n\n## Usage\n\npytest_terraform provides a `terraform` decorator with the following parameters:\n\n| Argument             | Required? | Type    | Default      | Description |\n| -----                | :---:     | ---     | ---          | ---         |\n| `terraform_dir`      | yes       | String  |              | Terraform module (directory) to execute. |\n| `scope`              | no        | String  | `"function"` | [Pytest scope](https://docs.pytest.org/en/stable/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session) - should be one of: `function`, or `session`. Other scopes like  `class`, `module`, and `package` should work but have not been fully tested. |\n| `replay`             | no        | Boolean | `True`       | Use recorded resources instead of invoking terraform. See [Replay Support](#replay-support) for more details. |\n| `name`               | no        | String  | `None`       | Name used for the fixture. This defaults to the `terraform_dir` when `None` is supplied. |\n| `teardown`           | no        | String  | `"default"`  | Configure which teardown mode is used for terraform resources. See [Teardown Options](#teardown-options) for more details. |\n\n### Example\n\n```python\nfrom boto3 import Session\nfrom pytest_terraform import terraform\n\n\n# We use the terraform decorator to create a fixture with the name of\n# the terraform module.\n#\n# The test function will be invoked after the terraform module is provisioned\n# with the results of the provisioning.\n#\n# The module `aws_sqs` will be searched for in several directories, the test\n# file directory, a sub directory `terraform`.\n#\n# This fixture specifies a session scope and will be run once per test run.\n#\n@terraform(\'aws_sqs\', scope=\'session\')\ndef test_sqs(aws_sqs):\n    # A test is passed a terraform resources class containing content from\n    # the terraform state file.\n    #\n    # Note the state file contents may vary across terraform versions.\n    #\n    # We can access nested datastructures with a jmespath expression.\n    assert aws_sqs["aws_sqs_queue.test_queue.tags"] == {\n        "Environment": "production"\n    }\n   queue_url = aws_sqs[\'test_queue.queue_url\']\n   print(queue_url)\n\n\ndef test_sqs_deliver(aws_sqs):\n   # Once a fixture has been defined with a decorator\n   # it can be reused in the same module by name, with provisioning\n   # respecting scopes.\n   #\n   sqs = Session().client(\'sqs\')\n   sqs.send_message(\n       QueueUrl=aws_sqs[\'test_queue.queue_url\'],\n       MessageBody=b"123")\n\n\n@terraform(\'aws_sqs\')\ndef test_sqs_dlq(aws_sqs):\n   # the fixture can also referenced again via decorator, if redefined\n   # with decorator the fixture parameters much match (ie same session scope).\n\n   # Module outputs are available as a separate mapping.\n   aws_sqs.outputs[\'QueueUrl\']\n```\n\n*Note* the fixture name should match the terraform module name\n\n*Note* The terraform state file is considered an internal\nimplementation detail of terraform, not per se a stable public interface\nacross versions.\n\n## Marks\n\nAll tests using terraform fixtures have a `terraform` mark applied so\nthey can be run/selected via the command line ie.\n\n```shell\npytest -k terraform tests/\n```\n\nto run all terraform tests only. See pytest mark documentation for\nadditional details, https://docs.pytest.org/en/stable/example/markers.html#mark-examples\n\n\n## Options\n\nYou can provide the path to the terraform binary else its auto discovered\n```shell\n--tf-binary=$HOME/bin/terraform\n```\n\nTo avoid repeated downloading of plugins a plugin cache dir is utilized\nby default this is `.tfcache` in the current working directory.\n```shell\n--tf-plugin-dir=$HOME/.cache/tfcache\n```\n\nTerraform modules referenced by fixtures are looked up in a few different\nlocations, directly in the same directory as the test module, in a subdir\nnamed terraform, and in a sibling directory named terraform. An explicit\ndirectory can be given which will be looked at first for all modules.\n\n```shell\n--tf-mod-dir=terraform\n```\n\nThis plugin also supports flight recording (see next section)\n```shell\n--tf-replay=[record|replay|disable]\n```\n\n### Teardown Options\n\n`pytest_terraform` supports three different teardown modes for the terraform decorator.\nThe default, `pytest_terraform.teardown.ON` will always attempt to teardown any and all modules via `terraform destory`.\nIf for any reason destroy fails it will raise an exception to alert the test runner.\nThe next mode, `pytest_terraform.teardown.IGNORE`, will invoke `terraform destroy` as with `teardown.ON` but will ignore any failures.\nThis mode is particularly help if your test function performs destructive actions against any objects created by the terraform module.\nThe final option is `pytest_terraform.teardown.OFF` which will remove the teardown method register all together.\nThis should generally only be used in very specific situations and is considered an edge case.\n\nThere is a special `pytest_terraform.teardown.DEFAULT` which is what the `teardown` parameter actually defaults to.\n\nTeardown options are available, for convenience, on the terraform decorator.\nFor example, set teardown to ignore:\n\n```python\nfrom pytest_terraform import terraform\n\n\n@terraform(\'aws_sqs\', teardown=terraform.TEARDOWN_IGNORE)\ndef test_sqs(aws_sqs):\n    assert aws_sqs["aws_sqs_queue.test_queue.tags"] == {\n        "Environment": "production"\n    }\n   queue_url = aws_sqs[\'test_queue.queue_url\']\n   print(queue_url)\n```\n\n## Hooks\n\npytest_terraform provides hooks via the pytest hook implementation.\nHooks should be added in the `conftest.py` file.\n\n### `pytest_terraform_modify_state`\n\nThis hook is executed after state has been captured from terraform apply and before writing to disk.\nThis hook does not modify state that\'s passed to the function under test.\nThe state is passed as the kwarg `tfstate` which is a `TerraformStateJson` UserString class with the following methods and properties:\n\n- `TerraformStateJson.dict` - The deserialized state as a dict\n- `TerraformStateJson.update(state: str)` - Replace the serialized state with a new state string\n- `TerraformStateJson.update_dict(state: dict)` - Replace the serialized state from a dictionary\n\n#### Example\n\n```python\ndef pytest_terraform_modify_state(tfstate):\n    print(str(tfstate))\n```\n\n#### Example AWS Account scrub\n\n```python\nimport re\n\ndef pytest_terraform_modify_state(tfstate):\n    """ Replace potential AWS account numbers with \'REDACTED\' """\n    tfstate.update(re.sub(r\'([0-9]+){12}\', \'REDACTED\', str(tfstate)))\n```\n\n## Flight Recording\n\nThe usage/philosophy of this plugin is based on using flight recording\nfor unit tests against cloud infrastructure. In flight recording rather\nthan mocking or stubbing infrastructure, actual resources are created\nand interacted with with responses recorded, with those responses\nsubsequently replayed for fast test execution. Beyond the fidelity\noffered, this also enables these tests to be executed/re-recorded against\nlive infrastructure for additional functional/release testing.\n\nhttps://cloudcustodian.io/docs/developer/tests.html#creating-cloud-resources-with-terraform\n\n### Replay Support\n\nBy default fixtures will save a `tf_resources.json` back to the module\ndirectory, that will be used when in replay mode.\n\nReplay can be configured by passing --tf-replay on the cli or via pytest config file.\n\n### Recording\n\nPassing the fixture parameter `replay` can control the replay behavior on an individual\ntest. The default is to operate in recording mode.\n\n@terraform(\'file_example\', replay=False)\ndef test_file_example(file_example):\n    assert file_example[\'local_file.bar.content\'] == \'bar!\'\n\n\n## XDist Compatibility\n\npytest_terraform supports pytest-xdist in multi-process (not distributed)\nmode.\n\nWhen run with python-xdist, pytest_terraform treats all non functional\nscopes as per test run fixtures across all workers, honoring their\noriginal scope lifecycle but with global semantics, instead of once\nper worker (xdist default).\n\nTo enable this the plugin does multi-process coodination using lock\nfiles, a test execution log, and a dependency mapping of fixtures\nto tests. Any worker can execute a module teardown when its done executing\nthe last test that depends on a given fixture. All provisioning and\nteardown are guarded by atomic file locks in the pytest execution\'s temp\ndirectory.\n\n### Root module references\n\n`terraform_remote_state` can be used to introduce a dependency between\na scoped root modules on an individual test, note we are not\nattempting to support same scope inter fixture dependencies as that\nimposes additional scheduling constraints outside of pytest native\ncapabilities. The higher scoped root module (ie session or module scoped)\nwill need to have output variables to enable this consumption.\n',
    'author': 'Kapil Thangavelu',
    'author_email': 'kapilt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cloud-custodian/pytest-terraform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
