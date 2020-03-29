# -*- coding: utf-8 -*-
import pandas as pd
import random
import uuid
import matplotlib.pyplot as plt
import numpy as np
import sys
from cadCAD.configuration import Configuration
from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import append_configs
from dask.distributed import Client
import Agent_factory as Af
import configparser
import copy

class Error(Exception):
   """Base class for other exceptions"""
   pass


class UndefinedCustomAgents(Error):
   """Raised when custom agents chosen set without definition """
   pass


"""### Read config file"""

config = configparser.ConfigParser()
config.read('config.ini')


"""### Helper functions """

def get_update_name(variable_name):
    return "add_" + variable_name

def create_agents_with_attributes(last_nr, set, claim_intent, claim_compliance, voter_drive, creator_intent, creator_design):
    for i in range(last_nr, last_nr + set):
        creation = Af.Create_custom_agents(i, claim_intent, claim_compliance, voter_drive, creator_intent, creator_design)
        individual_agent = creation.getCustomAgent()
        initial_agents.append(individual_agent)
    return initial_agents

def claim(agent, PAT_list, policy, s):
    gains = {}
    if len(PAT_list) >= 1:
        for pat in random.sample(PAT_list, random.randint(0, len(PAT_list))):
            already_existing_PATs = agent['token_wallet']
            if pat in already_existing_PATs:
                gains[pat] = already_existing_PATs[pat] + 1
            else:
                gains[pat] = 1

            #add activity according to claimer choice
            if policy == 'add_activity':
                agent['activity'] = agent['activity'] + 1
                add_activity_to_coresponding_PAT(pat, s)
            if policy == 'random_activity':
                flag = random.choice([True, False])
                if flag:
                    agent['activity'] = agent['activity'] + 1
                    add_activity_to_coresponding_PAT(pat, s)
                else:
                    pass
            if policy == 'no_activity':
                pass

    agent['token_wallet'].update(gains)

def add_activity_to_coresponding_PAT(pat_id, s):
    all_PATs = s['PATs']

    for PAT in all_PATs:
        if PAT['name'] == pat_id:
            PAT['activity'] = PAT['activity'] + 1


"""## Definitions"""
initial_agents_prep = []
initial_agents = []
initial_PAT_ag = []

# Human agents

if config['human agents']['agents_with_random_attributes'] == 'True':
    #print("------------RANDOM agent attributes --------------- ")
    for i in range(0, int(config['human agents']['number'])):
        creation = Af.Create_agents(i)
        individual_agent = creation.Get_initial_agents()
        initial_agents_prep.append(individual_agent)

    initial_agents = sum([ag for ag in initial_agents_prep], [])



if config['human agents']['custom_agents'] == 'True':
    #print("------------CUSTOM agent attributes --------------- ")


    number_of_sets = int(config['human agents']['number_of_custom_agent_sets'])
    last_id = 0

    for s in range(1, number_of_sets + 1):

            #name of variables to be read frpm the init file:           extract this into a separate method
            number_of_agents = "set" + str(s) + "_number_of_agents"
            claim_intent = "set" + str(s) + "_claim_intent"
            claim_compliance = "set" + str(s) + "_claim_compliance"
            voter_drive = "set" + str(s) + "_voter_drive"
            creator_intent = "set" + str(s) + "_creator_intent"
            creator_design = "set" + str(s) + "_creator_design"


            set = int(config['human agents'][number_of_agents])
            cl_intent = config['human agents'][claim_intent]
            cl_compliance = config['human agents'][claim_compliance]
            v_drive = config['human agents'][voter_drive]
            cr_intent = config['human agents'][creator_intent]
            cr_design = config['human agents'][creator_design]

            #except UndefinedCustomAgents:
            #    print("Undefined attributes for custom human agents!")

            create_agents_with_attributes(last_id, set, cl_intent, cl_compliance, v_drive, cr_intent,
                                          cr_design)
            last_id += set
           
