import sys


from jobdiary.texts import usage

def decode_args(args, encoding=None):
    """
    Convert all bytes args to str
    by decoding them using stdin encoding.
    """
    return [
        arg.decode(encoding)
        if type(arg) == bytes else arg
        for arg in args
    ]


def main(args=sys.argv[1:]):
    """
    The main function.
    Pre-process args, handle some special types of invocations,
    and run the main program with error handling.
    Return exit status code.
    """
    args = decode_args(args)

    include_debug_info = '--debug' in args

    if len(args) == 0 : print(usage())

    print(args)

    if include_debug_info:
        if args == ['--debug']:
            return

    return
