from lib import execSQL
import datetime
import locale
import os
import logging

logger = logging.getLogger(__name__)


def check_folder_exists(folder_path):
    """
    检查目标文件夹是否存在，若不存在则创建
    :param folder_path: 待检测的文件夹的路径
    :return:
    """
    # print("check folder exists soon...")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        # print(f"Folder '{folder_path}' created successfully.")
        logger.info("成功创建文件夹: "+folder_path)
    else:
        # print(f"Folder '{folder_path}' already exists.")
        logger.info(folder_path+": 文件夹已存在,不需要重新创建")


def prepareAndHandle(data):
    # 设置当前区域设置为中文（中国）
    locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
    # 获取当前日期
    current_date = datetime.datetime.now().date()
    # 获取今天是星期几（中文）
    weekday_today = current_date.strftime("%A")
    # logger.info("今天是" + weekday_today)

    # 解析得到数据库信息
    database_info = data["database"]
    # logger.info(str(database_info))

    # 解析邮件信息
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
        logger.info("正在处理的报表是: " + reportName)

        mail_info = dict()
        mail_info["reportName"] = report["reportName"]
        mail_info["subject"] = report["subject"]
        mail_info["content"] = report["content"]
        # 现在同一个报表有多个邮件接收者了
        mail_info["receivers"] = report["receivers"]
        mail_info["report_folder"] = report_folder
        mail_info["file_path"] = report_folder + "\\" + handledReportName
        mail_info["sqlFileLocation"] = "myfiles\\queries\\" + report["sqlName"]

        # 由于发送频率不高，可以每个针对每个报表链接一次数据库
        execSQL.okgogogo(database_info, sender_info, mail_info)
