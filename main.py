import pymysql
import pandas as pd
import json
import traceback
from datetime import datetime, timedelta
import os
import logging
import yagmail
import yaml
import logging.config

# 所有的配置
config_data = None

# 邮件发送方
sender_info = None

# 数据库连接以及语句执行相关
mysql = None
connections = None
current_connection = None
current_sql_name = None
current_sql_content = None
conn = None

# 所有的报表
reports = None

# 当前报表
current_report = None

# 当前报表要存放的的实际位置
current_folder_path = None
file_path_csv = None

# 今天需要处理的报表
reports_need_send = []

# 如果是需要分隔报表,则以列表形式存储所有子报表的存放位置,方便后续合并
sub_reports = []

# 合并报表的依据
merge_basis = []

WEEKDAY_EN_2_NUM = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7,
}

# 全局变量
DEFAULT_LOGGING_CONFIG_PATH = "logging.yaml"
DEFAULT_LOGGING_LEVEL = logging.INFO
LOGGING_ENV_KEY = "LOG_CFG"
CONFIG_PATH = "myfiles/config_test.json"
RESULT_FOLDER = "myfiles\\results\\"
QUERIES_FOLDER = "myfiles\\queries\\"


def controller():
    """
    A function that coordinates all aspects.
    :return:
    """
    preprocess_data()
    # 针对每个报表,查看今天是否需要发送,需要发送的报表的key保存在reports_need_send列表中
    global reports, reports_need_send
    for report_key, report_value in reports.items():
        when = report_value["when"]
        if need_operation_today(when):
            reports_need_send.append(report_key)
    # 找出了需要发送的报表,接下来针对每个需要发送的报表,进行处理
    # 枚举需要发送的报表
    for x in reports_need_send:
        global current_sql_name, current_report, current_connection
        # clear related data
        current_connection = None
        current_report = reports[x]
        cnt = 1
        if 'exec_sql_count' in current_report:
            cnt = current_report["exec_sql_count"]
        # 执行cnt次SQL
        for i in range(cnt):
            flag = 0
            if 'multi_sql' in current_report:
                flag = current_report["multi_sql"]
            # 需要分割来发送
            if flag:
                global merge_basis
                merge_basis = current_report["merge_basis"]
                # 分开执行每个sql就行,然后合并为1个,最后发送即可
                for t in current_report["sub_sql"]:
                    # get the sql name
                    current_sql_name = current_report["sub_sql"][t]
                    get_data_save_csv()
                # 合并报表之前,将file_path_csv的值更改为需要合并到的
                global file_path_csv
                today = datetime.date.today()
                file_path_csv = (
                        current_folder_path
                        + "\\"
                        + current_report["report_name"]
                        + "_"
                        + str(today)
                        + ".csv"
                )
                # merge report according to sub_reports
                merge_report()
            else:
                # get the sql name
                current_sql_name = current_report["sql_name"]
                get_data_save_csv()
            logging.info("To do: send email...")
            # if mysql:
            #     mysql.close()
            #     print("关闭游标")
            # if conn:
            #     conn.close()
            #     print("关闭链接")
        # 执行cnt次，但是发邮件只发一次
        send_email()


def preprocess_data():
    """
    Preprocess data: all connection data, all report data.
    :return:
    """
    global config_data, connections, sender_info, reports
    config_data = load_config()
    connections = dict()
    for x in config_data["connections"]:
        connections[x] = config_data["connections"][x]
    sender_info = config_data["sender_info"]
    reports = config_data["reports"]


def init_con():
    """
    Initialize the database connection.
    :return:
    """
    global current_connection
    host = current_connection["host"]
    port = int(current_connection["port"])
    user = current_connection["user"]
    password = current_connection["password"]
    charset = current_connection["charset"]
    global conn
    conn = pymysql.Connect(
        host=host,
        port=port,
        user=user,
        passwd=password,
        charset=charset,
    )
    cursor = conn.cursor()
    logging.info("数据库链接成功")
    return cursor


def fetch_current_sql_content(sql_name):
    """
    Get the content of the SQL file.
    :param sql_name: SQL file name
    :return: the content of the file
    """
    sql_path = QUERIES_FOLDER + sql_name
    global current_sql_content
    with open(sql_path, "r", encoding="utf-8") as file:
        current_sql_content = file.read()
    if current_sql_content is not None:
        logging.info("SQL语句读取成功")
        # yesterday = datetime.now() - timedelta(days=1)
        # yesterday = yesterday.strftime('%Y-%m-%d')
        # current_sql_content.format(yesterday)
        # print(current_sql_content)


def execute_and_fetch():
    """
    Execute the SQL statement for the global variable and return the query result.
    """
    logging.info("正在执行sql语句...")
    mysql.execute(current_sql_content)
    des = mysql.description
    title = [each[0] for each in des]
    result_list = [list(each) for each in mysql.fetchall()]
    return title, result_list


