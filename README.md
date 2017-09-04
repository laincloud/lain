# LAIN

[![MIT license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)
[![Gitter](https://badges.gitter.im/gitterHQ/gitter.svg)](https://gitter.im/laincloud/opensource)
[![Throughput Graph](https://graphs.waffle.io/laincloud/lain/throughput.svg)](https://waffle.io/laincloud/lain/metrics/throughput)

Lain 是一个基于 Docker 的 PaaS 系统。

其面向技术栈多样寻求高效运维方案的高速发展中的组织，DevOps 人力缺乏的 startup ，个人开发者。

统一高效的开发工作流，降低应用运维复杂度；在 IaaS / 私有 IDC 裸机的基础上直接提供应用开发，集成，部署，运维的一揽子解决方案。

设计目标包括但不限于：

- 降低系统管理复杂度
- 简化服务的部署管理
- 优化基础服务的调配
- 提高资源的使用效率
- 统一开发测试生产三环境
- 持续交付工作流的良好支持

## Latest Release

最新版是2.1.1。

- [下载](https://github.com/laincloud/lain/archive/v2.1.1.tar.gz)
- [Release note](https://github.com/laincloud/lain/releases/tag/v2.1.1)

## Quick Start

```shell
curl -fsSL https://github.com/laincloud/lain/archive/v2.1.1.tar.gz | tar xf -
cd lain-2.1.1
vagrant up
# Config DNS in local shell
sudo bash -c 'echo "192.168.77.201  console.lain.local" >> /etc/hosts'
```

初始化完成后即可在浏览器访问console:
```
http://console.lain.local
```

完整的文档在[这里](https://laincloud.gitbooks.io/white-paper/content/)，其中：
- [Install](https://laincloud.gitbooks.io/white-paper/install/cluster.html) 展示了如何从头开始构建 Lain 集群
- [LAIN App Demo](https://laincloud.gitbooks.io/white-paper/tutorial/first-lain-app.html) 展示了如何在 Lain 集群上部署应用

## LAIN 用户微信群
<img src="https://github.com/laincloud/files/raw/master/images/lwg.JPG" width="400">

## Contributors

- @[Qiangning Hong](https://github.com/hongqn)
- @[Jia Mi](https://github.com/mijia)
- @[flex](https://github.com/frostynova)
- @[Tachikoma](https://github.com/sunyi00)
- @[cloudfly](https://github.com/cloudfly)
- @[BaiJian](https://github.com/ericpai)
- @[Pan Li](https://github.com/panli889)
- @[Meng Wenbin](https://github.com/supermeng)
- @[chaoyiwang](https://github.com/wchaoyi)
- @[Zhuoyun Wei](https://github.com/wzyboy)
- @[Xu Tao](https://github.com/xtao)
- @[Chang Cheng](https://github.com/uronce-cc)
- @[Xu Yunnan](https://github.com/XuYunnan)
- @[Zhang Kai](https://github.com/bibaijin)
- @[Xu Zhuofu](https://github.com/ipush)
- @[Luo Libin](https://github.com/onlymellb)

## LICENSE

Lain is licensed under the [MIT license](LICENSE).
