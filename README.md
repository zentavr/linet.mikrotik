Zabbix Helpers To Fetch Mikrotik's Counters via API
---------------------------------------------------

These scripts rely on [PyPi librouteros library].

## Tuning up Zabbix

There is a Zabbix Template **Template Mikrotik API Poke**. It contains few macroses which you need probably to re-apply
when attach it to your host:
- **{$MTIK_API_HOST}** (default: `192.168.0.1`) - the IP address API listens to
- **{$MTIK_API_USER}** (default: `admin`) - the api user name. *read* permissions for the user is OK to start.
- **{$MTIK_API_PASSWORD}** (default: `admin`) - the API password
- **{$MTIK_API_SCRIPT_PARAMS}** (default: `-t`) - the additional parameters you want to pass to `zabbix.py` script.
  Separate with spaces. Probably the most interesting are:
    * `-t`: Use timestamps when sending the values
    * `-s`: Use SSL when do API call. The Certificate verification is disabled.
    * `-P PLUGINS`: the directory with the plugins to use related to the directory where `zabbix.py` is located.

## Installation on Zabbix Server

The code uses Python 2. All the dependencies are listed in [requirements.txt](requirements.txt) file.
Very likely you will use *Virtualenv* for the installation.

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
