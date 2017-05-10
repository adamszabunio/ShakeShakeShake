# -*- mode: ruby -*-
# vi: set ft=ruby :

# Require the AWS provider plugin
require 'vagrant-aws'

# Require YAML module
require 'yaml'

# Read YAML file with box details
cred = YAML.load_file('/Users/adamszabunio/.scripts/credentials.yml')

# Create and configure the AWS instance(s)
Vagrant.configure('2') do |config|

  # Use dummy AWS box
  config.vm.box = "ubuntu/xenial64"

  config.vm.provision :shell, path: "bootstrap.sh"

# Specify AWS provider configuration
  config.vm.provider :aws do |aws, override|
    # Read AWS authentication information from environment variables
    aws.access_key_id = cred['aws']['access_key_id']
    aws.secret_access_key = cred['aws']['secret_access_key']

    # Specify SSH keypair to use
    aws.keypair_name = "EC2_SSH_key_pair"

    # Specify region, AMI ID, and security group(s)
    aws.instance_type = "t2.micro"
    aws.region = "us-east-1"
    aws.ami = "ami-f4cc1de2"
    aws.security_groups = ['launch-wizard-1']

    # Specify username and private key path
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "~/.ssh/EC2_SSH_key_pair.pem"
    override.vm.box = "dummy"

  end

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider 'virtualbox' do |virtualbox, override|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
    override.vm.network "private_network", ip: "22.22.22.22"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
