#!/bin/bash

#4gb GPU memory
#32 GB system memory
#Nvidia driver version at least 384
#8 x CPU cors
#64-bit linux
#Docker version xxx
#Microk8s version xxx
#nivdia-docker2 (version or existence)
#kernel version 3.10
#Ensure VT-x or AMD-v virtualization is enabled
#500GB available drive space
#sudo command access
RED='\033[0;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
YELLOW='\e[33m'


function check_val {
    VALUE=$1
    MINIMUM=$2
    STRING=$3
    echo -n "$STRING ... "

    if [ $VALUE -ge $MINIMUM ]; then
        printf "${GREEN}PASSED${NC}\n"
    else
        printf "${RED}FAILED${NC}\n"
    fi
}

function compare_versions() {

    # Trivial v1 == v2 test based on string comparison
    [[ "$1" == "$2" ]] && return 0

    # Local variables
    local regex="^(.*)-r([0-9]*)$" va1=() vr1=0 va2=() vr2=0 len i IFS="."

    # Split version strings into arrays, extract trailing revisions
    if [[ "$1" =~ ${regex} ]]; then
        va1=(${BASH_REMATCH[1]})
        [[ -n "${BASH_REMATCH[2]}" ]] && vr1=${BASH_REMATCH[2]}
    else
        va1=($1)
    fi
    if [[ "$2" =~ ${regex} ]]; then
        va2=(${BASH_REMATCH[1]})
        [[ -n "${BASH_REMATCH[2]}" ]] && vr2=${BASH_REMATCH[2]}
    else
        va2=($2)
    fi

    # Bring va1 and va2 to same length by filling empty fields with zeros
    (( ${#va1[@]} > ${#va2[@]} )) && len=${#va1[@]} || len=${#va2[@]}
    for ((i=0; i < len; ++i)); do
        [[ -z "${va1[i]}" ]] && va1[i]="0"
        [[ -z "${va2[i]}" ]] && va2[i]="0"
    done

    # Append revisions, increment length
    va1+=($vr1)
    va2+=($vr2)
    len=$((len+1))

    # *** DEBUG ***
    #echo "TEST: '${va1[@]} (?) ${va2[@]}'"

    # Compare version elements, check if v1 > v2 or v1 < v2
    for ((i=0; i < len; ++i)); do
        if (( 10#${va1[i]} > 10#${va2[i]} )); then
            return 1
        elif (( 10#${va1[i]} < 10#${va2[i]} )); then
            return 2
        fi
    done

    # All elements are equal, thus v1 == v2
    return 0
}

function check_infra() {
    if which df &>/dev/null &&
            which lscpu &> /dev/null &&
            which awk &> /dev/null &&
            which cut &> /dev/null &&
            which tr &> /dev/null &&
            which grep &> /dev/null &&
            [ -f /proc/meminfo ];
    then 
        check_val 1 1 "Basics"
    else
        check_val 1 2 "Basics"
        printf "${RED}This checker uses basic linux commands df,lscpu,awk,cut,tr, and grep and system files like /proc/meminfo. Not all of them were found in your path.${NC}\n"
        exit
    fi


    if which cc &>/dev/null 
    then 
        check_val 1 1 "compiler"
    else
        check_val 1 2 "compiler"
        printf "${RED}the gcc package is required to install NVIDIA drivers.${NC}\n"
        exit
    fi


    ARCH=$(lscpu |awk '/Architecture/ { print $2 }')
    if [ $ARCH = "x86_64" ]; then
        check_val 0 0 "System Architecture: $ARCH"
    else
        check_val 0 1 "System Architecture: $ARCH"
    fi

    CPUS=$(lscpu |awk '/^CPU\(s\):/ { print $2 }')
    check_val $CPUS 8 "CPUS: $CPUS"

    MEMORY=$(awk '/MemTotal/ { print $2 }' /proc/meminfo)
    check_val $MEMORY 31000000 "Memory: $MEMORY"

    KERNEL=$(uname -r)
    compare_versions $KERNEL 3.10
    check_val 1 $? "Kernel: $KERNEL"

    MINSPACE=500000000000
    SPACE=$(df -B1 | awk -v MS="$MINSPACE" '{ if ($6 != "Mounted" && $4 >= MS ) print "  ",$6,$4 }')
    if [ -z "$SPACE" ]; then
        printf "Disk Space: 0 drives with 500GB available ${RED}FAILED${NC}\n"    
    else
        check_val 1 1 "Drives with enough available disk space for installation:"
        echo -e "${GREEN}$SPACE${NC}"
    fi

    if [ -z "$SUDO_USER" ]; then
        printf "${YELLOW}run check_val as sudo to verify sudo access is set approriately${NC}\n"
    else
        echo "sudo check_val complete. if errors are displayed above, installation will not be possible"
    fi

    SMI=$(which nvidia-smi 2>/dev/null)
    if [ -x "$SMI" ]; then 
        NVIDIA=$(nvidia-smi --query-gpu=gpu_name,gpu_bus_id,vbios_version,memory.total,driver_version --format=csv,noheader,nounits)
        GPU=$(echo -n "$NVIDIA"  | cut -d , -f 1 )
        GMEMORY=$(echo -n "$NVIDIA"  | cut -d , -f 4 |tr -d " ")
        GDRIVER=$(echo -n "$NVIDIA"  | cut -d , -f 5 |tr -d " ")

        echo "GPU Name: $GPU"

        compare_versions $GDRIVER 410.0
        check_val 1 $?  "NVIDIA Driver: $GDRIVER"

        check_val $GMEMORY 4000 "GPU Memory: $GMEMORY"
    else
        printf "nvidia-smi not found, GPU cannot be verified ... ${RED}FAILED${NC}\n"
    fi

    DOCKER=$(which docker 2>/dev/null)
    if [ -x "$DOCKER" ]; then
        DOCKERVERSION=$(docker version --format '{{.Server.Version}}'|grep ce)
        DOCKERVERSIONPLAIN=$(docker version --format '{{.Server.Version}}')
        compare_versions $DOCKERVERSION 18.06.1-ce
        check_val 1 $? "Docker Version: $DOCKERVERSIONPLAIN"
    else
        printf "docker not found ... ${RED}FAILED${NC}\n"
    fi

    DOCKERCOMPOSE=$(which docker-compose 2>/dev/null)
    if [ -x "$DOCKERCOMPOSE" ]; then
        DOCKERCVERSION=$(docker-compose version --short)
        compare_versions $DOCKERCVERSION 1.22.0
        check_val 1 $? "Docker Compose Version: $DOCKERCVERSION"
    else
        printf "docker-compose not found ... ${RED}FAILED${NC}\n"
    fi

    nex=$(which nvidia-docker 2>/dev/null)
    if [ -x "$nex" ]; then 
        NVIDIADOCKER=$(nvidia-docker version |(awk '/NVIDIA Docker/ { print $3 }'))
        compare_versions $NVIDIADOCKER 2.0
        check_val 1 $? "NVIDIA Docker: $NVIDIADOCKER"
    else
        printf "nvidia-docker cannot be found, nvidia-docker cannot be verified ... ${RED}FAILED${NC}\n"
    fi

    ex=$(which microk8s.status 2>/dev/null)
    if [ -x "$ex" ]; then
        MICROK8S=$(microk8s.status | grep 'is running')
        check_val 0 $? "$MICROK8S"
    else
        printf "MicroK8S is not installed ... ${RED}FAILED${NC}\n"
    fi

    KUBE=$(which kubectl 2>/dev/null)
    if [ -x "$KUBE" ]; then
        KUBENODES=$(kubectl describe nodes | wc -l)
        check_val $KUBENODES 2 "KUBECTL NODES: $(kubectl get nodes)"
    else
        printf "Kubectl is not available... ${RED}FAILED${NC}\n"
    fi
}
