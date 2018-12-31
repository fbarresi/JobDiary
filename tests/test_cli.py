import unittest
import jobdiary


class CliTests(unittest.TestCase):

    def test_base_command(self):
        version = jobdiary.run(['--version'])

        self.assertEqual(version, jobdiary.__version__)
