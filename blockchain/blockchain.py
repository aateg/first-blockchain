import hashlib
import json
from time import time

class Blockchain(object):
    """
        This is our Blockchain class, it is responsible for managing the chain.
        It will store transactions and have some helper methods for adding new
        blocks to the chain.
    """
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the genesis Block - Block with no predecessors
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
            Creates a new Block and adds it to the Chain
            Arguments:
                - proof: <int> The proof given by the Proof of Work algorithm
                - previous_hash: (Optional) <str> Hash of previous Block
            Return:
                - <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
            Adds a new transaction to the list of transactions
            Arguments:
                - sender: <str> Address of the sender
                - recipient: <str> Address of the recipient
                - amount: <int> Amount
            Return:
                - <int> Index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
            Simple Proof of Work Algorithm:
                - Find a number p' such that hash(pp') contains leading
                4 zeroes, where p is the previous p'
                - p is the previous proof, and p' is the new proof
            Arguments:
                - last_proof: <int>
            Return:
                - <int>
        """
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
            Validates the Proof: does hash(last_proof, proof)
            contain 4 leading zeroes?

            Arguments:
                - last_proof: <int> Previous Proof
                - proof: <int> Current Proof
            Return:
                - <bool> True if correct, Fals if not
        """
        guess = f'{last_proof}{proof}'.encode() # converts to unicode
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'


    @staticmethod
    def hash(block):
        """
            Creates a SHA-256 hash of a Block
            Arguments:
                - block: <dict> Block
            Return:
                - <str> hash
        """

        # we must make sure that the dict is ordered
        # or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # returns the last Block in the Chain
        return self.chain[-1]
