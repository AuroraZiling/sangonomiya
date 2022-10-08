
## 变量

1. character_5_w_list *5星角色(歪)列表*
2. character_5_list *5星角色列表*
3. character_4_list *4星角色列表*
4. weapon_5_w_list *5星武器(歪)列表*
5. weapon_5_list *5星武器列表*
6. weapon_4_list  *4星武器列表*
7. weapon_3_list *3星武器列表*

Tip: 提那里暂时视为 `character_5_list`

## 函数

### get_5

获取五星物品列表和长度

参数: `pray_mode` *祈愿类型(非UIGF)*

返回值: `(data_list, len(data_list))` *列表和列表长度*

### get_4

获取四星物品列表和长度

参数: `pray_mode` *祈愿类型(非UIGF)*

返回值: `(data_list, len(data_list))` *列表和列表长度*

### get_3

获取三星物品列表长度

参数: `pray_mode` *祈愿类型(非UIGF)*

返回值: `len(data_list)` *列表长度*

### guarantee

基础保底分析

参数: `pray_mode` *祈愿类型(非UIGF)*

返回值: `guarantee` *基础的保底分析(str)*