import unittest
import Fin4_ABM as model
import configparser

"""### Read config file"""

config = configparser.ConfigParser()
config.read('config.ini')

class MyTestCase(unittest.TestCase):

    def reconstruct_agent_database(self, data):
        reconstruction = []
        for i in range(0, len(data)):
            if isinstance(data[i], dict):
                reconstruction.append(data[i])
            if isinstance(data[i], list):
                reconstruction.append(data[i][0])
        return reconstruction

    def number_of_tokens_per_person(self, agent):
        distribution = 0
        for pat, number_of_tokens in agent['token_wallet'].items():
            if pat != "reputation":
                distribution += number_of_tokens
            else:
                pass
        return distribution

    def test_number_of_agents_created(self):
        print("Running test: number of agents created")
        rec_data = self.reconstruct_agent_database(model.raw_result[-1]['agents'])
        self.assertEqual(len(rec_data), int(config['human agents']['number']))

    def test_PAT_creator_creation(self):
        print("Running test: PAT creator - creation")
        initial_PAT_number = int(config['PAT agents']['number_initial_pats'])
        nr_new_PATs = len(model.raw_result[-1]["PATs"]) - initial_PAT_number
        print("nr new PATs", nr_new_PATs)
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

    def test_AT_ratio(self):
        print ("Running test: AT ratio")
        rec_data = self.reconstruct_agent_database(model.raw_result[-1]['agents'])
        for agent in rec_data:
            nr_tokens = self.number_of_tokens_per_person(agent)
            activity = agent['activity']
            if nr_tokens:
                if agent['claimer'] == "follower":
                    self.assertEqual(activity/nr_tokens, 1)
                if agent['claimer'] == "opportunistic":
                    self.assertLessEqual(activity / nr_tokens, 1)
                if agent['claimer'] == "cheater":
                    self.assertEqual(activity / nr_tokens, 0)
            else:
                self.assertEqual(activity, 0)


if __name__ == '__main__':
    unittest.main()
