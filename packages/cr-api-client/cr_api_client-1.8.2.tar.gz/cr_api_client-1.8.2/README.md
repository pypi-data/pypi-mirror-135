# AMOSSYS Cyber Range client API

## Installation

Note: it is recommanded to install the package in a virtualenv in order to avoid conflicts with version dependencies of other packages.

```sh
python3 setup.py install
```

## Configuration

Access to the Cyber Range is possible with either of the following configuration methods.

### Configuration through configuration file (CLI only)

It is possible to configure access to the Cyber Range through a configuration file, specified with the `--config` command line parameter:

```sh
$ cyber_range --help
(...)
--config CONFIG       Configuration file
(...)
```

Configuration file content should be of the form `--key = value` (without quotes in values), as in the following exemple:

```
[DEFAULT]
--core-url = https://[CORE-URL-API]
--scenario-url = https://[SCENARIO-URL-API]
--provisioning-url = https://[PROVISIONING-URL-API]
--redteam-url = https://[REDTEAM-URL-API]
--cacert = <PATH TO CA CERT>
--cert = <PATH TO CLIENT CERT>
--key = <PATH TO CLIENT PRIVATE KEY>
```

### Configuration through command line arguments (CLI only)

It is possible to configure access to the Cyber Range through command line arguments. See `cyber_range --help` command line output for available parameters:

```sh
$ cyber_range --help
(...)
  --core-url CORE_API_URL
                        Set core API URL (default: 'http://127.0.0.1:5000')
  --scenario-url SCENARIO_API_URL
                        Set scenario API URL (default: 'http://127.0.0.1:5002')
  --provisioning-url PROVISIONING_API_URL
                        Set provisioning API URL (default: 'http://127.0.0.1:5003')
  --redteam-url REDTEAM_API_URL
                        Set redteam API URL (default: 'http://127.0.0.1:5004')
  --cacert CACERT       Set path to CA certs
  --cert CERT           Set path to client cert
  --key KEY             Set path to client key
```

### Configuration through programmatic means

It is possible to configure access to the Cyber Range programmatically in Python:

```python
import cr_api_client.core_api as core_api
import cr_api_client.scenario_api as scenario_api
import cr_api_client.provisioning_api as provisioning_api
import cr_api_client.redteam_api as redteam_api

# Set URL API
core_api.CORE_API_URL = "https://[CORE-URL-API]"
scenario_api.SCENARIO_API_URL = "https://[SCENARIO-URL-API]"
provisioning_api.PROVISIONING_API_URL = "https://[PROVISIONING-URL-API]"
redteam_api.REDTEAM_API_URL = "https://[REDTEAM-URL-API]"

# Set server and client certificates for Core API
core_api.CA_CERT_PATH = <PATH TO CA CERT>
core_api.CLIENT_CERT_PATH = <PATH TO CLIENT CERT>
core_api.CLIENT_KEY_PATH = <PATH TO CLIENT PRIVATE KEY>

# Apply same server and client certificates to other API
redteam_api.CA_CERT_PATH = provisioning_api.CA_CERT_PATH = scenario_api.CA_CERT_PATH = core_api.CA_CERT_PATH
redteam_api.CLIENT_CERT_PATH = provisioning_api.CLIENT_CERT_PATH = scenario_api.CLIENT_CERT_PATH = core_api.CLIENT_CERT_PATH
redteam_api.CLIENT_KEY_PATH = provisioning_api.CLIENT_KEY_PATH = scenario_api.CLIENT_KEY_PATH = core_api.CLIENT_KEY_PATH
```

## CLI usage

See `cyber_range --help` command line output for available parameters:

```sh
$ cyber_range --help
(...)
```

## Programmatic usage

### Platform initialization API

Before starting a new simulation, the platform has to be initialized:

```python
core_api.reset()
redteam_api.reset_redteam()
```

### Simulation API

```python
# Create a simulation from a topology
core_api.create_simulation_from_topology(topology_file: str)

# Create a simulation from a basebox ID
core_api.create_simulation_from_basebox(basebox_id: str)

# Start the simulation, with current time (by default) or time where the VM was created (use_vm_time=True)
core_api.start_simulation(id_simulation: int, use_vm_time: bool)

# Pause a simulation (calls libvirt suspend API)
core_api.pause_simulation(id_simulation: int)

# Unpause a simulation (calls libvirt resume API)
core_api.unpause_simulation(id_simulation: int)

# Properly stop a simulation, by sending a shutdown signal to the operating systems
core_api.halt_simulation(id_simulation: int)

# Stop a simulation through a hard reset
core_api.destroy_simulation(id_simulation: int)

# Clone a simulation and create a new simulation, and return the new ID
core_api.clone_simulation(id_simulation: int) -> int

# Mirror all network traffic through a local network interface
core_api.tap_simulation(id_simulation: int, iface: str)

# Stop mirroring all network traffic
core_api.untap_simulation(id_simulation: int, iface: str)

# Delete a simulation in database
core_api.delete_simulation(id_simulation: int)
```

### Provisioning API

```python
# Apply provisioning configuration defined in YAML file on simulation defined in argument ID OR on machines defined in file
# ``wait`` parameter defines if the function wait for task to complete or not.

provisioning_execute(id_simulation: int = None,
                     machines_file: str = None,
                     provisioning_file: str,
                     debug: bool = False,
                     wait: bool = True,
                     ) -> Tuple[bool, str]:

# Apply ansible playbooks on specified target(s):
# ``wait`` parameter defines if the function wait for task to complete or not.

def provisioning_ansible(id_simulation: int = None,
                         machines_file: str = None,
                         playbook_path: str = None,
                         target_roles: List[str] = [],
                         target_system_types: List[str] = [],
                         target_operating_systems: List[str] = [],
                         target_names: List[str] = [],
                         extra_vars: str = None,
                         debug: bool = False,
                         wait: bool = True,
                         ) -> Tuple[bool, str]:

# Get status on targeted simulation
provisioning_api.provisioning_status(id_simulation: int)

# Get provisioning result on targeted simulation
provisioning_api.provisioning_result(id_simulation: int)
```

