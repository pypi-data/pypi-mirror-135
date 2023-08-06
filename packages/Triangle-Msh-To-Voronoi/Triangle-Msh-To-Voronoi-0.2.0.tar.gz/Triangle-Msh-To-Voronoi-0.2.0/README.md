# TriangleToVoronoi

## 使用方法：
1. 安装
```
pip install Triangle-Msh-To-Voronoi
```

2. 导入
```python
import TriToVoronoi as tv
```

2. 读取网格
```python
mshReader = tv.MshReader()
mshReader.ReadHmMsh(r'tri.msh')
```

3. 生成泰森多边形
```python
generateIGroups = [2]  #指定生成泰森多边形的分组，这些分组的单元必须是三角形，不能有双节点
outputFilePath = r'voronoi.msh'  #输出的GID格式Msh文件
outputFolderPath = r'.'            #输出的ele，cor文件夹目录
tv.GenerateVoronoi(generateIGroups,outputFilePath,outputFolderPath,mshReader.elements,mshReader.coords)
```

