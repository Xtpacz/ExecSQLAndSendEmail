import pymysql
import pandas as pd
import json
import traceback
import datetime
import locale
import os
import logging
import yagmail
import yaml
import logging.config


def sendEmail(sender_info, mail_info, file_path_csv):
    mail_host = sender_info["mail_host"]
    sender = sender_info["sender"]
    password = sender_info["password"]
    receivers = mail_info["receivers"]
    subject = mail_info["subject"]
    content = mail_info["content"]
    logging.info("\n准备发送邮件...")
    logging.info(
        "------------------------发送邮件的详细信息如下：------------------------"
        + "\n[INFO] - 发送人: "
        + sender
        + "\n[INFO] - 接收人: "
        + str(receivers)
        + "\n[INFO] - 主题: "
        + subject
        + "\n[INFO] - 邮件内容: "
        + content
        + "\n[INFO] - 附件: "
        + str(file_path_csv)
        + "\n[INFO] - ----------------------------------------------------------------------"
    )
    logging.info("准备完毕, 开始发送邮件...")
    try:
        mail = yagmail.SMTP(user=sender, password=password, host=mail_host)
        mail.send(
            to=receivers, subject=subject, contents=content, attachments=file_path_csv
        )
    except Exception as e:
        logging.warning("邮件发送失败，发送失败的邮件如下: " + str(file_path_csv))
    else:
        logging.info("邮件发送成功\n\n")


def search_and_save_csv(mysql, sql, file_path_csv):
    """
    执行查询语句并导出为csv的函数，此功能正常使用
    :param sql: 要执行的mysql指令
    :param file_path: 导出的csv文件名
    :return:
    """
    # 执行sql语句
    logging.info("执行sql语句...")
    mysql.execute(sql)

    # 拿到表头
    des = mysql.description
    title = [each[0] for each in des]

    # 拿到数据库查询的内容
    result_list = []
    for each in mysql.fetchall():
        result_list.append(list(each))
    logging.info("拿到了报表内容，接下来保存为csv格式文件")
    # 保存成dataframe
    df_dealed = pd.DataFrame(result_list, columns=title)
    # 保存成csv 这个编码是为了防止中文没法保存，index=None的意思是没有行号
    df_dealed.to_csv(
        file_path_csv, index=None, encoding="utf_8_sig", lineterminator="\r\n"
    )
    logging.info("成功导出报表!")


def init_con(database_info):
    host = database_info["host"]
    port = int(database_info["port"])
    user = database_info["user"]
    dbpassword = database_info["password"]
    charset = database_info["charset"]
    content = pymysql.Connect(
        host=host,
        port=port,
        user=user,
        passwd=dbpassword,
        charset=charset,
    )
    cursor = content.cursor()
    logging.info("数据库链接成功")
    return cursor


def okgogogo(database_info, sender_info, mail_info):
    # 初始化类
    mysql = init_con(database_info)

    # 读取sql语句内容
    with open(mail_info["sqlFileLocation"], "r", encoding="utf-8") as file:
        sql_content = file.read()
    if sql_content is not None:
        logging.info("SQL语句读取成功")

    # 先创建当前要写入的文件，之后再写入
    file_path_xlsx = mail_info["file_path"] + ".xlsx"
    file_path_csv = mail_info["file_path"] + ".csv"

    # 执行SQL查询并且保存报表, 若要保存为csv则传入file_path_csv，否则传入file_path_xlsx
    # 但是目前导出xlsx的功能还没有完成，后续完善
    logging.info("要生成的csv文件地址: " + file_path_csv)
    n = mail_info["count"]
    logging.info("这个SQL要执行 " + str(n) + " 次...")
    for i in range(1, n + 1):
        logging.info(
            "------------------------第" + str(i) + "次执行sql------------------------"
        )
        search_and_save_csv(mysql, sql_content, r"" + file_path_csv)

    sendEmail(sender_info, mail_info, file_path_csv)


def check_folder_exists(folder_path):
    """
    检查目标文件夹是否存在，若不存在则创建
    :param folder_path: 待检测的文件夹的路径
    :return:
    """
    # print("check folder exists soon...")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logging.info("成功创建文件夹: " + folder_path)
    else:
        logging.info(folder_path + ": 文件夹已存在,不需要重新创建")


def prepareAndHandle(data):
    # 设置当前区域设置为中文（中国）
    locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
    # 获取当前日期
    current_date = datetime.datetime.now().date()
    # 获取今天是星期几（中文）
    weekday_today = current_date.strftime("%A")

    # 使用字典来保存多个连接. 其中key是链接的名称, value是数据库链接信息
    dbs = dict()
    for x in data["connections"]:
        dbs[x] = data["connections"][x]
    mail = data["mail"]

    # 发送者的信息，包括邮件host，发送者邮箱，授权码
    sender_info = dict()
    sender_info["mail_host"] = mail["mail_host"]
    sender_info["sender"] = mail["sender"]
    sender_info["password"] = mail["password"]

    # 解析所有的报表信息
    reports = mail["reports"]
    # 遍历每个报表，先检查今天是否要发送这个报表，然后再以每个报表为单位进行处理
    for report_key, report in reports.items():
        database_info = dbs[report["db"]]
        reportName = report["reportName"]
        when = report["when"]
        # 如果这个报表今天不需要发送，则continue
        if when != weekday_today:
            continue
        # 获取当前日期，加工生成报表名称
        today = datetime.date.today()
        # 完整的报表名称例如：客户旅程表2023-07-15
        handledReportName = reportName + str(today)
        # 检查并构造文件夹
        # 文件路径例如：myfiles\\results\\客户旅程报表
        report_folder = "myfiles\\results\\" + reportName
        check_folder_exists(report_folder)
        # logger.info("文件夹已经建立或已存在: " + report_folder)
        logging.info("正在处理的报表是: " + reportName)

        mail_info = dict()
        mail_info["reportName"] = report["reportName"]
        mail_info["subject"] = report["subject"]
        mail_info["content"] = report["content"]
        # 现在同一个报表有多个邮件接收者了
        mail_info["receivers"] = report["receivers"]
        mail_info["report_folder"] = report_folder
        mail_info["file_path"] = report_folder + "\\" + handledReportName
        mail_info["sqlFileLocation"] = "myfiles\\queries\\" + report["sqlName"]
        mail_info["count"] = report["count"]
        # 由于发送频率不高，可以每个针对每个报表链接一次数据库
        okgogogo(database_info, sender_info, mail_info)


def setup_logging(
    default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"
):
    """
    Setup logging configuration
    """
    my_path = default_path
    value = os.getenv(env_key, None)
    if value:
        my_path = value
    if os.path.exists(my_path):
        with open(my_path, "rt") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    # logging.info(f"日志初始化 {__name__}")


def report_task():
    setup_logging()
    logging.info("程序开始")
    file_path = "myfiles/config.json"
    logging.info("读取config.json配置文件...")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    prepareAndHandle(data)
    logging.info("程序结束")
    input("按回车键退出")


if __name__ == "__main__":
    try:
        report_task()
    except Exception as e:
        logging.error(f"main Exception: {traceback.format_exc()}")
        raise
