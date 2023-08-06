netdevice
*********

Python modules to execute command on remote network device.

To install easily::

    pip install -U netdevice

Or to install by source code::

    netdevice-x.x.tar.gz
        pexpect-2.3.tar.gz
        xmltodict-0.10.2.tar.gz
        lxml-3.8.0.tar.gz
            Python-2.7.12.tgz
            libxml2-2.9.4.tar.gz

.. attention::

    lxml-3.8.0.tar.gz has some bug if you don't install to the default path,
    you must set the LD_LIBRARY_PATH enviroment varible in such case. please
    refer to the detail: python第三方库lxml源码安装&&使用笔记,
    http://blog.csdn.net/slvher/article/details/25829973

1. Introduction
===============

netdevice is a python module that allow you run shell command on local or
remote host in python. It's especially useful for network test automation:

When host is given, you can run the command on remote host and get the result
in the return:

.. code-block:: python

    from netdevice import cisco, junos, linux
    pc = linux.LinuxDevice("ssh://dev:1234@10.208.72.12")
    print(pc.cmd("ifconfig eth1"))

When the "server" parameter is not given, it run on local device and get the
result:

.. code-block:: python

    from netdevice import cisco, junos, linux
    #It ack as pc = linux.LinuxDevice("ssh:127.0.0.1")
    pc = linux.LinuxDevice()
    print(pc.cmd("whoami"))

Use help command show the documents::

    import from netdevice import cisco, junos, linux
    help(linux)
    help(junos)
    help(cisco)

2. Feature
==========

    1) Python Based: Plenty of features
    2) Environmentally friendly: can run anywhere where there is python and connect to the devices.
    3) Easy to Learn: Need know little about Python
    4) Easy to write: One case only have several to dozens of lines.
    5) Faster: run the testbed from local and is much faster.
    6) object oriented: Flexible and Easy to extend

3. Test architecture based on netdevice
===========================================

::

    +---------------------------------+------------+----------------------+
    |                                 |            | case1                |
    |                                 |            +----------------------+
    |  One case                       | Test Suite | ...                  |
    |                                 |            +----------------------+
    |                                 |            | caseN                |
    +---------------------------------+------------+----------------------+
    |  netdevice                                                          |
    |                                                                     |
    |  PC1                  DUT                  DUT                      |
    |  +---------------+    +---------------+    +---------------+        |
    |  | Linux devices |    | Junos devices |    | Cisco devices |  ...   |
    |  +---------------+    +---------------+    +---------------+        |
    |                       | Linux devices |    | Linux devices |  ...   |
    |                       +---------------+    +---------------+        |
    +---------------------------------------------------------------------+

                     test Architecture based on netdevice
 
4. Object overview
==================

4.1 LinuxDevice
---------------

4.1.1 Constructor
+++++++++++++++++

LinuxDevice is a common abstraction for linux like devices. It' flexible to
define a LinuxDevice object.

1) Use a url to define a netdevice, then you can execute the command and get
the result:

.. code-block:: python

    client = linux.LinuxDevice("ssh://root:1234@englab.ent-vm02.juniper.net")
    server = linux.LinuxDevice("telnet://root:1122@10.208.172.45:7012")
    print(client.cmd("ifconfig"))
    print(server.cmd("pwd"))

2) By desginating the necessary attribute such as hostname/username/password,
etc.

.. code-block:: python

    client = linux.LinuxDevice(username = "root", password = "1234",
        hostname = "alg-vm11")
    print(client.cmd("uname -a"))

3) Use the dictionary to describe the device, it's very useful for test
script. for examples:

