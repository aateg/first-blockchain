from blockchain.block import Block, isValidNewBlock

class Blockchain:

    def __init__(self):
        self.__chain = [Block.genesisBlock()]

    def __len__(self) -> int:
        return len(self.__chain)

    def createNextBlock(self, data: str) -> Block:
        latestBlock = self.__getLatestBlock()
        return Block(
            index = latestBlock.index + 1,
            data =  data,
            previousHash = latestBlock.hash
        )
    
    def __getLatestBlock(self) -> Block:
        return self.__chain[-1]

    def addBlock(self, newBlock: Block) -> None:
        latestBlock = self.__getLatestBlock()
        if isValidNewBlock(latestBlock, newBlock):
            self.__chain.append(newBlock)

    def getChain(self, withBlocks = False) -> list:
        if withBlocks:
            return self.__chain
        return [block.content for block in self.__chain]

# utils blockchain functions

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

