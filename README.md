# ExecSQLAndSendEmail
根据自己的需求：
定期从数据库中导出报表，然后将报表发送到特定邮箱



（自己用）

使用说明

将`main.py`打包成`.exe`文件之后

将`lib、logging.yaml、setup_logging.py、util.py`与`main.exe`放在同一个文件夹内

完成之后，整个项目的文件夹布局应该是这样子的：（可以生成目录结构的在线网站：）[Dir Tree Noter (yardtea.cc)](http://dir.yardtea.cc/)

```
projcet
├─ code
│    ├─ lib
│    │    ├─ doPrepare.py
│    │    ├─ execSQL.py
│    │    └─ sendEmail.py
│    ├─ logging.yaml
│    ├─ main.exe
│    ├─ setup_logging.py
│    └─ util.py
└─ files
       ├─ config.json
       ├─ queries
       │    ├─ to_Mary001.sql
       │    ├─ to_Mary002.sql
       │    └─ to_Jackson.sql
       └─ results
              ├─ Jackson
              │    └─ 2023-07-13
              │           └─ report_to_Jackson.csv
              └─ Mary
                   └─ 2023-07-13
                          ├─ report001_to_Mary.csv
                          └─ report002_to_Mary.csv
```

说明：

`queries`：存放SQL文件

`results`：存放查询出来的报表

其中`config.json`文件内容大致如下所示

```json
{
	"database":{
		"host":"server IP",
		"port":"port",
		"user":"username",
		"password":"password",
		"charset":"charset"
	},
	"mail":{
		"mail_host":"smtp.xxx.com",
		"sender":"xxx@xxx.com",
		"password":"Email authorization code",
		"to":{
			"people1":{
				"name":"Tom",
				"email":"xxx@xxx.com",
				"subject":"email subject",
				"content":"email content",
				"when":"What day of the week to send an email.",
				"queries":{
					"sql1":{ 
						"fileAddress":"The location where the SQL statement is stored.",
						"fileName":"The name of the generated report."
					}
				}
			},
			"people2":{
				"name":"Mary",
				"email":"xxx@xxx.com",
				"subject":"email subject",
				"content":"email content",
				"when":"What day of the week to send an email.",
				"queries":{
					"sql1":{
						"fileAddress":"The location where the SQL statement is stored.",
						"fileName":"The name of the generated report."
					},
					"sql2":{
						"fileAddress":"The location where the SQL statement is stored.",
						"fileName":"The name of the generated report."
					}
				}
			}
		}
	},
	"results_path":"The location where the generated report is saved."
}
```

