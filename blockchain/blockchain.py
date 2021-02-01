#!/usr/bin/python
# -*- coding: utf-8 -*-
from blockchain.block import Block
from time import time

BLOCK_GENERATION_INTERVAL = 10 # seconds
DIFFICULTY_ADJUSTMENT_INTERVAL = 10 # blocks

class Blockchain:

    def __init__(self):
        self.chain = [Block.genesisBlock()]

    def __len__(self) -> int:
        return len(self.chain)

    def createNextBlock(self, data: str) -> Block:
        latestBlock = self.getLatestBlock()
        difficulty = getDifficulty(self)
        nextTimestamp = time()
        newBlock = Block.findBlock(
            latestBlock.index + 1,
            data,
            latestBlock.hash,
            nextTimestamp,
            difficulty
        )
        return newBlock
    
    def getLatestBlock(self, step = -1) -> Block:
        return self.chain[step]

    def addBlock(self, newBlock: Block) -> None:
        latestBlock = self.getLatestBlock()
        if isValidNewBlock(latestBlock, newBlock):
            self.chain.append(newBlock)

    def getChain(self, withBlocks = False) -> list:
        if withBlocks:
            return self.chain
        return [block.content for block in self.chain]

# proof-of-work

def getAdjustedDifficulty(latestBlock: Block, blockchain: Blockchain) -> int:
    prevAdjustmentBlock = blockchain.getLatestBlock(-DIFFICULTY_ADJUSTMENT_INTERVAL)
    timeExpected = BLOCK_GENERATION_INTERVAL * DIFFICULTY_ADJUSTMENT_INTERVAL
    timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp
    if timeTaken < timeExpected / 2:
        return prevAdjustmentBlock.difficulty + 1
    elif timeTaken > timeExpected * 2:
        return prevAdjustmentBlock.difficulty - 1
    else:
        return prevAdjustmentBlock.difficulty

def getDifficulty(blockchain: Blockchain) -> int:
    latestBlock = blockchain.getLatestBlock()
    if latestBlock.index % DIFFICULTY_ADJUSTMENT_INTERVAL == 0 and \
        latestBlock.index != 0:
        return getAdjustedDifficulty(latestBlock, blockchain)
    return latestBlock.difficulty

# blockchain validations

def isValidChain(blockchain: Blockchain) -> bool:
    chain = blockchain.getChain(withBlocks = True)
    for i in range(1, len(chain)):
        previousBlock = chain[i - 1]
        currentBlock = chain[i]
        if not Blockchain.isValidNewBlock(previousBlock, currentBlock):
            return False
    return True 

def replaceChain(currentChain: Blockchain, newChain: Blockchain) -> Blockchain:
    if isValidChain(newChain) and len(newChain) > len(currentChain):
        return newChain
    return currentChain

def isValidNewBlock(previousBlock: Block, newBlock: Block) -> bool:
    if previousBlock.index + 1 != newBlock.index:
        #print("Invalid index Block")
        return False
    if previousBlock.hash != newBlock.previousHash:
        #print("Invalid previous hash")
        return False
    return True

def isValidTimestamp(newBlock: Block, previousBlock: Block) -> bool:
    return previousBlock.timestamp - 60 < newBlock.timestamp and \
        newBlock.timestamp - 60 < time()