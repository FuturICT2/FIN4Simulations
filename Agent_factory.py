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
import Personality_permutations as Pp

class Create_agents():

    def __init__(self, number):
        self.initial_number = 1
        self.initial_agents = []

        personality = Pp.Create_personas()
        personality_mix = personality.Get_personas()

        general_atributes_A = { 'uuid': uuid.uuid4(),
                                'type': 'A',
                                'name': number,
                                'token_wallet': {"reputation": 0},
                                'activity': 0,
                                'own_PATs': 0}

        general_atributes_A.update(personality_mix)

        #general_atributes_B = {'uuid': uuid.uuid4(),
        #             'type': 'B',
        #             'money': 20,
        #             'own_PATs': 0,
        #             'token_wallet': {"reputation": 0}}

        #general_atributes_B.update(personality_mix)

        permutation = [general_atributes_A] #, general_atributes_B]

        for atribute in permutation:
            for i in range(self.initial_number):
                agent = atribute
                self.initial_agents.append(agent)


    def Get_initia_agents(self):
        return self.initial_agents

class Initial_PAT_agents():

    def __init__(self, number):
        self.PAT_nr = number
        self.initial_PAT_agents = []

        for i in range(self.PAT_nr):
            init_PAT = {'uuid': uuid.uuid4(),
                        'type': 'PAT',
                        'name': i,
                        'creator_ID': None,
                        'purpose': 'noble', #'opportunistic', #'noble',
                        'design': 'careful',
                        'activity': 0}
            self.initial_PAT_agents.append(init_PAT)

    def Get_initial_PAT_agents(self):
        return self.initial_PAT_agents

class Crate_custom_PAT_agents():

    def __init__(self, name, number, intention, design, cr_id):
        self.PAT_agents = []

        for i in range(number):
            PAT = { 'uuid': uuid.uuid4(),
                    'type': 'PAT',
                    'name': name + i,
                    'creator_ID': cr_id,
                    'purpose': intention,
                    'design': design,
                    'activity': 0}
            self.PAT_agents.append(PAT)

    def Get_created_PAT_agents(self):
        return self.PAT_agents