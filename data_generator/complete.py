import sys
import re
import itertools
import numpy as np
from pathlib import Path
sys.path.append("..") # Adds higher directory to python modules path.
import os
from musicXML_parser import MusicXMLDocument
import utils
import constants

class OnsetGroup:
  def __init__(self):
    self.children = []

  def add_onset(self, child):
    self.children.append(child)

class Onset:
  def __init__(self, measure_position, time_position, notes):
    self.measure_position =  measure_position
    self.time_position = time_position
    self.notes = notes
    self.directions = []
    self.p_group = 0 #Boolean yes = 1 / no = 0
    self.f_group = 0 #Boolean yes = 1 / no = 0
    self.top_note_type = {
      "half": 0,
      "quarter":0,
      "eighth":0,
      "16th": 0,
      "dots": 0,
    }
    self.ritardando = 0
    self.cresc = 0
    self.decresc = 0
    self.pedal = 0
    self.first_beat = 0
    self.accent = 0
    self.staccato = 0

  def _append_directions(self, direction):
    self.directions.append(direction)

  def _set_top_note(self):
    NOTE_TYPES = ["half", "quarter", "eighth", "16th", "dot"]
    if len(self.notes) > 0:
      pitch_numbers = [x.pitch[1] for x in self.notes]
      max_pitch_index = pitch_numbers.index(max(pitch_numbers))
      top_note = [(x.note_duration._type, x.note_duration.dots) for x in self.notes][max_pitch_index]
      if top_note[0] in NOTE_TYPES:
        self.top_note_type[top_note[0]] = 1
      if top_note[1] == 1:
        self.top_note_type["dots"] = 1
      if top_note[0] == "32nd" or top_note[0] == "64th" or top_note[0] == "256th" or top_note[0] == "1024th":
        self.top_note_type["16th"] = 1
      if top_note[0] == "whole" or top_note[0] == "breve":
        self.top_note_type["half"] = 1

  def _set_dynamic_type(self):
    """
      check dynamic type and return binary
    """
    P_TYPES = ["ppp", "pp", "p", "mp"]
    F_TYPES = ["mf", "f", "ff", "fff", "sf"]

    if len(self.directions) > 0:
      for direction in self.directions:
        if direction[0]["type"] == "dynamic":
          dynamic_type = direction[0]["content"]
          if dynamic_type in P_TYPES:
            self.p_group = 1
          if dynamic_type in F_TYPES:
            self.f_group = 1
  
  def _set_ritardando(self):
    if len(self.directions) > 0:
      for direction in self.directions:
        if direction[0]["type"] == "words":
            words = str(direction[0]["content"])
            # check rit string in words
            if re.match(r'^rit', words):
              self.ritardando = 1

  def _set_cresc(self):
    if len(self.directions) > 0:
      for direction in self.directions:
        if direction[0]["type"] == "crescendo" and direction[0]["content"] == "start":
          self.cresc = 1
        if direction[0]["type"] == "words":
          words = str(direction[0]["content"])
          if re.match(r'^cresc', words):
            self.cresc = 1

  def _set_decresc(self):
    if len(self.directions) > 0:
      for direction in self.directions:
        if direction[0]["type"] == "diminuendo" and direction[0]["content"] == "start":
          self.decresc = 1
        if direction[0]["type"] == "words":
          words = str(direction[0]["content"])
          if re.match(r'^dim', words):
            self.decresc = 1
  
  def _set_pedal(self):
    if len(self.directions) > 0:
      for direction in self.directions:
        if direction[0]["type"] == "pedal" and direction[0]["content"] == "start":
          self.pedal = 1
  
  def _set_first_beat(self):
    if self.measure_position == 1:
      self.first_beat = 1

  def _set_accent(self):
    accents = [x.note_notations.is_accent for x in self.notes]
    if True in accents:
      self.accent = 1
  
  def _set_staccato(self):
    staccato = [x.note_notations.is_staccato for x in self.notes]
    if True in staccato:
      self.staccato = 1
    
    if len(self.directions) > 0:
      for direction in self.directions:
        if direction[0]["type"] == "words":
          words = str(direction[0]["content"])
          if re.match(r'^stacc', words):
            self.staccato = 1

