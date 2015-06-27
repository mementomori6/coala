import copy
import unittest
import sys
import subprocess

sys.path.insert(0, ".")
from coalib.misc.ContextManagers import (suppress_stdout,
                                         retrieve_stdout,
                                         simulate_console_inputs,
                                         preserve_sys_path,
                                         subprocess_timeout)
from coalib.misc.StringConstants import StringConstants


class ContextManagersTest(unittest.TestCase):
    def test_subprocess_timeout(self):
        p = subprocess.Popen([StringConstants.python_executable,
                              "-c",
                              "import time; time.sleep(0.5); print('hi')"])
        retval = None
        with subprocess_timeout(p, 0.2):
            retval = p.wait()
        self.assertNotEqual(retval, 0)

        p = subprocess.Popen([StringConstants.python_executable,
                              "-c",
                              "print('hi')"])
        retval = None
        with subprocess_timeout(p, 0.2):
            retval = p.wait()
        self.assertEqual(retval, 0)

        p = subprocess.Popen([StringConstants.python_executable,
                              "-c",
                              "print('hi')"])
        retval = None
        with subprocess_timeout(p, 0):
            retval = p.wait()
        self.assertEqual(retval, 0)

    def test_suppress_stdout(self):
        def print_func():
            print("func")
            raise NotImplementedError

        def no_print_func():
            with suppress_stdout():
                print("func")
                raise NotImplementedError

        old_stdout = sys.stdout
        sys.stdout = False

        self.assertRaises(AttributeError, print_func)
        self.assertRaises(NotImplementedError, no_print_func)

        sys.stdout = old_stdout

    def test_retrieve_stdout(self):
        with retrieve_stdout() as sio:
            print("test")
            self.assertEqual(sio.getvalue(), "test\n")

    def test_simulate_console_inputs(self):
        with simulate_console_inputs(0, 1, 2) as generator:
            self.assertEqual(input(), 0)
            self.assertEqual(generator.last_input, 0)
            generator.inputs.append(3)
            self.assertEqual(input(), 1)
            self.assertEqual(input(), 2)
            self.assertEqual(input(), 3)
            self.assertEqual(generator.last_input, 3)

    def test_preserve_sys_path(self):
        old_sys_path = copy.copy(sys.path)
        with preserve_sys_path():
            sys.path = 5

        self.assertEqual(old_sys_path, sys.path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
