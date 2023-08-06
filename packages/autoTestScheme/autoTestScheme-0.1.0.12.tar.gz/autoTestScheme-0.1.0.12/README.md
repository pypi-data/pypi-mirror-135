
## autoTestScheme提供的一些方法
### 目录相关
```python
import autoTestScheme
autoTestScheme.constant.BASE_DIR # 工作目录（当前项目）
autoTestScheme.constant.TMP_FOLDER # 缓存路径
```

### 读取json或者xml文件
```python
import autoTestScheme
autoTestScheme.file.Json # 读取JSON
autoTestScheme.file.AllureXml # 读取xml
```


### 当前环境
```python
import autoTestScheme
autoTestScheme.start_data.IS_DEBUG  # 是否调试
autoTestScheme.start_data.TEST_ENV  # 当前测试环境
```


# 版本说明
0.0.8.4

```
适配由于falsk版本过高导致的性能脚本启动失败问题
```
0.0.8.5
```
request优化
```