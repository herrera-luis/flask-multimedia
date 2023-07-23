import logging
from logging.handlers import RotatingFileHandler
import json
import os

class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'date': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'pathname': record.pathname,
            'line': record.lineno
        }
        return json.dumps(log_data)

def configure_logger(app):
    app.logger.setLevel(logging.INFO)
    logger_handler = logging.FileHandler('multimedia.log')
    logger_handler.setLevel(logging.INFO)
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(logger_formatter)
    log_dir = app.config.get('LOG_DIR', 'logs')
    log_file = os.path.join(log_dir, 'multimedia.log')
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(JSONLogFormatter())
    app.logger.addHandler(file_handler)