import unittest
import subprocess
import jobdiary


class CliTests(unittest.TestCase):

    def test_base_command(self):
        version = execute_shell('python3 -m jobdiary --version')

        self.assertEqual(version, jobdiary.__version__ + "\n")


def get_stdout(pi):
    result = pi.communicate()
    if len(result[0]) > 0:
        return result[0]
    else:
        return result[1]  # some error has occured


def execute_shell(command):
    return execute(command, wait=True, shellexec=True, errorstring='CLI Error')


def execute(command='', errorstring='', wait=True, shellexec=False, ags=None, env={'LC_ALL': 'C'}):
    try:
        if (shellexec):
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        else:
            p = subprocess.Popen(args=ags, env=env)

        if wait:
            p.wait()
            result = get_stdout(p)
            return str(result.decode("utf-8"))
        else:
            return p
    except subprocess.CalledProcessError as e:
        print('error occured:' + errorstring + str(e))
        return errorstring
    except Exception as ea:
        print('Exception occured:' + str(ea))
        return errorstring
