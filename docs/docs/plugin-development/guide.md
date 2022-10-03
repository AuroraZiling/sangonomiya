# 插件开发指南

*插件功能目前处于测试阶段，只能实现极少部分功能*

## 简介

插件在`Release 5 Development 7`版本中被引入，仅支持`Python`语言

插件将会从`工具箱`中加载并显示

![gpe_plugin_1.png](https://s2.loli.net/2022/10/02/JlQpEnmdgN6sTzO.png)

## 缺陷须知

1. 插件可调用的库受限
   >考虑到程序占用空间的问题，插件只能调用[部分第三方库](../references/libs.md)

2. `QHBoxLayout()` 和 `QVBoxLayout()` 是兼容性最好的布局方式
   >因为目前只测试过这俩布局方式，其他布局方式可能会出现问题

3. 插件间无法通信
   >目前还没有实现插件间通信的功能

## 流程

1. 在`plugins`文件夹下创建一个`.py`文件，文件名即为插件名
2. 在该文件中创建一个类，类名为`Plugin`
3. 在类中创建一个`__init__`方法，该方法中需要有一个`self`参数
4. 在`__init__`方法中创建一个`self.plugin_name`变量，类型为`str`，值为插件名或者插件的显示名
5. 在`__init__`方法中创建一个`self.plugin_author`变量，类型为`str`，值为插件作者
6. 在`__init__`方法中创建一个`self.all_layout`变量，定义为`QHBoxLayout()` 或 `QVBoxLayout()`
7. 编写控件，将控件添加到`self.all_layout`中

## 示例

```python
from PyQt6.QtWidgets import QVBoxLayout, QLabel


class Plugin:
    def __init__(self):
        super(Plugin, self).__init__()

        self.plugin_name = "Example Plugin"
        self.plugin_author = "Example Author"

        self.all_layout = QVBoxLayout()
        self.example_label = QLabel("Example Label")
        self.all_layout.addWidget(self.example_label)
```