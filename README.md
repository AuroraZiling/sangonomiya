# genshin-pray-export

**原神祈愿记录导出**

*原理(浅)讲解: [原神3.0 祈愿/抽卡记录导出工具原理讲解](https://www.bilibili.com/video/BV1cY4y1u758)*

## 下载 / Download

注：均为自释放压缩包

### Release 4 (推荐)
[阿里云盘: 下载/Download](https://www.aliyundrive.com/s/irQ2FkMH22H)

[蓝奏云: 下载/Download](https://auroraziling.lanzouv.com/inxVL0bfagwf) *密码:0000*

### Release 3
[阿里云盘: 下载/Download](https://www.aliyundrive.com/s/CPhESipXJHp)

[蓝奏云: 下载/Download](https://auroraziling.lanzouv.com/iApgh0aysecj) *密码: 0000*

### Release 2
[阿里云盘: 下载/Download](https://www.aliyundrive.com/s/rzJhKpizZ6Z)

[蓝奏云: 下载/Download](https://auroraziling.lanzouv.com/iKiEs0am4v6j) *密码: 0000*

### Release 1
[阿里云盘: 下载/Download](https://www.aliyundrive.com/s/rmi1YWstzXv)

[蓝奏云: 下载/Download](https://auroraziling.lanzouv.com/iF7b30am4qkd) *密码: 0000*

## 目标 / Goals

- [x] 支持彩色列表
- [x] 支持导出 (符合[统一可交换祈愿记录标准](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat))
- [x] 列表显示数据增多 (比如是否属于十连/单抽等)
- [ ] 多UID支持
- [ ] 可更新 *不需要卸载重装*
- [x] 基础的数据分析

## 打包 / Build

需要安装`pyinstaller`
```commandline
pip install pyinstaller
```

```commandline
pyinstaller pray.spec
```

## 已知Bug

1. 关于`qdarkstyle`的Warning:
   >No QCoreApplication instance found. Application patches not applied. You have to call load_stylesheet function after instantiation of QApplication to take effect.

2. **[严重]** 关于代理服务器无法恢复至默认的问题
   > 更新数据后，有可能出现代理服务器为消除的情况，导致无法正常上网
