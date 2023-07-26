# ExecSQLAndSendEmail
根据自己的需求：
定期从数据库中导出报表，然后将报表发送到特定邮箱



（自己用）

使用说明

将`main.py`打包成`.exe`文件之后

将`logging.yaml`与`main.exe`放在同一个文件夹内

完成之后，整个项目的文件夹布局应该是这样子的：（可以生成目录结构的在线网站：）[Dir Tree Noter (yardtea.cc)](http://dir.yardtea.cc/)

```
project
├─ logging.log
├─ logging.yaml
├─ main.exe
└─ myfiles
 	├─ config.json
 	├─ queries
 	│	├─ report_about_w_to_tom.sql
 	│	└─ report_about_a_to_jack.sql
 	└─ results
 	 	├─ report_about_w_to_tom
 	 	│	├─ report_about_w_to_tom2023-07-23.csv
 	 	│	└─ report_about_w_to_tom2023-07-26.csv
 	 	└─ report_about_a_to_jack
 	 	 	└─ report_about_a_to_jack2023-07-26.csv
```

说明：

`queries`：存放SQL文件

`results`：存放查询出来的报表

其中`config.json`文件内容大致如下所示

```json
{
	"connections":{
		"connection_1":{
			"host":"your host",
			"port":"3306",
			"user":"root",
			"password":"admin",
			"charset":"utf8"
		},
		"connection_2":{
			"host": "xx.xx.xx.xx",
			"port": "3306",
			"user": "root",
			"password": "admin",
			"charset": "utf8"
		},
		"connection_3":{
			"host": "xx.xx.xx.xx",
			"port": "3306",
			"user": "root",
			"password": "admin",
			"charset": "utf8"
		}
	},
	"mail":{
		"mail_host":"mail host",
		"sender":"sender's email address",
		"password":"your password",
		"reports":{
			"report_crm_1":{
				"db": "connection_1",
				"reportName":"your report name",
				"subject":"your subject",
				"content":"your content",
				"receivers":["receiver1's email address","receiver2's email address"],
				"when":"星期四",
				"sqlName":"sql_name.sql",
				"count": 1
			},
			"report_local_1":{
				"db": "connection_2",
				"reportName":"your report name",
				"subject":"your subject",
				"content":"your content",
				"receivers":["receiver1's email address","receiver2's email address"],
				"when":"星期三",
				"sqlName":"sql_name.sql",
				"count": 3
			},
			"report_remote_1": {
				"db": "connection_3",
				"reportName":"your report name",
				"subject":"your subject",
				"content":"your content",
				"receivers":["receiver1's email address","receiver2's email address"],
				"when":"星期三",
				"sqlName":"sql_name.sql",
				"count": 1
			}
		}
	}
}
```

