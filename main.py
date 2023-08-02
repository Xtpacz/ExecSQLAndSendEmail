# import sys
# import time
# import pymysql
# import pandas as pd
# import json
# import traceback
# import datetime
# import locale
# import os
# import logging
# import yagmail
# import yaml
# import logging.config
#
# database_info = None
# mail_info = dict()
# data = None
# file_path_csv = None
# sql_content = None
# sub_sql = None
# mysql = None
# WEEKDAY_EN_2_NUM  = {
#     "Monday": 1,
#     "Tuesday": 2,
#     "Wednesday": 3,
#     "Thursday": 4,
#     "Friday": 5,
#     "Saturday": 6,
#     "Sunday": 7,
# }
#
#
# def sendEmail():
#     receivers = mail_info["receivers"]
#     # 如果没有填写任何接收者的邮箱,则不发送邮件
#     if not receivers:
#         logging.info("没有填写接收人邮箱信息,这个报表保存在本地即可,不需要发送邮件")
#         return
#     mail_host = data["mail"]["mail_host"]
#     sender = data["mail"]["sender"]
#     password = data["mail"]["password"]
#     subject = mail_info["subject"]
#     content = mail_info["content"]
#     logging.info("准备发送邮件...")
#     logging.info(
#         "发送邮件的详细信息如下："
#         + "\n发送人: "
#         + sender
#         + "\n接收人: "
#         + str(receivers)
#         + "\n主题: "
#         + subject
#         + "\n邮件内容: "
#         + content
#         + "\n附件: "
#         + str(file_path_csv)
#         + "\n------------------------------------------------"
#     )
#     logging.info("准备完毕, 开始发送邮件...")
#     try:
#         mail = yagmail.SMTP(user=sender, password=password, host=mail_host)
#         mail.send(
#             to=receivers, subject=subject, contents=content, attachments=file_path_csv
#         )
#     except Exception as e:
#         logging.warning("邮件发送失败，发送失败的邮件如下: " + str(file_path_csv))
#     else:
#         logging.info("邮件发送成功！\n\n")
#
#
# def search_and_save_csv():
#     # 执行sql语句
#     logging.info("正在执行sql语句...")
#     mysql.execute(sql_content)
#
#     # 拿到表头
#     des = mysql.description
#     title = [each[0] for each in des]
#
#     # 拿到数据库查询的内容
#     result_list = []
#     for each in mysql.fetchall():
#         result_list.append(list(each))
#     logging.info("拿到了报表内容，接下来保存为csv格式文件")
#     # 保存成dataframe
#     df_dealt = pd.DataFrame(result_list, columns=title)
#     # 保存成csv 这个utf_8_sig编码是为了防止中文没法保存，index=None的意思是没有行号
#     df_dealt.to_csv(file_path_csv, index=None, encoding="utf_8_sig", lineterminator="\r\n")
#     logging.info("成功导出报表!\n")
#
#
# def init_con():
#     host = database_info["host"]
#     port = int(database_info["port"])
#     user = database_info["user"]
#     password = database_info["password"]
#     charset = database_info["charset"]
#     content = pymysql.Connect(
#         host=host,
#         port=port,
#         user=user,
#         passwd=password,
#         charset=charset,
#     )
#     cursor = content.cursor()
#     logging.info("数据库链接成功")
#     return cursor
#
#
# def okgogogo():
#     global sql_content
#     # 读取sql语句内容
#     with open(mail_info["sqlFileLocation"], "r", encoding="utf-8") as file:
#         sql_content = file.read()
#     if sql_content is not None:
#         logging.info("SQL语句读取成功")
#
#     # 先创建当前要写入的文件，之后再写入
#     global file_path_csv
#     file_path_csv = mail_info["file_path"] + ".csv"
#
#     # 执行SQL查询并且保存报表, 若要保存为csv则传入file_path_csv，否则传入file_path_xlsx
#     # 但是目前导出xlsx的功能还没有完成，后续完善
#     logging.info("要生成的csv文件地址: " + file_path_csv)
#     n = mail_info["exec_sql_count"]
#     logging.info("这个SQL要执行 " + str(n) + " 次\n")
#     for i in range(1, n + 1):
#         logging.info("第" + str(i) + "次执行sql")
#         search_and_save_csv()
#
#
# def check_folder_exists(folder_path):
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#         logging.info("成功创建文件夹: " + folder_path)
#     else:
#         logging.info(folder_path + ": 文件夹已存在,不需要重新创建")
#
#
# def prepareAndHandle():
#     # 获取当前日期以及当前是星期几,并将英文星期转换为数字1~7
#     current_date = datetime.datetime.now().date()
#     weekday_today = current_date.strftime("%A")
#     weekday_today = WEEKDAY_EN_2_NUM[weekday_today]
#
#     # 使用字典来保存多个连接. 其中key是链接的名称, value是数据库链接信息
#     dbs = dict()
#     for x in data["connections"]:
#         dbs[x] = data["connections"][x]
#     mail = data["mail"]
#
#     # 解析所有的报表信息
#     reports = mail["reports"]
#     # 遍历每个报表，先检查今天是否要发送这个报表，然后再以每个报表为单位进行处理
#     for report_key, report in reports.items():
#         when = report["when"]
#         # 如果这个报表今天不需要发送，则continue
#         if weekday_today not in when:
#             continue
#
#         # 配置这个报表需要的数据库链接信息
#         global database_info
#         database_info = dbs[report["connection"]]
#         # 初始化数据库链接
#         global mysql
#         mysql = init_con()
#
#         report_name = report["report_name"]
#         today = datetime.date.today()
#         # 完整的报表名称例如：客户旅程表_2023-07-15
#         handledReportName = report_name + "_" + str(today)
#         # 检查并构造文件夹,文件路径例如：myfiles\\results\\客户旅程报表
#         report_save_folder = "myfiles\\results\\" + report_name
#         check_folder_exists(report_save_folder)
#         logging.info("正在处理的报表是: " + report_name)
#
#         global mail_info
#         mail_info = report
#         mail_info["report_folder"] = report_save_folder
#         mail_info["file_path"] = report_save_folder + "\\" + handledReportName
#         mail_info["sqlFileLocation"] = "myfiles\\queries\\" + mail_info["sql_name"]
#
#         is_multi_sql = mail_info["multi_sql"]
#         if is_multi_sql == 1:  # 多个子SQL,都执行完了然后合并
#             logging.info("检测到要执行多个SQL,然后将csv文件合并")
#             global sub_sql
#             print(mail_info["sub_sql"])
#         else:
#             okgogogo()
#             sendEmail()
#
#
# def setup_logging(
#         default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"
# ):
#     """
#     Setup logging configuration
#     """
#     my_path = default_path
#     value = os.getenv(env_key, None)
#     if value:
#         my_path = value
#     if os.path.exists(my_path):
#         with open(my_path, "rt") as f:
#             config = yaml.safe_load(f)
#         logging.config.dictConfig(config)
#     else:
#         logging.basicConfig(level=default_level)
#
#
# def report_task():
#     setup_logging()
#     logging.Formatter.converter = time.localtime
#     logging.info("程序开始")
#     current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
#     logging.info("当前路径：" + current_path)
#     os.chdir(current_path)
#     logging.info("读取config.json配置文件...")
#     global data
#     with open("myfiles/config.json", "r", encoding="utf-8") as file:
#         data = json.load(file)
#     logging.info("配置文件读取成功！\n")
#
#     prepareAndHandle()
#
#     logging.info("程序结束")
#
#
# if __name__ == "__main__":
#     try:
#         report_task()
#     except Exception as e:
#         logging.error(f"main Exception: {traceback.format_exc()}")
#         raise
