import pandas as pd
import numpy as np


def flatten(lst):
    """Given a list, possibly nested to any level, return it flattened."""
    new_lst = []
    for item in lst:
        if isinstance(item, list):
            new_lst.extend(flatten(item))
        else:
            new_lst.append(item)
    return new_lst


def tryget_int(s, default):
    try:
        return int(s)
    except ValueError:
        return default


# color palettes taken from colorbrewer2.org
uni_directional_palettes_dict = \
    {
        4: ['#ffffff', '#fee0d2','#fc9272','#de2d26'],
        5: ['#ffffff', '#fee5d9','#fcae91','#fb6a4a','#cb181d'],
        6: ['#ffffff', '#fee5d9','#fcae91','#fb6a4a','#de2d26','#a50f15'],
        7: ['#ffffff', '#fee5d9','#fcbba1','#fc9272','#fb6a4a','#de2d26','#a50f15'],
        8: ['#ffffff', '#fee5d9','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#99000d'],
    }
bi_directional_palettes_dict = \
    {
        3: ['#ef8a62','#f7f7f7','#67a9cf'],
        4: ['#ca0020','#f4a582','#92c5de','#0571b0'],
        5: ['#ca0020','#f4a582','#f7f7f7','#92c5de','#0571b0'],
        6: ['#b2182b','#ef8a62','#fddbc7','#d1e5f0','#67a9cf','#2166ac'],
        7: ['#b2182b','#ef8a62','#fddbc7','#f7f7f7','#d1e5f0','#67a9cf','#2166ac'],
        8: ['#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'],
        9: ['#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac'],
       10: ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061'],
       11: ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061']
    }
regions_dict = \
{
    'west': ['AZ', 'CA', 'CO', 'ID', 'MT', 'NM', 'NV', 'OR', 'UT', 'WA', 'WY'],
    'south': ['AL', 'AR', 'DC', 'DE', 'FL', 'GA','KY', 'LA', 'MD', 'MS', 'NC', 'OK', 'SC', 'TN', 'TX', 'VA', 'WV'],
    'midwest':  ['IA', 'IL', 'IN', 'KS', 'MI', 'MN', 'MO', 'ND', 'NE', 'OH', 'SD', 'WI'],
    'northeast': ['CT', 'MA', 'ME', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT'],
}


def get_palette(ncat, bidi):
    '''
    input: ncat: integer, number of colors requested
    input: bidi: bool, return diverging colors if True or diverging colors otherwise
    output: returns list of color codes
    Get a palette with ncat number of colors that is either diverging (if bidi==True)
    or sequential (if bidi==False)
    '''
    if bidi:
        return bi_directional_palettes_dict[ncat]
    else:
        return uni_directional_palettes_dict[ncat]


def get_states_for_region(region_name):
    default_region_name = 'west'
    if region_name.lower() in regions_dict.keys():
        return regions_dict[region_name.lower()]
    else:
        return default_region_name
