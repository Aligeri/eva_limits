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
    :returns: int relating to test outcome.
    """
    return PYTEST_TO_XRAY[outcome]


def testrun_name():
    """Returns testrun name with timestamp"""
    now = datetime.utcnow()
    return 'Automated Run {}'.format(now.strftime(DT_FORMAT))




def get_xray_keys(items):
    """Return Tuple of Pytest nodes and TestRail ids from pytests markers"""
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
    def __init__(self, username, password, testplan):
        self.options = {
            'server': 'https://jira.adam.loc',
            'verify': False,  # SSL validation off because Jira use self signed certificate
        }
        self.username = username
        self.password = password
        self.testplan = testplan
        self.atlassian_jira = JIRA(options=self.options, basic_auth=(self.username, self.password))
        self.test_execution = None


    # pytest hooks

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
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

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """ Collect result and associated testcases (TestRail) of an execution """
        outcome = yield
        rep = outcome.get_result()
        if item.get_closest_marker(XRAY_PREFIX):
            testcaseids = item.get_closest_marker(XRAY_PREFIX).kwargs.get('ids')

            if rep.when == 'call' and testcaseids:
                for testcase in testcaseids:
                    self.update_test_status(
                        testcase,
                        self.test_execution,
                        PYTEST_TO_XRAY[outcome.get_result().outcome]
                    )
        return rep

    def update_test_status(self, issue_key, test_execution, status):
        """
        Обновляет статус testrun в test execution
        :param issue_key:
        :param test_execution:
        :param status: FAIL, PASS, ABORTED
        :return:
        """
        jsontest = {
            "status": status,
        }
        print("переменные " + issue_key + " " + test_execution + " " + status)
        a = requests.get("https://jira.adam.loc/rest/raven/1.0/api/testrun/?testExecIssueKey=%s&testIssueKey=%s" % (test_execution, issue_key),
                         auth=HTTPBasicAuth(self.username, self.password), verify=False)
        b = a.json()
        c = b.get("id")
        d = requests.put(("https://jira.adam.loc/rest/raven/1.0/api/testrun/%s/" % c), json=jsontest,
                         auth=HTTPBasicAuth(self.username, self.password), verify=False)


'''
    def pytest_sessionfinish(self, session, exitstatus):
        """ Publish results in TestRail """
        print('[{}] Start publishing'.format(TESTRAIL_PREFIX))
        if self.results:
            tests_list = [str(result['case_id']) for result in self.results]
            print('[{}] Testcases to publish: {}'.format(TESTRAIL_PREFIX, ', '.join(tests_list)))

            if self.testrun_id:
                self.add_results(self.testrun_id)
            elif self.testplan_id:
                testruns = self.get_available_testruns(self.testplan_id)
                print('[{}] Testruns to update: {}'.format(TESTRAIL_PREFIX, ', '.join([str(elt) for elt in testruns])))
                for testrun_id in testruns:
                    self.add_results(testrun_id)
            else:
                print('[{}] No data published'.format(TESTRAIL_PREFIX))

            if self.close_on_complete and self.testrun_id:
                self.close_test_run(self.testrun_id)
            elif self.close_on_complete and self.testplan_id:
                self.close_test_plan(self.testplan_id)
        print('[{}] End publishing'.format(TESTRAIL_PREFIX))

    # plugin

'''