## 欢迎大家来到我的库

参考资料(掘金)：https://juejin.cn/post/6844903800118083591

# python  lib 的更新操作：

命令： 注意：每次需要删除 文件夹（ dist ,ls_ai_lib.egg-info） 每次上传前修改 version 版本号

1（本地数据打包）python -m pip install --upgrade pip setuptools wheel 
2（# 运行setup.py ）python setup.py sdist 
3（进入dist
输入账号密码上传）python -m twine upload dist/*

账号:qaufue 密码:199595!@#

# 使用的方法

1， pip install ai_lib_ls 2，from ai_lib_ls import *
3，

