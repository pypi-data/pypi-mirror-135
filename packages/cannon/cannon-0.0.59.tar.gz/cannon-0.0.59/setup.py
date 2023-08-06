# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cannon']

package_data = \
{'': ['*']}

install_requires = \
['arrow==1.2.1',
 'exscript==2.6.3',
 'loguru==0.5.3',
 'textfsm==1.1.2',
 'traits==6.3.2']

setup_kwargs = {
    'name': 'cannon',
    'version': '0.0.59',
    'description': 'An SSH automation tool based on Exscript',
    'long_description': '# Introduction\n\n[cannon][1] is a wrapper around [exscript][2] to connect with remote server or network \ndevices with ssh.\n\n\n## Example Usage - Cisco IOS\n\nThis script will login, run a few show commands\n\n```python\nimport sys\n\nfrom cannon import Shell, Account\nfrom loguru import logger\n\nlog_stderr_id = logger.add(sink=sys.stderr)\n\n@logger.catch(default=True, onerror=lambda _: sys.exit(1))\ndef main():\n    sess = Shell(\n        host=\'route-views.routeviews.org\',\n        # route-views doesn\'t need password\n        account= Account(name=\'rviews\', password=\'\'),\n        debug=0,\n        json_logfile=\'/tmp/cmd_log.json\',\n        )\n\n    sess.execute(\'term len 0\')\n\n    sess.execute(\'show clock\')\n\n    sess.execute(\'show version\')\n    version_text = sess.response\n\n    # template is a TextFSM template\n    values = sess.execute(\'show ip int brief\',\n        template="""Value INTF (\\S+)\\nValue IPADDR (\\S+)\\nValue STATUS (up|down|administratively down)\\nValue PROTO (up|down)\\n\\nStart\\n  ^${INTF}\\s+${IPADDR}\\s+\\w+\\s+\\w+\\s+${STATUS}\\s+${PROTO} -> Record""")\n    print("VALUES "+str(values))\n    sess.close()\n```\n\n## Example Usage - Linux\n\n```python\nfrom getpass import getpass\nimport sys\n\nfrom cannon.main import Shell, Account\n\nlog_stderr_id = logger.add(sink=sys.stderr)\n\n@logger.catch(default=True, onerror=lambda _: sys.exit(1))\ndef main():\n    account = Account("mpenning", getpass("Login password: "))\n    conn = Shell(host="127.0.0.1", port=22, account=account, driver="generic", debug=0)\n    assert conn is not None\n    example_tfsm_template = """Value UNAME_LINE (.+)\n\nStart\n  ^${UNAME_LINE}\n"""\n    print(conn.execute("sudo uname -a", debug=0, template=example_tfsm_template, timeout=2))\n    print(conn.execute("whoami", debug=0, template=None, timeout=2))\n    #print("FOO2", conn.response)\n    conn.close(force=True)\n\nif __name__=="__main__":\n    main()\n```\n\n## Example test suite setup\n\n- `git clone git@github.com:knipknap/Exscript`\n- `cd` into `Exscript/tests/Exscript/protocols` and `chmod 600 id_rsa`\n- exscript spawns a local tests ssh daemon, `pytest Exscript/tests/Exscript/protocols/SSH2Test.py`\n- Connect with `ssh -i id_rsa -p 1236 user@localhost`\n- one command is supported: `ls`\n\n  [1]: https://pypi.python.org/pypi/cannon    # cannon on pypi\n  [2]: https://pypi.python.org/pypi/exscript  # Exscript on pypi\n',
    'author': 'Mike Pennington',
    'author_email': 'mike@pennington.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mpenning/cannon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
