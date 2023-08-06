# [MSSDK](https://github.com/cdmaxsmart/mssdk) 安装指导

## 重要提示

1. 首先请确认安装 [Python](https://www.python.org/) 3.6 及以上版本, 这里推荐 [Python](https://www.python.org/) 3.7.5 版本;
2. 推荐 [Anaconda](https://www.anaconda.com/), 可以解决大部分安装问题.

## 安装 mssdk

### 通用安装

```
pip install mssdk  --upgrade
```

### 国内安装-Python

```
pip install mssdk -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
```

### 国内安装-Anaconda

```
pip install mssdk -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --user  --upgrade
```

## 使用 mssdk

### 全局 token 设置

```python
import mssdk as qh
qh.set_token("在此处输入 token，可以联系麦思多维科技管理员获取")
```

如上代码进行设置后，之后在本地调取数据可以直接使用如下代码：

```python
from mssdk import pro_api
pro = pro_api()  # 此处由于全局 token 的设置，在本机不需要再次输入
commodity_flow_long_df = pro.commodity_flow_long(date="2018-08-08")
print(commodity_flow_long_df)
```

### 临时 token 设置

```python
from mssdk import pro_api
pro = pro_api(token="在此处输入您的token，可以通过联系管理员获取")  # 此处 token 仅供临时使用
commodity_flow_long_df = pro.commodity_flow_long(date="2018-08-08")
print(commodity_flow_long_df)
```


## R 语言支持

### 安装 Anaconda

[下载 Windows 64 位 Python 3.8 的 Anaconda](https://repo.anaconda.com/archive/Anaconda3-2020.07-Windows-x86_64.exe)


### 安装 R 语言

[下载 R](https://mirrors.tuna.tsinghua.edu.cn/CRAN/bin/windows/)

[下载 RStudio](https://download1.rstudio.org/desktop/windows/RStudio-1.3.959.exe)

先安装 R，再安装 RStudio，选择默认步骤安装即可。

### 在 R 语言中安装相应的包

[Reticulate](https://rstudio.github.io/reticulate/)

```
install.packages("reticulate")
```

在安装完成后通过

```
library(reticulate)
use_python("/usr/local/bin/python")
```

调用本地的 Python 程序，其中 usr 需要替换为本地电脑的用户名。

最后展示一段演示代码，此代码在 R 语言中通过 reticulate 包来调用 [MSSDK](https://github.com/cdmaxsmart/mssdk) 获取数据：

```
library(reticulate)  # 导入 reticulate 包
use_python("/king/local/bin/python")  # 其中的 king 为本地电脑用户名
# use_condaenv(condaenv="ak_test", required = TRUE)  # 也可以使用 conda 创建的虚拟环境，其中的 ak_test 为虚拟环境名称
ms <- import("mssdk")  # 类似于 import mssdk as ms
stock_df <- ms$stock_em_yysj(date="20200331")  # 类似于 ms.stock_em_yysj(date="20200331")
print(stock_df)  # 查看数据
```

```
   scode    sname  trademarket          reportdate              frdate
1 600396 金山股份   上交所主板 2020-03-31T00:00:00 2020-04-08T00:00:00
2 002913   奥士康 深交所中小板 2020-03-31T00:00:00 2020-04-08T00:00:00
3 002007 华兰生物 深交所中小板 2020-03-31T00:00:00 2020-04-08T00:00:00
4 002838 道恩股份 深交所中小板 2020-03-31T00:00:00 2020-04-09T00:00:00
5 603186 华正新材   上交所主板 2020-03-31T00:00:00 2020-04-09T00:00:00
6 300208 青岛中程 深交所创业板 2020-03-31T00:00:00 2020-04-09T00:00:00
               fcdate scdate tcdate              radate securitytypecode
1                   -      -      - 2020-04-08T00:00:00        058001001
2                   -      -      - 2020-04-08T00:00:00        058001001
3                   -      -      - 2020-04-08T00:00:00        058001001
4                   -      -      - 2020-04-09T00:00:00        058001001
5                   -      -      - 2020-04-09T00:00:00        058001001
6 2020-04-16T00:00:00      -      - 2020-04-16T00:00:00        058001001
  trademarketcode
1    069001001001
2    069001002003
3    069001002003
4    069001002003
5    069001001001
6    069001002002
```

## 安装报错解决方案

### 1. 安装 lxml 库失败的错误

- 安装 wheel, 需要在 Windows 的命令提示符中运行如下命令:

```
pip install wheel
```

- 在[这里下载](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml3)与您的 Python 版本对应的 **.whl** 文件, **注意别改文件名!**

以下提供 64 位电脑的版本, 所以下载对应的 64 位就可以, 点击如下链接也可以下载:

1. [lxml‑4.5.0‑cp36‑cp36m‑win_amd64.whl](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/software/lxml/lxml-4.5.0-cp36-cp36m-win_amd64.whl)
2. [lxml‑4.5.0‑cp37‑cp37m‑win_amd64.whl](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/software/lxml/lxml-4.5.0-cp37-cp37m-win_amd64.whl)
3. [lxml‑4.5.0‑cp38‑cp38‑win_amd64.whl](https://jfds-1252952517.cos.ap-chengdu.myqcloud.com/akshare/software/lxml/lxml-4.5.0-cp38-cp38-win_amd64.whl)

- 进入 **.whl** 所在的文件夹, 执行命令即可完成安装, 如下

```
pip install 带后缀的完整路径和文件名
```

### 2. 安装超时的错误

1.大致报错如下, 出现关键词 **amt** :

```
Traceback (most recent call last):
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/requests/packages/urllib3/response.py", line 228, in _error_catcher
yield
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/requests/packages/urllib3/response.py", line 310, in read
data = self._fp.read(amt)
File "/home/xiaoduc/.pyenv/versions/3.7.3/lib/python3.7/site-packages/pip/_vendor/cachecontrol/filewrapper.py", line 49, in read
data = self.__fp.read(amt)
```

2.解决方案如下:

方法一

```
pip --default-timeout=100 install -U mssdk
```

方法二

使用全局代理解决

### 3. 拒绝访问错误

1.大致报错如下, 出现关键词 **拒绝访问** :

```
Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/mac/Anaconda/anaconda3/lib/python3.7/site-packages/cv2/__init__.py'
Consider using the `--user` option or check the permissions.
```

2.解决方案如下:

方法一

```
pip install mssdk --user
```

方法二

使用管理员权限(右键单击选择管理员权限)打开 Anaconda Prompt 进行安装

### 4. 提示其他的错误

- 方法一: 确认并升级您的 Anaconda 或者 Python 到 64 位的 **Python3.7** 及以上版本
- 方法二: 使用 conda 的虚拟环境来安装, 详见 **[MSSDK](https://github.com/cdmaxsmart/mssdk) 环境配置** 板块的内容
