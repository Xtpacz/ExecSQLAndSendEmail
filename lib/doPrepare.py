import json
from lib import execSQL
import datetime
import locale


def prepareAndHandle():
    # 设置当前区域设置为中文（中国）
    locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")
    # 获取当前日期
    current_date = datetime.datetime.now().date()
    # 获取今天是星期几（中文）
    weekday_today = current_date.strftime("%A")
    print("今天是：", weekday_today)

    file_path = "../../files/config.json"
    # 读取JSON文件
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 解析数据库信息
    database = data["database"]
    host = database["host"]
    port = database["port"]
    user = database["user"]
    db_password = database["password"]
    charset = database["charset"]

    # 解析邮件信息
    mail = data["mail"]
    mail_host = mail["mail_host"]
    sender = mail["sender"]
    mail_password = mail["password"]

    # 解析收件人信息
    to = mail["to"]

    # 遍历每个收件人，以每个收件人为单位进行处理SQL发邮件
    for person_key, person_data in to.items():
        name = person_data["name"]
        receiver = person_data["email"]
        subject = person_data["subject"]
        content = person_data["content"]
        queries = person_data["queries"]
        need_send_day = person_data["when"]
        # 今天这个不需要对这个人发送邮件
        if need_send_day != weekday_today:
            continue

        # 获取当前日期
        today = datetime.date.today()
        # 将邮件主题加入当前日期
        subject = subject + str(today)
        print(
            "\nname = "
            + name
            + "\nemail = "
            + receiver
            + "\nsubject = "
            + subject
            + "\ncontent = "
            + content
            + "\n"
        )

        file_address = []
        file_name = []
        for query_key, query_data in queries.items():
            file_address.append(query_data["fileAddress"])
            file_name.append(query_data["fileName"])

        # 解析查询文件保存位置
        results_path = data["results_path"]
        results_path = results_path + name + "\\" + str(today) + "\\"
        # 由于发送频率不高，可以每个人都重新链接数据库
        execSQL.okgogogo(
            host,
            port,
            user,
            db_password,
            charset,
            mail_host,
            sender,
            mail_password,
            receiver,
            subject,
            content,
            file_address,
            file_name,
            results_path,
        )
