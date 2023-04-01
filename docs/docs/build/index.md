## 运行环境 / Environment

1. Python: `3.8`
2. OS: `Windows 10+ / MacOS`

## 安装 / Installation

需安装库: `PyQt6, PyQt6-Fluent-Widgets[full], PyQt6-Frameless-Window`

对应脚本:
```commandline
pip install PyQt6
pip install "PyQt6-Fluent-Widgets[full]" 
pip install PyQt6-Frameless-Window
```

## 打包 / Packaging

安装`pyinstaller`
```commandline
pip install pyinstaller
```

### Windows

```commandline
pyinstaller sangonomiya_win32.spec
```

### MacOS

```commandline
pyinstaller sangonomiya_macOS.spec
```