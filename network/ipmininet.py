from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.link import IPIntf
from ipmininet.node_description import NodeDescription
import subprocess


class FatTreeTopology(IPTopo):

    def build(self, *args, **kwargs):
        rl1 = self.addRouter("rl1", lo_addresses=["10.1.0.1/24"])
        rl2 = self.addRouter("rl2", lo_addresses=["10.2.0.1/24"])
        rl3 = self.addRouter("rl3", lo_addresses=["10.3.0.1/24"])
        rl4 = self.addRouter("rl4", lo_addresses=["10.4.0.1/24"])

        rs1 = self.addRouter("rs1", lo_addresses=["10.5.0.1/24"])
        rs2 = self.addRouter("rs2", lo_addresses=["10.6.0.1/24"])
        rs3 = self.addRouter("rs3", lo_addresses=["10.7.0.1/24"])
        rs4 = self.addRouter("rs4", lo_addresses=["10.8.0.1/24"])

        rc1 = self.addRouter("rc1", lo_addresses=["10.9.0.1/24"])

        # h1 = self.addHost("h1")
        # h2 = self.addHost("h2")
        # h3 = self.addHost("h3")
        # h4 = self.addHost("h4")
        # h5 = self.addHost("h5")
        # h6 = self.addHost("h6")
        # h7 = self.addHost("h7")
        # h8 = self.addHost("h8")

        # self.addLink(rl1, h1)
        # self.addLink(rl1, h2)
        # self.addLink(rl1, h3)
        # self.addLink(rl1, h4)
        # self.addLink(rl2, h5)
        # self.addLink(rl2, h6)
        # self.addLink(rl2, h7)
        # self.addLink(rl2, h8)

        lrs1rl1 = self.addLink(rs1, rl1)
        lrs1rl1[rs1].addParams(ip=("10.51.0.1/24"))
        lrs1rl1[rl1].addParams(ip=("10.51.0.2/24"))
        lrs1rl2 = self.addLink(rs1, rl2)
        lrs1rl2[rs1].addParams(ip=("10.52.0.1/24"))
        lrs1rl2[rl2].addParams(ip=("10.52.0.2/24"))
        lrs2rl1 = self.addLink(rs2, rl1)
        lrs2rl1[rs2].addParams(ip=("10.61.0.1/24"))
        lrs2rl1[rl1].addParams(ip=("10.61.0.2/24"))
        lrs2rl2 = self.addLink(rs2, rl2)
        lrs2rl2[rs2].addParams(ip=("10.62.0.1/24"))
        lrs2rl2[rl2].addParams(ip=("10.62.0.2/24"))

        lrc1rs1 = self.addLink(rc1, rs1)
        lrc1rs1[rc1].addParams(ip=("10.95.0.1/24"))
        lrc1rs1[rs1].addParams(ip=("10.95.0.2/24"))
        lrc1rs2 = self.addLink(rc1, rs2)
        lrc1rs2[rc1].addParams(ip=("10.96.0.1/24"))
        lrc1rs2[rs2].addParams(ip=("10.96.0.2/24"))


        super().build(*args, **kwargs)


# create veth in root namespace
#subprocess.run("sudo ip link add veth1_a type veth peer name veth1_b", shell=True)
#subprocess.run("sudo ip link add veth2_a type veth peer name veth2_b", shell=True)


net = IPNet(topo=FatTreeTopology(), allocate_IPs=False)
print("IPNet created")

rl1 = list(filter(lambda r:r.name=='rl1', net.routers))[0]
rl2 = list(filter(lambda r:r.name=='rl2', net.routers))[0]

_intf1 = IPIntf("veth1_b", rl1)
_intf2 = IPIntf("veth2_b", rl2)
_intf1.ip = "10.101.0.1/24"
_intf2.ip = "10.102.0.1/24"
print("IPIntf created")


try:
    print("net.start()")
    net.start()
    print("IPCLI")
    IPCLI(net)
finally:
    net.stop()
