# utils block functions

def hashMatchesDifficulty(hash: str, difficulty: int) -> bool:
    hashBinary = hexToBin(hash)
    if hashBinary[:4] == '0' * difficulty:
        return True
    return False

def hexToBin(hash: str) -> str:
    length = len(hash) * 4
    hexInt = int(hash, 16)
    hexBin = bin(hexInt)
    paddedBin = hexBin[2:].zfill(length)
    return paddedBin