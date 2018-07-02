Zabbix Helpers To Fetch Mikrotik's Counters via API
---------------------------------------------------

These scripts rely on [PyPi librouteros library].

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
