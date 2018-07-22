#!/usr/bin/env bash

function install_packages() {
    sudo apt-get update
    sudo apt-get install -y build-essential postgresql postgresql-contrib python3-pippython-dev virtualenv nginx supervisor
    # Install nodejs
    sudo curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
    sudo apt-get install -y nodejs
    # Install wkhtmltopdf
    sudo wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.xenial_amd64.deb
    sudo dpkg -i wkhtmltox_0.12.5-1.xenial_amd64.deb
    sudo apt-get -f install -y
    # Install java
    sudo apt-get update
    sudo apt-get install -y default-jre default-jdk
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install -y oracle-java8-installer
}
install_packages







