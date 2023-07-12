import pymysql
import pandas as pd
import sendEmail
import os

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
        print('数据库链接成功')

    def search_and_save(self, sql, csv_file):
        """
        执行查询语句并导出为csv的函数
        :param sql: 要执行的mysql指令
        :param csv_file: 导出的csv文件名
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
        df_dealed.to_csv(csv_file, index=None, encoding='utf_8_sig')

    def check_folder_exists(self, folder_path):
        """
        检查目标文件夹是否存在，若不存在则创建
        :param folder_path: 待检测的文件夹的路径
        :return:
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        else:
            print(f"Folder '{folder_path}' already exists.")

def okgogogo(host, port, user, dbpassword, charset ,mail_host, sender, password, receiver, subject, content, sqls_address, sqls_name, results_path):
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

    mysql.check_folder_exists(results_path)

    for i in range(len(sqls_name)):
        file_name = results_path + sqls_name[i] + '.csv'
        print("file_name = " + file_name)
        with open(sqls_address[i], "r", encoding='utf-8') as file:
            sql_content = file.read()
        mysql.search_and_save(sql_content, r''+file_name)

    attaches = []
    for i in range(len(sqls_name)):
        full_path = results_path + sqls_name[i] + '.csv'
        attaches.append(full_path)
        print(full_path)

    sendEmail.doEmail(mail_host, receiver, attaches, password, sender, subject, content)
