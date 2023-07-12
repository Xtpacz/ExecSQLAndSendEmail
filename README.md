# ExecSQLAndSendEmail
根据自己的需求：
定期从数据库中导出报表，然后将报表发送到特定邮箱

在`config.json`里面设置

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

