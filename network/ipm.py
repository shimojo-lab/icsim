import os
import datetime

from mininet.log import lg
from mininet.node import Node
from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.router.config import SSHd
from ipmininet.cli import IPCLI
from ipmininet.router.config.sshd import KEYFILE
from ssh_config import gen_ssh_config_file, write_file


capture_base_filename = f"capture_ompi_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}"
capture_dir = '/home/user/icsim/capture/'

class FatTreeTopology(IPTopo):

    def build(self, *args, **kwargs):
        rl1 = self.addRouter("rl1")
        rl2 = self.addRouter("rl2")
        rl3 = self.addRouter("rl3")
        rl4 = self.addRouter("rl4")
        rc1 = self.addRouter("rc1")
        rc2 = self.addRouter("rc2")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")
        h5 = self.addHost("h5")
        h6 = self.addHost("h6")
        h7 = self.addHost("h7")
        h8 = self.addHost("h8")
        h1.addDaemon(SSHd)
        h2.addDaemon(SSHd)
        h3.addDaemon(SSHd)
        h4.addDaemon(SSHd)
        h5.addDaemon(SSHd)
        h6.addDaemon(SSHd)
        h7.addDaemon(SSHd)
        h8.addDaemon(SSHd)

        self.addLink(rc1, rl1)
        self.addLink(rc1, rl2)
        self.addLink(rc1, rl3)
        self.addLink(rc1, rl4)

        self.addLink(rc2, rl1)
        self.addLink(rc2, rl2)
        self.addLink(rc2, rl3)
        self.addLink(rc2, rl4)

        self.addLink(rl1, h1)
        self.addLink(rl1, h2)
        self.addLink(rl2, h3)
        self.addLink(rl2, h4)
        self.addLink(rl3, h5)
        self.addLink(rl3, h6)
        self.addLink(rl4, h7)
        self.addLink(rl4, h8)

        self.addNetworkCapture(
            nodes=[h1, h2, h3, h4, h5, h6, h7, h8],
            base_filename=os.path.join(capture_dir, capture_base_filename),
            extra_arguments="")

        super().build(*args, **kwargs)


def connectToRootNS( network, switch, ip, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    print("root", root)
    intf = network.addLink( root, switch ).intf1
    print(intf)
    root.setIP( ip, intf=intf )
    # Add routes from root ns to hosts
    for route in routes:
        cmd = f"route add -net {route} dev {str(intf)}"
        print(cmd)
        root.cmd( cmd )
    for host in network.hosts:
        print( host.name, host.IP())

def get_sshd_key_filename():
    return KEYFILE

def get_host_info(net):
    info = []
    for host in net.hosts:
        info.append({
            'host_name': host.name,
            'host_ip': host.intf().ip,
        })
    return info

if __name__ == '__main__':
    lg.setLogLevel('info')
    net = IPNet(topo=FatTreeTopology())

    try:
        net.start()
        # connectToRootNS( net, switch=net['s1'], ip="10.123.123.1/32", routes=['192.168.6.0/24'] )
        # ssh config file
        keyfile = get_sshd_key_filename()
        host_info = get_host_info(net)
        config_str = gen_ssh_config_file(host_info, keyfile)
        write_file(os.path.join(os.path.dirname(__file__), 'ipm_ssh_config'), config_str)
        hostfile_str = "\n".join([host["host_name"] for host in host_info])
        write_file(os.path.join(os.path.dirname(__file__), '..', 'mpi', 'hostfile'), hostfile_str)
        print(f"sshd KeyFile: {keyfile}")
        print("Writing ssh config file")
        os.chmod(keyfile, 0o644)

        host_info = [f'{host["host_name"]}, {host["host_ip"]}' for host in host_info]
        write_file(os.path.join(capture_dir, capture_base_filename), "\n".join(host_info))

        IPCLI(net)
    finally:
        net.stop()