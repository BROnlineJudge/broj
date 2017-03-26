# -*- coding: utf-8 -*-
class CompilationError(Exception):
    pass


class JudgeError(Exception):
    pass


class UnsupportedLanguage(Exception):
    pass


class ConfigError(Exception):
    pass


class JudgeConnectionError(Exception):
    pass


class CourierConnectionError(Exception):
    pass
