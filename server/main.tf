variable "hostname" { default = "cluster" }
variable "domain" { default = "example.com" }
variable "memoryMB" { default = 1024*1 }
variable "cpu" { default = 1 }


terraform {
  required_providers {
    libvirt = {
      source = "dmacvicar/libvirt"
    }
  }
}

provider "libvirt" {
  # Configuration options
  uri = "qemu:///system"
}



resource "libvirt_volume" "os_image" {
  name = "ubuntu20"
  pool = "default"
  source = "https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64-disk-kvm.img"
  format = "qcow2"
}

resource "libvirt_volume" "VM1" {
  name = "VM1.qcow2"
  base_volume_id = libvirt_volume.os_image.id
}

resource "libvirt_volume" "VM2" {
  name = "VM2.qcow2"
  base_volume_id = libvirt_volume.os_image.id
}

# Use CloudInit ISO to add ssh-key to the instance
resource "libvirt_cloudinit_disk" "commoninit" {
          name = "${var.hostname}-commoninit.iso"
          pool = "default"
          user_data = data.template_file.user_data.rendered
}


data "template_file" "user_data" {
  template = file("${path.module}/cloud_init.cfg")
  vars = {
    hostname = var.hostname
    fqdn = "${var.hostname}.${var.domain}"
  }
}


resource "libvirt_domain" "VM1" {
  name = "VM1"
  memory = 1024
  vcpu = 2

  # network_interface {
  #   macvtap = "veth1_a"
  # }
  cloudinit = libvirt_cloudinit_disk.commoninit.id


  disk {
    volume_id = libvirt_volume.VM1.id
  }

  console {
    type = "pty"
    target_port = "0"
    target_type = "serial"
  }
}

resource "libvirt_domain" "VM2" {
  name = "VM2"
  memory = 1024
  vcpu = 2

  # network_interface {
  #   macvtap = "veth2_a"
  # }
  cloudinit = libvirt_cloudinit_disk.commoninit.id

  disk {
    volume_id = libvirt_volume.VM2.id
  }

  console {
    type = "pty"
    target_port = "0"
    target_type = "serial"
  }
}

output "ips" {
  # show IP, run 'terraform refresh' if not populated
  value = libvirt_domain.VM1
}
