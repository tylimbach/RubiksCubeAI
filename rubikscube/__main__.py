"""
__main__.py
Launch script intended to start the application
"""

__author__ = "Tyler Limbach"

import os
import sys
from rubikscube.src.menu import menu_loop

# # profiling imports
# import cProfile
# import pstats
# from pstats import SortKey


def clear():
    os.system("clear")


def main():
    """ Main function to start app
    """
    # set python hash seed to 0 for consistent hashing
    hash_seed = os.getenv('PYTHONHASHSEED')
    if not hash_seed:
        os.environ['PYTHONHASHSEED'] = '0'
        os.execv(sys.executable, [sys.executable] + sys.argv)

    menu_loop()



if __name__ == '__main__':
    main()

    # cProfile.run('main()', 'restats')
    # p = pstats.Stats('restats')
    # p.strip_dirs().sort_stats(SortKey.TIME).print_stats()
