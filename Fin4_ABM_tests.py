import unittest
import Fin4_ABM as model
import configparser

"""### Read config file"""

config = configparser.ConfigParser()
config.read('config.ini')

class MyTestCase(unittest.TestCase):

#---------------------- Helper functions---------------------------

    def number_of_tokens_per_person(self, agent):
        distribution = 0
        for pat, number_of_tokens in agent['token_wallet'].items():
            if pat != "reputation":
                distribution += number_of_tokens
            else:
                pass
        return distribution

    def calculate_total_agents_from_config_file(self):
        nr_agen_sets = int(config['human agents']['number_of_custom_agent_sets'])
        total_agents = 0
        if config['human agents']['custom_agents'] == "True":
            for set in range(1, nr_agen_sets + 1):
                set_name = "set" + str(set) +"_number_of_agents"
                total_agents += int(config['human agents'][set_name])
        if config['human agents']['agents_with_random_attributes'] == "True":
            total_agents += int(config['human agents']['number'])
        return total_agents

    def info_PATs_from_config_file(self):
        nr_agen_sets = int(config['PAT agents']['number_of_custom_PAT_sets'])
        total_agents = 0
        purpose = []
        design = []
        for set in range(1, nr_agen_sets + 1):
            set_name = "set" + str(set) + "_number_of_PATs"
            purpose_name = "set" + str(set) + "_token_purpose"
            design_name = "set" + str(set) + "_token_design"
            agents_per_set = int(config['PAT agents'][set_name])
            for i in range(0, agents_per_set):
                purpose.append(config['PAT agents'][purpose_name])
                design.append(config['PAT agents'][design_name])
            total_agents += agents_per_set
        return total_agents, purpose, design

#------------------------ Unittests -------------------------------

    def test_number_of_agents_created(self):
        print("Running test: number of agents created")
        self.assertEqual(
            len(model.raw_result[-1]['agents']),
            self.calculate_total_agents_from_config_file()
        )

    def test_PAT_creator_creation(self):
        print("Running test: PAT creator - creation")
        if config["PAT agents"]["human_agent_PAT_creation"] == "True":
            initial_PAT_number = int(config['PAT agents']['number_initial_pats'])
            nr_new_PATs = len(model.raw_result[-1]["PATs"]) - initial_PAT_number
            #print("nr new PATs", nr_new_PATs)
            for i in range(0, nr_new_PATs):
                creator_ID = model.raw_result[-1]["PATs"][initial_PAT_number + i]['creator_ID']
                PAT_purpose = model.raw_result[-1]["PATs"][initial_PAT_number + i]['purpose']
                PAT_design = model.raw_result[-1]["PATs"][initial_PAT_number + i]['design']
                for ag in model.raw_result[-1]['agents']:
                    try:
                        if ag['name']==creator_ID:
                            self.assertEqual(ag['creator_intention'], PAT_purpose)
                            self.assertEqual(ag['creator_design'], PAT_design)
                    except:
                        if ag[0]['name'] == creator_ID:
                            self.assertEqual(ag[0]['creator_intention'], PAT_purpose)
                            self.assertEqual(ag[0]['creator_design'], PAT_design)

        if config["PAT agents"]["custom_bootstrapping"] == "True":
            total_PATs_config, purpose_config, design_config = self.info_PATs_from_config_file()
            self.assertEqual(len(model.raw_result[-1]["PATs"]), total_PATs_config)
            for i in range(0, total_PATs_config):
                self.assertEqual(model.raw_result[-1]["PATs"][i]['purpose'], purpose_config[i])
                self.assertEqual(model.raw_result[-1]["PATs"][i]['design'], design_config[i])

    def test_AT_ratio(self):
        print ("Running test: AT ratio")
        for agent in model.raw_result[-1]['agents']:
            nr_tokens = self.number_of_tokens_per_person(agent)
            activity = agent['activity']
            if nr_tokens:
                if agent['claimer'] == "follower":
                    self.assertEqual(activity/nr_tokens, 1)
                if agent['claimer'] == "opportunistic":
                    self.assertLessEqual(activity/nr_tokens, 1)
                if agent['claimer'] == "cheater":
                    self.assertEqual(activity/nr_tokens, 0)
            else:
                self.assertEqual(activity, 0)


if __name__ == '__main__':
    unittest.main()