# PAT agents

creation_frequency = int(config['PAT agents']['frequency_PAT_creation'])  # in time-steps

if config['PAT agents']['human_agent_PAT_creation'] == 'True':
    PAT_agents = Af.Initial_PAT_agents(int(config['PAT agents']['number_initial_pats']))
    initial_PAT_ag = PAT_agents.Get_initial_PAT_agents()

if config['PAT agents']['custom_bootstrapping'] == 'True':

    number_of_PAT_sets = int(config['PAT agents']['number_of_custom_PAT_sets'])
    #print("number_of_PAT_sets: ", number_of_PAT_sets)

    for p in range(1, number_of_PAT_sets + 1):
        # name of variables to be read frpm the init file:           extract this into a separate method
        id = "set" + str(p) + "_init_id"
        number_of_PATs = "set" + str(p) + "_number_of_PATs"
        token_purpose = "set" + str(p) + "_token_purpose"
        token_design = "set" + str(p) + "_token_design"
        creator_id = "set" + str(p) + "_creator_id"

        init_id = int(config['PAT agents'][id])
        nr_PATs = int(config['PAT agents'][number_of_PATs])
        tk_purpose = config['PAT agents'][token_purpose]
        tk_design = config['PAT agents'][token_design]
        cr_id = int(config['PAT agents'][creator_id])

        PAT_agents = Af.Create_custom_PAT_agents(init_id, nr_PATs, tk_purpose, tk_design, cr_id)
        PATs = PAT_agents.Get_created_PAT_agents()

        initial_PAT_ag = initial_PAT_ag + PATs

PATS = "pats"
ADD_PATS = get_update_name(PATS)


"""### Initial conditions and parameters"""

initial_conditions = {
    'agents': initial_agents,
    'PATs': initial_PAT_ag,
    'initial nr. of PATs': int(config['PAT agents']['number_initial_pats']),
    'list_of_OPATs': []
}

simulation_parameters ={
    'T': range(int(config['general']['time_steps'])),
    'N': 1,
    'M': {}
}

"""### Policies"""

def random_claim_of_tokens(params, step, sL, s):

    pats_design = ("careful", "careless")
    pats_purpose = ('noble','opportunistic','malicious')
    agent_compliance = ('compliant', 'opportunistic', 'cheater')
    to_update = []
    
    # pats_all [ design ] [ purpose ]
    pats_all = dict([(y, dict([ (x,[]) for x in pats_purpose] )) for y in pats_design])
    agents_all = dict([ (x,[]) for x in agent_compliance] )
        
    #distinguish between careful and careless PATs
    for pt in s['PATs']:
        pats_all[pt['design']][pt['purpose']].append(pt['name'])

    # distinguish between compliant, opportunists and cheaters
    for agent in s['agents']:
        try:
            agents_all[agent[0]['claimer']].append(agent[0])
        except:
            agents_all[agent['claimer']].append(agent)
                        
    for compliant in agents_all['compliant']:
        pats = pats_all['careful'][compliant['claimer_PAT_intention']] + pats_all['careless'][compliant['claimer_PAT_intention']]
        if pats :
            to_update.append(compliant)
            claim(compliant, pats, 'add_activity', s)
        
    for opp in agents_all["opportunistic"]:
        opp_do = pats_all['careful'][opp['claimer_PAT_intention']]
        opp_rand = pats_all['careless'][opp['claimer_PAT_intention']]                                    
        claim(opp, opp_do, 'add_activity', s)
        claim(opp, opp_rand, 'random_activity', s)
        if opp_do + opp_rand : 
            to_update.append(opp)

    for ch in agents_all["cheater"]:
        pats = pats_all['careless'][ch['claimer_PAT_intention']]
        if pats :
            claim(ch, pats, 'no_activity', s)
            to_update.append(ch)

    return {'update_agents': {'update': to_update}}

