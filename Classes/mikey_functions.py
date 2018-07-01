"""
Miscellaneous functions I tend to use alot
"""
import os

def absolute_path(path):
    """ Returns an absolute path """
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            path
        )
    )
