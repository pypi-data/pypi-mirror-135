from contextlib import contextmanager
from select import select
from sys import stdin
from termios import tcgetattr, tcsetattr, ICANON, ECHO, TCSAFLUSH
from typing import Optional, Generator

ESC = '\x1b'
UP = '\x1b[A'
DOWN = '\x1b[B'
RIGHT = '\x1b[C'
LEFT = '\x1b[D'


def getkey() -> Optional[str]:
    if select([stdin], [], [], 0)[0]:
        res = stdin.read(1)
        while res == ESC or not res[-1].isalpha():
            res += stdin.read(1)
        return res
    return None


@contextmanager
def unbuffered_term() -> Generator[None, None, None]:
    file_descriptor = stdin.fileno()
    new_term = tcgetattr(file_descriptor)
    old_term = tcgetattr(file_descriptor)
    try:
        new_term[3] = (new_term[3] & ~ICANON & ~ECHO)  # type: ignore
        tcsetattr(file_descriptor, TCSAFLUSH, new_term)
        yield
    finally:
        tcsetattr(file_descriptor, TCSAFLUSH, old_term)
