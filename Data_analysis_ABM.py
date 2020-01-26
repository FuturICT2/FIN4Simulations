#!/usr/bin/env python
# coding: utf-8

import Fin4_ABM as model
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import pandas as pd

setup = model
#setup_name = "vs"

df = pd.DataFrame(setup.raw_result)

#t_step = setup.raw_result[len(setup.raw_result)-1]["timestep"]
#print(t_step)

#------------------- tokens/PAT -----------------------------
def calculate_total_tokens_per_pat(state):

    a = range(0, len(state['PATs']))
    distribution = dict((el, 0) for el in a)

    database = reconstruct_agent_database(state['agents'])
    for ag in database:
        for pat, number_of_tokens in ag['token_wallet'].items():
            print(pat, number_of_tokens)
            if pat != 'reputation':
                distribution[pat] += number_of_tokens

    #print ('distribution: ', distribution)
    return distribution

def histogram_of_activity_per_PAT(state):
    activity_hist = []

    for pat in state['PATs']:
        for i in range(0, pat['activity']):
            activity_hist.append(pat['name'])

    print ('activity_hist: ', activity_hist)
    return activity_hist

def histogram_of_token_per_PAT(state):
    pat_distribution = calculate_total_tokens_per_pat(state)
    histogram_list = []

    Keys = list(pat_distribution.keys())
    Values = list(pat_distribution.values())

    for v in range(0, len(Values)):
        for iter in range(0, Values[v]):
            histogram_list.append(Keys[v])

    #print("Keys: ", Keys)
    #print("Values: ", Values)
    #print("histog: ", histogram_list)

    return histogram_list

def reconstruct_agent_database(data):
    reconstruction = []

    for i in range(0, len(data)):
        if isinstance(data[i], dict):
            reconstruction.append(data[i])
        if isinstance(data[i], list):
            reconstruction.append(data[i][0])

    return reconstruction

def calculate_population_intention_array(state):

    intention_array = []
    database = reconstruct_agent_database(state['agents'])

    for ag in database:
        #print("-------------------------")
        #print(ag['claimer_PAT_intention'])
        intention_type = ag['claimer_PAT_intention']

        if intention_type == "noble":
            intention_array.append(1)
        if intention_type == "opportunistic":
            intention_array.append(2)
        if intention_type == "malicious":
            intention_array.append(3)

    #print(intention_array)

    return intention_array


def calculate_population_claim_style(state):

    style_array = []
    database = reconstruct_agent_database(state['agents'])

    for ag in database:
        #print("-------------------------")

        #print(ag['claimer'])
        clain_type = ag['claimer']

        if clain_type == "follower":
            style_array.append(1)
        if clain_type == "opportunistic":
            style_array.append(2)
        if clain_type == "cheater":
            style_array.append(3)
    #print(style_array)

    return style_array


#------------------population distribution --------------------------
if 1:
    n_bins = 3

    intent_array = calculate_population_intention_array(setup.raw_result[-1])
    intent = np.array(intent_array)
    print("intent: ", intent)

    claim_array = calculate_population_claim_style(setup.raw_result[-1])
    claimer = np.array(claim_array)
    print("claimer: ", claimer)

    fig, axs = pl.subplots(1, 2, sharey=True, tight_layout=True)
    fig.suptitle('Population distribution \n')
    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(intent, bins=n_bins)
    #axs[0].tick_params(axis=u'both', which=u'both', length=0)
    axs[0].set_title("Intention")
    axs[0].set(xlabel='noble      opportunistic     malicious')
    axs[1].hist(claimer, bins=n_bins)
    axs[1].set_title("Style")
    axs[1].set(xlabel='follower     opportunistic      cheater')

#fig, axs = plt.subplots(2, 2)
#axs[0, 0].plot(x, y)
#axs[0, 0].set_title('Axis [0,0]')
#axs[0, 1].plot(x, y, 'tab:orange')
#axs[0, 1].set_title('Axis [0,1]')
#axs[1, 0].plot(x, -y, 'tab:green')
#axs[1, 0].set_title('Axis [1,0]')
#axs[1, 1].plot(x, -y, 'tab:red')
#axs[1, 1].set_title('Axis [1,1]')

#for ax in axs.flat:
#    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    pl.savefig("Population_histograms" + ".png")
    pl.show()

#-------------------visualisation-------------------------------------
if 0:
    plt1 = pl.scatter(calculate_total_tokens_per_pat(setup.raw_result[-1]).keys(),
                      calculate_total_tokens_per_pat(setup.raw_result[-1]).values())

    pl.xticks(np.arange(0, 5, 1))
    pl.xlabel("PATs")
    pl.ylabel("nr. of tokens")
    pl.savefig("Tokens_per_PAT" + ".png")
    pl.show()

#-------------------PAT and activity distribution -------------------------------------
if 1:
    bins = np.linspace(0, 5, 10)

    pat_array = histogram_of_token_per_PAT(setup.raw_result[-1])
    activity_array = histogram_of_activity_per_PAT(setup.raw_result[-1])

    np_pat_array = np.array(pat_array)
    print("np_pat_array: ", np_pat_array)
    np_activity_array = np.array(activity_array)
    print("np_activity_array ", np_activity_array)

    plt.hist([np_pat_array, np_activity_array], bins, label=['tokens', 'activity'])
    plt.legend(loc='upper right')

    plt.title("PAT impact")
    plt.ylabel('PAT id')

    plt.savefig("PAT impact" + ".png")
    plt.show()

