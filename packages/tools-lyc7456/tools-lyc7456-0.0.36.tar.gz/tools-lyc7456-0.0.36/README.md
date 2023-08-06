> Write by lyc at 2021-7-6  
> 项目地址：[tools-lyc7456 Gitee](https://gitee.com/lyc7456/tools-lyc7456)  


# tools-lyc7456

lyc7456 运维开发小工具。

```bash
$ pip install --upgrade tools-lyc7456
```

## 目录说明

```bash
tools-lyc7456
├── README.md       # 项目说明
├── CHANGELOG.md    # 更新记录
├── LICENSE
├── pyproject.toml
├── setup.py        # 构建主文件
│   ├── src         # 源码目录
└────── tests       # 单元测试目录
```


## 打包与发布 Pypi

> 发布参考：[Python包发布到Pypi](https://www.lyc7456.com/python/20210706145324.html)    

```bash
# 打包
$ python -m build

#发布 Pypi
$ python -m twine upload --repository pypi dist/*
```


