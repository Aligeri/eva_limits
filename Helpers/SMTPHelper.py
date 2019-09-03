import smtplib
import imaplib
import email
import re
import time
from conftest import *


class SMTPHelper():
    def __init__(self):
        self.__smtp_ssl_host ='smtp.gmail.com'
        self.__smtp_ssl_port = 465

    def __getEmailFromGmail(self, address, password, email_from, email_subject):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', "993")
        retries_left = 20
        mail.login(address, password)
        mail.list()
        mail.select('"INBOX"')
        search = ("(FROM '%s')" % email_from)
        result, data = mail.search(None, search)
        ids = data[0]
        id_list = ids.split()
        while retries_left >= 0:
            try:
                if data[0] == b'':
                    time.sleep(3)
                    mail.select('"INBOX"')
                    search = ("(FROM '%s' SUBJECT '%s')" % (email_from, email_subject))
                    result, data = mail.search(None, 'FROM', email_from, 'SUBJECT', '"%s"' % email_subject)
                    ids = data[0]
                    id_list = ids.split()
                    retries_left -= 1
                    continue
                else:
                    retries_left = -2
                    continue
            except IndexError:
                retries_left -= 1
        if retries_left == -1:
            raise ValueError("Email is not found")
        latest_email_id = id_list[-1]
        result, data = mail.fetch(latest_email_id, "(UID BODY[TEXT])")
        raw_email = data[0][1]
        return raw_email

    def __getEmailAsString(self, address, password, email_from, email_subject=''):
        raw_email = self.__getEmailFromGmail(address, password, email_from, email_subject)
        msg = email.message_from_bytes(raw_email)
        msgtext = msg.as_string()
        email_string = re.sub('=\n', '', msgtext)
        return email_string

    def get_multisig_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "https:\/\/\w*?\.?freewallet\.org\/multisig\/email\/\w*"
        multisig_link = re.search(pattern, email_string).group(0)
        return multisig_link

    def get_verification_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "https:\/\/\w*?\.?freewallet\.org(\/email-validate\/.*?)]"
        verification_link = re.search(pattern, email_string).group(1)
        fixed_link = re.sub("(=3D=3D)", "==", verification_link)
        domain_link = email_url + fixed_link
        return (domain_link)

    def get_registration_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "(https:\/\/\w*?\.?freewallet\.org\/email-temporary\/.*?)]"
        registration_link = re.search(pattern, email_string).group(1)
        return (registration_link)

    def get_multisig_transaction_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "(https:\/\/\w*?\.?freewallet\.org\/multisig\/tx\/.*?)]"
        registration_link = re.search(pattern, email_string).group(1)
        return (registration_link)

    def delete_emails_from_gmail(self, address, password):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', "993")
        mail.login(address, password)
        mail.select('INBOX')
        result, data = mail.search(None, "(FROM 'Freewallet')")
        for num in data[0].split():
            mail.store(num, '+FLAGS', '(\Deleted)')
        mail.expunge()

    def sendEmailFromGmail(self, address, password):
        server = smtplib.SMTP_SSL()
        server.connect(self.__smtp_ssl_host, self.__smtp_ssl_port)
        server.login(address, password)
        server.sendmail("kindlyfindattached0@gmail.com", "madokamelpo@gmail.com", "something")
        server.quit()


