os_type = (ENV['OS_TYPE'] || "centos").downcase

case os_type
when "centos"
  Vagrant.configure(2) do |config|
    (1..3).each do |i|
      nodename = "node#{i}"
      config.vm.define nodename, primary: i == 1, autostart: i == 1 do |node|
        node.vm.box = "laincloud/centos-lain"
        node.vm.hostname = nodename
        node.vm.provider "virtualbox" do |v|
          v.memory = i == 1 ? 1536 : 768
        end
        if i == 1
          node.vm.provision "shell",
                            inline: "sudo /vagrant/bootstrap "\
                                    "-m https://l2ohopf9.mirror.aliyuncs.com "\
                                    "-r docker.io/laincloud --vip=192.168.77.201"
        end
        node.vm.network "private_network", ip: "192.168.77.2#{i}"
      end
    end
  end

when "ubuntu"
  ENV["LC_ALL"] = "C"

  unless Vagrant.has_plugin?("vagrant-disksize")
    puts "please install disksize plugin first."
    puts "cmd: vagrant plugin install vagrant-disksize"
    raise "vagrant-disksize is not isntalled."
  end

  Vagrant.configure(2) do |config|
    (1..3).each do |i|
      nodename = "node#{i}"
      config.vm.define nodename, primary: i == 1, autostart: i == 1 do |node|
        node.vm.box = "ubuntu/xenial64"
        node.vm.hostname = nodename
        node.disksize.size = '30GB'
        node.vm.provider "virtualbox" do |v|
          v.memory = i == 1 ? 1536 : 768
        end

        if i == 1
          node.vm.provision "shell",
                            inline: "sudo python3 /vagrant/bootstrap "\
                                    "-m https://l2ohopf9.mirror.aliyuncs.com "\
                                    "-r docker.io/laincloud --vip=192.168.77.201"
        else
          node.vm.provision "shell",
                            inline: "sed -i 's/^PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config && "\
                                    "systemctl restart sshd &&" \
                                    "echo 'root:vagrant'  | chpasswd &&" \
                                    "sed -i s/archive.ubuntu.com/mirrors.ustc.edu.cn/g /etc/apt/sources.list && " \
                                    "apt update && apt install -y python"
        end
        node.vm.network "private_network", ip: "192.168.77.2#{i}"
      end
    end
  end
else
  puts "invalid os type"
end
