## 作用
> 通过此脚本，可以很快的创建一个新的商业项目

## 程序说明
程序的思路是把一个原型的模块，复制到一个目录下面（最好不要放到项目的目录下），通过脚本把原来的模块名和文件名称替换
你要创建的模块名，然后修改 sites.php 和 settings.php 创建软连接，导入数据库。

## 使用说明
- 安装依赖：
    因为涉及 Python 操作数据库，所有安装支持 MySQLdb。mac 下只要执行下面命令就行了：
    
    ```shell
    sudo easy_install mysql-python
    ```
- 配置说明：
  下载脚本，然后打开脚本，前面几行程序代码：
  ```python
  #配置文件
  TEPLATE_FILE_PATH  =  '/Users/liuzhang/project/';
  TEPLATE_DATABASE_FILE_PATH = '/Users/liuzhang/project/biz_2013_bak.sql'
  TEPLATE_MODULE_NAME = 'lxws'
  PROJECT_FILE_PATH  =  '/Users/liuzhang/php/biz_2012/'
  ```
   - TEPLATE_FILE_PATH 是你的以此为模板的模块目录地址 
   - TEPLATE_DATABASE_FILE_PATH 数据库文件地址
   - TEPLATE_MODULE_NAME 模板的模块名称
   - PROJECT_FILE_PATH 项目地址
  
- 执行脚本
  配置好了以后，直接执行了下面的命令：
   ```shell
  python create_biz_project.py -m mymodule -h mydomain -d biz_mydatabase
  ```
  - m 是 模块名称
  - h 是 域名
  - d 是 项目的数据库名称

## 其他
- 有兴趣的可以研究，欢迎使用反馈。