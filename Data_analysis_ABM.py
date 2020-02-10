#!/usr/bin/env python
# coding: utf-8

import Fin4_ABM as model
import matplotlib
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import pandas as pd

setup = model
#setup_name = "vs"

df = pd.DataFrame(setup.raw_result)

total_agents = len(setup.raw_result[-1]['agents'])
#print(t_step)

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    #total_agents = len(state['agents'])
    s = str(100 * y / total_agents)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


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
    activity_hist_noble = []
    activity_hist_opp = []
    activity_hist_malicious = []

    for pat in state['PATs']:
        for i in range(0, pat['activity']):
            if pat['purpose'] == 'noble':
                activity_hist_noble.append(pat['name'])
            if pat['purpose'] == 'opportunistic':
                activity_hist_opp.append(pat['name'])
            if pat['purpose'] == 'malicious':
                activity_hist_malicious.append(pat['name'])

    print ('activity_hist_noble: ', activity_hist_noble)
    return activity_hist_noble, activity_hist_opp, activity_hist_malicious

def histogram_of_token_per_PAT(state):

    pat_distribution = calculate_total_tokens_per_pat(state)

    histogram_list_noble = []
    histogram_list_opp = []
    histogram_list_malicious = []

    Keys = list(pat_distribution.keys())
    Values = list(pat_distribution.values())

    for v in range(0, len(Values)):
        for iter in range(0, Values[v]):
            if state['PATs'][v]['purpose'] == 'noble':
                histogram_list_noble.append(Keys[v])
            if state['PATs'][v]['purpose'] == 'opportunistic':
                histogram_list_opp.append(Keys[v])
            if state['PATs'][v]['purpose'] == 'malicious':
                histogram_list_malicious.append(Keys[v])

    #print("Keys: ", Keys)
    #print("Values: ", Values)
    #print("histog: ", histogram_list)

    return histogram_list_noble, histogram_list_opp, histogram_list_malicious

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

        if clain_type == "compliant":
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

    formatter = FuncFormatter(to_percent)

    fig, axs = pl.subplots(1, 2, sharey=True, tight_layout=True)
    #fig.suptitle('Population distribution \n')

    axs[0].hist(intent, bins=n_bins, alpha=0.7, histtype='bar', ec='black', rwidth=0.5)
    axs[0].set_xlim([1, 3])
    axs[0].set_title("Intention")
    axs[0].set_xticklabels([])
    axs[0].set(xlabel='noble      opportunistic     malicious')
    axs[1].hist(claimer, bins=n_bins, alpha=0.7, histtype='bar', ec='black', rwidth=0.5)
    axs[1].set_xlim([1, 3])
    axs[1].set_title("Compliance")
    axs[1].set_xticklabels([])
    axs[1].set(xlabel='compliant     opportunistic      cheater')
    fig.gca().yaxis.set_major_formatter(formatter)

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
    bins = np.linspace(0, len(setup.raw_result[-1]["PATs"]) - 1, 2 * len(setup.raw_result[-1]["PATs"]))

    pat_array_noble, pat_array_opp, pat_array_malicious = histogram_of_token_per_PAT(setup.raw_result[-1])
    activity_array_noble, activity_array_opp, activity_array_malicious = histogram_of_activity_per_PAT(setup.raw_result[-1])

    np_pat_array_noble = np.array(pat_array_noble)
    np_pat_array_opp = np.array(pat_array_opp)
    np_pat_array_malicious = np.array(pat_array_malicious)
    print("np_pat_array_noble: ", np_pat_array_noble)
    print("np_pat_array_opp: ", np_pat_array_opp)
    print("np_pat_array_malicious: ", np_pat_array_malicious)

    np_activity_array_noble = np.array(activity_array_noble)
    np_activity_array_opp = np.array(activity_array_opp)
    np_activity_array_malicious = np.array(activity_array_malicious)
    print("np_activity_array_noble: ", np_activity_array_noble)
    print("np_activity_array_opp: ", np_activity_array_opp)
    print("np_activity_array_malicious: ", np_activity_array_malicious)

    plt.hist([np_pat_array_noble, np_activity_array_noble], bins, label=['noble tokens', 'noble activity'], color=["green", "lightgreen"])
    plt.hist([np_pat_array_opp, np_activity_array_opp], bins, label=["opp tokens", "opp activity"], color=["orange", "yellow"])
    plt.hist([np_pat_array_malicious, np_activity_array_malicious], bins, label=['malicious tokens', 'malicious activity'], color=["red", "pink"])

    plt.legend(loc='upper right')

    plt.title("PAT impact")
    plt.xlabel('PAT id')

    plt.savefig("PAT impact" + ".png")
    plt.show()

