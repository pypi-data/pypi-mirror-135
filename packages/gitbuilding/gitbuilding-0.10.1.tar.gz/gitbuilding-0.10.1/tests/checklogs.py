import logging

def no_logs(name, level=logging.WARN):
    """
    Decorator that raises an assertion error if the named logger logs anything
    at the set logging level or higher. Default level is WARN.
    """
    def no_logs_decorator(func):
        def wrapped_method(*args, **kwargs):
            handler = RaiseHandler(level)
            logger = logging.getLogger(name)
            logger.addHandler(handler)
            try:
                func(*args, **kwargs)
                logger.removeHandler(handler)
            except Exception as exception:
                #remove handeler and re-raise
                logger.removeHandler(handler)
                raise exception
        return wrapped_method
    return no_logs_decorator

class RaiseHandler(logging.Handler):
    """
    A child class of logging.Handler. This class raises an assertion error
    for any log it is to emit.
    """

    def __init__(self, level=logging.NOTSET):
        super().__init__(level=level)
        self.formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def emit(self, record):
        """
        Raise an assertion error if there was a log above the logging level
        """
        if record.levelno >= self.level:
            message = 'Unexpected logging:\n' + self.format(record)
            raise AssertionError(message)

