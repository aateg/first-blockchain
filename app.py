from flask import Flask, jsonify, request, abort
from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/blocks', methods = ['GET'])
def getBlocks():
    return jsonify(blockchain.getChain())

@app.route('/mineBlock', methods = ['POST'])
def createBlock():
    content = request.json
    if content:
        newBlock = blockchain.createNextBlock(content['data'])
        blockchain.addBlock(newBlock)
        return jsonify(newBlock.content)
    else:
        abort(400)

#@app.route('/peers')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
