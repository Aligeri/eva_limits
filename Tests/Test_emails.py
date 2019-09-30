import pytest
from Helpers.SMTPHelper import *
from Config.Users import *
from Helpers.SQLHelper import *
from Pages.BasePage import Page
from Helpers.HostelHelper import *

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

    @pytest.mark.skip()
    def test_set_limit(self):
        helper = SQLHelper()
        a = helper.settings_payouts_limits("user_amount_too_big", 1.00000001)

    #@pytest.mark.skip()
    def test_get_wallet(self):
        helper = SQLHelper()
        a = helper.get_user_account_id('testermail38@gmail.com')
        print(a)

    def test_hostel(self):
        helper = HostelHelper()
        a = helper.get_transaction_details("status", '2e6c3678-4c99-420c-b8de-4e8ca6c11e3a')
        print(a)

    def test_hostel2(self):
        helper = HostelHelper()
        a = helper.send_transaction("doge", "d2000d0b-010e-4308-b2a3-0f38b444f8bf", "2")

    def test_get_exec(self):
        helper = XrayHelper()
        helper.update_test_status()
