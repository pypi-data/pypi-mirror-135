#!/usr/bin/python3.9 cli.py
import os

import click
from UNKnownDB.DB import LightDB

key_list = ['start']


def start(get):
    try:
        os.mkdir('./' + get)
    except FileExistsError:
        pass
    open('./' + get + '/__init__.py', 'w').close()
    with open('./' + get + '/manage.py', 'w') as manage:
        manage.write(
            """
from UsefulHelper.manager import *


# build()


if __name__ == '__main__':
    print('Debugging')
    main()
else:
    main()
        """
        )
    with open('./' + get + '/pack.py', 'w') as pack:
        pack.write("""
pass
        """)
    with LightDB.Data(path='./' + get + '/info', name=get) as db:
        print(db)
    return 'Done'


def stop():
    exit()


@click.command()
@click.option(
    "--things", prompt="UsefulHelper>>",
    help="NONE."
)
def main(things):
    split = things.split(' ')
    first = split[0]
    if first in key_list:
        info = eval(first)(split[1])
        print(info)
        things = None
        main(things)
    elif first == 'stop':
        stop()
    else:
        print(things + " isn't support")
        things = None
        main(things)


if __name__ == '__main__':
    print('Debugging')
    main()
else:
    main()
