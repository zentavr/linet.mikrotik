Zabbix Helpers To Fetch Mikrotik's Counters via API
---------------------------------------------------

These scripts rely on [PyPi librouteros library].
The reason is why this code was born is that Mikrotik's vendor does not hurry with implementing SNMP OIDs for the 
certain interesting counters. When **Linet LTD** started to migrate to Mikrotiks - they missed an opportunity to monitor
the health of their NAS in many ways like they did before.

Currently, we monitor the next:

*  [radius.py](plugins/radius.py): Radius CoA counters: `/radius incoming monitor`
*  [radius.py](plugins/radius.py): Radius Client counters: `/radius monitor`
*  [bgp.py](plugins/bgp.py): BGP Peer Counters: `/routing bgp peer print status`
*  [irq.py](plugins/irq.py): System IRQ Counters: `/system resource irq print`
*  [firewall.py](plugins/firewall.py): Firewall Counters `/ip firewall <table> print stats`

## Installation

In the example below we use a template which monitors the single Mikrotik Node. If you want to minitor several Mikrotiks 
from a single zabbix_agent - you can fetch the concept and clone the items for several Mikrotiks.

The concept is:

1.  We define **mikrotik.api.discovery** item (manually or using the template) on the node with `zabbix_agentd` available. 
  The item accepts a couple of parameters
2.  We define **mikrotik.api.discovery** in `zabbix_agentd` configuration file
3.  Zabbix Server pokes for **mikrotik.api.discovery**. The item's first parameter is **another** host name  of Mikrotik 
  we want to monitor. Mikrotik does not have zabbix_agentd inside, right?
4.  Poking **mikrotik.api.discovery** spawns the execution of `zabbix.py` which returns some data. This bunch of data get
  forwarded to `zabbix_sender`
5.  A lot of other items defined via Zabbix Template as **Zabbix Trapper** items. So they are being collected during the 
  previous step and pushed into the server with `zabbix_sender`.

### Creating the user in Mikrotik
You need to create an separate group. Go to *System* - *Users* and create the new group:

*  **Name**: `api_read`
*  **Policies**:
    *  `test`
    *  `api`
    *  `read`
    *  `winbox`

Create a user and put it into `api_read` group.

### Tuning up Zabbix

Tested with Zabbix 3.2.

There is a Zabbix Template **Template Mikrotik API Poke**. It contains few macroses which you need probably to re-apply
when attach it to your host:

-  **{$MTIK_HOSTNAME}** (default: `Mikrotik`) - the host name in Zabbix inventory to assign values to.
-  **{$MTIK_API_HOST}** (default: `192.168.0.1`) - the IP address API listens to
-  **{$MTIK_API_USER}** (default: `admin`) - the api user name. *read* permissions for the user is OK to start.
-  **{$MTIK_API_PASSWORD}** (default: `admin`) - the API password
-  **{$MTIK_API_SCRIPT_PARAMS}** (default: `-t`) - the additional parameters you want to pass to `zabbix.py` script.
    Separate with spaces. Probably the most interesting are:
    *  `-t`: Use timestamps when sending the values
    *  `-s`: Use SSL when do API call. The Certificate verification is disabled.
    *  `-P PLUGINS`: the directory with the plugins to use related to the directory where `zabbix.py` is located.


Before importing any templates you need to import Value Maps (Administration - General - Value Maps):

*  **ciscoBgpPeerState** can be found [here][ciscoBgpPeerState value maps]
*  **Mikrotik BGP Administrative Status** can be found [here][Mikrotik BGP Administrative Status value maps]
*  **Mikrotik Firewall Rule Status** can be found [here][Mikrotik Firewall Rule Status value maps]

The next templates are available:

*  **Template Mikrotik API Poke** - defines 2 items which Zabbix server pokes to (user parameters defined in zabbix_agent
    config). While it happens, the execution of `zabbix.py` happens - it pokes for values using Mikrotik API and 
    forwarding the results through `zabbix_sender` happens.
    
    The [template][Template Mikrotik API Poke] should be attached to the host where zabbix_sender and Python is installed.
    Also, the macroses should be defined (see above).

*  **Template Mikrotik BGPv4** - is being used for BGP Peers Monitoring. It discovers for the peers using low level 
    discovery, assigns items and triggers for the peer and also builds a couple of charts.
    
    The [template][Template Mikrotik BGPv4] should be attached to the Mikrotik node.
    Very likely, you need to edit an every single item and define/redefine `Allowed Hosts` value. The default is 
    `127.0.0.1`. This option tells Zabbix from which hosts it will accept the values for *Zabbix Trapper* items.

