### 说明
- 生成各种语言下的html格式的文件
- 减少人工的复制粘贴方式，及其在ios和Android移动端可以很好支持
- 特开发此工具

### 文件说明
- index.html为模板文件
- Excel为各种语言的字符串内容
- 生成的最终html文件路径：Project\mb20G\pivacy_policy

### 运行
- 打开cmd命令，进入到文件所在的目录privacy_policy.py，然后输入命令python privacy_policy.py EN LT ... ...（可同时输入多个语言的简称）

### 规则
- Excel的第二行必须是语言的简称，且各语言简称必须唯一性
- StrID字符串也必须和语言简称在同一行上，且和id在同一列上 
