"""
__main__.py
Launch script intended to start the application
"""

__author__ = "Tyler Limbach"

import os
import sys


def main():
    """ Main function to start app
    """
    # set the script path
    sys.path.append(os.path.dirname(__file__))

    from src.menu import menu_loop

    menu_loop()


if __name__ == '__main__':
    main()

    # # profiling imports
    # import cProfile
    # import pstats
    # from pstats import SortKey

    # cProfile.run('main()', 'restats')
    # p = pstats.Stats('restats')
    # p.strip_dirs().sort_stats(SortKey.TIME).print_stats()