.. code-block:: python

    skater = {
            "url": "ssh://root:1234@skater.englab.juniper.net",
            "int0": {"name": "reth1.0", "inet": "42.0.0.11/24", "inet6": "2002::11/64", "zone": "untrust" },
            "int1": {"name": "reth0.0", "inet": "41.0.0.11/24", "inet6": "2001::11/64", "zone": "trust" },
            }
    ent_vm02 = {
            "url": "ssh://root:1234@ent-vm02.englab.juniper.net",
            "int0": { 'name': 'eth1', 'inet': '42.0.0.2/24', 'inet6': '2002::2/64'},
            }
    ent_vm01 = {
            "scheme": "ssh",
            "username": "root",
            "password": "1234",
            "hostname": "ent-vm01.englab.juniper.net",
            "int0": { 'name': 'eth1', 'inet': '41.0.0.2/24', 'inet6': '2001::2/64'},
            }
    client = linux.LinuxDevice(**ent_vm02)
    server = linux.LinuxDevice(**ent_vm01)
    dut = junos.JunosDevice(**skater)
    print(client.cmd("ifconfig"))
    print(client["int0"]["inet"])
    dut.cli("show security flow status")

4.1.2 Attributes
++++++++++++++++

LinuxDevice operate based on its attributes. User input those attributes and
can use them after that. Some attributes are pre-defined and the LinuxDevices
will use them when login, log, configuration and so on. use can change those
attribtes. Other attrubutes are defined totally by users and user define how
to use them.

1) Pre-defined attributes:

I list the following pre-define attributes and their default value and the
meaning of them.

.. code-block:: python

    default = {
        # mandtory, if not given, it will fail to construct a device
        "scheme":     "ssh",     # login method, default is ssh, support ssh
                                 # and telnet now;
        "username":      None,   # Usename to login;
        "hostname":          None,   # A ip address or hostname that can connect
         
        # Optional, if not given, use the default
        "password":      None,   # Password to login, could be omitted if use
                                 # public key;
        "root_password": None,   # Root password is used since some configuration
                                 # need root privillage. If not provided, some
                                 # configurationa or command would fail since
                                 # privilage.
        "url":       None,       # url to connect the server, use url insteading
                                 # scheme/username/passowrd/hostname/port
        "name":       None,      # name of the devices, only used for log. if not
                                 # set, the first part of hostname is used.
        "autologin":  True,      # If ture, will login the devices immediately.
        #"interfaces": [
        #    #{"name": "ge-7/1/0.0", "inet": "1.1.1.1/24", "inet6": "2001::1/64", "zone": "trust" },
        #    #{"name": "ge-7/1/1.0", "inet": "2.2.2.1/24", "inet6": "2002::1/64", "zone": "untrust" },
        #    ],                   # A list of interfaces the device use; Will
        #                         # configure the interface onto the devices if
        #                         # autoconfig is True
        "preconfig":  [],        # A list of cmd/configuration the device will
                                 # configure before test;
        "postconfig": [],        # A list of cmd/configuration the device will
                                 # configure after test;
        #"autoconfig": False,     # If ture, will not configure the interface
        #                         # and preconfig automatically.
                                  
        # log related
        "log_file": "test_%s.log" %(time.strftime("%Y%m%d%H%M%S", time.localtime())),
                                 # log files, set None to disable recording log in file.
        "log_level":  LOG_INFO,  # log level, 0-7, the higher it's, the more log
                                 # recorded.
        "log_color":  None,      # log color, if not set will choose randomly;
                                 # Use self.test_color() to see what each color
                                 # looks like
        "log_time":   True,      # record the log with local time;
        #"log_thread": True,      # record the log with thread name;

        # User can also define Whatever attributes you want.
        # ...
    }

2) User-defined attributes:

Besides the pre-defined attributes, user can define their own attributes,
since those kinds of attributes are used for user only, they can be in any
type, for examples:

.. code-block:: python

    client = linux.LinuxDevice("telnet://root:1122@10.208.172.45:7012",
                               "int0": { 'name': 'eth1', 'inet': '42.0.0.2/24', 'inet6': '2002::2/64'},
                               description = "Beijing")
    client["season"] = "summer"
    print(client["season"], client["description"])
    print(client["int0"]["inet"])

4.1.3 Methods
+++++++++++++

