import numpy as np
from .constants import *
from manim import SVGMobject

ALPHAS = {
    "stem":{
        "width":16.00022333751562,
        "heigth":0.36623730881369715,
        "unit_vector":np.array([ 3.15654676e-01,  9.48874136e-01, 0]),
        "vector_length":0.6966207908464077,
    },
    "flat":{
        'width': 1.9047617482816004, 
        'vector_length': 1.1188564231965377, 
        'unit_vector': np.array([-9.58018319e-01,  2.86706992e-01, 0]), 
    },
    "sharp":{
        'width': 1.7777778087577196,
        'vector_length': 1.103450979190911,
        'unit_vector': np.array([-1.0000000e+00,  1.9213607e-16, 0]),
    },
    "natural":{
        'width': 2.5396825839395993,
        'vector_length': 1.1034510746729629,
        'unit_vector': np.array([-1.00000000e+00, -8.65304011e-08, 0]),
    },
    'ks_sharp': {
        'width': 0.5862067384103721,
        'dy': 4,
    },
    'ks_flat': {
        'width': 0.5923343343242982,
        'dy': 9,
    },
    "clefs":{
        "c":{
            "symbol": SVGMobject("manimusic/music_symbols/c_clef",**CLEF_CONFIG)[5],
            "height":1,
        },
        "g":{
            "symbol": SVGMobject("manimusic/music_symbols/g_clef",**CLEF_CONFIG)[5],
            "height":ALPHA_HEIGHT_G_CLEF,
            "down":ALPHA_DOWN_G_CLEF,
        },
        "f":{
            "symbol": SVGMobject("manimusic/music_symbols/f_clef",**CLEF_CONFIG)[5],
            "height":ALPHA_HEIGHT_F_CLEF,
            "down":ALPHA_DOWN_F_CLEF,
        },
    }
}

