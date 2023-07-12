import logging


class MyLog:
    def __init__(self):
        logging.basicConfig(
            filename="basic.log",
            level=logging.DEBUG,
            filemode="w+",
            format="%(name)s-%(levelname)s-%(message)s"
        )

    def test(self):
        print("logging.........")
        logging.info('This will write in basic.log')
        logging.debug('This will not write in basic.log')
