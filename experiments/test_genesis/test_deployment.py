from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
 
# Connect to an Ethereum node
infura_url = 'http://10.160.0.71:8545'
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if the connection is successful
if web3.isConnected():
    print('Connected to Ethereum node')
else:
    print('Connection failed')

# Contract address and ABI
contract_address = '0x4e59b44847b379578588920cA78FbF26c0B4956C'
with open('./test/test2/LinkToken.abi', 'r') as f:
    contract_abi = json.load(f)

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Check if the contract is deployed by checking its code at the address
contract_code = web3.eth.getCode(contract_address).hex()
print(f'Contract code at address {contract_address}: {contract_code}')

if contract_code != b'0x' and contract_code != '0x' and contract_code != b' ':
    print('Contract is deployed successfully')
else:
    print('Contract is not deployed')
    
## Check total supply
total_supply = contract.functions.totalSupply().call()
print(f'Total supply: {total_supply}')

# my_account = web3.eth.account.from_key('20aec3a7207fcda31bdef03001d9caf89179954879e595d9a190d6ac8204e498')
# amount_to_send = web3.toWei(1, 'ether')
# contract_address = web3.toChecksumAddress(contract_address)
# # Send ETH to the contract
# transaction = {
#     'from': my_account.address,
#     'to': contract_address,
#     'value': amount_to_send,
#     'gas': 2000000,
#     'gasPrice': web3.toWei('50', 'gwei'),
#     'nonce': web3.eth.getTransactionCount(my_account.address),
#     'chainId': 1337
# }
# signed_txn = web3.eth.account.signTransaction(transaction, my_account.key)
# tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
# print(f'Transaction sent, waiting for receipt...')
# receipt = web3.eth.waitForTransactionReceipt(tx_hash)
# print(f'Transaction receipt: {receipt}')

# user_address = my_account.address
# print(f'User address: {user_address}')
# balance = contract.functions.balanceOf(user_address).call()
# print(f'Link token balance of the user: {balance}')




#
# def increase_counter(value, from_address, private_key):
#     # Build the transaction
#     nonce = web3.eth.getTransactionCount(from_address)
#     transaction = contract.functions.increaseCounter(value).buildTransaction({
#         'from': from_address,
#         'nonce': nonce,
#         'gas': 2000000,
#         'gasPrice': web3.toWei('50', 'gwei')
#     })

#    
#     signed_txn = web3.eth.account.signTransaction(transaction, private_key)

#    
#     txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
#     return txn_hash

# # View the counter
# def view_counter():
#     counter_value = contract.functions.sayHello().call()
#     return counter_value


# from_address = '0x2e2e3a61daC1A2056d9304F79C168cD16aAa88e9'
# private_key = '20aec3a7207fcda31bdef03001d9caf89179954879e595d9a190d6ac8204e498'
# value_to_increase = 10


# txn_hash = increase_counter(value_to_increase, from_address, private_key)
# print(f'Transaction hash: {txn_hash.hex()}')


# receipt = web3.eth.waitForTransactionReceipt(txn_hash)
# print('Transaction receipt:', receipt)

# current_counter = view_counter()
# print(f'Current counter value: {current_counter}')
