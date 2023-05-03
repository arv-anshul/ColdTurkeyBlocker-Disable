""" Disable or Enable all your Cold Turkey Blockers. """

import json
import os
import sqlite3

DB_PATH = r'/Library/Application Support/Cold Turkey/data-app.db'


def disableBlocker():
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)

        # Create a cursor object
        c = conn.cursor()

        # Execute the SQL statement to fetch settings data
        s = (c.execute("SELECT value FROM settings WHERE key = 'settings'")
             .fetchone()[0])
        data = json.loads(s)

        # Fetching the blockers
        blocks = data['blocks']

        # Checking your blockers
        print('\nChecking the blockers...')
        for i, blocker in enumerate(blocks):
            if blocker == 'Frozen Turkey':
                continue
            if blocks[blocker]['enabled'] == 'true':
                print(f'{i+1}. "{blocker}"  >>  Enabled.')
            else:
                print(f'{i+1}. "{blocker}"  >>  Disabled.')

        # Asking what to do.
        print('\n~~~~~~~>>>>>  "enable all" OR "disable all"  <<<<<~~~~~~~\n')
        inp = input('What the f*ck you want? ')

        for i, blocker in enumerate(blocks):
            # Enable all the blockers
            if inp == 'enable all':
                if blocks[blocker]['enabled'] == 'false':
                    if blocker != 'Frozen Turkey':
                        blocks[blocker]['enabled'] = 'true'
                        print(f'{i+1}. "{blocker}"  >>  Enabled.')

            # Disable all the blockers
            elif inp == 'disable all':
                if blocks[blocker]['enabled'] != 'false':
                    if blocker != 'Frozen Turkey':
                        blocks[blocker]['enabled'] = 'false'
                        print(f'{i+1}. "{blocker}"  >>  Disabled.')

            else:
                print('\n~~~~~~~>>>>>  Rerun the Program  <<<<<~~~~~~~\n')
                print('~~~~~~~>>>>>  "enable all" OR "disable all"  <<<<<~~~~~~~\n')
                break

        c.execute("""UPDATE settings set value = ? WHERE "key" = 'settings'""",
                  (json.dumps(data),))

    except Exception as e:
        print('\n~~~~~~~>>>>>  Take A Look on the Process  <<<<<~~~~~~~\n')
        print(e)

    finally:
        if conn:
            conn.commit()
            conn.close()
        os.system(r'killall Cold\ Turkey\ Blocker')
        os.system(r'open /Applications/Cold\ Turkey\ Blocker.app')


def main():
    if os.path.exists(DB_PATH):
        print("Data file found.\nLet's disable your blockers of Cold Turkey Blocker.")
        disableBlocker()

    else:
        print("Looks like Cold Turkey Blocker is not installed.\nIf it is installed then run it at least once.")


if __name__ == '__main__':
    main()
