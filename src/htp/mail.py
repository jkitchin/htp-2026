"""Send email over SMTP, optionally with a file attachment."""

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def send_mail(toaddrs, subject, message, fromaddr, mailserver):
    """Send a plain-text email to one or more recipients.

    Parameters
    ----------
    toaddrs : str or iterable of str
        Destination address or addresses. A single message is sent
        with every recipient listed in the ``To:`` header.
    subject : str
        Subject line of the message.
    message : str
        Body of the message.
    fromaddr : str
        Address placed in the ``From:`` header and used as the SMTP
        envelope sender.
    mailserver : str
        Hostname of the SMTP server to connect to.
    """
    if isinstance(toaddrs, str):
        to_list = [toaddrs]
    else:
        to_list = list(toaddrs)

    msg = MIMEText(message)
    msg["From"] = fromaddr
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    with smtplib.SMTP(mailserver) as server:
        server.sendmail(fromaddr, to_list, msg.as_string())


def send_mail_with_attachment(
    fromaddr,
    toaddrs,
    subject,
    message,
    attachment,
    mailserver,
):
    """Send an email with a single file attachment to each recipient.

    One message is sent per recipient so that addresses are not
    disclosed to each other.

    Parameters
    ----------
    fromaddr : str
        Address placed in the ``From:`` header.
    toaddrs : iterable of str
        Destination addresses. One message is sent to each.
    subject : str
        Subject line of the message.
    message : str
        Body text of the message.
    attachment : str
        Path to a file to attach. Sent as ``application/octet-stream``
        with the file's basename as the attachment filename.
    mailserver : str
        Hostname of the SMTP server to connect to.
    """
    with open(attachment, "rb") as f:
        payload = f.read()
    filename = os.path.basename(attachment)

    for toaddr in toaddrs:
        msg = MIMEMultipart()
        msg["From"] = fromaddr
        msg["To"] = toaddr
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject

        msg.attach(MIMEText(message))

        part = MIMEBase("application", "octet-stream")
        part.set_payload(payload)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{filename}"',
        )
        msg.attach(part)

        with smtplib.SMTP(mailserver) as server:
            server.sendmail(fromaddr, [toaddr], msg.as_string())
