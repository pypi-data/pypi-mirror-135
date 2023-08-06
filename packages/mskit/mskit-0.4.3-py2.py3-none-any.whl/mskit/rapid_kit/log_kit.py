import datetime
import logging
import sys


def console_file_logger(
        logger_name='root',
        log_path=None,
        log_console_level=logging.DEBUG,
        log_file_level=None,
        log_console_format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        log_file_format=None,
        write_init_logs=False,
        reset_handlers=True
):
    """
    TODO: custom init messages
    TODO: multi log handlers
    Setup a logger with name `logger_name` and store in `log_path` if path is defined
    """
    logger = logging.getLogger(logger_name)

    if len(logger.handlers) > 0:
        if reset_handlers:
            for h in logger.handlers:
                logger.removeHandler(h)
        else:
            return logger

    start_time = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")
    stored_msgs = [
        f'Logger "{logger_name}" created at {start_time}',
        f'Logger "{logger_name}" has level (console): "{log_console_level}"',
        f'Logger "{logger_name}" has format (console): "{log_console_format}"',
    ]

    logger.setLevel(log_console_level)

    formatter = logging.Formatter(log_console_format)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(log_console_level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    if log_path is not None:
        file_handler = logging.FileHandler(log_path)

        if log_file_level is None:
            log_file_level = log_console_level
        file_handler.setLevel(log_file_level)

        if log_file_format is None:
            log_file_format = log_console_format
            formatter = logging.Formatter(log_file_format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stored_msgs.extend([
            f'Set store path of logger {logger_name} to: {log_path}'
            f'Logger "{logger_name}" has level (file): "{log_file_level}"'
            f'Logger "{logger_name}" has format (file): "{log_file_format}"'
        ])

    if write_init_logs:
        for msg in stored_msgs:
            logger.info(msg)

    return logger
