# -*- coding: utf-8 -*-
from enum import IntEnum, unique

@unique
class Verdict(IntEnum):
    AC = 1
    PE = 2
    WA = 3
    CE = 4
    RTE = 5
    TLE = 6
    MLE = 7
    JE = 8

    @staticmethod
    def _name_dict():
        return {
            Verdict.AC: 'Accepted',
            Verdict.PE: 'Presentation Error',
            Verdict.WA: 'Wrong Answer',
            Verdict.CE: 'Compilation Error',
            Verdict.RTE: 'Runtime Error',
            Verdict.TLE: 'Time Limit Exceeded',
            Verdict.MLE: 'Memory Limit Exceeded',
            Verdict.JE: 'Judge Error'
        }

    def __str__(self):
        return Verdict._name_dict()[self]

    def __repr__(self):
        return '<Verdict : \'' + str(self) + '\'>'

