import requests
import json
from Helpers.SQLHelper import *
import time

class HostelHelper:
    def get_transaction_details(self, parameter, transaction_id):
        """
        Получает параметр из данных транзакции
        :param parameter: получаемый параметр (status)
        :param transaction_id: id транзакции
        :return: значение параметра
        """
        response = requests.get('http://hostel.cain.loc:80/v1/transactions/%s' % transaction_id)
        data = response.json().get("data")
        assert response.status_code == 200
        value = data.get("%s" % parameter)
        return value

    def send_transaction(self, currency, receiver, amount, sender="emitter"):
        """
        Создает новую транзакцию и коммитит ее в хостеле
        :param currency: валюта btcmain/doge
        :param receiver: accound id получателя
        :param amount: сумма
        :param sender: отправитель, по умолчанию emitter
        :return: пока что response на отправку транзакции, TODO: допилить проверку 200
        """
        transaction_json = {
          "currency": currency,
          "sender": sender,
          "receiver": receiver,
          "amount": amount,
          "hidden": False,
          "needs_approval": False,
          "flags": 0,
          "ttl_sec": 0,
          "comment": "0",
          "custom_type": "0",
          "custom_id": "0"
        }
        response = requests.post("http://hostel.cain.loc:80/v1/transactions/transfers", json=transaction_json)
        transaction_id = response.json().get("data").get("transaction_id")
        response_put = requests.put("http://hostel.cain.loc:80/v1/transactions/%s" % transaction_id)
        assert response_put.status_code == 200


    def check_status_transaction_by_email(self, email, date, waiting_approval=True):
        sql = SQLHelper()
        accountId = sql.get_user_account_id(email)

        retries_left = 4
        while retries_left > 0:
            try:
                response = requests.get(
                    "http://hostel.cain.loc:80/v1/transactions?account=%s&&&&&from=%s&&&&sort_by=first_timestamp&sort=DESC&&&&&&&&&" % (
                    accountId[0], date))
                status = response.json().get("data")[0].get("status")
                if waiting_approval:
                    assert status == ("waiting_approval")
                else:
                    assert status != "waiting_approval"
                return
            except:

                time.sleep(2)
                retries_left -= 1
        raise Exception("poshev naher")



