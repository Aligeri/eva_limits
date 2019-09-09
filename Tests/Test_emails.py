import pytest
from Helpers.SMTPHelper import *
from Config.Users import *
from Helpers.SQLHelper import *
from Pages.BasePage import Page
from Helpers.XrayHelper import *

# Это тестовый файл, тут я всякие коннекшены к SQL и SMTP отрабатываю, чтобы ненароком всю базу не снести,
# Здесь нет настоящих тестов
class TestClass():
    @pytest.mark.skip()
    def test_EmailSending(self):
        helper = SMTPHelper()
        SMTPHelper.sendEmailFromGmail(helper, "kindlyfindattached0@gmail.com", "qWeaSd123")

    @pytest.mark.skip()
    def test_EmailReceiving(self):
        helper = SMTPHelper()
        #helper.delete_emails_from_gmail("kindlyfindattached0@gmail.com", "qWeaSd123")
        a = SMTPHelper.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password, 'Freewallet')
        print(a)

    @pytest.mark.skip
    def test_delete_limit(self):
        helper = SQLHelper()
        a = helper.delete_limits_by_email_from_database(ExistingBasicUser.email)
        print(a)

    def test_get_exec(self):
        helper = XrayHelper()
        helper.update_test_status()
