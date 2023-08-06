#!/bin/bash

# Ensure Sudo
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
. $DIR/infra/check_infra.sh
. $DIR/infra/utils.sh
. $DIR/infra/ubuntu_setup.sh
BASENAME=$(basename "$0")
export PATH=$PATH:/snap/bin:$DIR


read -r -d '' base_usage <<- EOM
    Command line interface for indico's deployment docker image.

    $(basename "$0") [COMMAND]

    COMMAND:
        help
            Print this help message

        check
            Verifies that current machine meets specs required to run Indico's application

        create
            Install all necessary tools and packages needed for the installation

EOM


function configure_kubelet() {
    updated_kubelet_conf=false
    updated_apiserver_conf=false
    kubelet_conf=/var/snap/microk8s/current/args/kubelet
    apiserver_conf=/var/snap/microk8s/current/args/kube-apiserver

    # POD CIDR
    curr_arg=$(cat $kubelet_conf | grep -- "--pod-cidr")
    if [ -z "$curr_arg" ]; then
        echo "--pod-cidr=10.1.1.0/16" >> $kubelet_conf
        updated_kubelet_conf=true
    elif ! [[ "$curr_arg" =~ --pod-cidr=.*\/16$ ]]; then
        [[ $curr_arg =~ --pod-cidr=(.*)\/ ]]
        sed -i "s@$curr_arg@--pod-cidr=${BASH_REMATCH[1]}/16@g" $kubelet_conf
        updated_kubelet_conf=true
    fi

    # POD LIMIT
    curr_arg=$(cat $kubelet_conf | grep -- "--max-pods")
    if [ -z "$curr_arg" ]; then
        echo "--max-pods=200" >> $kubelet_conf
        updated_kubelet_conf=true
    elif [ "$curr_arg" != "--max-pods=200" ]; then
        sed -i "s/$curr_arg/--max-pods=200/g" $kubelet_conf
        updated_kubelet_conf=true
    fi

    # ALLOW PRIVILEGED
    curr_arg=$(cat $apiserver_conf | grep -- "--allow-privileged")
    if [ -z "$curr_arg" ]; then
        echo "--allow-privileged=true" >> $apiserver_conf
        updated_apiserver_conf=true
    elif [ "$curr_arg" != "--allow-privileged=true" ]; then
        sed -i "s/$curr_arg/--allow-privileged=true/g" $apiserver_conf
        updated_apiserver_conf=true
    fi

    if $updated_kubelet_conf; then
        systemctl restart snap.microk8s.daemon-kubelet
    fi

    if $updated_apiserver_conf; then
        systemctl restart snap.microk8s.daemon-apiserver
    fi

}


function install_microk8s() {
    if ! command -v microk8s.kubectl >/dev/null 2>&1; then
        snap install microk8s --classic --channel=1.15/stable
    elif ! snap info microk8s | grep '^tracking:.*1\.15/stable$'; then
        snap refresh --channel=1.15/stable microk8s
    fi

    configure_kubelet
    echo "Enabling microk8s"
    # First check and modify the kubelet as necessary


    if ! microk8s.status | grep "microk8s is running"; then
        microk8s.start
    fi
    snap alias microk8s.kubectl kubectl || echo ''
    microk8s.enable dns gpu
    microk8s.status && microk8s.inspect
}

function setup() {
    if has_internet; then
        set -e
        # Nvidia and main packages come from the os setup.sh file
        install_main_packages
        install_nvidia
        install_microk8s
    else
        echo "Currently not implemented"
    fi
}


command_to_run=$1; shift

case "${command_to_run}" in
  check)
      check_infra $@
      ;;
  create)
      setup $@
      ;;
  help)
      echo "$base_usage"
      exit 1
      ;;
esac

