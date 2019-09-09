import requests
from requests.auth import HTTPBasicAuth
import os
import datetime
import time
from jira import JIRA

class XrayHelper:

    XRAY_MARKER_NAME = "xray"

    def __init__(self):
        self.options = {
            'server': 'https://jira.adam.loc',
            'verify': False,  # SSL validation off because Jira use self signed certificate
        }
        self.atlassian_jira = JIRA(options=self.options, basic_auth=('solinichenko', 'madokaqWeaSd123'))

    def get_execution(self):
        a = requests.get("https://jira.adam.loc/rest/raven/1.0/api/testexec/QA-1412/test", auth=HTTPBasicAuth("solinichenko", "madokaqWeaSd123"), verify=False)
        b = a.json()

    def create_execution_for_smoke(self, test_execution):
        add_tests = {
            "add": [
                "QA-1176"
            ]
        }
        execution_id = requests.post(("https://jira.adam.loc/rest/raven/1.0/api/testexec/%s/test" % test_execution), json=add_tests, auth=HTTPBasicAuth("solinichenko", "madokaqWeaSd123"), verify=False)

    def create_test_execution(self):
        test_execution_title = 'Web smoke execution ' + str(time.time())

        fields = {
            'project':
            {
                'key': 'QA'
            },
            'summary': test_execution_title,
            'description': 'automated test execution',
            'issuetype': {'name': 'Test Execution'},
        }
        test_execution = self.atlassian_jira.create_issue(fields=fields)
        return test_execution.key

    def create_execution_and_associate_with_smoke(self):
        test_execution = self.create_test_execution()
        self.create_execution_for_smoke(test_execution)

    def update_test_status(self):

        jsontest = {
                "status": "FAIL",
        }
        a = requests.get("https://jira.adam.loc/rest/raven/1.0/api/testrun/?testExecIssueKey=QA-1415&testIssueKey=QA-1047",
                         auth=HTTPBasicAuth("solinichenko", "madokaqWeaSd123"), verify=False)
        b = a.json()
        c = b.get("id")
        d = requests.put(("https://jira.adam.loc/rest/raven/1.0/api/testrun/%s/" % c), json=jsontest,
                         auth=HTTPBasicAuth("solinichenko", "madokaqWeaSd123"), verify=False)
        e = d


