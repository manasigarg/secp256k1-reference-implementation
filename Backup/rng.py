# ==================================================================================================
#                                          GLOBAL IMPORTS
# ==================================================================================================

import random
import time


# ==================================================================================================
#                                          LOCAL IMPORTS
# ==================================================================================================

from logger import *


# ==================================================================================================
#                                   RANDOM NUMBER GENERATOR (RNG)
# ==================================================================================================

class RNG:

    def __init__(self, limit):

        self.dir = r"C:\Users\Veda Sadhak\Desktop\ECC\rng.txt"
        self.limit = limit

    def generate(self):

        self.rng = random.randint(1,self.limit+1)
        logger.info("Random int: {}".format(self.rng))
        return self.rng

    def store(self):

        file = open(self.dir,'w')
        file.write(str(self.rng))

    def read(self):

        file = open(self.dir,'r')
        self.rng = int(file.read())

        logger.info("Random int: {}".format(self.rng))

        return self.rng






# ==================================================================================================
#                                            TEST CODE
# ==================================================================================================

if __name__ == '__main__':

    logger.setLevel(logging.INFO)

    rng = RNG(limit=1000000)

    # rng.generate()

    # rng.store()

    rng.read()