import os
from datetime import datetime


class Logger:
    def __init__(self, directory, name=''):
        self._log_directory = directory
        self._name = name
        self._create_error_file_name()

    def log_error(self, error):
        print(error)
        self._create_log_base_directory()
        self._create_log_directory()
        timestamp = datetime.now().strftime("%H:%M:%S:%f")
        open(self.error_file_name, 'a').write(
            "{} {}: {}\n".format(self._name, timestamp, error))

    def _create_log_base_directory(self):
        if not os.path.exists('logs'):
            os.mkdir('logs')

    def _create_log_directory(self):
        if not os.path.exists(os.path.join('logs', self._log_directory)):
            os.mkdir(os.path.join('logs', self._log_directory))

    def _create_error_file_name(self):
        self.error_file_name = os.path.join(
            'logs', self._log_directory, datetime.now().strftime("%Y-%m-%d-%H:%M:%S:%f.txt"))
