import pymysql
import pandas as pd
import os
from openpyxl.reader.excel import load_workbook
import logging

from lib import sendEmail

logger = logging.getLogger(__name__)


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
        # logger.info("报表头部是: " + str(title))

        # 拿到数据库查询的内容
        result_list = []
        for each in self.cursor.fetchall():
            result_list.append(list(each))

        # 保存成dataframe
        df_dealed = pd.DataFrame(result_list, columns=title)
        # 保存成csv 这个编码是为了防止中文没法保存，index=None的意思是没有行号
        df_dealed.to_csv(
            file_path, index=None, encoding="utf_8_sig", lineterminator="\r\n"
        )
        logger.info("成功导出报表!")


def okgogogo(database_info, sender_info, mail_info):
    """
    导出报表以及发送邮件
    :param database_info: 数据库链接信息
    :param sender_info: 发送端的基本信息
    :param mail_info: 邮件的基本信息
    :return:
    """
    host = database_info["host"]
    port = database_info["port"]
    user = database_info["user"]
    db_password = database_info["password"]
    charset = database_info["charset"]
    # 初始化类
    mysql = MysqlSave(host, int(port), user, db_password, charset)

    # 没有xlsx后缀的文件路径
    # file_name_without_suffix = results_path + sqls_name[i]
    # print("file_name_without_suffix = " + file_name_without_suffix)

    # 读取sql语句内容
    with open(mail_info["sqlFileLocation"], "r", encoding="utf-8") as file:
        sql_content = file.read()
    if sql_content is not None:
        logger.info("SQL语句读取成功")

    # 先创建当前要写入的文件，之后再写入
    file_path_xlsx = mail_info["file_path"] + ".xlsx"
    file_path_csv = mail_info["file_path"] + ".csv"

    # 执行SQL查询并且保存报表, 若要保存为csv则传入file_path_csv，否则传入file_path_xlsx
    # 但是目前导出xlsx的功能还没有完成，后续完善
    logger.info("要生成的csv文件地址: " + file_path_csv)
    logger.info("正在导出报表, 请稍等...")
    mysql.search_and_save_csv(sql_content, r"" + file_path_csv)

    # for i in range(len(sqls_name)):
    #     full_path = results_path + sqls_name[i] + ".csv"
    #     attaches.append(full_path)
    #     print(full_path)

    sendEmail.doEmail(sender_info, mail_info, file_path_csv)
