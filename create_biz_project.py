# -*- coding: utf-8 -*- 
# Author		: liuzhang
# Created		: 20 Apr 2016
# Version		: 1.0
 
import os
import shutil
import MySQLdb
import re
import sys
import getopt

#配置文件
TEPLATE_FILE_PATH  =  '/Users/liuzhang/project/';
TEPLATE_DATABASE_FILE_PATH = '/Users/liuzhang/project/biz_2013_bak.sql'
TEPLATE_MODULE_NAME = 'lxws'
PROJECT_FILE_PATH  =  '/Users/liuzhang/php/biz_2012/'

#获取参数
project_module_name = ''
project_domain_name = ''
project_database_name = ''

opts, args = getopt.getopt(sys.argv[1:], "m:h:d:") 

if len(opts) < 3: 
  	print("创建参数不完整") 
  	sys.exit(1)
for op, value in opts:   
	if op == "-m":  
		project_module_name = value    
	elif op == "-h":    
		project_domain_name = value    
	elif op == "-d":   
		project_database_name = value

#替换为当前模块名
temp_copy_path = TEPLATE_FILE_PATH + project_module_name
temp_copy_module_path = TEPLATE_FILE_PATH + project_module_name + '/modules/' + project_module_name + '/'
temp_copy_theme_path = TEPLATE_FILE_PATH + project_module_name + '/themes/' + project_module_name + '/'
shutil.copytree(TEPLATE_FILE_PATH + TEPLATE_MODULE_NAME, temp_copy_path, True)
os.rename(temp_copy_path + '/modules/' +  TEPLATE_MODULE_NAME,  temp_copy_module_path)
os.rename(temp_copy_path + '/themes/' + TEPLATE_MODULE_NAME,  temp_copy_theme_path)
files_list =  os.listdir(temp_copy_module_path)

for file_name in files_list:
	if (os.path.isfile(temp_copy_module_path + file_name)):
		file_obj = open(temp_copy_module_path + file_name, 'r')
		contents = file_obj.read()
		replaced_contents = contents.replace(TEPLATE_MODULE_NAME,  project_module_name)
		file_obj.close()
		file_obj = open(temp_copy_module_path + file_name, 'w');
		file_obj.write(replaced_contents)
		file_obj.close()
		os.rename(temp_copy_module_path + file_name, temp_copy_module_path + file_name.replace(TEPLATE_MODULE_NAME,  project_module_name))

os.rename(temp_copy_theme_path + TEPLATE_MODULE_NAME + '.info'  , temp_copy_theme_path + project_module_name + '.info' )
file_obj = open(temp_copy_theme_path + 'template.php', 'r')
contents = file_obj.read()
replaced_contents = contents.replace(TEPLATE_MODULE_NAME,  project_module_name)
file_obj.close()
file_obj = open(temp_copy_theme_path + 'template.php', 'w')
file_obj.write(replaced_contents)
file_obj.close()

file_obj = open(temp_copy_path+'/settings.php', 'r')
content = file_obj.read()
file_obj.close()
m1 = re.findall(r"\'php_(.*?)\'", content)
m2 = re.findall(r"SERVER\['HTTP_HOST'\] \. \"/(.*?)\"", content)
m3 = re.findall(r"==\s*\'(.*?)\'", content)
replaced_content = content.replace(m3[0],  project_database_name)
replaced_content_text = replaced_content.replace(m2[0],  project_domain_name)
replaced_content_pk = replaced_content_text.replace(m1[0],  project_module_name)
file_obj = open(temp_copy_path+'/settings.php', 'w')
file_obj.write(replaced_content_pk)
file_obj.close()

#复制到biz目录
shutil.move(temp_copy_path, PROJECT_FILE_PATH + 'sites/' + project_module_name)
print 'create module OK'

#域名写入sites.php
domain_str = "\n$sites['dxy.net."+ project_domain_name + "'] = '" + project_module_name +"';\n"
domain_str += "$sites['dxy.cn."+ project_domain_name + "'] = '" + project_module_name +"';\n"
file_obj = open(PROJECT_FILE_PATH + 'sites/sites.php', 'a')
file_obj.write(domain_str)
file_obj.close

#建立软连接
os.system("cd " + PROJECT_FILE_PATH + "; ln -s . " + project_domain_name)
print 'create soft link OK'

#导入数据库
conn = MySQLdb.connect(host="192.168.200.252",user="php_biz",passwd="drink_coffee",port=3307,charset="utf8")
sql = 'CREATE DATABASE  '+project_database_name+'  DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
cursor = conn.cursor()
cursor.execute(sql)
conn.select_db(project_database_name)

for line in open(TEPLATE_DATABASE_FILE_PATH).read().split(';\n'):
	try:
		if (line):
			cursor.execute(line)
			conn.commit()
	except Exception, e:
		print e
	finally:
		pass
cursor.close()
conn.close()
print 'create database OK'
