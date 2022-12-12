#!/bin/bash

mn_dir="./network"
tf_dir="./server"
echo $mn_dir
echo $tf_dir

# create veth
echo "create veth"
sudo ip link add veth1_a type veth peer name veth1_b
sudo ip link add veth2_a type veth peer name veth2_b
echo "done: create veth"

# create VMs
echo "cd $tf_dir"
cd $tf_dir
echo "terraform apply"
terraform apply
echo "done: terraform apply"

echo "cd $mn_dir"
cd $mn_dir
sudo ip link set promisc on veth1_a
sudo ip link set promisc on veth1_b
sudo ip link set promisc on veth2_a
sudo ip link set promisc on veth2_b
sudo ip link set promisc on macvtap0
sudo ip link set promisc on macvtap1

echo " promisc on to veth and macvtap"

ip addr show veth1_a
ip addr show veth1_b
echo "set link done"


echo "create mininet"
sudo python3 ./network/main.py

