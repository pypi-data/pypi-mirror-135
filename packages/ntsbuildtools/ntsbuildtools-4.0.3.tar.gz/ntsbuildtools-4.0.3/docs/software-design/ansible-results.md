Processing the results of an Ansible Playbook execution has some difficulties. 


## Assumptions

1. We ingest JSON results, using ['Ansible screen output as JSON' callback](https://docs.ansible.com/ansible/2.9/plugins/callback/json.html)
    * Warning: At this time this feature is in 'preview.' Specifically note that: *"This callback is not guaranteed to have a backwards compatible interface."*


## Ansible Playbook Results explained

Our data structure will (roughly) align with the structure of the data as it is provided by Ansible: 
there is a `playbook` that contains a collection of `tasks`, and each `task` is executed against a collection of `hosts`.
An example of the 'playbook result output' looks like the following:   

* Playbook
  * Task 1
    * Host A Result 
    * Host B Result
    * Host C Result
  * Task 2
    * Host A Result
    * Host C Result

> 'Playbook' contains 'Tasks', while 'Tasks' contain 'Host Results'.

### Goal of PlaybookResults data structure

We need a data structure that makes it easier to produce a 'useful report' of the Playbook results.

Our 'useful report' should first report on any **failures**. 
If there are not any **failures**, then instead the report should show any *relevant* **diffs** that were produced by the Playbook.

Concretely, our Playbook Result data structure should support the following functionality:

1. Iterate over all the 'Host Results' that indicate some **failure**.
    * Should be sorted by the original 'order of execution'.
2. Iterate over all 'Host Results' of a particular 'Task' (by task name).
    * Should be sorted by the original 'order of execution'. 
3. Infer the 'Task Name(s)' that execute a particular 'module' (by module name).
    * E.g. For the `junos_ansible` solution, we want to display all of the 'Host Results' that are associated to the Task that executes the [`junos_config` module](https://docs.ansible.com/ansible/latest/collections/junipernetworks/junos/junos_config_module.html).

This Playbook Result data structure is a simple 'Collection' with some filtering functionality.
However, how we actually parse the **failure** and **diff** out from the 'Host Results' still needs to be determined.
Those details are discussed below.

## Ansible Task 'Return Values' explained

To support our top-level goals for the Playbook Result data structure, we need to process each Ansible 'Host Result' to produce either a **failure** or **diff** message.
So, we need to investigate [Ansible's Return Values](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html) to determine how to *consistently* extract **diffs** and **failures**.

Unfortunately, the structure and format of Ansible's Return Values are quite variable.
Lets look at examples of what the JSON "Return Value" data looks like for some tasks that we are interested in.

> *JSON output for a failed `junos_facts` task (Authentication Failed).*
    
    "hosts": {
        "ah-ldr1-gw.net.uoregon.edu": {
            "_ansible_no_log": false,
            "action": "junos_facts",
            "changed": false,
            "failed": true,
            "invocation": {
                ... omitted for brevity...
            },
            "msg": "AuthenticationException('Authentication failed.')"
        },
        "cc-ldr1-gw.net.uoregon.edu": {
            ... omitted for brevity...
        },
        "task": {
            "duration": {
                "end": "2021-09-28T20:32:45.965906Z",
                "start": "2021-09-28T20:32:44.126224Z"
            },
            "id": "00155dda-16a5-d4bd-866e-000000000047",
            "name": "juniper : get junos facts"
        }
    }

> *JSON output for a successful `junos_config` task.*

    "hosts": {
        "cc-9-7-xs-leaf1.net.uoregon.edu": {
            "_ansible_no_log": false,
            "action": "junos_config",
            "changed": true,
            "diff": {
                "prepared": "[edit system login]\n+    user netmaint {\n+        uid 2000;\n+        class super-user;\n... shortened for brevity..."
            },
            "invocation": {
                ... omitted for brevity...
            },
            "warnings": [
                "mgd: statement has no contents; ignored"
            ]
        }
        "cc-9-7-border-leaf1.net.uoregon.edu": {
            ... omitted for brevity...
        },
    },
    "task": {
        "duration": {
            "end": "2021-03-18T20:57:27.925459Z",
            "start": "2021-03-18T20:57:24.531996Z"
        },
        "id": "00505680-fffe-6032-5e88-000000000064",
        "name": "apply templated configuration to juniper device"
    }

> *JSON output for a failed `junos_config` task (Module Failure).*

    "hosts": {
        "emu-cdr1-gw.net.uoregon.edu": {
            "_ansible_no_log": false,
            "action": "junos_config",
            "changed": false,
            "exception": "Traceback (most recent call last):\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/module_utils/network/common/netconf.py\", line 83, in parse_rpc_error\n  File \"src/lxml/etree.pyx\", line 3213, in lxml.etree.fromstring\n  File \"src/lxml/parser.pxi\", line 1876, in lxml.etree._parseMemoryDocument\n  File \"src/lxml/parser.pxi\", line 1764, in lxml.etree._parseDoc\n  File \"src/lxml/parser.pxi\", line 1126, in lxml.etree._BaseParser._parseDoc\n  File \"src/lxml/parser.pxi\", line 600, in lxml.etree._ParserContext._handleParseResultDoc\n  File \"src/lxml/parser.pxi\", line 710, in lxml.etree._handleParseResult\n  File \"src/lxml/parser.pxi\", line 639, in lxml.etree._raiseParseError\n  File \"<string>\", line 1\nlxml.etree.XMLSyntaxError: Start tag expected, '<' not found, line 1, column 1\n\nDuring handling of the above exception, another exception occurred:\n\nTraceback (most recent call last):\n  File \"/home/ctrown/.ansible/tmp/ansible-local-7734tgh0ofwi/ansible-tmp-1624309204.8872814-23352-51114633116966/AnsiballZ_junos_config.py\", line 102, in <module>\n    _ansiballz_main()\n  File \"/home/ctrown/.ansible/tmp/ansible-local-7734tgh0ofwi/ansible-tmp-1624309204.8872814-23352-51114633116966/AnsiballZ_junos_config.py\", line 94, in _ansiballz_main\n    invoke_module(zipped_mod, temp_path, ANSIBALLZ_PARAMS)\n  File \"/home/ctrown/.ansible/tmp/ansible-local-7734tgh0ofwi/ansible-tmp-1624309204.8872814-23352-51114633116966/AnsiballZ_junos_config.py\", line 40, in invoke_module\n    runpy.run_module(mod_name='ansible.modules.network.junos.junos_config', init_globals=None, run_name='__main__', alter_sys=True)\n  File \"/usr/lib/python3.6/runpy.py\", line 205, in run_module\n    return _run_module_code(code, init_globals, run_name, mod_spec)\n  File \"/usr/lib/python3.6/runpy.py\", line 96, in _run_module_code\n    mod_name, mod_spec, pkg_name, script_name)\n  File \"/usr/lib/python3.6/runpy.py\", line 85, in _run_code\n    exec(code, run_globals)\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/modules/network/junos/junos_config.py\", line 483, in <module>\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/modules/network/junos/junos_config.py\", line 447, in main\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/modules/network/junos/junos_config.py\", line 363, in configure_device\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/module_utils/network/junos/junos.py\", line 251, in load_config\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/module_utils/network/common/netconf.py\", line 76, in __rpc__\n  File \"/tmp/ansible_junos_config_payload_cttqvfil/ansible_junos_config_payload.zip/ansible/module_utils/network/common/netconf.py\", line 108, in parse_rpc_error\nansible.module_utils.connection.ConnectionError: b'error: number of AE devices configured 71 is more than device-count 63.\\nerror: configuration check-out failed'\n",
            "failed": true,
            "module_stderr": "... omitted for brevity (value was identical to the 'exception' property above)...",
            "module_stdout": "",
            "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error",
            "rc": 1
        },
        "oh-cdr1-gw.net.uoregon.edu": {
            ... omitted for brevity...
        }
    },
    "task": {
        "duration": {
            "end": "2021-06-21T21:00:10.793662Z",
            "start": "2021-06-21T21:00:04.468408Z"
        },
        "id": "989096dd-8ab4-e598-c8c5-00000000006d",
        "name": "apply templated configuration to juniper device"
    }

Unfortunately, when we drill into that per-host 'Return Values object', the provided properties vary.
See the table below that compares the Return Values from these examples:

> *Table: Comparison of per-host 'Return Values'.*

|Return Values      | Successful `junos_config` | `junos_config` Module Failure | `junos_fact` Authentication Failed    |
|-------------------|---------------------------|-------------------------------|---------------------------------------|
|**action**         | x                         | x                             | x                                     |
|**changed**        | x                         | x                             | x                                     |
|**invocation**     | x                         |                               | x                                     |
|**diff**           | x                         |                               |                                       |
|**warnings**       | x                         |                               |                                       |
|**failed**         |                           | x                             | x                                     |
|**msg**            |                           | x                             | x                                     |
|**exception**      |                           | x                             |                                       |
|**module_stderr**  |                           | x                             |                                       |
|**module_stdout**  |                           | x                             |                                       |
|**rc**             |                           | x                             |                                       |

From our examples, we can infer that the **per-host 'Return Value object' *changes* depending on *many* factors.**
So, we will be handling several 'Return Value objects' that do NOT have a standard structure.

### Goals for processing Ansible Return Values

We want to ingest the various raw 'Return Values' and produce a standardized `TaskResult` data structure.
So, what is needed in the `TaskResult` data structure?
More specifically, what is needed to enable the functionality needed by our `PlaybookResults` data structure?
I think that this is a minimal set of attributes that are required:

    TaskResult
      ansible_module: str
      task_name: str
      host_name: str
      failed: bool
      error_or_diff_message: str

We now have an idea of what is needed in our `TaskResult` objects.
However, we don't know where do we put the responsibility of parsing the 'raw Return Values' (JSON) into these objects.

We do know that the 'Return Values' (JSON) are implemented per-ansible-module.
So, it is logical to separate our parsing-logic by ansible-module.

### ReturnValues solution

> Implementation: See the `ntsbuildtools.ansible.return_values` package.

We use a `ReturnValues` class to define our interactions with the "raw Return Values".
The `ntsbuildtools.ansible.return_values` package contains a default `ReturnValues` class in `default.py`.:
* `ReturnValues` objects must provide the `pretty_error` and `pretty_diff` methods.
* `ReturnValues` objects are constructed given only the 'raw Return Values' (JSON).

Logic for getting the `pretty_error` or `pretty_diff` may be distinct **per Ansible Module**.
So, there is a Factory for creating various `ReturnValues` objects based on ansible module name.
That Factory can register any number of `ReturnValues` subclasses.

> Note: We create the `ReturnValues` subclasses as-needed.

Conceptually, there will be one `ReturnValues` subclass per Ansible Module.
For now, we have one prime example that is worth reviewing: 

* `JunosConfigReturnValues` class parses the raw Return Values from [junos_config Ansible Module](https://docs.ansible.com/ansible/latest/collections/junipernetworks/junos/junos_config_module.html#return-values).
