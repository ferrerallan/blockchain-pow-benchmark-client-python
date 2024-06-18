import requests
import time
import curses
from block import Block
from block_info import BlockInfo
import hashlib

BLOCKCHAIN_SERVER = "http://localhost:3000"
miner_wallet = {"privateKey": "123456", "publicKey": "allankey"}

total_mined = 0


def get_next_block_info():
    response = requests.get(f"{BLOCKCHAIN_SERVER}/blocks/next")
    return response.json()


def mine_block(stdscr, block_info):
    global total_mined
    new_block = Block.from_block_info(block_info)

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(3, 0, f"Mining block #{block_info['index']}")
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    

    try:
        new_block.mine(block_info["difficulty"], miner_wallet["publicKey"])

        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(1, 0, "Block mined! Sending to blockchain...")
        stdscr.attroff(curses.color_pair(2))
        stdscr.refresh()
        

        requests.post(f"{BLOCKCHAIN_SERVER}/blocks/", json=new_block.to_dict())

        total_mined += 1

        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1, 0, f"Total mined: {total_mined}")
        stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()        
    except Exception as e:
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(3, 0, "****************")
        stdscr.addstr(4, 0, "*** YOU LOST ***")
        stdscr.addstr(5, 0, "****************")
        stdscr.attroff(curses.color_pair(4))
        stdscr.refresh()
        


def mine(stdscr):
    global total_mined

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    curses.curs_set(0)
    stdscr.nodelay(1)
    

    while True:
        try:
            stdscr.clear()
            stdscr.addstr(0, 0, f"### PYTHON ###")
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(1, 0, f"Total mined: {total_mined}")
            stdscr.attroff(curses.color_pair(1))

            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(2, 0, "Fetching next block info...")
            stdscr.attroff(curses.color_pair(1))

            stdscr.refresh()

            block_info = get_next_block_info()
            mine_block(stdscr, block_info)
        except:
            pass


if __name__ == "__main__":
    curses.wrapper(mine)
