from lib import doPrepare
import util
import logging
import json


def report_task():
    util.setup_logging()
    logging.info("程序开始")
    file_path = "myfiles/config.json"
    logging.info("读取config.json配置文件...")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    doPrepare.prepareAndHandle(data)
    logging.info("程序结束")
    input("按回车键退出")


if __name__ == "__main__":
    report_task()
