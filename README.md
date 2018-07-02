Zabbix Helpers To Fetch Mikrotik's Counters via API
---------------------------------------------------

These scripts rely on [PyPi librouteros library].

## Installation

In the example below we use a template which monitors the single Mikrotik Node. If you want to minitor several Mikrotiks 
from a single zabbix_agent - you can fetch the concept and clone the items for several Mikrotiks.

The concept is:
1. We define **mikrotik.api.discovery** item (manually or using the template) on the node with `zabbix_agentd` available. 
  The item accepts a couple of parameters
2. We define **mikrotik.api.discovery** in `zabbix_agentd` configuration file
3. Zabbix Server pokes for **mikrotik.api.discovery**. The item's first parameter is **another** host name  of Mikrotik 
  we want to monitor. Mikrotik does not have zabbix_agentd inside, right?
4. Poking **mikrotik.api.discovery** spawns the execution of `zabbix.py` which returns some data. This bunch of data get
  forwarded to `zabbix_sender`
5. A lot of other items defined via Zabbix Template as **Zabbix Trapper** items. So they are being collected during the 
  previous step and pushed into the server with `zabbix_sender`.

### Creating the user in Mikrotik
You need to create an separate group. Go to *System* - *Users* and create the new group:
* **Name**: `api_read`
* **Policies**:
  * `test`
  * `api`
  * `read`
  * `winbox`

Create a user and put it into `api_read` group.

### Tuning up Zabbix

There is a Zabbix Template **Template Mikrotik API Poke**. It contains few macroses which you need probably to re-apply
when attach it to your host:
- **{$MTIK_HOSTNAME}** (default: `Mikrotik`) - the host name in Zabbix inventory to assign values to.
- **{$MTIK_API_HOST}** (default: `192.168.0.1`) - the IP address API listens to
- **{$MTIK_API_USER}** (default: `admin`) - the api user name. *read* permissions for the user is OK to start.
- **{$MTIK_API_PASSWORD}** (default: `admin`) - the API password
- **{$MTIK_API_SCRIPT_PARAMS}** (default: `-t`) - the additional parameters you want to pass to `zabbix.py` script.
  Separate with spaces. Probably the most interesting are:
    * `-t`: Use timestamps when sending the values
    * `-s`: Use SSL when do API call. The Certificate verification is disabled.
    * `-P PLUGINS`: the directory with the plugins to use related to the directory where `zabbix.py` is located.

### Installation on Zabbix Server

The code uses Python 2. All the dependencies are listed in [requirements.txt](requirements.txt) file.
Very likely you will use *Virtualenv* for the installation. I used `/etc/zabbix/.venv` as a viartualenv directory.

As usual, everything which is in `/etc/zabbix/zabbix_agentd.d` gets included by `zabbix_agentd`. Put or symlink 
[userparameter_mikrotik_getdata.conf](zabbix_agentd.d/userparameter_mikrotik_getdata.conf) to something in 
`/etc/zabbix/zabbix_agentd.d` in order to start.

## Low Level Discovery

    ./zabbix.py -H 192.168.0.1 -u apiuser -p apipassword -s -P lld_plugins 2>/dev/null

## Fetch Counters

    ./zabbix.py -H 192.168.0.1 -u apiuser -p apipassword -s 2>/dev/null

## Zabbix Sender Examples

On the Zabbix server an item of type **Zabbix trapper** should be created with corresponding key. 
**Note** that incoming values will only be accepted from hosts specified in **Allowed hosts** field for this item.  

Read the values from file:

    zabbix_sender -c /etc/zabbix/zabbix_agentd.conf \
        --host mtik.local \
        --input-file /path/to/parameters_file

Read the values from STDIN:

    cat /path/to/parameters_file | zabbix_sender -c /etc/zabbix/zabbix_agentd.conf \
        --host mtik.local \
        --real-time \
        --input-file -

---

[PyPi librouteros library]: https://pypi.org/project/librouteros/
