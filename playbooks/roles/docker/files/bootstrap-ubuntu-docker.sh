#!/bin/bash
#
# Created by Yu Yang <yyangplus@NOSPAM.gmail.com> on 2017-12-11
#
if ! which dockerd 2>&1 >/dev/null; then
    sudo apt-get remove docker docker-engine docker.io
    sudo apt-get update
    sudo apt-get -y install \
         linux-image-extra-$(uname -r) \
         linux-image-extra-virtual

    sudo apt-get -y install \
         apt-transport-https \
         ca-certificates \
         curl \
         software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository \
         "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce=17.09.1~ce-0~ubuntu
fi
