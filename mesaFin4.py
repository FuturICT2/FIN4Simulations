from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import mesaConfigCreateAgents 
from mesaPATAgent   import PATAgent
from mesaHumanAgent import HumanAgent
import mesaConfigCreateAgents
import random

class MesaFin4(Model):
    """A simple model of an economy of intentional agents and tokens.
    """
    creation_frequency = 0

    def update_creation_frequency(self, v):
        MesaFin4.creation_frequency = v

    def __init__(self):
        #self.num_agents = N
        self.schedule = RandomActivation(self)
        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},
        #     agent_reporters={"Wealth": "wealth"}
        # )
        # Create agents(
        mesaConfigCreateAgents.configAgents(self)
        print(MesaFin4.creation_frequency)
        #self.running = True
        #self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        #self.datacollector.collect(self)

    def run_model(self, n):
        print(MesaFin4.creation_frequency)
        for i in range(n):
            print(i)
            self.step()
            #if i % MesaFin4.creation_frequency == 0:
            random.choice(self.schedule.agents).create_pat()

if __name__ == "__main__":
    m = MesaFin4()  
    m.run_model(10)      