def create_pat(params, step, sL, s):
    agents = s['agents']
    initial_PAT_nr = len(s['PATs'])
    print("PAT timestep", s['timestep'])
    #creation_frequency = config['PAT agents']['number_initial_pats'] #config['PAT agents']['frequency_PAT_creation']
    #print('creation frequency: ', creation_frequency)

    if s['timestep'] > 0 and s['timestep'] % creation_frequency == 0:
        creator_name = random.randrange(len(agents))
        #print ("creator_name: ", creator_name)
        for ag in agents:
            try:
                if ag['name'] == creator_name:
                    creator = ag
            except:
                if ag[0]['name'] == creator_name:
                    creator = ag[0]

        #print("creator: ", creator)
        intention = creator['creator_intention']
        creator_ID = creator['name']
        design = creator['creator_design']
        PAT_agents = Af.Create_custom_PAT_agents(initial_PAT_nr, 1, intention, design, creator_ID)
        initial_PAT_ag = PAT_agents.Get_created_PAT_agents()
        #print(initial_PAT_ag)
        return {'update_PATs': {'add': initial_PAT_ag}}

    else:
        #print("I am passing PAT creation")
        return {'update_PATs': {'add': None}}


"""### State update functions (variables)"""

def update_PATs(params, step, sL, s, _input):
    y = 'PATs'
    x = s['PATs']

    data = _input.get("update_PATs", {})
    removed_PATs = data.get("remove", [])
    removed_uuids = [PAT['uuid'] for PAT in removed_PATs]
    updated_PATs = data.get("update", [])

    updated_uuids = [PAT["uuid"] for PAT in updated_PATs]
    added_PATs = data.get("add", [])

    for PAT in x:
        try:
            theuuid = PAT["uuid"]
        except:
            theuuid = PAT[0]["uuid"]

        if uuid in removed_uuids:
            x.remove(PAT)
        if theuuid in updated_uuids:
            updated_PAT = [PAT for PAT in updated_PATs if PAT["uuid"] == theuuid]
            x.remove(PAT)
            x.append(updated_PAT)

    if added_PATs:
        for PAT in added_PATs:
            x.append(PAT)

    return (y, x)

def update_agents(params, step, sL, s, _input):
    y = 'agents'
    x = copy.copy(s['agents'])

    data = _input.get("update_agents", {})
    removed_agents = data.get("remove", [])
    removed_uuids = [agent['uuid'] for agent in removed_agents]
    updated_agents = data.get("update", [])

    updated_uuids = [agent["uuid"] for agent in updated_agents]
    added_agents = data.get("add", [])

    for agent in x:
        try:
            uuid = agent["uuid"]
        except:
            uuid = agent[0]["uuid"]

        if uuid in removed_uuids:
            x.remove(agent)
        if uuid in updated_uuids:
            updated_agent = [agent for agent in updated_agents if agent["uuid"] == uuid]
            x.remove(agent)
            x.append(updated_agent)

    for agent in added_agents:
        x.append(agent)

    return (y, x)


"""### State update blocks"""
if config['PAT agents']['custom_bootstrapping'] == 'True':
    partial_state_update_blocks = [
        {
            'policies': {'random_claim_of_tokens': random_claim_of_tokens},
            'variables': {'agents': update_agents},

        }
    ]
else:
    partial_state_update_blocks = [
        {
        'policies': {'random_claim_of_tokens': random_claim_of_tokens},
        'variables': {'agents': update_agents},

        },
        {
        'policies': {'create_pat': create_pat},
        'variables': {'PATs': update_PATs}

        }
    ]

"""### Configuration and Execution"""


config = Configuration(initial_state=initial_conditions, #dict containing variable names and initial values
                       partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
                       sim_config=simulation_parameters #dict containing simulation parameters
                      )

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
exec_mode = ExecutionMode()
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config])
raw_result, tensor = executor.execute()


with open("output.json", 'a') as result_file:
    result_file.write('\n' + str(raw_result) + '\n')
result_file.close()
