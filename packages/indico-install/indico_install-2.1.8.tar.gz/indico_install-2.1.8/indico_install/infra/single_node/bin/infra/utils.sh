#!/bin/bash

function has_internet() {
    res=100
    if command -v wget >/dev/null 2>&1; then
        wget -q --spider http://google.com
        res=$?
    elif command -v nc >/dev/null 2>&1; then
        echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1
        res=$?
    elif command -v curl >/dev/null 2>&1; then
        curl -Is http://www.google.com | head -1 | grep 200
        res=$?
    elif command -v ping >/dev/null 2>&1; then
        ping -q -w 1 -c 1 8.8.8.8 > /dev/null
        res=$?
    else
        echo "Unable to determine internet"
    fi

  if [ $res -eq 0 ]; then
      return 0 #True
  else
      return 1 # False
  fi
}
