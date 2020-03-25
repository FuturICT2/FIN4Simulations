from mesa import Agent, Model
import uuid
import random

class PATAgent(Agent):
    all_pats = []
    name = -1
    purpose = ['noble','opportunistic','malicious']
    design  = ["careful", "careless"]
    
    def __init__(self, model):
        self.unique_id = uuid.uuid4()
        super().__init__(self.unique_id, model)
        PATAgent.name = PATAgent.name + 1
        PATAgent.all_pats.append(self)        
        
    def random_init(self) :          
        self.attrib = {'uuid': self.unique_id,
                        'type': 'PAT',
                        'name': PATAgent.name,
                        'creator_ID': None,
                        'purpose': random.choice(PATAgent.purpose),
                        'design':  random.choice(PATAgent.design),
                        'activity': 0}
        print("------------random pat---------------")
        print(self.attrib )
        print("---------------------------")
        
    def custom_init(self, tk_purpose, tk_design, cr_id):
        self.attrib = {'uuid': self.unique_id,
                        'type': 'PAT',
                        'name': PATAgent.name,
                        'creator_ID': cr_id,
                        'purpose': tk_purpose,
                        'design': tk_design,
                        'activity': 0}
        print("-----------custom pat----------------")
        print(self.attrib)
        print("---------------------------")

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()
            
                    
if __name__ == "__main__":
    m = Model()        
    a = PATAgent(m)
    a.random_init()
    
    b = PATAgent(m)
    b.custom_init(1,2,3)