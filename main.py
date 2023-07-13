from lib import doPrepare
import util
import logging
import json


def report_task():
    util.setup_logging()

    logging.info("Starting the application")

    file_path = "../files/config.json"
    logging.info("读取配置文件")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    doPrepare.prepareAndHandle(data)
    logging.info("Finishing the application")
    input('Press <Enter>')


if __name__ == "__main__":
    report_task()
