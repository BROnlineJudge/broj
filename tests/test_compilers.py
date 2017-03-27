# -*- coding: utf-8 -*-
from ej import compilers
from ej import exceptions
import os
import tempfile
import unittest


class TestCompilers(unittest.TestCase):
    def test_unsupported_languages(self):
        wrong_supported_languages = ['CPP', 'C', 'C++', 'c++', 'cPP',
                                     'PY', 'Python', 'PYTHON',
                                     'RB', 'Ruby', 'RUBY', 'ruby',
                                     'JAVA', 'Java']
        unsupported_languages = ['rs', 'haskell', 'abc', 'xablau', None, 3, 0,
                                 True, False, [], (), {}, print]
        for lang in (wrong_supported_languages + unsupported_languages):
            with self.subTest(lang=lang):
                with self.assertRaises(exceptions.UnsupportedLanguage):
                    compilers.compile(lang, 'None', 'None')


class TestCompilersCpp(unittest.TestCase):
    def setUp(self):
        self.lang = 'cpp'
        self.dir, self.file = set_up_for(self.lang)

    def tearDown(self):
        tear_down(self.dir, self.file)

    def test_compiler_cpp_success(self):
        code = '''
int main() {
    return 0;
}
        '''
        write(self, code)
        expected = os.path.join(self.dir.name, 'prog')
        compiler_result = compilers.compile(self.lang, self.dir.name,
                                            self.file.name)
        self.assertEqual(expected, compiler_result)

    def test_compiler_cpp_compilation_error(self):
        c1 = '''
hello compilation error
        '''
        c2 = '''
import os
print('wrong language bro')
        '''
        c3 = '''
#include <iostream>
int main() {
    cout << "no std" << endl;
    return 0;
}
        '''
        compilation_error_codes = [c1, c2, c3]
        for code in compilation_error_codes:
            write(self, code)
            with self.assertRaises(exceptions.CompilationError):
                compilers.compile(self.lang, self.dir.name, self.file.name)

    def test_compiler_cpp_tle(self):
        pass


class TestCompilersPython(unittest.TestCase):
    def setUp(self):
        self.lang = 'py'

    def test_compiler_python_success(self):
        filename = 'test.py'
        compiler_result = compilers.compile(self.lang, '_', filename)
        self.assertEqual(filename, compiler_result)


def set_up_for(lang):
    temp_dir = tempfile.TemporaryDirectory()
    temp_file = tempfile.NamedTemporaryFile(dir=temp_dir.name,
                                            delete=True,
                                            suffix='.' + lang)
    return temp_dir, temp_file


def tear_down(temp_dir, temp_file):
    temp_file.close()
    temp_dir.cleanup()


def write(tester, code):
    tester.file.seek(0)
    tester.file.truncate()
    tester.file.write(code.encode())
    tester.file.seek(0)


if __name__ == '__main__':
    unittest.main()
