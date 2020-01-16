# -*- coding: utf-8 -*-

import pandas as pd
import random
import uuid
import matplotlib.pyplot as plt
import numpy as np
from cadCAD.configuration import Configuration
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import append_configs
from dask.distributed import Client
import Agent_factory as Af

if __name__ == '__main__':
    client = Client()

"""## Definitions"""
#Human agents
n_A = 4
#n_B = 1

#PAT agents
n_initial_pat = 2

initial_agents_prep = []
initial_agents = []
initial_PAT_ag = []

for i in range(n_A):
    creation = Af.Create_agents(i)
    individual_agent = creation.Get_initia_agents()
    initial_agents_prep.append(individual_agent)       # = creation.Get_initia_agents()

initial_agents = sum([ag for ag in initial_agents_prep], [])

PAT_agents = Af.Initial_PAT_agents(n_initial_pat)
initial_PAT_ag = PAT_agents.Get_initial_PAT_agents()

def get_update_name(variable_name):
    return "add_" + variable_name

PATS = "pats"
ADD_PATS = get_update_name(PATS)

#Human: Agent 1


#for i in range(n_A):
#    wallet = {"reputation": 0}
#    agent = {'uuid': uuid.uuid4(),
#             'type': 'A',
#             'money': 1,
#             'own_PATs': 0,
#             'token_wallet': wallet}
#    initial_agents.append(agent)

#Human: Agent 2

#for i in range(n_B):
#    wallet = {"reputation": 0}
#    agent = {'uuid': uuid.uuid4(),
#             'type': 'B',
#             'money': 20,
#             'own_PATs': 0,
#             'token_wallet': wallet}
#    initial_agents.append(agent)

#PAT: Agent 1

#for i in range(n_pat_A):
#    agent = {'uuid': uuid.uuid4(),
#             'robustness': 'high',
#             'ideal': 'nobel',
#             'popularity': 0}
#    initial_agents.append(agent)

#PAT: Agent 2

#for i in range(n_pat_B):
#    agent = {'uuid': uuid.uuid4(),
#             'robustness': 'low',
#             'ideal': 'nobel',
#             'popularity': 0}
#    initial_agents.append(agent)

"""### Initial conditions and parameters"""

initial_conditions = {
    'agents': initial_agents,
    'PATs': initial_PAT_ag,
    'initial nr. of PATs': n_initial_pat,
    'list_of_OPATs': []
}

simulation_parameters ={
    'T': range(2),
    'N': 1,
    'M': {}
}

"""### Policies"""

def random_claim_of_tokens(params, step, sL, s):
    agents = s['agents']
    initial_pats = s['PATs']
    pats_list = []
    gains = {}
    honest_agents_claiming = []
    cheater_agents_claiming = []

    for pt in initial_pats:
        pats_list.append(pt['name'])

    print("pat_list: ", pats_list)

#TODO

    for agent in agents:
        print("################################################")
        print('agent in token claiming: ', agent, "\n")

        try:
            if agent[0]['claimer'] == 'follower' or agent[0]['claimer'] == 'opportunistic':
                honest_agents_claiming.append(agent[0])
            else:
                cheater_agents_claiming.append(agent[0])
        except:
            if agent['claimer'] == 'follower' or agent['claimer'] == 'opportunistic':
                honest_agents_claiming.append(agent)
            else:
                cheater_agents_claiming.append(agent)

    print("---------------------------------------------------")
    print("honest_agents_claiming", honest_agents_claiming)

    for claimer_A in honest_agents_claiming:
        for pat in random.sample(pats_list, random.randint(0, len(pats_list))):
            print ("pat: ", pat)
            already_existing_PATs = claimer_A['token_wallet']
            if pat in already_existing_PATs:
                gains[pat] = already_existing_PATs[pat] + 1
            else:
                gains[pat] = 1
        claimer_A['token_wallet'].update(gains)

    #agent_B = [agent for agent in agents if agent['type'] == 'B']
    #B_riches = [person for person in agent_B if person['money'] >= sum_threshold]
    #for rich in B_riches:
    #    rich['money'] -= 1

    return {'update_agents': {'update': honest_agents_claiming}} #,
            #'update_agents': {'update': agent_B}} #,'update_agents': {'add': good_riches}}

def create_pat(params, step, sL, s):
    agents = s['agents']
    initial_PAT_nr = s['initial nr. of PATs']
    print("timestep", s['timestep'])

    if s['timestep'] > 0 and s['timestep'] % 3 == 0:
        creator = agents[-1][0]
        intention = creator['creator_intention']
        print("**********************************************************")
        print("intention: ", intention)
        design = creator['creator_design']
        print("**********************************************************")
        print("design", design)
        PAT_agents = Af.Crate_custom_PAT_agents(initial_PAT_nr, 1, intention, design)
        initial_PAT_ag = PAT_agents.Get_created_PAT_agents()
        print(initial_PAT_ag)
        return {'update_PATs': {'add': initial_PAT_ag}}

    else:
        print("I am passing PAT creation")
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
            uuid = PAT["uuid"]
        except:
            uuid = PAT[0]["uuid"]

        if uuid in removed_uuids:
            x.remove(PAT)
        if uuid in updated_uuids:
            updated_PAT = [PAT for PAT in updated_PATs if PAT["uuid"] == uuid]
            x.remove(PAT)
            x.append(updated_PAT)

    if added_PATs:
        for PAT in added_PATs:
            x.append(PAT)

    return (y, x)

def update_agents(params, step, sL, s, _input):
    y = 'agents'
    x = s['agents']

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
executor = Executor(exec_context, [config]) # Pass the configuration object inside an array
raw_result, tensor = executor.execute()


with open("output.txt", 'a') as result_file:
    result_file.write('\n' + str(raw_result) + '\n')
result_file.close()

#jsonObj = new Json(raw_result)
#jsonObj.prettyPrint