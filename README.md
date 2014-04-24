ut_ali:
Ali数据挖掘大赛程序

说明：

安装python开发环境,建立沙盒环境并激活:

    $virtualenv alienv & source alienv/bin/activate

下载源码:

    $git clone https://github.com/UTT/ut_ali ut_ali

直接下载zip打包文件[地址](https://github.com/UTT/ut_ali/archive/master.zip)


进入到ut_engine目录运行:

    $cd ut_ali/ut_engine
    $python start.py run

可以到/output/latest目录下查看预测结果:
    result.txt

或者直接运行一下命令察看结果:

    $python start.py result

本地预测和评估:

    $python start.py score

提交代码:


enjoy!
