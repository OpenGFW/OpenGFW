# OpenGFW

本项目用来翻越[防火长城](https://zh.wikipedia.org/wiki/%E9%98%B2%E7%81%AB%E9%95%BF%E5%9F%8E)。

运行OpenGFW.py脚本生成的pac文件包含相关规则帮助自动识别流量从而判断是否使用代理服务器进行科学上网。

进行相关配置后可以无忧无虑的科学上网。

## 运行环境

* Pythin 2.7.X 
* Python库**Request**

## 安装
### Python 2.7.X

[官方下载Python](https://www.python.org/)

###Request

使用[pip](https://pip.pypa.io/en/stable/installing/)安装Request非常方便。

`
下载[get-pip.py](https://bootstrap.pypa.io/get-pip.py)
$ pip install requests 
`
## 使用

~~~
Usage: python OpenGFW.py <type> <host> <port>

Examples:
	python OpenGFW.py PROXY 127.0.0.1 8088
	python OpenGFW.py SOCKS 127.0.0.1 1080
	python OpenGFW.py SOCK5 127.0.0.1 1080

~~~

pac使用方法参考：

[GFWList](https://github.com/FelisCatus/SwitchyOmega/wiki/GFWList)

## 感谢

感谢[gfwlist](https://github.com/gfwlist/gfwlist)提供相关规则