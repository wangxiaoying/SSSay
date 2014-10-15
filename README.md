#SSSay

##Packages

- MySQL
- Python 3.4
- PyMySQL
	`pip3 install PyMySQL`
- simplejson
	`pip3 install simplejson`

##SQL backup & recovery

###Backup
数据库的结构由Django自动生成，因此在备份的时候只备份表中的数据即可。
`mysqldump -u sssay -p -t sssay {TABLE_NAME} > {TABLE_NAME}.sql`

其中 `-t` 参数的作用就是，只导出数据而不导出表结构SQL。

###Recovery
进入 mysql 终端，运行：
`source xxx.sql`