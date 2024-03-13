from web3 import Web3 as w3
import logging
import binascii
from hexbytes import HexBytes

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger.setLevel(logging.CRITICAL)

if __name__ == '__main__':

    infura_source = "https://ropsten.infura.io/v3/9091fdcd87d24aa18b0aa3222a12f7de"
    conn = w3(w3.HTTPProvider(infura_source))

    # transaction = {
    #     # Note that the address must be in checksum format:
    #     'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
    #     'value': 1000000000,
    #     'gas': 2000000,
    #     'gasPrice': 234567897654321,
    #     'nonce': 0,
    #     'chainId': 1
    # }

    # 'rawTransaction': HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'),
    # 'hash': HexBytes('0x6893a6ee8df79b0f5d64a180cd1ef35d030f3e296a5361cf04d02ce720d32ec5'),
    # 'v': 37
    # 'r': 4487286261793418179817841024889747115779324305375823110249149479905075174044,
    # 's': 30785525769477805655994251009256770582792548537338581640010273753578382951464,

    transaction = {
        'nonce' : conn.eth.getTransactionCount('0x2c7536E3605D9C16a7a3D7b1898e529396a65c23') + 1,
        'gasPrice' : 21000,#conn.eth.gasPrice,
        'gas' : 1000,
        'to' : '0x0aCA1E3f5e997295B3EF340f528E2B6a5970B6A9',
        'value' : 1000,
        'data' : HexBytes('0x48656c6c6f20426c6f636b636861696e21'),  # Hello Blockchain!
        'chainId' : 4
    }


    key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
    signed = conn.eth.account.signTransaction(transaction, key)

    print(binascii.hexlify(signed.rawTransaction))
    print(binascii.hexlify(signed.hash))
    print(signed.r)
    print(signed.s)
    print(signed.v)
