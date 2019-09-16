# -*- coding: UTF-8 -*-
from datetime import datetime
from operator import itemgetter
import requests
from requests.auth import HTTPBasicAuth
import pytest
import re
import warnings
from jira import JIRA
import time
import os
import base64
from json import dumps

# Reference: http://docs.gurock.com/testrail-api2/reference-statuses

PYTEST_TO_XRAY = {
    "passed": "PASS",
    "failed": "FAIL",
    "skipped": "ABORTED"
}

DT_FORMAT = '%d-%m-%Y %H:%M:%S'

XRAY_PREFIX = 'xray'


def xray(*ids):

    return pytest.mark.xray(ids=ids)


def get_test_outcome(outcome):
    """
    Return numerical value of test outcome.

    :param str outcome: pytest reported test outcome value.
    :returns: string relating to test outcome.
    """
    return PYTEST_TO_XRAY[outcome]


def testrun_name():
    """Returns testrun name with timestamp"""
    now = datetime.utcnow()
    return 'Automated Run {}'.format(now.strftime(DT_FORMAT))




def get_xray_keys(items):

    testcaseids = []
    for item in items:
        if item.get_closest_marker(XRAY_PREFIX):
            testcaseids.append(
                (
                    item,
                    item.get_closest_marker(XRAY_PREFIX).kwargs.get('ids')
                )
            )
    return testcaseids


class PytestXrayPlugin(object):
    def __init__(self, username, password, testplan, test_execution):
        self.options = {
            'server': 'https://jira.adam.loc',
            'verify': False,  # SSL validation off because Jira use self signed certificate
        }
        self.username = username
        self.password = password
        self.testplan = testplan
        self.atlassian_jira = JIRA(options=self.options, basic_auth=(self.username, self.password))
        self.test_execution = test_execution


    # pytest hooks

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        if self.test_execution is None:
            self.test_execution = self.create_test_execution()
            self.create_execution_for_smoke()


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

    def create_execution_for_smoke(self):
        add_tests = {
            "add": [
                self.testplan
            ]
        }
        execution_id = requests.post(("https://jira.adam.loc/rest/raven/1.0/api/testexec/%s/test" % self.test_execution), json=add_tests, auth=HTTPBasicAuth("solinichenko", "madokaqWeaSd123"), verify=False)

    def create_execution_and_associate_with_smoke(self):
        self.create_test_execution()
        self.create_execution_for_smoke()

    @pytest.hookimpl(trylast=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        rep = outcome.get_result()



        if item.get_closest_marker(XRAY_PREFIX):
            testcaseids = item.get_closest_marker(XRAY_PREFIX).kwargs.get('ids')
            if rep.when == 'call' and testcaseids:


                for testcase in testcaseids:
                    if rep.outcome == "failed":

                        feature_request = item.funcargs['request']
                        driver = feature_request.getfixturevalue('driver')
                        dirname = os.path.dirname(__file__)
                        screenshot_file_path = "{}/../screenshots/{}.png".format(dirname, item.name)
                        driver.save_screenshot(
                            screenshot_file_path
                        )

                        self.update_test_status(
                            testcase,
                            self.test_execution,
                            PYTEST_TO_XRAY[outcome.get_result().outcome],
                            str(outcome.get_result().longrepr),
                            self.get_screenshot(item.name)
                        )
                    else:
                        self.update_test_status(
                            testcase,
                            self.test_execution,
                            PYTEST_TO_XRAY[outcome.get_result().outcome])

        return rep

    def get_screenshot(self, test_name):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'screenshots')
        screenshot_file_path = "{}/../screenshots/{}.png".format(dirname, test_name)
        with open(screenshot_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            base64_string = encoded_string.decode("utf-8")
            #json_data = dumps(encoded_string, indent=2)
            return base64_string

    def update_test_status(self, issue_key, test_execution, status, comment='', screenshot=''):
        """
        Обновляет статус testrun в test execution
        :param issue_key:
        :param test_execution:
        :param status: FAIL, PASS, ABORTED
        :return:
        """
        if status == "FAIL":
            jsontest = {
                "status": status,
                "comment": comment,
                "evidences": {
                    "add": [{
                        "filename": (issue_key+".jpeg"),
                        "contentType": "image/jpeg",
                        "data": screenshot
                    }]
                }
            }
        else:
            jsontest = {
                "status": status
            }
        try:
            a = requests.get("https://jira.adam.loc/rest/raven/1.0/api/testrun/?testExecIssueKey=%s&testIssueKey=%s" % (test_execution, issue_key),
                             auth=HTTPBasicAuth(self.username, self.password), verify=False)
            b = a.json()
            c = b.get("id")
            d = requests.put(("https://jira.adam.loc/rest/raven/1.0/api/testrun/%s/" % c), json=jsontest,
                             auth=HTTPBasicAuth(self.username, self.password), verify=False)
        except:
            print("there is no %s test in %s execution" % (issue_key, test_execution))
