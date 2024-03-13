# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

from web3 import Web3 as w3
import binascii
from hexbytes import HexBytes
from Crypto.Hash import keccak
import eth_utils # TODO: Need to implement checksum
from transaction import Unsigned_Transaction
from transaction import Signed_Transaction
import rlp

# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

from logger import *
from sig import Signature

# ==================================================================================================
#                                            ETHEREUM
# ==================================================================================================

class Ethereum:

    CHAIN_ID = 3

    def __init__(self):

        self.sig = Signature()

    def init_infura(self):

        try:

            logger.info("Connecting to Infura...")

            self.infura_source = "https://ropsten.infura.io/v3/9091fdcd87d24aa18b0aa3222a12f7de"
            # self.infura_source = "https://rinkeby.infura.io/v3/9091fdcd87d24aa18b0aa3222a12f7de"
            self.conn = w3(w3.HTTPProvider(self.infura_source))

            # logger.info("Latest block #: {}".format(self.conn.eth.getBlock('latest')['number']))

            logger.info("Infura connected")

        except Exception as e:

            raise("Unable to connect to Infura. {}".format(e))

    def gen_keys(self, load=True):

        self.sig.generate_key_pair(load=load)

        self.pri_key = self.sig.pri_key
        self.pub_key = self.sig.pub_key

    def gen_address(self):# pub_key_coord):

        # # TEST CASE
        # # PUBLIC KEY: 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        # # ETH ADDRESS: 0x7e5f4552091a69125d5dfcb7b8c2659029395bdf
        # pub_key = '0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8'

        pub_key_x_hex = hex(self.pub_key.x)
        pub_key_y_hex = hex(self.pub_key.y)

        pub_key = "{}{}".format(pub_key_x_hex,pub_key_y_hex.replace("0x",""))

        logger.info("pub_key: {}".format((pub_key)))
        pub_key_bytes = HexBytes(pub_key)
        logger.info("pub_key_bytes: {}".format(pub_key_bytes))
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(pub_key_bytes)
        pub_key_hash = keccak_hash.hexdigest()
        logger.info("pub_key_hash: {}".format(pub_key_hash))

        # Formatting the address
        eth_address = "-{}".format(pub_key_hash)[-40:]
        eth_address = eth_address.replace(r"\n", "")
        eth_address = eth_address.replace("-b'", "")
        eth_address = eth_address.replace("'", "")
        eth_address = "0x{}".format(eth_address)

        eth_address = eth_utils.to_checksum_address(eth_address)
        logger.info('generated address: {}'.format(eth_address))

        self.eth_address = eth_address

    def gen_acc(self, load=True):

        self.gen_keys(load=load)
        self.gen_address()

    def get_nonce(self, addr):

        return self.conn.eth.getTransactionCount(addr)

    def sign(self, msg):

        self.r,self.s = self.sig.sign(msg)

        logger.info("r: {}".format(self.r))
        logger.info("s: {}".format(self.s))

    def verify(self, msg, r, s):

        self.sig.verify(msg,r,s)

    def sign_tx(self, to, value):

        # Unit test
        # self.nonce = 0
        # self.gas_price = 234567897654321
        # self.gas = 2000000
        # self.to = HexBytes('0xF0109fC8DF283027b6285cc889F5aA624EaC1F55')
        # self.value = 1000000000
        # self.chain_id = 1
        # self.data = HexBytes('')
        # The above unit test should return the following
        # 'rawTransaction': HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428'),
        # 'hash': HexBytes('0x6893a6ee8df79b0f5d64a180cd1ef35d030f3e296a5361cf04d02ce720d32ec5'),
        # 'v': 37
        # 'r': 4487286261793418179817841024889747115779324305375823110249149479905075174044,
        # 's': 30785525769477805655994251009256770582792548537338581640010273753578382951464,

        # Generating transaction parameters
        self.nonce = self.get_nonce(addr=self.eth_address)
        self.gas_price = 50000000000#self.conn.eth.gasPrice #self.conn.toWei('10', 'gwei')# wei
        self.gas = 25000
        self.to = HexBytes(to)
        self.value = value
        self.data = HexBytes('0x48656c6c6f20426c6f636b636861696e21')  # Hello Blockchain!
        self.chain_id = self.CHAIN_ID
        self.v = self.chain_id
        self.r = 0
        self.s = 0

        logger.info("Nonce: {}".format(self.nonce))

        # Initializing unsigned transaction
        usign_tx = Unsigned_Transaction(nonce    = self.nonce,
                                        gasPrice = self.gas_price,
                                        gas      = self.gas,
                                        to       = self.to,
                                        value    = self.value,
                                        data     = self.data,
                                        v        = self.v,
                                        r        = self.r,
                                        s        = self.s)

        # Serializing via recursive length prefix
        usign_tx_serialized = rlp.encode(Unsigned_Transaction.serialize(usign_tx))
        logger.info("usign_tx_serialized: {}".format(usign_tx_serialized))


        # Hashing
        usign_tx_hash = keccak.new(digest_bits=256)
        usign_tx_hash.update(usign_tx_serialized)
        usign_tx_hash = usign_tx_hash.hexdigest()
        logger.info("usign_tx_hashed: {}".format(usign_tx_hash))
        # Internal: 6b7a2a28f4f08335bdc066d8e292bf42991d9ac7c343fd6c8aeb17936ac3b18d
        # External: 6b7a2a28f4f08335bdc066d8e292bf42991d9ac7c343fd6c8aeb17936ac3b18d

        # Signing
        self.r,self.s = self.sig.sign(msg=usign_tx_hash,byte_format=False)
        logger.info("tx sig r: {}".format(self.r))
        logger.info("tx sig s: {}".format(self.s))

        # Verifying
        self.sig.verify(msg=usign_tx_hash,r=self.r,s=self.s,byte_format=False)

    def verify_tx(self):

        logger.info("Verify tx placeholder")

    def send_tx(self):

        self.v = 42 #self.CHAIN_ID #TODO: Write function t calculate v from chain id

        # Initializing signed transaction
        sign_tx = Signed_Transaction(nonce    = self.nonce,
                                     gasPrice = self.gas_price,
                                     gas      = self.gas,
                                     to       = self.to,
                                     value    = self.value,
                                     data     = self.data,
                                     v        = self.v,
                                     r        = self.r,
                                     s        = self.s)

        # Serializing via recursive length prefix
        sign_tx_serialized = rlp.encode(Signed_Transaction.serialize(sign_tx))
        logger.info("sign_tx_serialized: {}".format(sign_tx_serialized))

        # Generating hex of serialized transaction
        raw_tx = '0x' + sign_tx_serialized.hex()
        logger.info("raw tx: {}".format(raw_tx))

        logger.info("Balance: {}".format(self.conn.eth.getBalance(self.eth_address)))  # wei
        logger.info("Gas Price: {}".format(type(self.gas_price)))
        logger.info("Gas * Gas_Price: {} gwei".format((self.gas * self.gas_price)))

        final_tx = self.conn.eth.sendRawTransaction(raw_tx)

        logger.info("Sent transaction: {}".format(final_tx))
        logger.info("Sent transaction hex: {}".format(binascii.hexlify(final_tx)))

# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    # Initialization
    logger.info("\n---------- Initialization ----------\n")
    eth = Ethereum()
    eth.init_infura()
    eth.gen_acc()

    # Sign check
    # logger.info("\n\n---------- Sign/Verify Test ----------\n")
    # msg = "Hello Blockchain!"
    # eth.sign(msg)
    # eth.verify(msg,eth.r,eth.s)

    # Sign transaction
    logger.info("\n\n---------- Sign Transaction ----------\n")
    eth.sign_tx(to='0x0aCA1E3f5e997295B3EF340f528E2B6a5970B6A9',
                value=10)

    logger.info("\n\n---------- Send Transaction ----------\n")
    eth.send_tx()
