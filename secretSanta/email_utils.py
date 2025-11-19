import imaplib
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from secretSanta import logger


def send_email(
    email_address: str,
    message_body: str,
    subject: str,
    host_email_address: str,
    host_pwd: str,
    image_path: str = None,
):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(host_email_address, host_pwd)

    # Are we including an image?
    embedded_image = False
    if image_path is not None and not os.path.isfile(image_path):
        logger.warning(f"Could not find {image_path}")
    if image_path is not None and os.path.isfile(image_path):
        embedded_image = True

    # Make sure to use the related is important if image is used
    if embedded_image:
        logger.debug("Will include image")
        msg = MIMEMultipart("related")
    else:
        logger.debug("No image included")
        msg = MIMEMultipart("alternative")

    msg["Subject"] = subject
    msg["From"] = "The Secret Santa Corporation"
    msg["To"] = email_address

    if embedded_image:
        msg_alt = MIMEMultipart("alternative")
        msg.attach(msg_alt)
        # HTML body with reference to image via cid
        html_with_image = f"""
        <html>
        <body>
            {message_body}
            <br><br>
            <div style="text-align:center;">
                <img src="cid:embedded_image" style="max-width:400px;">
            </div>
            <br>
            PS: You may consult our refactored code here: https://github.com/malihass/SecretSanta  

        </body>
        </html>
        """
        msg_alt.attach(MIMEText(html_with_image, "html"))

        # Attach image with Content-ID
        with open(image_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<embedded_image>")
            img.add_header("Content-Disposition", "inline")
            msg.attach(img)
    else:
        part1 = MIMEText(message_body, "html")
        msg.attach(part1)  # text must be the first one

    server.sendmail(host_email_address, email_address, msg.as_string())

    logger.info("Email has been sent")
    server.quit()


def deleteSentEmails(host_email, host_pwd):
    box = imaplib.IMAP4_SSL("smtp.gmail.com", 993)
    box.login(host_email, host_pwd)
    box.select('"[Gmail]/Sent Mail"')
    typ, data = box.search(None, "ALL")
    for num in data[0].split():
        box.store(num, "+FLAGS", "\\Deleted")
    box.expunge()
    box.close()
    logger.info("Send box emptied")
    box.logout()
