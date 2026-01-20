import numpy as np
import itertools as it

get_norm = np.linalg.norm

SHARP_PROG = [4, 1,  5, 2, -1, 3,  0]
FLAT_PROG  = [0, 3, -1, 2, -2, 1, -3]

# CONSTANTS

ERROR_NUMBER_CLEFS ="""

-----------------------------------
           #clefs > #staffs
-----------------------------------

"""

CLEF_CONFIG = {"stroke_width":0,"stroke_opacity":0,"fill_opacity":1}

ALPHA_HEIGHT_G_CLEF = 0.5743147103253643
ALPHA_HEIGHT_F_CLEF = 1.2929782931297076
ALPHA_DOWN_G_CLEF = -57.673398215985706
ALPHA_DOWN_F_CLEF = -8.176884884446107
ALPHA_HEIGHT_STEM  = 0.41596100500179733
ALPHA_WIDTH_HALF_DOT = 3.0644336712207947
ALPHA_LENGTH_VECTOR_HALF_DOT = 1.018861808179335
UNIT_VECTOR_HALF_DOT = np.array([9.30474096e-01,3.66357690e-01,0])
ALPHA_LENGTH_STEM = 0.41596100500179733
ALPHA_LENGTH_VECTOR_STEM = 0.7190178571802391
UNIT_VECTOR_STEM = np.array([-3.26004674e-01,-9.45368157e-01,0])
ALPHA_STROKE_STEM = 0.11963381920678877
ALPHA_ADDITIONAL_LINE = 0.686664
ALPHA_STAFF_ADDITIONAL_LINE = 0.5437653622504716
ALPHA_BEMOL_SCALE = 1.4461098901098903
UNIT_VECTOR_BEMOL = np.array([-9.11981280e-01,4.10231818e-01,0])
ALPHA_BEMOL_LENGTH_VECTOR = 0.8946186251034574

KEY_DICTIONARY = {"C":0,
                  "C#":1,
                  "Db":1,
                  "D":2,
                  "D#":3,
                  "Eb":3,
                  "E":4,
                  "F":5,
                  "F#":6,
                  "Gb":6,
                  "G":7,
                  "G#":8,
                  "Ab":8,
                  "A":9,
                  "A#":10,
                  "Bb":10,
                  "B":11}

KEY_DICTIONARY_REG = {"C":0,
                      "D":1,
                      "E":2,
                      "F":3,
                      "G":4,
                      "A":5,
                      "B":6}

KEY_PROGRETION = ["C",
                  "C#",
                  "Db",
                  "D",
                  "D#",
                  "Eb",
                  "E",
                  "F",
                  "F#",
                  "Gb",
                  "G",
                  "G#",
                  "Ab",
                  "A",
                  "A#",
                  "Bb",
                  "B"]

KEY_PROGRETION_IN = {"C": 0,
                     "M": 1,
                     "D": 2,
                     "N": 3,
                     "E": 4,
                     "F": 5,
                     "O": 6,
                     "G": 7,
                     "P": 8,
                     "A": 9,
                     "Q": 10,
                     "B": 11}

KEY_PROGRETION_IN_REV = {0: "C",
                         1: "M",
                         2: "D",
                         3: "N",
                         4: "E",
                         5: "F",
                         6: "O",
                         7: "G",
                         8: "P",
                         9: "A",
                         10: "Q",
                         11: "B"}

KEY_PROGRETION_IT = it.cycle(KEY_PROGRETION)

KEYBOARD_PROPORTION = 1.32

