import pymysql
import pandas as pd
import configparser
import sendEmail

# 从queries.py里面获取要执行的sql语句
from queries import sql1

class MysqlSave:

    def __init__(self):
        # 读取配置文件
        configFile = 'config.ini'
        con = configparser.ConfigParser()
        con.read(configFile, encoding='utf-8')

        # 设置连接数据库相关的主机、端口、用户名、密码
        host = dict(con.items('dbhost'))['dbhost']
        port = int(dict(con.items('dbport'))['dbport'])
        user = dict(con.items('dbuser'))['dbuser']
        passwd = dict(con.items('dbpwd'))['dbpwd']
        charset = dict(con.items('dbcharset'))['dbcharset']

        self.content = pymysql.Connect(
            host=host,  # mysql的主机ip
            port=port,  # 端口
            user=user,  # 用户名
            passwd=passwd,  # 数据库密码
            charset=charset,  # 使用字符集
        )
        self.cursor = self.content.cursor()

    def search_and_save(self, sql, csv_file):
        """
        导出为csv的函数
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

if __name__ == '__main__':

    # 初始化类
    mysql = MysqlSave()

    # 执行查询操作并保存至csv文件
    mysql.search_and_save(sql1, 'sql2.csv')

    # 读取配置文件
    configFile = 'config.ini'
    con = configparser.ConfigParser()
    con.read(configFile, encoding='utf-8')

    # 设置邮箱授权码、发送人、接收人
    password = dict(con.items('password'))['password']
    sender = dict(con.items('sender'))['sender']
    receivers = []
    receivers_dict = dict(con.items('receivers'))
    for key in receivers_dict:
        receivers.append(receivers_dict[key])

    # 要发送的文件所在的文件夹
    filepath = dict(con.items('filepath'))['filepath']
    at1 = filepath + 'sql2.csv'
    at2 = filepath + '\\test.txt'

    attaches = [r''+at1, r''+at2]
    sendEmail.doEmail(receivers, attaches, password, sender)