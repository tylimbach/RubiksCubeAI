"""
__main__.py
Launch script intended to start the application
"""

__author__ = "Tyler Limbach"

# # profiling imports
# import cProfile
# import pstats
# from pstats import SortKey


def __main__():
    """ Main function to start app
    """
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    # set python hash seed to 0 for consistent hashing
    hash_seed = os.getenv('PYTHONHASHSEED')
    python_path = os.getenv('PYTHONPATH')

    print(sys.path)

    # if not hash_seed: #or python_path == '.':
    #     os.environ['PYTHONHASHSEED'] = '0'
    #     #os.environ['PYTHONPATH'] = '.'
    #     os.execv(sys.executable, [sys.executable] + sys.argv)

    from cubesolver.src.menu import menu_loop

    menu_loop()


if __name__ == '__main__':
    __main__()

    # cProfile.run('main()', 'restats')
    # p = pstats.Stats('restats')
    # p.strip_dirs().sort_stats(SortKey.TIME).print_stats()
