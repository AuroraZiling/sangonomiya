# Sangonomiya

## 注意 / Notice

截至目前，本工具暂无数据自动更新功能，仅靠工具版本更新是低效的。

打算在Release 7对整个项目重构，并重写UI(基于[PyQt-Fluent-Widgets
](https://github.com/zhiyiYo/PyQt-Fluent-Widgets))

---

*该项目更新频率将在2023.7之前放缓，上学中*

*由于MiHoYo疑似在3.2版本更改了Authkey格式，有可能会对旧版本(R5及之前)产生影响*

**原神祈愿记录导出工具**

![](https://img.shields.io/badge/Language-Python-blue.svg?style=flat-square)

**文档: [GPE Documents](https://auroraziling.github.io/genshin-pray-export/)**

*原理(浅)讲解: [原神3.0 祈愿/抽卡记录导出工具原理讲解](https://www.bilibili.com/video/BV1cY4y1u758)*

## 下载 / Download

注：均为自释放压缩包

*历史版本见上文提到的文档*

*由于目前未实现更新功能，每个Release的发布内容将会尽可能多*

*如果你使用了较新的Microsoft Edge, 访问蓝奏云下载会出现(您可能拼写错误)的问题，[如何解决?](https://www.bilibili.com/video/BV1i24y197X7)*

### Release 6 (推荐)

[阿里云盘](https://www.aliyundrive.com/s/ay3Y7WJbJho)

[蓝奏云](https://auroraziling.lanzouv.com/b02juwo3g)

## 卸载 / Uninstall

由于是绿色软件，不会在其他位置留下任何文件

删除整个文件夹即可

## 已实现功能 / Implemented Features

- [x] 彩色列表
- [x] JSON导入/导出 (符合[UIGF统一可交换祈愿记录标准](https://github.com/DGP-Studio/Snap.Genshin/wiki/StandardFormat))
- [x] 列表显示数据增多 (比如是否属于十连/单抽等)
- [x] 基础的数据分析
- [x] 公告显示
- [x] 当期UP池显示
- [x] 多UID

## 打包 / Usage

需要安装`pyinstaller`
```commandline
pip install pyinstaller
```

```commandline
pyinstaller pray.spec
```

## 更新日志 / Changelog

[Change Log](https://auroraziling.github.io/sangonomiya/dev_logs/r7/)

## 使用须知 / Notice

1. 在清除代理设置时，会操作注册表
> 有关键值:
> HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Internet Settings -> ProxyEnable
> HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Internet Settings -> ProxyServer

## 已知Bug

1. [无影响]关于`qdarkstyle`的Warning:
   >No QCoreApplication instance found. Application patches not applied. You have to call load_stylesheet function after instantiation of QApplication to take effect.
2. 占用空间过大(约150MB~320MB):
   >蓝奏云不好传，原因是游戏内公告显示的内置浏览器模块
3. [3.1]对于提那里的判断失效
   >目前统一视作歪出来的

## 维护者 / Maintainer

[@AuroraZiling](https://github.com/auroraziling)

## 贡献 / Contributing

欢迎提出 [Issue](https://github.com/AuroraZiling/genshin-pray-export/issues) 或 [Pull Request](https://github.com/AuroraZiling/genshin-pray-export/pulls)

## 许可证 / License

[GNU General Public License v3.0](https://github.com/AuroraZiling/genshin-pray-export/blob/main/LICENSE)
