import os

SCORE_ROOT = "../chopin_piano_score_dataset/scores_xml"
SCORE_LIST = [dirName[2] for dirName in os.walk(SCORE_ROOT)][0]
OUTPUT_DIR = "../complete"
