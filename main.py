# This is a sample Python script.
import doPrepare
from apscheduler.schedulers.blocking import BlockingScheduler

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def report_task():
    doPrepare.prepareAndHandle()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    schduler = BlockingScheduler()
    schduler.add_job(report_task, 'cron', hour=10)
    schduler.start()


    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
