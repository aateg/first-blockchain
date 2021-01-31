#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import sha256

class Block:

    def __init__(self, index: int, data: str, previousHash: str):

        self.index = index
        self.previousHash = previousHash
        self.timestamp = str(datetime.now())
        self.data = data
        self.hash = self.generateHash()
        self.content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "previousHash": self.previousHash
        }

    def __str__(self):
        return f"Block({self.content})"

    def generateHash(self):
        msg = str(self.index) + self.timestamp + \
            self.data + self.previousHash
            
        return sha256(msg.encode('utf-8')).hexdigest()

    @staticmethod
    def genesisBlock():
        return Block(
            index = 0, 
            data = "I'm the genesis Block",
            previousHash = "0")

# utils block functions
def isValidNewBlock(previousBlock: Block, newBlock: Block) -> bool:
    if previousBlock.index + 1 != newBlock.index:
        #print("Invalid index Block")
        return False
    if previousBlock.hash != newBlock.previousHash:
        #print("Invalid previous hash")
        return False
    return True


if __name__ == '__main__':
    b0 = Block.genesisBlock()
    print(b0)
    print(type(b0.hash))
    