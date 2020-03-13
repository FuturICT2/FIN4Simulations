# FIN4Sim
Welcome to the Finance4 simulation platform!                                

1. Purpose

	In addition to being sustainable and scalable, the FIN4 system should also be resilient to unintended user behaviour. 
	We use simulations to improve the cryptoeconomic design towards system stability and to avoid dynamics that may result from 
	not fully accounting for the “human factor”. Our definition of an ideal stable system includes token creators with noble intent,
	tokens invulnerable to manipulation and users using the tokens as intended. In contrast, bad situations can occur due to token
	creators with malicious intent, tokens vulnerable to manipulation or users cheating.
 
2. Constructs and Concepts 
 
	In our agent-based approach, we have human agents which fulfill certain roles 
	(like token claimers or token creators) and token-type agents.  

	Human agent: 

	Attributes:
		1. 	Universal unique identifier (uuid)
		2.  ID (sequential natural number)
		3.  Token wallet
		4.  Action count
		5.  Claimer compliance
		6.  Claimer intention
		7.  Voter profile
		8.  Token creator intention
		9.  Token creator design

	Roles
		Token claimer:
			-       Claimer compliance (compliant, opportunist, cheater) (*attribute 5)
			-       Claimer intention (noble, opportunistic, malicious) (*attribute 6)

		Token voter
			-       Assessment driven (objective)
			-       Gain driven (subjective) (*attribute 7)
			
		Token creator
			-       Intention (noble, opportunistic, malicious) (*attribute 8)
			-       Design (careful, careless) (*attribute 9)
 
 
	Type of token (PAT = positive action token) agent: 

	Attributes
		1.  uuid
		2.  ID
		3.  Creator ID
		4.  Action count
		5.  Purpose
		6.  Design


	Human agent roles and attributes - Definitions: 

		Claimer compliance - the attitude the individual (human agent) has with respect to the rules for obtaining a token for an action. 
		It can be compliant with the rules, opportunistic when given the chance or always a cheater. 

		Claimer intention -  the intent of the token that an agent looks for in order to obtain a token. Agents looking for nobel claimer 
		intention are the agents valuing the nobel action to obtain the specific token. Same for opportunistic and maliciously intended 
		claimers. 

		Token wallet - the sum of tokens of a certain type that a human agent possesses (after claiming tokens). Reputation tokens are 
		included here as well.   

		Assessment driven voter - voter who votes objectively,  analysis the attributes of the token before voting for or against it becoming 
		an official token 

		Gain driven voter - voter who votes subjective, analysing only how many tokens of that type he has in his token wallet and the 
		advantage he would acquire if the token becomes official or not 

		Token creator intent - the intention that the creator has in mind for the created token. It can be nobel, opportunistic or malicious.  

		Token creator design - the way the creator designs the proof mechanism of the token. It can be carefully done (there is no way people 
		can claim a token without doing the action) or careless (there is a way for people to claim the token without doing the action).

		Action - for every token claimed, one had to do the action the token requires. In general we refer to this as “positive action” but 
		it is not necessarily the case.

		Token agent attributes and concepts - Definitions: 

		Token purpose - the general type of objective the token type is created for. The options in our simulations are currently: noble, 
		opportunistic and malicious. 
 
		Token design - the way the token proof is established by the creator. Every time a token is claimed for an action, the claimer has 
		to prove that the action happened. The design of the proof mechanism can be careful (the token creator makes sure it is not easy to 
		claim a token without doing the action for it) or careless (it allows loopholes or ways of cheating in the claiming process). 

		Token bootstrapping mechanism - the launching of the token system in a community with already existing token types, designed by 
		default and not by the human agents in the community. In our case, we think that a small number of noble, carefully designed token 
		types can have an influence on the overall token claiming just by setting an example. 


3. Token creation by a human agent

	The token agent creation mechanism relies on the simulation timestep meaning that one can specify the timestep interval between two 
	token creations. 

	The new token agents are created by the human agents. The ID of the human agent creator is selected randomly. Once the ID of the 
	creator is selected, the creator agent will transfer its token creator intention (which can be noble, opportunistic or malicious) 
	to the newly created token purpose attribute. Similarly, the token creator design attribute of the human agent is transferred to the
	token design attribute of the token agent. 

	What we want to model this way is the fact that, e.g. a noble person is very likely to create a token with a noble intent. Similarly, 
	someone who is used to creating carelessly designed tokens is more probable to continue doing so. 

4. Token claiming 

	There are two important processes to consider in the modeling of token claiming by the human agents: 
	the purpose-intention alignment and the design alignment. 

		Purpose-intention alignment
		
			The token type creator creates a token with a specific intent (nobel, opportunistic or malicious) and thansfers this attribute
			to the token. The token claimer perceives the intention of the token type as noble, opportunistic or malicious. 
		
		Design-compliance alignment
	
			*for more imformation see ...
	

