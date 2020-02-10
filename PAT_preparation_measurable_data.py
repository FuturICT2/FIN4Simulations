#!/usr/bin/env python
# coding: utf-8

import collections
import Fin4_ABM as model
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import pandas as pd
import random

setup = model
#setup_name = "vs"
df = pd.DataFrame(setup.raw_result)

#t_step = setup.raw_result[len(setup.raw_result)-1]["timestep"]
#print(t_step)

class Classifications(): 
    def __init__(self):
        self.state = setup.raw_result[-1]
        self.nr_PATs = len(self.state["PATs"])
        self.x_population_compliance = []
        self.y_token_design_robustness = []
        self.z_token_intent = []
        self.tokens = []
        self.action = []



#------------------- tokens/PAT -----------------------------
    def distribution_tokens_per_pat(self):

        a = range(0, len(self.state['PATs']))
        self.distribution = dict((el, 0) for el in a)

        database = self.reconstruct_agent_database(self.state['agents'])
        for ag in database:
            for pat, number_of_tokens in ag['token_wallet'].items():
                print(pat, number_of_tokens)
                if pat != 'reputation':
                    self.distribution[pat] += number_of_tokens

        print ('distribution: ', self.distribution)
        return self.distribution

    def tokens_per_pat(self):
        dist = self.distribution_tokens_per_pat()
        #sorted_dictionary = collections.OrderedDict(sorted(dist.items()))
        #print("sorted dictionary: ", sorted_dictionary)
        for key in dist:
            self.tokens.append(dist[key])

        print("nr tokens per pat: ", self.tokens)
        return self.tokens

    def action_per_pat(self):
        for p in self.state["PATs"]:
            self.action.append(p['activity'])
            
        print ("action: ", self.action)
        return self.action

    def design_per_pat(self):
        for p in self.state["PATs"]:
            if p["design"] == 'careful':
                self.y_token_design_robustness.append(0.5)
            else:
                self.y_token_design_robustness.append(-0.5)
                
        print("y_token_design_robustness: ", self.y_token_design_robustness)
        return self.y_token_design_robustness

    def purpose_per_pat(self):
        for p in self.state["PATs"]:
            if p["purpose"] == 'noble':
                self.z_token_intent.append(0.5)             # 1 - noble
            if p["purpose"] == 'opportunistic':
                self.z_token_intent.append(0)               # 0 - opportunistic
            if p["purpose"] == 'malicious':
                self.z_token_intent.append(-0.5)            # -1 - malicious
        print("z_token_intent: ", self.z_token_intent)
        return self.z_token_intent

    def population_compliance(self):
        print("nr PATs: ", self.nr_PATs) 
        for p in range(0, self.nr_PATs):
            self.x_population_compliance.append(random.uniform(-1, 1))
        print("x_population_compliance: ", self.x_population_compliance)
        return self.x_population_compliance

    def reconstruct_agent_database(self, data):
        reconstruction = []

        for i in range(0, len(data)):
            if isinstance(data[i], dict):
                reconstruction.append(data[i])
            if isinstance(data[i], list):
                reconstruction.append(data[i][0])

        return reconstruction

