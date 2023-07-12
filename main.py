from lib import doPrepare
from log import MyLog
import logging


def report_task():
    doPrepare.prepareAndHandle()


if __name__ == "__main__":
    mylog = MyLog()
    mylog.test()
    logging.debug("debug test")
    # schduler = BlockingScheduler()
    # schduler.add_job(report_task, "cron", hour=10)
    # schduler.start()
    # report_task()
