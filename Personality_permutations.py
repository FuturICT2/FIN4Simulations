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

class Create_personas():

    def __init__(self):
        self.PAT_claimer = ['follower', 'cheater', 'opportunistic'] #_design
        #self.PAT_claimer_intention = ['nobel', 'opportunistic', 'malicious'] this is a dimension equal to the creator intention
        self.PAT_voter = ['assessment', 'gain']
        self.PAT_creator_intention = ['noble', 'opportunistic', 'malicious']
        self.PAT_creator_design = ['careful', 'careless']

        self.persona = {}

        claimer = random.choice(self.PAT_claimer)
        voter = random.choice(self.PAT_voter)
        creator_intention = random.choice(self.PAT_creator_intention)
        creator_design = random.choice(self.PAT_creator_design)

        self.persona.update({'claimer': claimer,
                             'claimer_PAT_intention': creator_intention,
                             'voter': voter,
                             'creator_intention': creator_intention,
                             'creator_design': creator_design})




    def Get_personas(self):
        return self.persona



