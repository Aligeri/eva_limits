import requests
import json

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
        return response_put
