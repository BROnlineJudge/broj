from ej.verdict import Verdict
from ej import exceptions
import subprocess


def compile(language, directory, filename):
    compiler_func = _get_compiler_func(language)
    return compiler_func(directory, filename)


def _get_compiler_func(language):
    try:
        compiler_func = _dispatch_compiler[language]
        return compiler_func
    except:
        raise exceptions.UnsupportedLanguage


def _compile_cpp(directory, filename):
    executable = 'prog'
    prog = directory + '/' + executable

    try:
        subprocess.run(args=['g++', filename, '-o', prog],
                       timeout=5, check=True)
    except subprocess.CalledProcessError:
        raise exceptions.CompilationError
    except subprocess.TimeoutExpired as tle:
        raise exceptions.JudgeError

    return prog


def _compile_c(directory, filename):
    raise exceptions.CompilationError


def _compile_python(directory, filename):
    raise exceptions.CompilationError


def _compile_java(directory, filename):
    raise exceptions.CompilationError


def _compile_ruby(directory, filename):
    raise exceptions.CompilationError



_dispatch_compiler = {
    'cpp': _compile_cpp,
    'c': _compile_c,
    'py': _compile_python,
    'java': _compile_java,
    'rb': _compile_ruby,
}

