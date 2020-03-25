# -*- coding: utf-8 -*-
from mesa import Agent, Model
import uuid
import Personality_permutations as Pp
from mesaPATAgent   import PATAgent
import random

class HumanAgent(Agent):
    name = -1
    compliance = ['compliant', 'opportunistic', 'cheater']
    
    def __init__(self, model):
        self.unique_id = uuid.uuid4()
        super().__init__(self.unique_id, model)
        HumanAgent.name = HumanAgent.name + 1        
        
    def random_init(self) :          
        personality = Pp.Create_personas()
        personality_mix = personality.Get_personas()
        general_attributes_A = { 'uuid': self.unique_id,
                                'type': 'A',
                                'name': self.name,
                                'token_wallet': {"reputation": 0},
                                'activity': 0,
                                'own_PATs': 0}
        general_attributes_A.update(personality_mix)
        general_attributes_A.update(personality_mix)
        self.attrib = general_attributes_A
        # print("------------random agent---------------")
        # print(general_attributes_A)
        # print("---------------------------")


        
    def custom_init(self, claimer_intention, compliance, voter, creator_intention, creator_design):
        general_atr_A = {'uuid': self.unique_id,
                                'type': 'A',
                                'name': self.name,
                                'token_wallet': {"reputation": 0},
                                'activity': 0,
                                'own_PATs': 0}
        custom_persona= {'claimer': compliance,
                             'claimer_PAT_intention': claimer_intention,
                             'voter': voter,
                             'creator_intention': creator_intention,
                             'creator_design': creator_design}

        self.attrib = (lambda d: d.update(custom_persona) or d)(general_atr_A)
        # print("-----------custom agent----------------")
        # print(self.attrib)
        # print("---------------------------")

    def claim(self):
        # here I claim just one token. Should I instead claim as many as possible?
        pats = PATAgent.pats
        if self.attrib['compliance'] == 'compliant' :
            pat = random.choice(pats)
            act = True
        elif self.attrib['compliance'] == 'opportunistic' :
            pat = random.choice(pats)
            if pat.attrib['design'] == 'careful' :
                act = True
            else :
                act = random.choice([True, False])
        elif self.attrib['compliance'] == 'cheater' :
            pat = random.choice(filter(lambda x: x.attrib['design'] == 'careless', pats) )
            act = False
        if act :
            self.attrib['activity'] = self.attrib['activity'] + 1
            pat.attrib['activity'] =  pat.attrib['activity'] + 1
        self.attrib['token_wallet'] = self.attrib.get('token_wallet', 0) + 1
        
    def create_pat(self):
        #if s['timestep'] > 0 and s['timestep'] % creation_frequency == 0:
        #creator_name = random.randrange(len(agents))
        #print ("creator_name: ", creator_name)
        p = PATAgent()
        p.custom_init(self.attrib['creator_intention'], 
                      self.attrib['creator_design'], 
                      self.attrib['name'])
        
        def step(self):
            self.claim()

        
if __name__ == "__main__":
    m = Model()        
    a = HumanAgent(m)
    a.random_init()
    
    b = HumanAgent(m)
    b.custom_init(1,2,3,4,5)