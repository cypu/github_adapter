import os
from unittest import TestLoader, TextTestRunner

if __name__ == "__main__":
    loader = TestLoader()
    start_dir = os.path.join(os.getcwd(), 'tests')
    suite = loader.discover(start_dir)
    runner = TextTestRunner()
    runner.run(suite)
