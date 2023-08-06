#!/bin/bash

function install_nvidia_driver() {
    # Drivers
    add-apt-repository ppa:graphics-drivers -y
    apt-get update
    apt-get install -y nvidia-driver-440
    modprobe nvidia
    echo "Please restart the machine with '/sbin/shutdown -r now' at your earliest convinience"
}

function uninstall_old_nvidia() {
    if command -v docker >/dev/null 2>&1; then
        docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
    fi
    systemctl stop docker
    apt-get -y purge nvidia*
    #while [ $(lsmod | grep nvidia) ]; do
    lsmod | grep nvidia | awk '{ print $1; }' | xargs -r rmmod
    #done
}

function install_nvidia() {
    if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
        version=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | sed -e 's/\.[0-9]*//')
        if [ "$version" -ge 440 ]; then
            nvidia-smi
        else
            echo "Using NVIDIA driver verison $version incompatible with finetune"
            uninstall_old_nvidia
            install_nvidia_driver
        fi
    else
       echo "Command nvidia-smi not found"
       install_nvidia_driver
    fi
}

function install_main_packages() {
    apt update
    apt install -y snapd wget curl iptables python3 python3-pip postgresql-client jq
    apt-get -y install iptables-persistent
    echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections
    echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections
    iptables -P FORWARD ACCEPT
    iptables-save > /etc/iptables/rules.v4

    if command -v ufw >/dev/null 2>&1; then
        ufw default allow routed
    fi
    snap --help
    snap refresh
}
