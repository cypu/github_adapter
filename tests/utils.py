import os


class TestConfigLoaderMixin(object):

    def load_test_config(self):
        test_config = os.path.join(os.getcwd(), 'test_config')
        self.test_config_data = {}

        with open(test_config, 'r') as f:
            for line in f.readlines():
                k, v = line.split(':')
                self.test_config_data.update({k.strip(): v.strip()})