LinuxDevice support the folowing method:

    def __init__(self, server = None, \*\*kwargs)

        This is the constructor for LinuxDevice, The parameter pass the
        attribute that the object needs.

        @server: the standard url of the server, support the query parameters.
        @kwargs: attributes of the server, the parameter in this part could be used as the attribute of the object.

        For example:

            client = linux.LinuxDevice("telnet://root:1122@10.208.172.45:7012",
                                       "int0": { 'name': 'eth1', 'inet': '42.0.0.2/24', 'inet6': '2002::2/64'},
                                       description = "Beijing")

    __del__(self):

        Recycle resource when the object is destroied.

    def login(self, terminal_type = 'ansi', login_timeout = 10):

        Connect the object with the constructor attribute.

        The defualt attribute "autologin" is True, so normally it will be auto
        called. Set attribute "autologin" as False and you must call it
        explictly.

    def relogin(self):

        Kill the current session and relogin.

    def cmd(self, cmd, expect = None, timeout = 20, control = False,
            format = "output", command_leading = "\033[0;31m$ \033[0m",
            command_color = "no_color", command_bg_color = "no_color",
            output_color = "no_color", output_bg_color = "no_color",
            \*\*kwargs):

        Execute a command provided by @cmd on remote Linuxdevice and return the
        execution result, If the @expect is found, it succeed and return
        immediately, or it will wait for at most @timeout seconds. The return
        result will be desginated by @format:
        
        @ expect: the prompt the execute is expected to include. If not
                  provided, the self.prompt is used. For some applications,
                  i.e ftp, it will not use the system's prompt so you must give
                  the expected prompt.

        @ timeout: Hong long to wait before it's thinked as timeout, if it
                   timeout a "CTRL + C" will be trriggered, so please set the
                   proper timeout carefully;

        @ control: If it is True, send a control character to the child such as
                   Ctrl-C or Ctrl-D. For example, to send a Ctrl-G (ASCII 7):: 

                       self.cmd('g', control = True)

        @ format: If it's "output", the execute output of the command will be
        returned, whether it succeed or timeout. 

        If it's "status", the execute status will be return, if return and the
        @expect is found, it will return True, or it return False. 
        
        If it's "both", the tuple (status, output) will be return and you can
        check both of them.

        @ command_leading: Which leading chars to add before command in the log.

        @ command_color: Which color to show the command in the log.

        @ command_bg_color: Which background color to show the command in the log.

        @ output_color: Which color to show the output in the log.

        @ output_bg_color: Which background color to show the output in the log.

        @ redirect: Noramlly the output would be shown on screen or log file,
                    if this is set then the output of the command would be
                    saved in the given file, it's especially useful for execute
                    command with big output. "/dev/null" would redirect the
                    output to a hole. For example:

            pc.cmd("ifconfig", redirect = "ifconfig_result.log")

        [CAUTION]: please increase the timeout value if the command is
        time-consuming, or it will cause failure.

    def log (self, message, level = LOG_NOTICE, leading = None, color =
            "no_color", bg_color = "no_color", log_level = None, \*\*kwargs):

        record the log to file self["log_file"] with the color
        self["log_color"], with the local time if self['log_time'] is True,
        the log looks like::

            [ regazara ][2017-05-16 16:02:07]: ssh login succeed.

        @ message: The log text.

        @ level: The log level of the text. Will not show if it's large than
        the self["log_level"].

        @log_level: will override the level

        @ color: The log color of the text.

        @ bg_color: The log background color of the text.

    def sleep (self, timeout, total = 50, char = '>', description = "sleep"):

        Sleep with progress bar, the granularity is 0.1 second. something like
        that:

        sleep 7/10[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>               ][71%]

    dumps(self):

        Dump all its attributes.

    get_file(self, filename, localname = '.', timeout = -1):

        Get file from remote host, only support scp now, will support other
        methods later.

        @filename: file to get from the host.

        @localname: save name after download

        @timeout: How long to wait for the files to be downloaded. If the file
        is very big, set it to a big value or it will fail.

    put_file(self, filename, remotedir, timeout = -1):

        Put local file to remote host, only support scp now, will support
        other methods later.

        @filename: file to put from the local. local means the host where you
        execute this scriopt.

        @remotedir: save name after upload.

        @timeout: How long to wait for the files to be uploaded. If the file
                  is very big, set it to a big value or it will fail.

    def get_files (self, \*args, \*\*kwargs):

        Get files from remote host. Compared @get_file, can't desgnate the
        local file name, but can get files at a time.

    def reboot (self):

        reboot the device and reconnect to it until it bootup.

    def pktsend (self, pkt, src = None, dst = None, sport = None, dport = None)

        Replay the packet like tcpreplay on the linux box. The packet should
        include the ip header + tcp/udp header + payload in hex format. for
        example:

        0x4500003077e240008006a5a50ac645c70aa8820b049f00154e372b0e
        000000007002ffff27e60000020405b401010402

        @pkt: the packet in hex plain text format;

        @src: replace the source ip addrss in the @pkt, if none use the value
              in the @pkt;

        @dst: replace the destination ip addrss in the @pkt; if none use the
              value in the @pkt;

        Examples::

            sync = '45 00 00 30 77 e2 40 00 80 06 a5 a5 0a c6 45 c7
                    0a a8 82 0b 04 9f 00 15 4e 37 2b 0e 00 00 00 00
                    70 02 ff ff 27 e6 00 00 02 04 05 b4 01 01 04 02'
            client.pktsend(syn, src = "1.1.1.2", dst = "2.2.2.2")

    tcpreplay (self, remote, filename, saddr = None, sport = None,
            daddr = None, dport = None, proto = None, replay_range = None)

        Replay the packet capture file @filename, the file could be collected
        by tnpdump or wireshark.

        @remote: the server which is linuxdevice object.
        @filename: the packet capture file.
        @saddr: the client address in the packet capture.
        @daddr: the server address in the packet capture.
        @sport: the client port in the packet capture.
        @dport: the server port in the packet capture.
        @port: the protol that to be replayed in the packet capture.
        @replay_range: the list of frame number to be replayed in the packet capture.

        It's based on sendip-2.5-mec-2, besides, there is some bugs to support ipv6::

            Index: sendip.c
            ===================================================================
            RCS file: /home/ypguo/.cvsroot/sendip/sendip.c,v
            retrieving revision 1.1.1.1
            diff -u -p -r1.1.1.1 sendip.c
            --- sendip.c	3 Jan 2018 04:02:31 -0000	1.1.1.1
            +++ sendip.c	3 Jan 2018 04:04:29 -0000
            @@ -686,9 +686,14 @@ int main(int argc, char *const argv[]) {
                                            free(packet.data);
                                            unload_modules(FALSE,verbosity);
                                            return 1;
            -			} else {
            -				af_type = AF_INET;
            -			}
            +            } else {
            +                if (strchr(argv[gnuoptind], ':')) {
            +                    /* the destination address is ipv6 address. */
            +                    af_type = AF_INET6;
            +                } else {
            +                    af_type = AF_INET;
            +                }
            +            }
                            }
                            else if(first->optchar=='i') af_type = AF_INET;
                            else if(first->optchar=='6') af_type = AF_INET6;

    def test_color (self):

        print the color name in the color.

    __getitem__(self, name):

        Get certain attribute, for example::

            print(self["name"])

    __setitem__(self, name, value):

        Set certain attribute, for example::

            self["color"] = "red"

    The following methods combile frequently-used methods:

    def x_configure_interface (self, \*args):

        Re-configure the interface with the given parameters.
        The interface looks like this, you can configure multi interfaces in
        one time, for examples:

        int0 = { 'name': 'eth1', 'inet': '41.0.0.2/24', 'inet6': '2001::2/64'}
        int1 = { 'name': 'eth2', 'inet': '42.0.0.2/24', 'inet6': '2002::2/64'}
        dut.x_configure_interface(int0, int1)

    def x_configure_route (self, local, gateway, remote):

        Re-configure the interface with the given parameters, for examples:

        #int0 = { 'name': 'eth1', 'inet': '41.0.0.2/24', 'inet6': '2001::2/64'}
        client.x_configure_route(client["int0"], dut["int0"], server["int0"])

    def x_get_interfaces (self, name):

        Get interface configuration given a interface name.

    def x_ftp (self, \*args, \*\*kwargs):

        Login the remote ftp server and execute some command. Example:

            client.x_ftp("pwd", "ls", "bye", hostname = "42.0.0.2", username = "root", password = "Embe1mpls")

        Or:

            client.x_ftp("pwd", hostname = "42.0.0.2", username = "root", password = "Embe1mpls")
            client.x_ftp("ls", "pwd")
            client.x_ftp("bye")

        @args: command list need to be executed
        @kwargs: hostname/username/password parameters If need to auto logint the
        remote ftp server, hostname/username/password should be given

