from nose.tools import *
from unittest.mock import *
from ej import models
from ej.verdict import Verdict
import judge

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


def test_tle():
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
    assert_equals(verdict, Verdict.TLE)

    verdict = judge.get_verdict(1, 'cpp', (code % 0.5))
    assert_not_equals(verdict, Verdict.TLE)

def test_ce():
    code = '''
{
xablau;;;;;
}
    '''

    do_problem_mock('ce test', 1, [''], [''])
    verdict = judge.get_verdict(1, 'cpp', code)
    assert_equals(verdict, Verdict.CE)

def test_je():
    code = '''
int main() {
    return 0;
}
    '''

    do_problem_mock('je test', 1, [], [])
    verdict = judge.get_verdict(1, 'cpp', code)
    assert_equals(verdict, Verdict.JE)

def test_rte():
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
    assert_equals(verdict, Verdict.RTE)

def test_ac():
    code = '''
#include <iostream>
int main() {
    std::cout << "AC" << std::endl;
    return 0;
}
    '''

    do_problem_mock('ac test', 1, [''], ['AC\n'])
    verdict = judge.get_verdict(1, 'cpp', code)
    assert_equals(verdict, Verdict.AC)


def test_wa():
    code = '''
#include <iostream>
int main() {
    std::cout << "wa pls" << std::endl;
    return 0;
}
    '''

    do_problem_mock('wa test', 1, [''], [''])
    verdict = judge.get_verdict(1, 'cpp', code)
    assert_equals(verdict, Verdict.WA)

def test_pe():
    code = '''
#include <iostream>
int main() {
    std::cout << "ANSWER" << std::endl;
    return 0;
}
    '''

    do_problem_mock('pe test', 1, [''], ['ANSWER'])
    verdict = judge.get_verdict(1, 'cpp', code)
    assert_equals(verdict, Verdict.PE)
