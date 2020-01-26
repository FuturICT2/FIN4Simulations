import unittest
import Fin4_ABM as run

class MyTestCase(unittest.TestCase):
    def agent_creation(self):
        run.raw_result[-1]
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
