from flask import Flask, request, jsonify
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

app = Flask(__name__)

# Sepolia testnet RPC URL (replace with your own if you have one)
SEPOLIA_RPC_URL = "https://rpc.sepolia.org"

# Contract address from the OpenSea link
CONTRACT_ADDRESS = "0x370c68fa87cdb35cfecdb519c958ede276230401"

# ABI for ERC721 token (minimal ABI for ownerOf function)
ABI = [
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

# Initialize contract
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

def verify_nft_ownership(wallet_address, nft_number):
    try:
        # Convert wallet_address to checksum address
        wallet_address = Web3.to_checksum_address(wallet_address)
        
        # Call the ownerOf function of the smart contract
        owner = contract.functions.ownerOf(int(nft_number)).call()
        
        # Compare the owner address with the provided wallet address
        return owner.lower() == wallet_address.lower()
    except Exception as e:
        print(f"Error verifying NFT ownership: {str(e)}")
        return False

def verify_signature(wallet_address, nft_number, signature):
    message = f"{wallet_address}{nft_number}"
    message_hash = encode_defunct(text=message)
    
    try:
        recovered_address = Account.recover_message(message_hash, signature=signature)
        return recovered_address.lower() == wallet_address.lower()
    except Exception as e:
        print(f"Error verifying signature: {str(e)}")
        return False

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    wallet_address = data.get('wallet_address')
    nft_number = data.get('nft_number')
    signature = data.get('signature')

    if not all([wallet_address, nft_number, signature]):
        return jsonify({"auth": "failed", "reason": "Missing wallet address, NFT number, or signature"}), 400

    # Verify signature
    if not verify_signature("0xE83cDeCfD1B75819787Bf1fAF7272D7ba057a0e1", nft_number, signature):
        return jsonify({"auth": "failed", "reason": "Invalid signature"}), 401

    # Verify NFT ownership
    if verify_nft_ownership(wallet_address, nft_number):
        return jsonify({"auth": "success"}), 200
    else:
        return jsonify({"auth": "failed", "reason": "NFT ownership not verified"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
