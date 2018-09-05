from pathlib import Path
import numpy as np
import constants

SCORE_LIST = constants.SCORE_LIST 
OUTPUT_DIR = constants.OUTPUT_DIR

for SCORE in SCORE_LIST:
  SCORE_NAME = Path(SCORE).stem
  PATH = "{}/{}.npy".format(OUTPUT_DIR, SCORE_NAME)
  nnn = np.load(PATH)
  for i, nn in enumerate(nnn):
    if np.sum(nn[:4]) == 0:
      print('{} top note has no duration value'.format(PATH))
 