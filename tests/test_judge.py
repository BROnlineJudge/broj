# -*- coding: utf-8 -*-
from mock import *
from ej import models
from ej.verdict import Verdict
import unittest
import judge


class TestJudge(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tle_cpp(self):
        code = '''
#include <iostream>
#include <chrono>
#include <thread>
int main() {
    using namespace std::chrono_literals;
    std::this_thread::sleep_for(%ss);
    std::cout << std::endl;
    return 0;
}
        '''

        do_problem_mock('tle test', 1, [''], [''])
        verdict = judge.get_verdict(1, 'cpp', (code % 1.5))
        self.assertEqual(verdict, Verdict.TLE)

        verdict = judge.get_verdict(1, 'cpp', (code % 0.5))
        self.assertNotEqual(verdict, Verdict.TLE)

    def test_ce_cpp(self):
        code = '''
{
xablau;;;;;
}
        '''

        do_problem_mock('ce test', 1, [''], [''])
        verdict = judge.get_verdict(1, 'cpp', code)
        self.assertEqual(verdict, Verdict.CE)

    def test_je_cpp(self):
        code = '''
int main() {
    return 0;
}
        '''

        do_problem_mock('je test', 1, [], [])
        verdict = judge.get_verdict(1, 'cpp', code)
        self.assertEqual(verdict, Verdict.JE)

    def test_rte_cpp(self):
        code = '''
#include <csignal>
int main()
{
    std::raise(SIGSEGV);
    return 0;
}
        '''

        do_problem_mock('rte test', 1, [''], [''])
        verdict = judge.get_verdict(1, 'cpp', code)
        self.assertEqual(verdict, Verdict.RTE)

    def test_ac_cpp(self):
        code = '''
#include <iostream>
int main() {
    std::cout << "AC" << std::endl;
    return 0;
}
        '''

        do_problem_mock('ac test', 1, [''], ['AC\n'])
        verdict = judge.get_verdict(1, 'cpp', code)
        self.assertEqual(verdict, Verdict.AC)


    def test_wa_cpp(self):
        code = '''
#include <iostream>
int main() {
    std::cout << "wa pls" << std::endl;
    return 0;
}
        '''

        do_problem_mock('wa test', 1, [''], [''])
        verdict = judge.get_verdict(1, 'cpp', code)
        self.assertEqual(verdict, Verdict.WA)

    def test_pe_cpp(self):
        code = '''
#include <iostream>
int main() {
    std::cout << "ANSWER" << std::endl;
    return 0;
}
        '''

        do_problem_mock('pe test', 1, [''], ['ANSWER'])
        verdict = judge.get_verdict(1, 'cpp', code)
        self.assertEqual(verdict, Verdict.PE)

    def test_ac_python(self):
        code = '''
print("AC")
        '''

        do_problem_mock('ac test', 1, [''], ['AC\n'])
        verdict = judge.get_verdict(1, 'py', code)
        self.assertEqual(verdict, Verdict.AC)

    def test_pe_python(self):
        do_problem_mock('pe test', 1, [''], ['ANSWER'])
        code = '''
print("Answer")
        '''
        verdict = judge.get_verdict(1, 'py', code)
        self.assertEqual(verdict, Verdict.PE)
        code = '''
print("ANSWER")
        '''
        verdict = judge.get_verdict(1, 'py', code)
        self.assertEqual(verdict, Verdict.PE)

    def test_wa_python(self):
        code = '''
print("WA")
        '''

        do_problem_mock('wa test', 1, [''], ["AC\n"])
        verdict = judge.get_verdict(1, 'py', code)
        self.assertEqual(verdict, Verdict.WA)

    def test_tle_python(self):
        code = '''
import time
time.sleep(%s)
        '''

        do_problem_mock('tle test', 1, [''], [''])
        verdict = judge.get_verdict(1, 'py', (code % 1.5))
        self.assertEqual(verdict, Verdict.TLE)

        verdict = judge.get_verdict(1, 'py', (code % 0.5))
        self.assertNotEqual(verdict, Verdict.TLE)

    def test_rte_python(self):
        code = '''
print(1/0)
        '''

        do_problem_mock('rte test', 1, [''], ["ANSWER"])
        verdict = judge.get_verdict(1, 'py', code)
        self.assertEqual(verdict, Verdict.RTE)


def do_problem_mock(title, time_limit, inputs, outputs):
    if(len(inputs) != len(outputs)):
        raise

    mock_problem = MagicMock()
    mock_problem.title = title
    mock_problem.time_limit = time_limit
    mock_problem.test_cases = []

    for i in range(0, len(inputs)):
        mock_test_case = MagicMock()
        mock_test_case.input_ = inputs[i]
        mock_test_case.output = outputs[i]
        mock_test_case.problem = mock_problem
        mock_problem.test_cases.append(mock_test_case)

    models.Problem = MagicMock()
    models.Problem.__getitem__.return_value = mock_problem


if __name__ == '__main__':
    unittest.main()
