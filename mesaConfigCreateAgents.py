from mesa import Model
import configparser
from mesaHumanAgent import HumanAgent
from mesaPATAgent   import PATAgent


def configAgents(m: Model) :
    # Create human agents
    config = configparser.ConfigParser()
    config.read('config.ini')

    if config['human agents']['agents_with_random_attributes'] == 'True':
        print("------------RANDOM agent attributes --------------- ")
        for i in range(0, int(config['human agents']['number'])):
            a = HumanAgent(m)
            a.random_init()
            m.schedule.add(a)            
        
    if config['human agents']['custom_agents'] == 'True':
        print("------------CUSTOM agent attributes --------------- ")
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
                for i in range(last_id, last_id + set):
                    a = HumanAgent(m)
                    a.custom_init(cl_intent, cl_compliance, v_drive, cr_intent,
                                  cr_design)
                    m.schedule.add(a) 
                last_id += set
                
                
# now create PAT agents
# to go into model
#creation_frequency = int(config['PAT agents']['frequency_PAT_creation'])  # in time-steps

    if config['PAT agents']['initial_PAT_agents'] == 'True':
        for i in range(int(config['PAT agents']['number_initial_pats'])):
            p = PATAgent(m)
            p.random_init()
            m.schedule.add(p)              
            
    if config['PAT agents']['custom_bootstrapping'] == 'True':
        number_of_PAT_sets = int(config['PAT agents']['number_of_custom_PAT_sets'])
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
            for i in range(nr_PATs):
                p = PATAgent(m)
                p.custom_init(tk_purpose, tk_design, cr_id)
                m.schedule.add(a) 

if __name__ == "__main__":
    from mesa.time import RandomActivation
    class EmptyModel(Model):
        def __init__(self):
            self.schedule = RandomActivation(self)     
    m = EmptyModel()        
    configAgents(m)