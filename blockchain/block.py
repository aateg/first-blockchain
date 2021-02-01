#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations
from hashlib import sha256
from blockchain.utils import hashMatchesDifficulty

class Block:

    def __init__(self, index: int, data: str,  timestamp: float,
        previousHash: str, blockHash: str, difficulty: int, nonce: int):

        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp 
        self.data = data
        self.hash = blockHash
        self.difficulty = difficulty
        self.nonce = nonce

        self.content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "previousHash": self.previousHash,
            "difficulty": self.difficulty,
            "nonce": self.nonce
        }

    def __str__(self):
        return f"Block({self.content})"

    @staticmethod
    def calculateHash(index: int, previousHash: str, timestamp: float, 
        data: str, difficulty: int, nonce: int) -> str:
        msg = str(index) + str(timestamp) + data + \
            previousHash + str(difficulty) + str(nonce)
            
        return sha256(msg.encode('utf-8')).hexdigest()

    @classmethod
    def genesisBlock(cls) -> Block:
        return cls(
            index = 0, 
            blockHash = '91a73664bc84c0baa1fc75ea6e4aa6d1d20c5df664c724e3159aefc2e1186627',
            previousHash = '', 
            timestamp = 1465154705, 
            data = 'my genesis block!!', 
            difficulty = 0, 
            nonce = 0)

    @classmethod
    def findBlock(cls, index: int, data: str, previousHash: str, 
        timestamp: float, difficulty: int) -> Block:
        """Find hash for block given difficulty, iterate over nonce
        to obtain the hash that matches difficulty 
        Args:
            - Parameters to create a single block
        Returns:
            - Block
        """
        nonce = 0
        while True:
            hashOfNonce = Block.calculateHash(index, previousHash, 
                timestamp, data, difficulty, nonce)
            if hashMatchesDifficulty(hashOfNonce, difficulty):
                return cls(index, data, timestamp, previousHash, hashOfNonce, difficulty, nonce)
            nonce += 1
