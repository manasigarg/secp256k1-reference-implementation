# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

import rlp
import rlp.sedes.big_endian_int as big_endian_int
import rlp.sedes.text as text
from rlp.sedes.binary import binary
from rlp.sedes.binary import Binary

# ==================================================================================================
#                                            TRANSACTION
# ==================================================================================================


class Unsigned_Transaction(rlp.Serializable):

    fields = \
    (
        ('nonce', big_endian_int),
        ('gasPrice', big_endian_int),
        ('gas', big_endian_int),
        ('to', Binary.fixed_length(20, allow_empty=True)),
        ('value', big_endian_int),
        ('data', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int)
    )

class Signed_Transaction(rlp.Serializable):

    fields = \
    (
        ('nonce', big_endian_int),
        ('gasPrice', big_endian_int),
        ('gas', big_endian_int),
        ('to', Binary.fixed_length(20, allow_empty=True)),
        ('value', big_endian_int),
        ('data', binary),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int)
    )



# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    tx = Transaction(nonce=1,
                     gasPrice=21000,
                     gas=100000,
                     to='0x0aCA1E3f5e997295B3EF340f528E2B6a5970B6A9',
                     value=0,
                     data='Hello Blockchain!',
                     chainId=3)

    print(rlp.encode(Transaction.serialize(tx)))
