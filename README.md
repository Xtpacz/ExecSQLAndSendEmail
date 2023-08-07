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
    "connections": {
        "connection_001": {
            "host": "database IP",
            "port": "database port",
            "user": "database username",
            "password": "database password",
            "charset": "utf8"
        },
        "connection_002": {
            "host": "database IP",
            "port": "database port",
            "user": "database username",
            "password": "database password",
            "charset": "utf8"
        }
    },
    "sender_info": {
        "mail_host": "your mail host",
        "sender": "sender's email",
        "password": "email password"
    },
    "reports": {
        "report_local_test": {
            "connection": "connection_001",
            "report_name": "test report name",
            "subject": "test report subject",
            "content": "test report content",
            "receivers": ["receiver1's email", "receiver2's email"],
            "when": [1, 2, 3, 5],
            "sql_name": "",
            "exec_sql_count": 1,
            "multi_sql": 1,
            "sub_sql": {
                "sql1": "test_sub_sql1.sql",
                "sql2": "test_sub_sql2.sql"
            },
            "merge_basis": ["id", "name"]
        },
        "report_to_mary_1": {
            "connection": "connection_002",
            "report_name": "report_to_mary",
            "subject": "report subject",
            "content": "report content",
            "receivers": [
                "receiver1's email",
                "receiver2's email",
                "receiver3's email"
            ],
            "when": [2, 7],
            "sql_name": "your_sql.sql",
            "exec_sql_count": 2,
            "multi_sql": 0
        }
    }
}

```

