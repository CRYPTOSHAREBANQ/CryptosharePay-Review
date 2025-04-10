import requests
import json
import time
import os

class CryptoApis:
    def __init__(self, network = "mainnet"):
        self.BASE = "https://rest.cryptoapis.io/v2"
        self.querystring = {"limit":20,"offset":0}
        self.CALLBACK_BASE_URL = "https://cryptoapis.cryptosharepay.com/v1/webhooks"
        self.RECEIVE_CALLBACK_ON = 4
        self.HEADERS = {
        'Content-Type': "application/json",
        'X-API-Key': "72b793e11a85dd231d46fc3a3f73d274a834b475"
        }
        self.AVAILABLE_WALLET_IDS = {
            "mainnet": "61c3e127dcb1a20006034d02",
            "testnet": "628364e2c09ab200073d70c5",
            "mordor": "628364e2c09ab200073d70c5",
            "goerli": "628364e2c09ab200073d70c5",
            "nile": "628364e2c09ab200073d70c5",
        }

        self.WALLET_ID = self.AVAILABLE_WALLET_IDS[network]
        self.CALLBACK_SECRET_KEY = "CryptoApisCS"
        
    def get_confirmed_transactions(self, blockchain, network):

        if blockchain == "ethereum":
            if network == "mainnet":
                pass
            elif network == "ropsten":
                address = "0xc6981d668ca9e04735efba2cf93110fee883191a"

        url = self.BASE +  f"/blockchain-data/{blockchain}/{network}/addresses/{address}/transactions"
        request = requests.get(url, headers=self.HEADERS, params=self.querystring).json()

        return request["data"]["items"]

    def get_transaction_details_by_transactionid(self, blockchain, network, transactionid):
        url = self.BASE +  f"/blockchain-data/{blockchain}/{network}/transactions/{transactionid}"
        request = requests.get(url, headers=self.HEADERS).json()

        return request["data"]["item"]

    def get_token_transaction_details_by_transactionid(self, blockchain, network, transactionHash):
        url = self.BASE +  f" /blockchain-data/{blockchain}/{network}/transactions/{transactionHash}/tokens-transfers"
        request = requests.get(url, headers=self.HEADERS).json()

        return request["data"]["items"]

    def get_exchange_rate_by_symbols(self,fromSymbol, toSymbol):
        url = self.BASE +  f"/market-data/exchange-rates/by-symbols/{fromSymbol}/{toSymbol}?context=&calculationTimestamp={int(time.time())}"
        request = requests.get(url, headers=self.HEADERS).json()
        
        return request['data']["item"]
    
    def is_valid_address(self, blockchain, network, address):
        url = self.BASE +  f"/blockchain-tools/{blockchain}/{network}/addresses/validate"
        data ={
                "context": "",
                "data": {
                    "item": {
                        "address": f"{address}"
                    }
                }
            }

        request = requests.post(url, headers=self.HEADERS, json=data).json()
        
        return request["data"]["item"]["isValid"]
    
    def generate_deposit_address(self, blockchain, network, counter, address_type):
        url = self.BASE +  f"/wallet-as-a-service/wallets/{self.WALLET_ID}/{blockchain}/{network}/addresses"
        data = {
                "context": "",
                "data": {
                        "item": {
                                "label": f"cryptosharepay|{address_type}|{blockchain}|{network}|{counter}"
                                }
                }
            }
        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]["address"]

    def generate_coin_subscription(self, blockchain, network, address):
        url = self.BASE +  f"/blockchain-events/{blockchain}/{network}/subscriptions/address-coins-transactions-confirmed"
        data = {
                "context": "",
                "data": {
                    "item": {
                        "address": address,
                        "allowDuplicates": False,
                        "callbackSecretKey": self.CALLBACK_SECRET_KEY,
                        "callbackURL": f"{self.CALLBACK_BASE_URL}/cryptoapis/subscriptions/ConfirmedCoinTransactions/"
                    }
                }
            }
        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]
    
    def delete_blockchain_subscription(self, blockchain, network, reference_id):
        url = self.BASE +  f"/blockchain-events/{blockchain}/{network}/subscriptions/{reference_id}"

        request = requests.delete(url, headers=self.HEADERS).json()

        return request["data"]["item"]


    def generate_token_subscription(self, blockchain, network, address):
        url = self.BASE +  f"/blockchain-events/{blockchain}/{network}/subscriptions/address-tokens-transactions-confirmed"
        data = {
                "context": "",
                "data": {
                    "item": {
                        "address": address,
                        "allowDuplicates": False,
                        "callbackSecretKey": self.CALLBACK_SECRET_KEY,
                        "callbackUrl": f"{self.CALLBACK_BASE_URL}/cryptoapis/subscriptions/ConfirmedTokenTransactions/",
                        "receiveCallbackOn": self.RECEIVE_CALLBACK_ON
                    }
                }
            }
        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]
    
    def generate_coins_transaction_from_wallet(self, blockchain, network, address, amount, data = ""):
        url = self.BASE + f"/wallet-as-a-service/wallets/{self.WALLET_ID}/{blockchain}/{network}/transaction-requests"
        data = {
                "context": "",
                "data": {
                    "item": {
                        "callbackSecretKey": self.CALLBACK_SECRET_KEY,
                        # "callbackUrl": f"{self.CALLBACK_BASE_URL}/cryptoapis/callbacks/ConfirmationsCoinTransactions",
                        "feePriority": "standard",
                        "note": data,
                        "prepareStrategy": "optimize-size",
                        "recipients": [
                            {
                                "address": address,
                                "amount": amount
                            }
                        ]
                    }
                }
            }

        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]

    def generate_coins_transaction_from_address(self, blockchain, network, sending_address, recipient_address, amount):
        url = self.BASE + f"/wallet-as-a-service/wallets/{self.WALLET_ID}/{blockchain}/{network}/addresses/{sending_address}/transaction-requests"
        data = {
                "context": "",
                "data": {
                    "item": {
                        "amount": amount,
                        "callbackSecretKey": self.CALLBACK_SECRET_KEY,
                        # "callbackUrl": f"{self.CALLBACK_BASE_URL}/cryptoapis/callbacks/ConfirmationsCoinTransactions",
                        "feePriority": "standard",
                        "note": "",
                        "recipientAddress": recipient_address
                    }
                }
            }
        
        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]

    def generate_token_transaction_from_address(self, blockchain, network, sending_address, token_identifier, recipient_address, amount):
        url = self.BASE + f"/wallet-as-a-service/wallets/{self.WALLET_ID}/{blockchain}/{network}/addresses/{sending_address}/token-transaction-requests"
        data = {
            "context": "",
            "data": {
                "item": {
                    "amount": amount,
                    "callbackSecretKey": self.CALLBACK_SECRET_KEY,
                        # "callbackUrl": f"{self.CALLBACK_BASE_URL}/cryptoapis/callbacks/ConfirmationsTokenTransactions",
                    "feePriority": "standard",
                    "note": "",
                    "recipientAddress": recipient_address,
                    "tokenIdentifier": token_identifier
                }
            }
        }

        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]
    
    def generate_single_transaction_from_address_without_fee_priority(self, blockchain, network, sending_address, recipient_address, amount):
        url = self.BASE + f"/wallet-as-a-service/wallets/{self.WALLET_ID}/{blockchain}/{network}/addresses/{sending_address}/feeless-transaction-requests"

        data = {
                "context": "",
                "data": {
                    "item": {
                        "amount": amount,
                        "callbackSecretKey": self.CALLBACK_SECRET_KEY,
                        # "callbackUrl": f"{self.CALLBACK_BASE_URL}/cryptoapis/callbacks/ConfirmationsCoinTransactions",
                        "note": "",
                        "recipientAddress": recipient_address
                    }
                }
            }
        
        request = requests.post(url, headers=self.HEADERS, json=data).json()

        return request["data"]["item"]
        
                            
        

if __name__ == "__main__":
    # cryptoapis_client = CryptoApis()
    # data = cryptoapis_client.is_valid_address("ethereum", "mainnet", "0x392113e7C692108c16C2Bb642720D059066721D5")
    # print(type(data)
    # exchange_rate = cryptoapis_client.get_exchange_rate_by_symbols("ETH", "USD")["rate"]
    # print(exchange_rate)
    # crypto = CryptoApis()
    # data = crypto.get_transaction_details_by_transactionid("ethereum", "ropsten", "0x312af4de375e8851bb40e7cd3358286663e7809f279c3e2c2fb55d506cf41e95")

    # r = cryptoapis_client.generate_coins_transaction_from_wallet("litecoin", "mainnet","MNJmGBTC9CwtHUTgxkx3TKU8Nmw9qBq6Qd","0.002")
    # print(r)
    # print(data)

    pass
    # print("This is a module")
    # crypto = CryptoApis()
    # content = crypto.confirmed_transactions("ethereum", "ropsten")
    # print(content["data"]["items"])
    # # print(content["data"]["items"])
    # print(len(content["data"]["items"]))