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
        logger.warning("邮件发送失败，发送失败的邮件如下: " + str(attaches))
    else:
        logger.info("邮件发送成功")


def doEmail(sender_info, mail_info, file_path_csv):
    mail_host = sender_info["mail_host"]
    sender = sender_info["sender"]
    password = sender_info["password"]
    receivers = mail_info["receivers"]
    subject = mail_info["subject"]
    content = mail_info["content"]
    logger.info("准备发送邮件...")
    logger.info(
        "发送邮件的详细信息如下："
        + "\n发送人: "
        + sender
        + "\n接收人: "
        + str(receivers)
        + "\n主题: "
        + subject
        + "\n邮件内容: "
        + content
        + "\n附件: "
        + str(file_path_csv)
        + "\n"
    )
    logger.info("准备完毕, 开始发送邮件...")
    send_mail(sender, password, receivers, subject, content, file_path_csv, mail_host)
