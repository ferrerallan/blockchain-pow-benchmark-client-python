import hashlib
from block_info import BlockInfo
from validation import Validation
import time

class Block:
    def __init__(self, index=0, timestamp=None, data='', previous_hash='', nonce=0, miner=''):
        self.index = index
        self.timestamp = timestamp or int(time.time())
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.hash = self.get_hash()

    def get_hash(self):
        return hashlib.sha256(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}{self.miner}".encode()).hexdigest()

    def is_valid(self, previous_hash, previous_index, difficulty):
        if self.index < 0:
            return Validation(False, 'Index must be greater than 0')
        if self.previous_hash != previous_hash:
            return Validation(False, 'Incorrect previous hash')
        if previous_index != self.index - 1:
            return Validation(False, 'Incorrect previous index')
        if not self.nonce:
            return Validation(False, 'No mined')

        prefix = '0' * difficulty
        if not self.hash.startswith(prefix):
            return Validation(False, 'Incorrect hash')

        return Validation(True, '')

    def mine(self, difficulty, miner):
        self.miner = miner
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.get_hash()

    @classmethod
    def from_block_info(cls, block_info):
        return cls(
            index=block_info['index'],
            data=block_info['data'],
            previous_hash=block_info['previousHash']
        )

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previousHash': self.previous_hash,
            'nonce': self.nonce,
            'miner': self.miner,
            'hash': self.hash
        }
