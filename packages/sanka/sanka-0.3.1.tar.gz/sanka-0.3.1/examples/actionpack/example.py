from actionpack.actions import Read
from actionpack.actions import Write
from os import environ as envvars
from sanka import sanka
from sanka import YaDead
from time import sleep
from time import perf_counter as stopwatch


datafile = 'datafile'
delay = int(envvars.get('CALL_DELAY_SECONDS', 0))
duration = int(envvars.get('RUN_DURATION_SECONDS', 10))


def write(tally: int):
    return Write(datafile, str(tally), append=True).perform(should_raise=True)


@sanka(callback=write, cumulative=False, only_callback_when_dead=False)
def some_function():
    pass


def main():
    start = stopwatch()
    elapsed = 0
    while True:
        try:
            some_function()
            sleep(delay)
            elapsed = round(stopwatch() - start, 3)
            if elapsed > duration:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            some_function(YaDead)
            result = Read(datafile).perform(should_raise=True)
            tallies = [int(tally) for tally in result.value.strip('\n').split('\n')]
            message = f'After {elapsed} seconds, "{some_function}" was called this many times:'
            print(message, sum(tallies))
            return


if __name__ == '__main__':
    main()

