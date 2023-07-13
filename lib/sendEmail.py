import yagmail
import logging

logger = logging.getLogger(__name__)


def send_mail(
    sender=None,
    password=None,
    receivers=None,
    subject=None,
    contents=None,
    attaches=None,
    host=None,
):
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
        mail.send(
            to=receivers, subject=subject, contents=contents, attachments=attaches
        )
    except Exception as e:
        print("邮件发送失败", e)
        logger.warning("邮件发送失败，发送失败的邮件如下: " + str(attaches))
    else:
        print("邮件发送成功")
        logger.info("邮件发送成功, 发送成功的附件如下: " + str(attaches))


def doEmail(mail_host, receivers, attaches, password, sender, subject, content):
    logger.info(
        "发送邮件的详细信息如下："
        + "\n发送人:"
        + sender
        + "\n接收人:"
        + str(receivers)
        + "\n主题:"
        + subject
        + "\n邮件内容:"
        + content
        + "\n附件:"
        + str(attaches)
    )
    logger.info("开始发送邮件")
    send_mail(sender, password, receivers, subject, content, attaches, mail_host)