5. cadCAD

	The  FIN4 simulation code is open source and is based on time steps, using cadCAD, an open source tool for “complex adaptive dynamics
	computer-aided design”. At every time step, key variables are updated through actions or policies.
 

6. Get started: 

	- install cadCAD (https://cadcad.org/)
		pip3 install cadCAD
		for more information see https://github.com/BlockScience/cadCAD?
		
	- run the simulations and store the output in a separate file 
		python Fin4_ABM.py 
		
	- run the simulation through the visualizasion module
		python 
	
	

7. Structure of the main file Fin4_ABM.py



5. The config.ini file
	
	Knowing how to modify the configuration file is very important! 
	
[general]
time_steps = 6 																	=> total number of timesteps the simulation will execute
output_file_name = 'output.json'												=> name the output file. it will be created in the same folder as Fin4_ABM.py


[human agents]																	=> human agents (one of the two types of agents)
#---------------------------------------OPTION 1 ---------------------------	=> one can chose to have a certain number of human agents with randomly distributed attibutes 
agents_with_random_attributes = False											=> for this option to be active, make "agents_with_random_attributes" True and chose the number of the human agents by setting the value of "number"
number = 5																		=> DON'T FORGET to set "custom_agents" False at OPTION 2, otherwise the current settings at OPTION 1 will be overwritten  
#---------------------------------------OPTION 2 ---------------------------	=> This option offers the possibility of defining one or more groups of human agents with specific attributes
custom_agents = True															=> if you only want custom defined human agents, make sure the "agents_with_random_attributes" is False
; if custom_agents = True, define the agents sets:				
number_of_custom_agent_sets = 2												    => one can choose as many sets of agents as one wants. what is important is to have as many sets below as numbers selected, othewise the simulation will crash 
; the above number has to match the sets defined below:							=> having more sets than the number set will not crash the simulation

; set 1																			=> all the attributes withing a set have the prefix of the set number: 'set1_'/'set2_' etc.
set1_number_of_agents = 5														=> number of agents withing the set
set1_claim_intent = noble														=> the calimer intention can be 'noble', 'opportunistic' or 'malicious'
set1_claim_compliance = opportunistic											=> complaince of the claimers can be 'compliant', 'cheater' or 'opportunistic'
set1_voter_drive = assessment													=> the drive of agents when voting. can be 'assesment' or 'gain'
set1_creator_intent = noble														=> the purpose of the type of token being created by agents or the intention for which the agents create a type of token. can be 'noble', 'opportunistic' or 'malicious'
set1_creator_design = careless													=> the design of the proof mechanism of the token type being created by these agents. can be 'careful' or 'careless'

; set 2
set2_number_of_agents = 5
set2_claim_intent = malicious
set2_claim_compliance = opportunistic
set2_voter_drive = assessment
set2_creator_intent = malicious
set2_creator_design = careless

 
[PAT agents]																	=> means 'positive action token' and they are the types of tokens being either created by the human agents (OPTION 1) or chosen at the begining of the simulation (OPTION 2) 
#---------------------------------------OPTION 1 ---------------------------	=> one can choose to have agents creating types of tokens AND have a few custom ones defined at the begining of the simulation
initial_PAT_agents = False														=> do you want to start the simulation with custom token types and then let human agents creat their own? True/False 
number_initial_pats = 2															=> how many token types do you want to start the simulation with? at the moment these PATs are 'noble' in purpose and 'careful' in design
;in times steps
frequency_PAT_creation = 3														=> every 'frequency_PAT_creation' time steps a random human agent is chosen to creat a new token type passing on the creator intent and the creator design  
#---------------------------------------OPTION 2 ---------------------------	=> in this case (if the previous option is False) this refers to predefining all the existent token types in the system  
custom_bootstrapping = True
number_of_custom_PAT_sets = 2													=> sets of predifined token types. having more sets defined here than actual atribute sets below will cause the simulation to crash 
; the above number has to match the sets defined below:

; set 1																			=> all the attributes withing a set have the prefix of the set number: 'set1_'/'set2_' etc.
set1_init_id = 0																=> the ID of the first PAT created within this set. make sure you don't overwrite PATs with different attributes. 
set1_number_of_PATs = 2															=> how many PATs do you want with this set of attributes? 
set1_token_purpose = noble														=> purpose of the PAT (inherited from the creator human agent) can be 'noble', 'opportunistic' or 'malicious'
set1_token_design = careful														=> proof design of the PAT (inherited from the creator human agent) can be 'careful' or 'careless'
;arbitrarily big number because for bootstrapping it doesn't matter
set1_creator_id = 10000

; set 2
set2_init_id = 2
set2_number_of_PATs = 3
set2_token_purpose = malicious
set2_token_design = careful
;arbitrarily big number because for bootstrapping it doesn't matter
set2_creator_id = 10000