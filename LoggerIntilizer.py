import logging
import os


path = os.path.dirname(os.path.abspath(__file__))

def setup_logger(name='main_script_log', log_file='/main_script_processes.log', level=logging.DEBUG):
    """To setup as many loggers as you want"""
    log_file = path +log_file
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler = logging.FileHandler(log_file,mode='a')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(handler)
    logger.disabled = False

    return logger