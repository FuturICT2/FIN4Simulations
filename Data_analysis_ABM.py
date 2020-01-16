#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pylab as pl
#import Fin4_special_tokens as st
#import Fin4_special_tokens_comunity as stc
import Fin4_AB_simplemodel as model

setup = model
#setup_name = "vs"

df = pd.DataFrame(setup.raw_result)

#t_step = setup.raw_result[len(setup.raw_result)-1]["timestep"]
#print(t_step)

#------------------- tokens/PAT -----------------------------
def calculate_total_tokens_per_pat(state):
    a = range(0, 3) # PAT agents - pass automatically #TODO
    distribution = dict((el, 0) for el in a)
    print(state['agents'])
    for ag in state['agents']:
        print(ag['token_wallet'])
        for pat, number_of_tokens in ag['token_wallet'].items():
            print(pat, number_of_tokens)
            if pat != 'reputation':
                distribution[pat] += number_of_tokens
    return distribution

#print("total tokens per PAT", calculate_total_tokens_per_pat(setup.raw_result[-1]))

import numpy as np

#-------------------visualisation-------------------------------------
plt1 = pl.scatter(calculate_total_tokens_per_pat(setup.raw_result[-1]).keys(),
           calculate_total_tokens_per_pat(setup.raw_result[-1]).values())

pl.xticks(np.arange(0, 5, 1))
#pl.title(vs.name)
pl.xlabel("PATs")
pl.ylabel("nr. of tokens")
pl.savefig("First" + ".png")
pl.show()