class OnsetCreator:
  def __init__(self, xml_path, output_path):
    self.xml_path = xml_path
    self.output_path = output_path
    self.readXML()

  def readXML(self):
    print("{} Start to read : {} {}".format("="*5, self.xml_path, "="*5))
    XMLDocument = MusicXMLDocument(self.xml_path)
    parts = XMLDocument.parts[0]
    measure_num = len(parts.measures)

    # init onset_group
    onset_group = OnsetGroup()

    for i in range(measure_num):
      # Read all notes in a measure
      measure =  parts.measures[i]

      # Remove rest notes, tied stop notes, grace nots
      notes = delete_notes(measure.notes)

      # Sort notes by time position
      sorted_notes = sorted(notes, key=lambda note: note.note_duration.time_position)
      
      # Get direcitons in a measure
      measure_directions = [[dict({"time_position": utils.convert_float(x.time_position)}, **x.type)] for x in measure.directions]

      # Grouping Notes
      note_on_set_group = {utils.convert_float(k): [
        v for v in sorted_notes if v.note_duration.time_position == k] 
        for k, val in itertools.groupby(sorted_notes, lambda x: x.note_duration.time_position
      )}
            
      for key in note_on_set_group:
        measure_position = i+1
        onset = Onset(measure_position, key, note_on_set_group[key])
        if len(measure_directions) > 0:
          for direction in measure_directions:
            direction_time_position = direction[0]["time_position"]
            if direction_time_position == onset.time_position:
                onset._append_directions(direction)
        
        # set Dynamic type p or f
        onset._set_dynamic_type()

        # set top note type
        onset._set_top_note()

        # set ritardando
        onset._set_ritardando()

        # set _set_wedge
        onset._set_decresc()
        onset._set_cresc()

        onset._set_pedal()

        # set _first beat
        onset._set_first_beat()
        onset._set_accent()
        onset._set_staccato()

        # append new onset to onset_group class
        onset_group.add_onset(onset)

    # print results
    print("Total Onsets: ", len(onset_group.children))

    # convert to numpy array
    all_onsets = np.array([[*x.top_note_type.values(), x.p_group, x.f_group,
    x.ritardando, x.cresc, x.decresc, x.pedal, x.first_beat, x.accent, x.staccato] for x in onset_group.children])

    save_to_npy(self.output_path, all_onsets)
    
# TODO : make file save module
def save_to_npy(path, data):
  if data is not None:
    try:
      print("{} Save to : {} {}".format("="*5, path, "="*5))
      np.save(path, data)
    except:
      print("Failed to save file.")

def delete_notes(notes):
  # Remove rest notes, tied stop notes, grace not
  """
  TODO
  condition = [
    "is_rest"
    "tied_stop",
    "is_grace_note"
  ]
  """
  removed_notes = [x for x in notes 
    if x.is_rest == False and
    x.note_notations.tied_stop == False and 
    x.note_duration.is_grace_note == False
  ]
  return removed_notes

ROOT = constants.SCORE_ROOT
SCORES = constants.SCORE_LIST 
OUTPUT_DIR = constants.OUTPUT_DIR

def main():
  for SCORE in SCORES:
    XML_PATH = "{}/{}".format(ROOT, SCORE)
    SCORE_NAME = Path(SCORE).stem
    OUTPUT_PATH = "{}/{}.npy".format(OUTPUT_DIR, SCORE_NAME)
    OnsetCreator(XML_PATH, OUTPUT_PATH)

if __name__ == "__main__":
  os.system("rm -rf {}".format(OUTPUT_DIR))
  os.mkdir(OUTPUT_DIR)
  main()
