"""
Only For Mac
------------
Disable or Enable all your Cold Turkey Blockers in one command.
"""

import json
import os
import random
import sqlite3
import string

DB_PATH = r'/Library/Application Support/Cold Turkey/data-app.db'
LENGTH = 50


def blocker_summary(blocks: dict):
    print('\n' + '*'*LENGTH)

    for blocker in blocks:
        if blocker == 'Frozen Turkey':
            continue
        if blocks[blocker]['enabled'] == 'true':
            print(f'Block Enabled:  {blocker}')
        else:
            print(f'Block Disabled: {blocker}')

    print('*'*LENGTH + '\n')


def random_string(length: int) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def cli_decorate(
        *args: str, center_txt: str | None = None, sep='\n', length: int = 50,
):
    if center_txt:
        print('\n' + f' {center_txt} '.center(length, '*'))
    else:
        print('\n' + '*'*length)

    print(f"{sep.join(args)}")
    print('*'*length + '\n')


def get_user_input() -> bool | None:
    while True:
        txt = random_string(4)
        print(txt)
        inp = input(
            'To disable all blocker enter above string '
            'by following the indexing of [::-2]\n'
        )

        # Exit the loop and process
        if inp == '123ABC':
            return None

        if len(txt)//2 == len(inp) and inp == txt[::-2]:
            return True
        else:
            cli_decorate(
                f'Answer is {txt[::-2]}',
                'Exit with "123ABC"',
                center_txt='Enter Again'
            )


def operation_on_blocks(blocks: dict, what: bool | None) -> dict | None:
    if what is None:
        print('Exiting the process.')
        return None

    one_disabled = False
    for blocker in blocks:
        # Ignore Frozen Turkey block
        if blocker == 'Frozen Turkey':
            continue

        # Return if one block disabled
        if one_disabled:
            return blocks

        if blocks[blocker]['enabled'] == 'true':
            blocks[blocker]['enabled'] = 'false'
            cli_decorate(f'Now Disable: {blocker}'.center(LENGTH))
            one_disabled = True


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()

        s = (c.execute("SELECT value FROM settings WHERE key = 'settings'")
             .fetchone()[0])
        data = json.loads(s)
        blocks = data['blocks']

        # Display blocks summary
        blocker_summary(blocks)
        user_input = get_user_input()

        blocks = operation_on_blocks(blocks, user_input)

        # Replace the blocks if modified
        if blocks is not None:
            data['blocks'] = blocks

        c.execute("""UPDATE settings set value = ? WHERE "key" = 'settings'""",
                  (json.dumps(data),))
    except Exception as e:
        print('Error:\n   ', e)
    else:
        conn.commit()
    finally:
        conn.close()
        os.system(r'killall Cold\ Turkey\ Blocker')


if __name__ == '__main__':
    main()
