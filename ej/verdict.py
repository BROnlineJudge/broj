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