### Scenario API

```python
scenario_api.scenario_play(id_simulation: int, scenario_path: str,
                              debug_mode: str = 'off', speed: str = 'normal',
                              scenario_file_results: str = None)
```

This method makes it possible to play  scenario defined in ``scenario path`` on simulation defined in ``id_simulation``.
These parameters are **mandatory**.

The following parameters are optional:

* ``debug_mode``: This parameter has to be used for **debug** only. It corresponds to the level of verbosity of the debug traces generated during the execution of user actions:
  * ``'off'``: no debug traces,
  * ``'on'``:  with debug traces,
  * ``'full'``: with maximum debug traces.

  The default is ``'off'``. Debug traces are generated **on the server side only**.

* ``speed``: This parameter affects the speed of typing keys on the keyboard and the speed of mouse movement:
  * ``'slow'``: slow speed,
  * ``'normal'``:  normal speed,
  * ``'fast'``: fast speed.

  The default is ``'normal'``.

* ``scenario_file_results``: This parameter makes it possible to get the scenario results (of user actions) in a file.
  Results are stored using a json format. The file name should be absolute (``'/tmp/results.json'`` for example).

  Here an example:

  ```json
  {
    "success": true,
    "scenario_results": [
        {
            "name": "scenario.py",
            "success": true,
            "target": {
                "name": "CLIENT1",
                "role": "client",
                "basebox_id": 70,
                "ip_address": "localhost",
                "vnc_port": 5901
            },
            "action_packs": {
                "operating_system": "operating_system/windows7"
            },
            "action_list": [
                {
                    "name": "open_session",
                    "parameters": {
                        "password": "7h7JMc67",
                        "password_error": "false",
                        "login": "John"
                    },
                    "start_time": "2021-03-01 12:39:25.119",
                    "end_time": "2021-03-01 12:39:57.325",
                    "success": true,
                    "implemented": true
                },
                {
                    "name": "close_session",
                    "parameters": {},
                    "start_time": "2021-03-01 12:40:02.330",
                    "end_time": "2021-03-01 12:40:09.303",
                    "success": true,
                    "implemented": true
                }
            ]
        }
    ]
  }
  ```

Here are some examples of calling this method:

```python
scenario_api.scenario_play(1, './scenarios/my_scenario') # this is the common way

scenario_api.scenario_play(1, './scenarios/my_scenario', scenario_file_results='/tmp/results.json')

scenario_api.scenario_play(1, './scenarios/my_scenario', debug_mode='full', speed='fast')
```

### Redteam API

```python
redteam_api.execute_scenario(attack_list: str)
```

This method executes sequentially each attack in list.
For each attack this method displays started time and ending time (last_update).

```python
redteam_api.execute_attack_name(attack_name: str,  waiting_worker: bool = True)
```

This method execute one attack, selected by name. 

```python
def init_knowledge(data: List[dict])
```

Load data into knowledge database.

Example :
```
[
  {"software": 
    {"host_ip": "192.168.33.11", 
    "software": {"category": "os"}, 
    "credentials":[{"username": "Administrateur", "password": "Beezh35;"}]
    }
  }
]
```

```python
def attack_infos(id_attack: str)
```

Get status and output for attack.

Example :
```
status = "success",
output = [
  {
  "attack_session": {
   "idAttackSession": 1,
   "source": "vffxlcationgreedinessb.com",
   "type": "powershell",
   "identifier": "d67672cb-8f64-420a-a7ba-1d33d7b7fd45",
   "privilege_level": 1,
   "idHost": 1
  }
 }
]

```

```python
redteam_api.list_workers()
```

This method list all workers availabe in platform.
List of attributes :
* stability
* reliability
* side_effect
* killchain_step : step in MITRE ATT&CK killchain

```json
{
  "worker_id":"1548_002_001",
  "name":"uac_bypass",
  "description":"Use Metasploit uac bypass",
  "stability":"CRASH_SAFE",
  "reliability":"ALWAYS",
  "side_effect":"NETWORK_CONNECTION",
  "killchain_step":"privilege_escalation",
  "repeatable":false
}
```


```python
redteam_api.list_attacks()
```

This method return all attack (available, successed or failed) with time information and origin.
List of attributes :
* idAttack : Identifier for attack action
* status : Attack status (failed, success or runnable)
* created_date
* started_date
* last_update : End time
* values : Values send to the worker
* output : Data generated by this attack
* source: idAttack that created it

Here an example :
```json
{
  "idAttack":13,
  "worker":
  {
    "worker_id":"1548_002_001",
    "name":"uac_bypass",
    "description":"Use Metasploit uac bypass",
    "stability":"FIRST_ATTEMPT_FAIL",
    "reliability":"ALWAYS",
    "side_effect":"NETWORK_CONNECTION",
    "killchain_step":"privilege_escalation",
    "repeatable":false
    },
  "status":"success",
  "created_date":"2021-04-21 10:33:00",
  "started_date":"2021-04-21 10:37:04",
  "last_update":"2021-04-21 10:37:06",
  "values":"{\"Host.ip\": \"192.168.2.101\", \"AttackSession.type\": \"windows/x64/meterpreter/reverse_tcp\", \"AttackSession.source\": \"192.168.2.66\", \"AttackSession.identifier\": \"1\"}",
  "output": "",
  "source":1}
```


*In progress*