def get_data_save_csv():
    """
    Call the execute_and_fetch () method
    and
    save the result in a csv file with a local path of file_path_csv.
    """
    global current_connection
    # fetch the sql content by its name
    fetch_current_sql_content(current_sql_name)
    # return
    current_connection = connections[current_report["connection"]]
    # initialize the database connection
    global mysql
    mysql = init_con()
    # create the folder to save the file
    create_folder_exists()
    # create the file path
    create_csv_path()
    # logging.info(f"当前报表:{file_path_csv}")
    # get data and save
    title, result_list = execute_and_fetch()
    df_dealt = pd.DataFrame(result_list, columns=title)
    df_dealt.to_csv(
        file_path_csv, index=None, encoding="utf_8_sig", lineterminator="\r\n"
    )
    logging.info(f"成功导出报表:{file_path_csv}\n")


def create_csv_path():
    """
    Create file_path_csv value.
    """
    today = datetime.today().strftime("%Y-%m-%d")
    global file_path_csv
    flag = 0
    if 'multi_sql' in current_report:
        flag = current_report["multi_sql"]
    if flag:
        # If it is a report that needs to be split, use the sql name to name it.
        global sub_reports
        file_path_csv = (
                current_folder_path
                + "\\"
                + current_sql_name[:-4]
                + "_"
                + str(today)
                + ".csv"
        )
        sub_reports.append(file_path_csv)
    else:
        # For reports that do not need to be split, use the report name to name the file.
        file_path_csv = (
                current_folder_path
                + "\\"
                + current_report["report_name"]
                + "_"
                + str(today)
                + ".csv"
        )


def create_folder_exists():
    """
    Create a folder to hold the report results.
    """
    global current_folder_path
    current_folder_path = RESULT_FOLDER + current_report["report_name"]
    if not os.path.exists(current_folder_path):
        os.makedirs(current_folder_path)
        logging.info(f"Folder created: {current_folder_path}")
    else:
        logging.info(f"Folder already existed: {current_folder_path}")


def merge_report():
    """
    Combine multiple reports based on sub_reports.
    :return:
    """
    global sub_reports

    # First read the first csv file as the underlying DataFrame.
    base_df = pd.read_csv(sub_reports[0])

    # Iterate over the remaining csv files and merge with the underlying DataFrame one by one.
    for file_path in sub_reports[1:]:
        df = pd.read_csv(file_path)
        base_df = pd.merge(base_df, df, how="left", on=merge_basis)

    # Save the merged DataFrame to a new csv file.
    base_df.to_csv(file_path_csv, index=False)


def need_operation_today(when):
    """
    Check whether an operation is required today,
    and the report needs to return True, otherwise it returns False.
    :param when: the number of weekday. eg: Monday-> 1
    :return: True of False
    """
    current_date = datetime.now().date()
    weekday_today = current_date.strftime("%A")
    weekday_today = WEEKDAY_EN_2_NUM[weekday_today]
    if weekday_today in when:
        return True
    else:
        return False


def setup_logging():
    """
    Setup logging configuration
    """
    my_path = DEFAULT_LOGGING_CONFIG_PATH
    value = os.getenv(LOGGING_ENV_KEY, None)
    if value:
        my_path = value
    if os.path.exists(my_path):
        with open(my_path, "rt") as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=DEFAULT_LOGGING_LEVEL)


def load_config():
    """
    Import the configuration file and return the loaded file information.
    :return: the loaded file information
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        logging.error("打开配置文件config.json异常!")


def send_email():
    """
    Send mail according to the currently executed report (current_report) and file_path_csv.
    :return:
    """
    global current_report
    receivers = current_report["receivers"]
    if not receivers:
        logging.info("没有填写接收人邮箱信息,这个报表保存在本地即可,不需要发送邮件")
        return
    logging.info(f"准备发送邮件至: {receivers}")
    cc = []
    if 'cc' in current_report:
        cc = current_report["cc"]
    logging.info(f"抄送至: {cc}")
    logging.info(f"附件: {file_path_csv}")

    try:
        mail = yagmail.SMTP(
            user=sender_info["sender"],
            password=sender_info["password"],
            host=sender_info["mail_host"],
        )
        mail.send(
            to=receivers,
            cc=cc,
            subject=current_report["subject"],
            contents=current_report["content"],
            attachments=file_path_csv,
        )
    except Exception as e:
        logging.warning(f"邮件发送失败，发送失败的邮件: {file_path_csv} ")
    else:
        logging.info("邮件发送成功！\n")


if __name__ == "__main__":
    try:
        setup_logging()
        controller()

    except Exception as e:
        logging.error(f"main Exception: {traceback.format_exc()}")
        raise
