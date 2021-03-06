# Ali OSS upload files

Depend on [https://github.com/aliyun/aliyun-oss-python-sdk](https://github.com/aliyun/aliyun-oss-python-sdk)

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
    
    python publisher.py --env=xxx --dir=xxx [--prefix=xxx] [--cover]

4. 等待执行
5. 结束

参数说明

* --env  [必填] 要上传到什么环境 PROD_EN | PROD_CN | QA_EN ...
* --dir     [必填] 要上传的目录名称, 必须是完整路径
* --cover   [选填] 默认false, 是否覆盖重名文件
* --prefix  [选填] 默认 '' , 是否给文件添加访问路径前缀
* --exclude [选填] 默认空, 排除不上传的文件的后缀名 --exclude=html,jade
* --only    [选填] 默认空, 只上传具有指定后缀名的文件  --only=html

文件访问路径:
https://oss-cn-beijing.aliyuncs.com/{bucket}//{key}

example
https://oss-cn-beijing.aliyuncs.com/bj-mc-prod-asset/mc-official/images/index/tech-text-card-icon.png
