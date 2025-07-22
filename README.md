# rpaPAK

rpa解封包工具qt版，支持解包\封包renpy的.rpa文件

![GitHub watchers](https://img.shields.io/github/watchers/kota-rina3/rpaPAK-qt)   ![GitHub License](https://img.shields.io/github/license/kota-rina3/rpaPAK-qt)   ![GitHub Release](https://img.shields.io/github/v/release/kota-rina3/rpaPAK-qt)   ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/kota-rina3/rpaPAK-qt/total)


------------

### 编译


先安装pyqt6和nuitka模块

`pip3 install pyqt6 nuitka`
> 安装模块到系统，请添加
> 
> `--break-system-packages`
> 
>下载速度慢，挂镜像源
> 
>`-i https://mirrors.aliyun.com/pypi/simple/`

然后在项目根目录下输入编译命令

`nuitka --onefile --standalone --windows-console-mode=disable --show-progress --lto=yes --jobs=4 --enable-plugins=pyqt6 --include-data-file=./pak_ui.ui=./pak_ui.ui --include-data-file=./chs_patch.qm=./chs_patch.qm rpaPAK-qt.py`

### 有Bug 或 想添加新功能？

先fork分支，在自己的分支修改好后，再向上游推送

### TODO：

适配arm64版Windows

适配MacOS（Intel芯片和Apple芯片）

Linux端arm64和龙架构支持（龙架构为新世界ABI2.0）

给Linux用户打deb包

GUI优化
