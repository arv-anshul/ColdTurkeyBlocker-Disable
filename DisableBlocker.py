import sqlite3
import json
import os
import time

DB_PATH = '/Library/Application Support/Cold Turkey/data-app.db'


def disableBlocker():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        s = c.execute(
            "SELECT value FROM settings WHERE key = 'settings'").fetchone()[0]
        data = json.loads(s)

        # fetching the blockers
        blocks = data['blocks']

        # checking the blockers
        print('\nChecking the blockers...')
        time.sleep(3)
        for i, blocker in enumerate(blocks):
            if blocks[blocker]['enabled'] == 'true':
                print(f'{i}. "{blocker}"  >>  Enabled.')
            else:
                print(f'{i}. "{blocker}"  >>  Disabled.')

        # asking what to do.
        print('\n~~~~~~~>>>>>  "enable all" OR "disable all"  <<<<<~~~~~~~\n')
        inp = input('What the f*ck you want? ')

        # disabling the blockers
        for i, blocker in enumerate(blocks):
            if inp == 'enable all':
                print('\nEnabling the blocker.')
                blocks[blocker]['enabled'] = 'true'
                print(f'>> Now, "{blocker}" is Enabled.')
                c.execute(
                    """UPDATE settings set value = ? WHERE "key" = 'settings'""", (json.dumps(data),))
                conn.commit()

            elif inp == 'disable all':
                print('\nDisabling the blocker.')
                blocks[blocker]['enabled'] = 'false'
                print(f'>> Now, "{blocker}" is Disabled.')
                c.execute(
                    """UPDATE settings set value = ? WHERE "key" = 'settings'""", (json.dumps(data),))
                conn.commit()

            else:
                print('\n~~~~~~~>>>>>  Rerun the Program  <<<<<~~~~~~~\n')
                print('~~~~~~~>>>>>  "enable all" OR "disable all"  <<<<<~~~~~~~\n')
                break

    except Exception as e:
        print('\n~~~~~~~>>>>>  Take A Look on the Process  <<<<<~~~~~~~\n')
        print(e)

    finally:
        if conn:
            conn.close()
            os.system('killall Cold\ Turkey\ Blocker')


def main():
    if os.path.exists(DB_PATH):
        print("Data file found.\nLet's disable your blockers of Cold Turkey Blocker.")
        disableBlocker()

    else:
        print("Looks like Cold Turkey Blocker is not installed.\nIf it is installed then run it at least once.")


if __name__ == '__main__':
    main()
