from hashlib import sha256
import time
from datetime import datetime
# import asyncio
from multiprocessing import Process, Event, Manager


# RSA, DSA - asymmetric
# AES, RC4 - symmetric
# public locks, private unlocks


# SHA isn't encryption, it's a one-way hash function. AES (Advanced_Encryption_Standard) is a symmetric encryption standard. 
# one way function - to hack must use brute force
# SHA 256 is a cryptographic hash algorithm which does not use any key. So there is no question of symmetric/asymmetric.
# bitcoin mining: guess a nonce - one time usage number - so that the hash has n number of 0 digit
# first person guesses right gets the reward
# transaction -> string -> sha256 -> hash; protocol requires first n digits = 0
# transaction -> string + some nonce (guesswork) -> sha256 -> hash such that the hash's first n digits = 0
# guess right -> produce a new hash with first n 0 digits -> update new hash into the block
# 256bit, 64 bit in hexadecimal (16)
# why mining: forver changing the hashes = maintain security
# height: number of blocks
# The amount of the reward halves after the creation of every 210,000 blocks, or roughly every four years.
# The block reward is made of two components: the block subsidy and the transactions fees. The block subsidy consists of newly generated coins and represents the biggest part of a block reward.
# It's encoded in hexadecimal so the resulting string is easier to work with and debug. The actual hash is always in binary, but in most programming languages and libraries, the default output from a hash function is an ascii/utf8 string of hexadecimal encoded binary string.
# The difficulty is automatically adjusted based the amount of computational power on the network, or hashrate, to keep the time it takes to mine a block roughly stable at 10 minutes. The higher the hashrate, the higher the difficulty, and vice versa.
# output_hash_object = sha256((input.encode('utf-8')))
# output_utf8_encoded = sha256((input.encode('utf-8'))).hexdigest()
# output_ascii_encoded = sha256((input.encode('ascii'))).hexdigest()
# print(output_hash_object)
# print(output_ascii_encoded)
# print(output_utf8_encoded)



class BitcoinMiner:
    def __init__(self):
        pass
    def check_params_costs(self):    
        if not self.electricity_consumed:
            raise BaseException(f'\nelectricity_consumed is not specified!')
        if not self.electricity_price_per_hour:
            raise BaseException(f'\nelectricity_price_per_hour is not specified!')
    def check_params_nonce(self):    
        if not self.max_nonce:
            raise BaseException(f'\nblock_number is not specified!')
    def check_params_miner_input(self):
        if not self.block_number:
            raise BaseException(f'\nblock_number is not specified!')
        if not self.transactions:
            raise BaseException(f'\ntransactions is not specified!')
        if not self.previous_hash:
            raise BaseException(f'\nprevious_hash is not specified!')
        if not self.difficulty:
            raise BaseException(f'\ndifficulty is not specified!')
    def check_params_sha256_hash(self):    
        if not self.string:
            raise BaseException(f'\nstring (input) is not specified!')
    def miner_input(self, block_number, transactions, previous_hash, difficulty):
        self.block_number = block_number
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.check_params_miner_input()
    def set_max_nonce(self, max_nonce):
        self.max_nonce = max_nonce
        self.check_params_nonce()
        self.max_nonce = max_nonce
    def sha256_hash(self, string, encoding='utf-8'):
        self.string = string
        self.check_params_sha256_hash()
        hash = sha256((string.encode(encoding))).hexdigest()
        return hash
    def mine(self):
        print('\nmining starts')
        prefix = '0'*self.difficulty
        self.start_time = datetime.now()
        for nonce in range(0, self.max_nonce, 1):
            string = str(self.block_number) + str(self.transactions) + str(self.previous_hash) + str(nonce)
            new_hash = self.sha256_hash(string)
            if new_hash.startswith(prefix):
                end_time = datetime.now()
                print('end_time', type(end_time))
                time_taken = (end_time - self.start_time).total_seconds()
                self.time_taken = time_taken
                message = 'Success'
                print(f"\n{message}")
                results = {
                    'message': message,
                    'nonce': nonce,
                    'time_taken': self.time_taken,
                    'new_hash': new_hash
                }
                self.results = results
                print(self.results)
                return self.results 
        raise BaseException(f"Couldn't find nonce after trying {self.max_nonce} times!")
    def net_costs(self, electricity_consumed=1, electricity_price_per_hour=1):
        self.electricity_consumed = electricity_consumed
        self.electricity_price_per_hour = electricity_price_per_hour
        self.check_params_costs()
        costs = {
            # 'time_taken': self.time_taken,
            # 'time_taken': time_taken,
            # 'electricity_price': electricity_price,
        }
        return costs
    def set_bitcoin_details(self, price, block_reward):
        self.price = price
        self.block_reward = block_reward
    def net_profit(self):
        net_profit = {
            'bitcoin_price': self.bitcoin_price
        }
        return net_profit

        
    
if __name__ == '__main__':
    bm = BitcoinMiner()
    
    
    MAX_NONCE = 999999999
    bm.set_max_nonce(MAX_NONCE)
    
    
    # API zone
    block_number = 5
    transactions = """
    sender:EisenMann
    amount:4000
    unit:$
    to:FeuerMaedchen
    """
    previous_hash = '0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7'
    block_reward = 6.25
    price = 44108.40
    # end API zone
    
    
    bm.set_bitcoin_details(block_reward=block_reward, price=price)
    difficulty = 5
    bm.miner_input(block_number, transactions, previous_hash, difficulty)
    
    results = bm.mine()
    print(results)
    
    # manager = Manager()
    # return_dict = manager.dict()
    # event = Event()
    # p1 = Process(target=bm.timer, args=(event,))
    # p2 = Process(target=bm.mine, args=(event,))
    # p2.start()
    # p1.start()
    # if event.is_set():
    #     # p1.terminate()
    #     print('---')
    #     p1.join()
    









