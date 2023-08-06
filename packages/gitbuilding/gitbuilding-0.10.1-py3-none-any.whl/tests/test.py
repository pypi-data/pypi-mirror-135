import sys
import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    passed_all = unittest.TextTestRunner().run(testsuite).wasSuccessful()
    if not passed_all:
        sys.exit(1)
