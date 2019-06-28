from flask import Flask, jsonify, request
from blockchain.blockchain import Blockchain
from textwrap import dedent
from uuid import uuid4

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route("/")
@app.route("/home")
def home():
    return "Welcome to Guilherme's Blockchain"

@app.route('/mine', methods=['GET'])
def mine():
    """
        Here it is where the magic happens
        1. Calculate the proof of work
        2. Reward the miner (us) by adding a transaction granting us coin
        3. Forge the new Block by adding it to the chain
    """
    # we run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # we must receive a reward for finding the proof
    # the sender is "0" to signify that this node has mined a new coin
    block.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # forge the new Block by adding to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(message), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that the required fields ate in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to a Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200
