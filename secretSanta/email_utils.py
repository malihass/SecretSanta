import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(
    email_address, message_body, subject, host_email_address, host_pwd
):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(host_email_address, host_pwd)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "The Secret Santa Corporation"
    msg["To"] = email_address

    part1 = MIMEText(message_body, "html")
    msg.attach(part1)  # text must be the first one
    server.sendmail(host_email_address, email_address, msg.as_string())

    print(" Email has been sent ")
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
    print(" Send box emptied ")
    box.logout()
