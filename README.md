# Ali OSS upload files

depend on [https://github.com/aliyun/aliyun-oss-python-sdk](https://github.com/aliyun/aliyun-oss-python-sdk)

### requirements

* Python3

### Installation

    pip instlal oss2

### Setup

新建 ``settings.py`` 文件, 填入配置项

配置项格式参考 ``settings.sample.py``

### Usage

1. 上传内容需要放在一个目录中
2. 把准备好的目录放在 seat 目录下
3. 执行上传命令
    
    python publisher.py --bucket=xxx --dir=xxx [--cover]

4. 等待执行
5. 结束

参数说明

* --env  [必填] 要上传到什么环境 PROD_EN | PROD_CN | QA_EN ...
* --dir     [必填] 要上传的目录名称
* --cover   [选填] 默认false, 是否覆盖重名文件
