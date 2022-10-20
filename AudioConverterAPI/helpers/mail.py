from email.message import EmailMessage
import smtplib

sender = "equipo_nube_36@outlook.com"
password = "ZarayJeysonLizErik36"
smtpServer = "smtp-mail.outlook.com"
smtpPort = 587

def sendMail(receiver, subject, message, file, fileName, fileExtension):
    email = EmailMessage()
    email["From"] = sender
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(message)
    email.add_attachment(file, maintype='application', subtype=fileExtension, filename=fileName)
    smtp = smtplib.SMTP(smtpServer, port=smtpPort)
    smtp.starttls()
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, email.as_string())
    smtp.quit()