# Genshin Pray Export

**原神祈愿记录导出工具**

![](https://img.shields.io/badge/Language-Python-blue.svg?style=flat-square)

*原理(浅)讲解: [原神3.0 祈愿/抽卡记录导出工具原理讲解](https://www.bilibili.com/video/BV1cY4y1u758)*

## 下载 / Download

注：均为自释放压缩包

*由于目前未实现更新功能，每个Release的发布内容将会尽可能多*

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
- [x] 基础的数据分析
- [x] 公告显示 **已实装R5D4**
- [ ] 图表导出数据 **预计在Release 5实现**
- [ ] 工具箱 *卡池历史记录等* **预计在Release 5实现**
- [ ] 当期UP池显示 **预计在Release 5实现**
- [ ] 多UID支持 **仅计划内**
- [ ] 可更新 *不需要卸载重装* **仅计划内**
- [ ] 真正的文件校验 **仅计划内**
- [ ] 攻略跳转 **仅计划内**
- [ ] 米游社信息显示 **仅计划内**

## 打包 / Usage

需要安装`pyinstaller`
```commandline
pip install pyinstaller
```

```commandline
pyinstaller pray.spec
```

## 更新日志 / Changelog

[Change Log](https://github.com/AuroraZiling/genshin-pray-export/releases)

## 已知Bug

1. [无影响]关于`qdarkstyle`的Warning:
   >No QCoreApplication instance found. Application patches not applied. You have to call load_stylesheet function after instantiation of QApplication to take effect.
2. 武器祈愿效果未知:
   >暂时无法测试，因为没原石抽

## 维护者 / Maintainer

[@AuroraZiling](https://github.com/auroraziling)

## 贡献 / Contributing

欢迎提出 [Issue](https://github.com/AuroraZiling/genshin-pray-export/issues) 或 [Pull Request](https://github.com/AuroraZiling/genshin-pray-export/pulls)

## 许可证 / License

[GNU General Public License v3.0](https://github.com/AuroraZiling/genshin-pray-export/blob/main/LICENSE)
