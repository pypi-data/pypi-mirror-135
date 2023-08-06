### chariot-plugin

---

#### 简介
**chariot-plugin**是千乘系统插件的生成器，用于生成插件基本架构．简单实用．

#### 基本架构
```txt
.
├── actions
│   ├── __init__.py
│   ├── ???.py     
│   ├── models.py
├── Dockerfile
├── help.md
├── icon.png
├── main.py
├── Makefile
├── plugin.spec.yaml
├── requirements.txt
├── SDK
│   ├── base.py
│   ├── chariot.py
│   ├── cli.py
│   ├── __init__.py
│   ├── models.py
│   ├── plugin.py
│   ├── subassembly.py
│   └── web.py
├── tests
│   ├── ???.json
└── triggers
    └── models.py
    └── ???.py
```

- plugin.spec.yaml: 编排文件，自行编写，用于生成插件，声明参数及类型验证．
- actions/???.py: 自动生成，用于编写脚本，是插件的最基本组件之一，也是最常使用的．
- triggers/???.py: 自动生成，用于编写需循环触发的脚本，常用于工作流开头分发任务．
- actions/models.py & triggers/models.py: 自动生成，也可自行修改，用于类型验证，语法参考[pydantic](https://github.com/samuelcolvin/pydantic)
- tests/???.json: 自动生成，用于测试　action和trigger 脚本

#### 环境要求
- python3.+

#### 安装
> pip install chariot-plugin 

#### 插件开发
- 千乘社区: https://www.chariots.cn/market/introduction

#### 官网
- 碳泽官网: https://www.tanze.net.cn/about-Tanze
