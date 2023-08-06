# arcfutil-cvkit

使用OpenCV的arcfutil AFF工具包

## 安装

```commandline
pip install arcfutil-cvkit
```
由于使用了native namespace package结构，在手动安装时请使用pip：

```commandline
pip install -e .
```

## 功能

- 图片转黑线（暂时只有这一个

## 用法

### 图片转黑线函数`image_to_arc()`

```python
from arcfutil.cv import image_to_arc as i2a

arcs = i2a(image_path, time)
```
#### 参数

|参数名|类型|说明|默认值|
|--|--|--|--|
|path|str|图片路径|
|time|int|生成黑线的时间点|
|size|list|接收一个带有4个浮点数的列表，控制图片映射的坐标范围（以原点为基准`[上,右,下,左]`）|`[1,1.5,-0.2,-0.5]`|
|max_gap|float|Hough变换中线之间的最大间隔，过大会导致线之间相连，过小会导致线之间缝隙增大|10|
