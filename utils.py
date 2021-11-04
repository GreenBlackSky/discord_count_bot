import logging
from functools import wraps


logger = logging.getLogger('discord')


def int_arg(method):
    @wraps(method)
    async def _wrapper(ctx, *args):
        if not args:
            raise Exception("count till what?")
        elif len(args) > 1:
            raise Exception(f"can't count to {args}")
        countdown = args[0]
        if not countdown.isnumeric():
            raise Exception(f"can't count to {countdown}")

        return await method(ctx, int(countdown))

    return _wrapper