4.2 JunosDevice
---------------

4.2.1 Constructor
+++++++++++++++++

JunosDevice is a common abstraction for Juniper network devices. It derives
from LinuxDevice so it has every method of LinuxDevice, except some of them
are overrided. Please use the similar way to define a JunosDevice, for
example:

.. code-block:: python

    dut = junos.JunosDevice("ssh://root:Juniper@10.219.29.61")
    print(dut["username"])
    print(dut.cli("show security flow session"))

4.2.2 Methods
+++++++++++++

Besides all the methods derived from LinuxDevice, JunosDevice support the
folowing extra methods:

    def cmd (self, cmd, mode = "shell", timeout = 30, \*\*kwargs):

        There are total 4 modes for junos devices:

            1) shell: execute the command in shell mode and return the result,
                this is the default mode and it looks like linux.cmd().

            2) cli: execute the command in cli mode and return the result,
                self.cmd(cmd, mode = "cli") equal to self.cli(cmd), see detail
                in seld.cli()

            3) configure: execute the command in configure mode and return the
                result, self.cmd(cmd, mode = "configure") equal to
                self.configure(cmd), see detail in seld.configure()

            4) vty: execute the command in vty mode and return the result,
                self.cmd(cmd, mode = "vty") equal to self.vty(cmd), see detail
                in seld.vty()

        Supported options include:

            timeout: time to wait for the execute command return. default is 5
                     seconds

    cli (self, cmd, parse = None, timeout = 30, \*\*kwargs):

        equal cmd(..., mode = "cli")

        Execute a list of cli command and return the execution result of the
        last command.

        @parse: Normally, the result will be plain text or xml text. But if
        the @parse is given, the result will be parsed and a list of
        dictionary for @parse will be returned. It's useful to parse the xml
        result. For example the following command return a list of session in
        dictionary::
        
            sessions = dut.cli('show security flow session',
                               parse = "flow-session")
            print sessions[0]['session-identifier']

        while the following command will return the plain text result::

            output = dut.cli('show security flow session')
            print output

    configure(self, cmd, \*\*kwargs):

        equal cmd(..., mode = "configure"), Execute a configure command and
        return the result of the last command. Sematics is like self.cli, see
        detail in self.cli(), For example, Execute a configure command::

            dut.configure('set security flow traceoptions flag all')
            dut.configure('set security traceoptions file flow.log size 50m')
            dut.configure('set security traceoptions level verbose')
            dut.configure('set security traceoptions flag all')
            dut.configure('commit')

    def vty (self, \*args, \*\*kwargs):

        equal cmd(..., mode = "vty")

        Execute every line in every argument on every SPU(if not given) and
        return the result.

        Supported options include:

            timeout: time to wait for the execute command return. default is 5
                     seconds
            tnp_addr: tnp address to execute, if not execut the command on
                      every SPU.

    def get_spus (self, \*\*kwargs):
    
        Get the spu list of the srx.

    print_session (self, session):
        
        Convert a or lists of session in dictionary to plain text. print it as
        show of "show security flow session".

        @session: it could be a session or a list of session.

    install_image (self, image):
        
        Install a image and reboot the dut, wait until it is up with all
        SPU/SPC.
        
        @local: install a local image, first upload the image to /var/tmp/ on
        the DUT and then install it.

        @remote: install a image on the DUT

    def x_print_session (self, sessions):

        Convert a or lists of session in dictionary to plain text.

    def x_configure_trace (self, \*args, \*\*kwargs):
        configure trace file, For examples:

            dut.x_configure_trace("flow", "alg dns", "dynamic-application",
                                  filename = "flow.log", size = "50m")

    def x_configure_vty_trace (self, \*args, \*\*kwargs):
        configure trace file
        
        An examples, to enable flow/policy/dynamic-application traceoption and
        write the trace into one file:

            dut.x_configure_vty_trace("flow", "policy", "fwdd",
                                  filename = "flow.log", size = "50m")