*  **Template Mikrotik Firewall Statistics** Monitors the stats coming from Mikrotik Firewall. In order to discover the 
   rule, assign a comment to it. The comment **must** start with `ZBX` in order to be monitored by the plugin. Currently
   we monitor bytes and packets per second values. The chart is available for the counters as well.

    The [template][Template Mikrotik Firewall Statistics] should be attached to the Mikrotik node. likely, you need to 
    edit an every     single item and define/redefine `Allowed Hosts` value. 
    The default is `127.0.0.1`. This option tells Zabbix from which hosts it will accept the values for *Zabbix Trapper* 
    items.

*  **Template Mikrotik Radius Counters** - is being used for RADIUS Client counters monitoring. It discovers the servers
    defined in Mikrotik's settings and adds items and charts for them. It monitors RADIUS Incoming CoA counters as well. 
    
    The [template][Template Mikrotik Radius Counters] should be attached to 
    the Mikrotik node. Very likely, you need to edit an every single item and define/redefine `Allowed Hosts` value. 
    The default is `127.0.0.1`. This option tells Zabbix from which hosts it will accept the values for *Zabbix Trapper* 
    items.

*  **Template Mikrotik IRQ Counters** - is being used for System IRQ counters monitoring. It discovers the IRQs
    available in Mikrotik's settings and adds items and charts for them.
    
    The [template][Template Mikrotik IRQ Counters] should be attached to 
    the Mikrotik node. Very likely, you need to edit an every single item and define/redefine `Allowed Hosts` value. 
    The default is `127.0.0.1`. This option tells Zabbix from which hosts it will accept the values for *Zabbix Trapper* 
    items.

### Installation on Zabbix Server

The code uses Python 3 (tested in 3.11.3). All the dependencies are listed in [requirements.txt](requirements.txt) file.
Very likely you will use *Virtualenv* for the installation. I used `/etc/zabbix/.venv` as a virtualenv directory.

As usual, everything which is in `/etc/zabbix/zabbix_agentd.d` gets included by `zabbix_agentd`. Put or symlink 
[userparameter_mikrotik_getdata.conf](zabbix_agentd.d/userparameter_mikrotik_getdata.conf) to something in 
`/etc/zabbix/zabbix_agentd.d` in order to start.

#### Known Issues
*  Python2 support was removed

## Hints

### Low Level Discovery

Low Level discovery plugins are in `lld_plugins` folder. Everything which is `*.py` (except `__*`) will be dynamically 
included and `run()` with the parameters will be executed. 

    ./zabbix.py -H 192.168.0.1 -u apiuser -p apipassword -s -P lld_plugins 2>/dev/null

### Fetch Counters

The plugins which fetch the data using API calls are in `plugins` folder. Everything which is `*.py` (except `__*`) will
be dynamically included and `run()` with the parameters will be executed. 

    ./zabbix.py -H 192.168.0.1 -u apiuser -p apipassword -s 2>/dev/null

### Zabbix Sender Examples

On the Zabbix server an item of type **Zabbix trapper** should be created with corresponding key(s). 
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
[Upgrade to Python 2.7.11 on Ubuntu]: http://mbless.de/blog/2016/01/09/upgrade-to-python-2711-on-ubuntu-1404-lts.html
[PyPi librouteros library]: https://pypi.org/project/librouteros/

[ciscoBgpPeerState value maps]: zabbix_templates/zbx_valuemaps_bgp_status.xml
[Mikrotik BGP Administrative Status value maps]: zabbix_templates/zbx_valuemaps_mtik_bgp_admin_status.xml
[Mikrotik Firewall Rule Status value maps]: zabbix_templates/zbx_valuemaps_mtik_firewall.xml

[Template Mikrotik API Poke]: zabbix_templates/zbx_template_API_Poke.xml
[Template Mikrotik BGPv4]: zabbix_templates/zbx_template_BGP.xml
[Template Mikrotik Firewall Statistics]: zabbix_templates/zbx_template_firewall_stats.xml
[Template Mikrotik Radius Counters]: zabbix_templates/zbx_template_Radius_Counters.xml
[Template Mikrotik IRQ Counters]: zabbix_templates/zbx_template_IRQ_Counters.xml

[Keeping in sync git repos]: https://moox.io/blog/keep-in-sync-git-repos-on-github-gitlab-bitbucket/
