## 函数

### jsonToOriginal

将UIGF的json格式的数据转换为原始数据(GPE内部使用的数据格式)

参数: `uigf_data` *UIGF的json格式的数据*

返回值: `original_data` *原始数据*

### OriginalToJson

将原始数据(GPE内部使用的数据格式)转换为UIGF的json格式的数据

参数:
1. `basedir` *文件所在根目录*
2. `paths` *根目录下的文件(相对路径); 可用`os.listdir()`*

返回值: `json` *UIGF的json格式的数据*