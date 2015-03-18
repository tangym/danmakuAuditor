## 部署

### windows
- 安装[chocolatey](https://chocolatey.org/)
- 安装python3环境
```bash
choco install python
```
- 安装pip包管理器
```bash
choco install pip
```
- 安装依赖库requests
```bash
pip install requests
```
- 安装依赖库PyQt4
~下载[SIP](http://jaist.dl.sourceforge.net/project/pyqt/sip/sip-4.16.6/sip-4.16.6.zip)，并解压~（太麻烦了）
根据python版本和操作系统版本选择相应下载Non-official的[PyQt4](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)，打开命令行切换到下载目录下
```bash
pip install PyQt4-*.whl
```
- 检查环境配置是否成功
```bash
python --version
```
应显示`python 3.x.x`版本号
```bash
pip freeze
```
应显示
```bash
PyQt4==4.x.x
requests==x.x.x
```
- 运行程序
```bash
python danmaku_exam_gui.py
```


### ubuntu
- 安装python3环境
```bash
sudo apt-cache update
sudo apt-get install python3
```

- 使用pip安装依赖库
```bash
sudo apt-get install pip3
pip3 install requirements.txt
```

- 运行`danmaku_exam_gui.py`
```bash
python3 danmaku_exam_gui.py
```


## 功能

### uuid
uuid可以由用户输入，也可以由程序生成。
生成uuid根据时间和mac地址计算得到的hash值（32位字符，表示一个16进制数），
从随机位置开始，等间隔地取$n$个5 bits，依次将每个5 bits转换为$[0, 63]$的整数，
对应到大小写字母及数字字符上。本程序设置生成4位字符。

> TODO: 点击连接后，应该将uuid输入框和生成按钮置灰

### 快捷键
可以使用快捷键`Enter`

> TODO: 补充文档和注释

### 弹幕审核日志
程序自动在`danmaku_exam_gui.log`文件记录弹幕审核通过和拒绝的历史。

> TODO: 调整编码问题，使日志文件显示人类能看得懂的中文弹幕


## 文件说明
- `danmaku_exam_gui.py`
- `config.py`
- `channel.py`
- `shorten_id.py`

## 注意
- 建议在演示时，使用**至少3条不同颜色**的弹幕。
- 由于目前使用的审核服务器url是播放弹幕使用的url，因此会导致审核通过一条弹幕后，重新收到该弹幕。看起来就像是将弹幕挪到队尾一样，实际上是已经发送同时又收到一条弹幕。
- 可以使用快捷键，但可能是由于服务器原因（也有可能是其他原因），不能过快的连续发送弹幕（会导致部分弹幕被丢弃）。
