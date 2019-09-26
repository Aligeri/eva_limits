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

    def test_email_delete(self):
        helper = SMTPHelper()
        #helper.delete_emails_from_gmail("kindlyfindattached0@gmail.com", "qWeaSd123")
        helper.delete_emails_from_gmail(ExistingBasicUser2.email, ExistingBasicUser2.password, "Freewallet",
                                      "Login attempt to your Freewallet account")

        #a = SMTPHelper.delete_emails_from_gmail(NewBasicUser.email, NewBasicUser.password, 'Freewallet')
        #print(a)


    def test_delete_limit(self):
        helper = SQLHelper()
        helper.change_2fa_parameters_by_email("vasiliyautomation+699@gmail.com", "true", "true", "false")


    def test_get_exec(self):
        helper = XrayHelper()
        helper.update_test_status()
