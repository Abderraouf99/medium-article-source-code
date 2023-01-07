import logging
import os


class ScriptLogger:
    def __init__(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(dir_path, 'script_logs.log')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def log(self, msg: str):
        self.logger.info(msg)
