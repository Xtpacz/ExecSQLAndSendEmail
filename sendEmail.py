# 示例：登陆邮箱，并发送一封邮件；自己的163邮箱，给自己的qq邮箱发，不打扰别人
import yagmail
import schedule

def send_mail(sender=None, password=None, receivers=None,
              subject='重新测试定时发送报表', contents=None, attaches=None, host='smtp.163.com'):
    """
    定时发送报表
    :param sender:发件人
    :param password: 验证码
    :param receivers: 收件人
    :param subject: 主题
    :param contents: 内容
    :param attaches: 附件
    :param host: 服务器
    :return: none
    """
    try:
        mail = yagmail.SMTP(user=sender, password=password, host=host)
        mail.send(to=receivers, subject=subject, contents=contents, attachments=attaches)
    except Exception as e:
        print('邮件发送失败', e)
    else:
        print('邮件发送成功')


# if __name__ == '__main__':

def doEmail(receivers, attaches, password, sender):
    print('开始发邮件')
    contents = ["测试内容"]
    schedule.every(30).seconds.do(send_mail, sender=sender,
                                  password=password,
                                 receivers=receivers,
                                 contents=contents,
                                 attaches=attaches)
    while True:
        schedule.run_pending()