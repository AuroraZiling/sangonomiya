<p align="center">
  <img width="22%" align="center" src="https://s1.imagehub.cc/images/2023/04/02/5fb7cf5f774ace41b2f0ac57712011e7.md.png" alt="logo">
</p>
<h1 align="center">
  Sangonomiya
</h1>
<p align="center">
  原神祈愿记录工具
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS-lightgreen?style=flat-square" alt="Platform Win32 | Linux | macOS"/>
  </a>

  <a style="text-decoration:none">
    <img src=https://img.shields.io/badge/Language-Python-blue.svg?style=flat-square alt="GPL-3.0"/>
  </a>

  <a style="text-decoration:none">
    <img src=https://img.shields.io/badge/License-GPLv3-orange?style=flat-square alt="GPL-3.0"/>
  </a>
</p>


---

## 注意

本项目目前处于过期状态，即原神3.2版本后的变化均无法兼容

---

*该项目更新频率将在2023.7之前放缓，上学中*

**文档(Github Pages): [Sangonomiya Documents](https://auroraziling.github.io/sangonomiya/)** 

**文档(Netlify): [Sangonomiya Documents](https://sangonomiya.netlify.app/)** [![Netlify Status](https://api.netlify.com/api/v1/badges/41a6827f-3fdb-4026-a374-542a46df6461/deploy-status)](https://app.netlify.com/sites/sangonomiya/deploys)

## 下载 / Download

注：均为自释放压缩包

*历史版本见上文提到的文档*

*如果你使用了较新的Microsoft Edge, 访问蓝奏云下载会出现(您可能拼写错误)的问题，[如何解决?](https://www.bilibili.com/video/BV1i24y197X7)*

### Release 6

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

## 状态 / Status

![Sangonomiya](https://repobeats.axiom.co/api/embed/eec0093cddd14f5e609233104ac2487225cd4c3f.svg "Repobeats analytics image")

## 维护者 / Maintainer

[@AuroraZiling](https://github.com/auroraziling)

## 贡献 / Contributing

欢迎提出 [Issue](https://github.com/AuroraZiling/genshin-pray-export/issues) 或 [Pull Request](https://github.com/AuroraZiling/genshin-pray-export/pulls)

## 许可证 / License

[GNU General Public License v3.0](https://github.com/AuroraZiling/genshin-pray-export/blob/main/LICENSE)