5. An example
=============

In this example, we login the client linux device and then ftp the server.
Check if there is session generated on the Juniper SRX firewall. Then tear
down the connection:

.. code-block:: python

    #!/usr/bin/env python
    from netdevice import cisco, junos, linux

    if __name__ == '__main__':
        dut = junos.JunosDevice("ssh://regress:1234@regazara.englab.juniper.net",
                root_password = "5678")
        client = linux.LinuxDevice("ssh://root:5678@ent-vm01.englab.juniper.net",
                interfaces = [ { 'name': 'eth1', 'inet': '1.1.1.2/24', 'inet6': '2001::2/64'} ])
        server = linux.LinuxDevice("ssh://root:5678@ent-vm02.englab.juniper.net",
                interfaces = [ { 'name': 'eth1', 'inet': '2.2.2.2/24', 'inet6': '2002::2/64'} ])

        client.cmd("ip route add 2.2.2.0/24 via 1.1.1.1 dev eth1")
        server.cmd("ip route add 1.1.1.0/24 via 2.2.2.1 dev eth1")
        dut.cli("clear security flow session application ftp")

        # connect to the server and list the files.
        client.cmd('ftp %s' %(server["interfaces"][0]["inet"].split('/')[0]), expect = "Name")
        client.cmd(server["username"], expect = "Password")
        client.cmd(server["password"], expect = "ftp")
        output = client.cmd('ls', expect = "ftp> ")
        if "226" in output:
            print("ftp output is shown.")
        else:
            print("ftp failed to connect the server.")

        # check the session and tear down the connection.
        sessions = dut.cli('show security flow session application ftp', parse = "flow-session")
        client.cmd('bye')

        if sessions and sessions[0]["flow-information"][0]['pkt-cnt'] > 0 and \
                sessions[0]["flow-information"][1]['pkt-cnt'] > 0:
            print("Session found, pass!")
        else:
            print("Failed to find the session")

