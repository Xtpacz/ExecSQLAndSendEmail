import pymysql
import pandas as pd
import xlwt
import os
import datetime
import xlsxwriter
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

import sendEmail


class MysqlSave:
    def __init__(self, host, port, user, dbpassword, charset):
        """
        初始化
        :param host: mysql主机的ip
        :param port: 端口
        :param user: 数据库用户名
        :param dbpassword: 数据库密码
        :param charset: 使用字符集
        """
        self.content = pymysql.Connect(
            host=host,
            port=port,
            user=user,
            passwd=dbpassword,
            charset=charset,
        )
        self.cursor = self.content.cursor()
        print("数据库链接成功")

    def search_and_save_xlsx(self, sql, file_path):
        """
        执行查询语句并导出为xlsx的函数
        :param sql: 要执行的mysql指令
        :param file_path: 导出的xlsx文件名
        :return:
        """
        # TODO(Xtpacz):完成直接生成到xlsx文件的功能

        # 执行sql语句
        self.cursor.execute(sql)

        # 拿到表头
        des = self.cursor.description
        title = [each[0] for each in des]

        # 拿到数据库查询的内容
        result_list = []
        for each in self.cursor.fetchall():
            result_list.append(list(each))

        # 创建空xlsx文件
        if not os.path.exists(file_path):
            try:
                fp = open(file_path, mode="w+", encoding="utf-8")
                print("file has been create successfully")
                fp.close()
            except IOError:
                print("create file failed.......")
        df = pd.DataFrame(result_list)
        book = load_workbook(file_path)
        with pd.ExcelWriter(file_path) as writer:
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            df.to_excel(
                writer, sheet_name="SHEET", startrow=1, index=False, header=False
            )
        book.close()

    def search_and_save_csv(self, sql, file_path):
        """
        执行查询语句并导出为csv的函数，此功能正常使用
        :param sql: 要执行的mysql指令
        :param file_path: 导出的csv文件名
        :return:
        """
        # 执行sql语句
        self.cursor.execute(sql)

        # 拿到表头
        des = self.cursor.description
        title = [each[0] for each in des]

        # 拿到数据库查询的内容
        result_list = []
        for each in self.cursor.fetchall():
            result_list.append(list(each))

        # 保存成dataframe
        df_dealed = pd.DataFrame(result_list, columns=title)
        # 保存成csv 这个编码是为了防止中文没法保存，index=None的意思是没有行号
        df_dealed.to_csv(file_path, index=None, encoding="utf_8_sig")

    def check_folder_exists(self, file_path):
        """
        检查目标文件夹是否存在，若不存在则创建
        :param folder_path: 待检测的文件夹的路径
        :return:
        """
        print("check folder exists soon...")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            print(f"Folder '{file_path}' created successfully.")
        else:
            print(f"Folder '{file_path}' already exists.")


def okgogogo(
    host,
    port,
    user,
    dbpassword,
    charset,
    mail_host,
    sender,
    password,
    receiver,
    subject,
    content,
    sqls_address,
    sqls_name,
    results_path,
):
    """
    导出报表以及发送邮件
    :param host: mysql主机ip
    :param port: 端口
    :param user: 数据库用户名
    :param dbpassword: 数据库密码
    :param charset: 字符集
    :param mail_host: 发送者邮箱的host
    :param sender: 发送者邮箱
    :param password: 邮箱授权码
    :param receiver: 接收者邮箱
    :param subject: 邮件主题
    :param content: 邮件内容
    :param sqls_address: SQL语句的位置
    :param sqls_name: SQL语句的名字
    :param results_path: 导出的报表保存的位置
    :return:
    """
    # 初始化类
    mysql = MysqlSave(host, int(port), user, dbpassword, charset)

    # 遍历每个sql语句
    for i in range(len(sqls_name)):
        # 没有xlsx后缀的文件路径
        file_name_without_suffix = results_path + sqls_name[i]
        print("file_name_without_suffix = " + file_name_without_suffix)

        # 读取sql语句内容
        with open(sqls_address[i], "r", encoding="utf-8") as file:
            sql_content = file.read()

        # 创建保存报表的文件夹
        mysql.check_folder_exists(results_path)

        # 先创建当前要写入的文件，之后再写入
        file_path_xlsx = file_name_without_suffix + ".xlsx"
        file_path_csv = file_name_without_suffix + ".csv"

        print("file_path = " + file_path_xlsx)

        # 执行SQL查询并且保存报表, 若要保存为csv则传入file_path_csv，否则传入file_path_xlsx
        # 但是目前导出xlsx的功能还没有完成，后续完善
        mysql.search_and_save_csv(sql_content, r"" + file_path_csv)

    attaches = []
    for i in range(len(sqls_name)):
        full_path = results_path + sqls_name[i] + ".csv"
        attaches.append(full_path)
        print(full_path)

    sendEmail.doEmail(mail_host, receiver, attaches, password, sender, subject, content)
