from web3 import Web3

INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

contract_address = "0xYourContractAddressHere"
contract_abi = [...]  # Extracted from DeVote_contract.zip

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def register_on_blockchain(user):
    tx = contract.functions.registerUser(user).build_transaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, "YourPrivateKey")
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

def record_vote(voter, candidate):
    tx = contract.functions.castVote(voter, candidate).build_transaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, "YourPrivateKey")
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)