6. Q/A
======

1) Why some command return timeout?

For time consuming command i.g. scp, ftp get command, please set the @timeout
properly to avoid the command timeout.

Please make sure there is no command timeout since the output of the last
command will messup the result of the next command.

If a command timeout, either send a CTRL + C to kill the current session:

    client.cmd("c", control = True)

or kill the current session and relogin the device to open a new session:

    client.relogin()

7. Changelog
============

1.0.0: Official release.

1.0.4: For ssh, add  -o GSSAPIAuthentication=no to accelerate the login process.

1.0.6: 1) When configure interface in junos, don't configure the zone.
    2) print the junos specific attritue in the init.
    3) remove some verbose log when login.

1.0.7: 1) Change or add the some private function: x_set_interface, x_set_zone, x_set_policy, besides, we won't commit the change after the functions, users must commit the change by his own.
    2) add the release version in each object, you can see what version the script run.

1.0.9: 1) Fix some bugs.

1.0.10: 1) Don't show the commit process in other thread. There are some issue on it.

1.1.1: 1) Add a new device: OvsHost, a OpenvSwitch object.

1.1.4: 1) LinuxDevice: It doesn't work for pexpect issue: 669, add a workaround to work. 2) OvsDevice: Support connecting the vm device.

1.1.6: 1) It's easy to create ovs topology.

1.1.8: support start virtual machine on the phicisial machine.

1.1.10: Fix some bugs.

1.1.15: Bug fix: ovs couldn't add the interface in rare cases.

1.1.22: OVS now support vhostuser port, although it's said deprecated, you can configure it anyway. You can configure it as following:

vhostuser:

    "-chardev": "socket,id=char1,path=/usr/local/var/run/openvswitch/p0,reconnect=1",

vhostuserclient:

    "-chardev": "socket,id=char1,path=/usr/local/var/run/openvswitch/p0,server",

1.1.30: Support tap netdev.
1.1.33: Support bond port.

1.2.1: 1) LinuxDevice support login itself, then it would run sh command locally.
       2) Support new device: ovn.
