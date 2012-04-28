#-*- coding:utf-8 -*-

import sys
import sched
import os
import time
import functools
import traceback


check_ext = ['.py', '.rst']


def make_checker(root):

    cache = {}


    def update_cache(path, status):

        ext = os.path.splitext(path)[1]

        if ext not in check_ext:
            return (True, status)

        try:
            mtime = os.stat(path).st_mtime
        except OSError:
            traceback.print_exc()
            return (True, status)
            
        past = cache.get(path)

        cache[path] = mtime

        if past is None:
            print('add new file:', path)
            return (True, True)
        elif past < mtime:
            print('updated:', path)
            return (True, True)

        return (True, status)
        


    def check_file(chfunc, initstate):

        status = initstate

        for path, dirs, files in os.walk(root):

            for f in files:

                (cont, status) = chfunc(os.path.join(path, f), status)

                if not cont:
                    return status

        return status
    

    check_file(update_cache, False)


    def make():

        os.system('make html')
    

    def update_check():

        st = check_file(update_cache, False)

        if st:
            make()


    update_check()
            
    return update_check



def reentrant(f, scheduler, interval=30, args=()):

    @functools.wraps(f)
    def schedule():

        f()

        scheduler.enter(interval, 1, schedule, args)

    schedule()

    return schedule



def main(argv=sys.argv[1:]):

    scheduler = sched.scheduler(time.time, time.sleep)
    
    checker = make_checker(os.getcwd())

    reentrant(checker, scheduler, interval=5)

    scheduler.run()


if __name__ == '__main__':
    main()
        
