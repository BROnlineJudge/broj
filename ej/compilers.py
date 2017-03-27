# -*- coding: utf-8 -*-
from ej import exceptions
import os
import subprocess


def compile(language, directory, filename):
    """
    Compiles given source code.

    :param language: Language being compiled
    :param directory: Directory that contains the source file
    :param filename: Source file
    :returns: Check the related compilation function for each language.
    :raises: Check the related compilation function for each language.
    """
    compiler_func = _get_compiler_func(language)
    return compiler_func(directory, filename)


def _get_compiler_func(language):
    """
    Retrieves the compilation function for the given language.

    :param language: Language being compiled
    :returns: That language's compilation function.
    :raises UnsupportedLanguage: For languages that are not supported by BROJ.
    """
    try:
        compiler_func = _dispatch_compiler[language]
        return compiler_func
    except:
        raise exceptions.UnsupportedLanguage


def _compile_cpp(directory, filename):
    """
    Compiles C++ source code.

    :returns: The compiled executable's path.
    :raises CompilationError: For source code that does not compile.
    :raises JudgeError: For any other error.
    """
    try:
        exec_filename = 'prog'
        exec_path = os.path.join(directory, exec_filename)
        subprocess.run(args=['g++', filename, '-std=c++14', '-o', exec_path],
                       timeout=5, check=True)
        return exec_path
    except subprocess.CalledProcessError:
        raise exceptions.CompilationError
    except:
        raise exceptions.JudgeError


def _compile_python(directory, filename):
    """
    Simply returns the given filename, since Python does not need compilation.

    :returns: The given filename.
    """
    return filename


_dispatch_compiler = {
    'cpp': _compile_cpp,
    'py': _compile_python,
}
