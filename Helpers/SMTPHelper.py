import smtplib
import imaplib
import email
import re
import time
from conftest import email_url


class SMTPHelper():
    def __init__(self):
        self.__smtp_ssl_host ='smtp.gmail.com'
        self.__smtp_ssl_port = 465

    def __getEmailFromGmail(self, address, password, email_from, email_subject=''):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', "993")
        retries_left = 50
        mail.login(address, password)
        mail.list()
        mail.select('"INBOX"')
        result, data = mail.search(None, 'FROM', email_from, 'SUBJECT', '"%s"' % email_subject)
        ids = data[0]
        id_list = ids.split()
        while retries_left >= 0:
            try:
                if data[0] == b'':
                    time.sleep(3)
                    mail.select('"INBOX"')
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
        try:
            pattern = "https:\/\/\w*?\.?freewallet\.org(\/multisig\/email\/.*?)[<\]]"
            multisig_link = re.search(pattern, email_string).group(0)
        except:
                pattern = 'via email.*?(https:.*?)" style'
            nonfixed_link = re.search(pattern, email_string).group(1)
            multisig_link = re.sub("upn=3D", "upn=", nonfixed_link)
        return multisig_link

    def get_verification_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "https:\/\/\w*?\.?freewallet\.org(\/email-validate\/.*?)[<\]]"
        verification_link = re.search(pattern, email_string).group(1)
        fixed_link = re.sub("(=3D=3D)", "==", verification_link)
        domain_link = email_url + fixed_link
        return (domain_link)

    def get_registration_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        try:
            pattern = "(https:\/\/\w*?\.?freewallet\.org\/email-temporary\/.*?)[<\]]"
            registration_link = re.search(pattern, email_string).group(1)
        except:
            pattern = 'claim.*?(https:.*?)" style'
            nonfixed_link = re.search(pattern, email_string).group(1)
            registration_link = re.sub("upn=3D", "upn=", nonfixed_link)
        return (registration_link)

    def get_multisig_transaction_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "(https:\/\/\w*?\.?freewallet\.org\/multisig\/tx\/.*?)[<\]]"
        registration_link = re.search(pattern, email_string).group(1)
        return (registration_link)

    def get_session_drop_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "https:\/\/\w*?\.?freewallet\.org(\/auth\/session-drop\/.*?)[<\]]"
        session_link = re.search(pattern, email_string).group(1)
        fixed_link = re.sub("(=3D=3D)", "==", session_link)
        domain_link = email_url + fixed_link
        return (domain_link)

    def delete_emails_from_gmail(self, address, password, email_from, email_subject):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', "993")
        mail.login(address, password)
        mail.select('INBOX')
        result, data = mail.search(None, 'FROM', email_from, 'SUBJECT', '"%s"' % email_subject)
        for num in data[0].split():
            mail.store(num, '+FLAGS', '(\Deleted)')
        mail.expunge()

    def sendEmailFromGmail(self, address, password):
        server = smtplib.SMTP_SSL()
        server.connect(self.__smtp_ssl_host, self.__smtp_ssl_port)
        server.login(address, password)
        server.sendmail("kindlyfindattached0@gmail.com", "madokamelpo@gmail.com", "something")
        server.quit()

    def get_change_mail_link_from_email(self, address, password, email_from, email_subject=''):
        email_string = self.__getEmailAsString(address, password, email_from, email_subject)
        pattern = "(https:\/\/\w*?\.?freewallet\.org\/user\/email-change-validate\/.*?)[<\]]"
        verification_link = re.search(pattern, email_string).group(1)
        return (verification_link)
