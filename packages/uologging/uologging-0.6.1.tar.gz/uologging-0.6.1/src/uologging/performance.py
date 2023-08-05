import time
import logging
from functools import wraps


def trace(logger: logging.Logger, capture_args=True):
    """Decorator to trace the execution time of a Python function or method.

    Uses INFO log level for logging the traced function's "exec time".
    Also will log the traced function's entry and exit at DEBUG log level.

    Args:
        logger (logging.Logger): The logger instance for the function's module.
        capture_args (bool, optional): When tracing the function, capture the 
            arguments provided to the function and add them to the log message.
            Defaults to True.

    Example:

    First, get the logger for your Python module.

        import logging
        logger = logging.getLogger(__name__)

    Then, use the trace_time decorator with that logger as the argument.

        import uologging
        @uologging.trace(logger)
        def my_slow_function():
            import time
            time.sleep(1)
        my_slow_function()
    """
    def _trace_time(func):
        @wraps(func)
        def timed(*args, **kw_args):
            if capture_args:
                func_str_repr = f'{func.__module__}:{func.__name__}({args!r},{kw_args!r})'
            else:
                func_str_repr = f'{func.__module__}:{func.__name__}(...)'
            try:
                logger.debug(f'Starting: {func_str_repr}', stacklevel=2)
                start = time.time()
                result = func(*args, **kw_args)
                end = time.time()
                logger.debug(f'Finished: {func_str_repr}', stacklevel=2)
                logger.info(f'{func_str_repr} exec time: {end - start:.2f} sec', stacklevel=2)
            except TypeError as e:
                if "unexpected keyword argument 'stacklevel'" not in str(e):
                    raise e
                # If this is a TypeError because 
                logger.debug(f'Starting: {func_str_repr}')
                start = time.time()
                result = func(*args, **kw_args)
                end = time.time()
                logger.debug(f'Finished: {func_str_repr}')
                logger.info(f'{func_str_repr} exec time: {end - start:.2f} sec')
            return result
        return timed
    return _trace_time
