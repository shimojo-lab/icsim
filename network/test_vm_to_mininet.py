from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.link import IPIntf

class TestVmToMininetTopology(IPTopo):
    def build(self, *args, **kwargs):
        r1 = self.addRouter("r1")
        s1 = self.addSwitch("s1")

        self.addLink(r1, s1)

        super().build(*args, **kwargs)

net = IPNet(topo=TestVmToMininetTopology())

#s1 = list(filter(lambda r:r.name=='s1', net.switches))[0]
#_intf1 = IPIntf("veth1_b", s1)
#print("IPIntf created")


try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
