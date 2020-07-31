# -*- coding: utf-8 -*-


import random

class Create_personas():

    def __init__(self):
        self.PAT_claimer = ['compliant', 'cheater', 'opportunistic'] #_design
        #self.PAT_claimer_intention = ['nobel', 'opportunistic', 'malicious'] this is a dimension equal to the creator intention
        self.PAT_voter = ['assessment', 'gain']
        self.PAT_verifier = ['True', 'False']
        self.PAT_creator_intention = ['noble', 'opportunistic', 'malicious']
        self.PAT_creator_design = ['careful', 'careless']

        self.persona = {}

        claimer = random.choice(self.PAT_claimer)
        voter = random.choice(self.PAT_voter)
        verifier = random.choice(self.PAT_verifier)
        creator_intention = random.choice(self.PAT_creator_intention)
        creator_design = random.choice(self.PAT_creator_design)

        self.persona.update({'claimer': claimer,
                             'claimer_PAT_intention': creator_intention,
                             'voter': voter,
                             'verifier': verifier,
                             'creator_intention': creator_intention,
                             'creator_design': creator_design})


    def Get_personas(self):
        return self.persona



