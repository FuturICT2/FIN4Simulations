#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import random
import pandas as pd
import matplotlib.pylab as pl


# In[3]:


import cadCAD
from cadCAD import engine
from cadCAD.configuration import Configuration
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor


# In[4]:


simulation_parameters = {
    'T': range(20),
    'N': 1,
    'M': {}
}


# # Test of Basic Design

# In[5]:


# general constants

TIMESTEP = 'timestep' # access to current timestep with s[TIMESTEP]


# In[6]:


def get_update_name(variable_name):
    return "add_" + variable_name


# In[7]:


USERS = "users"
PATS = "pats"
OPATS = "opats"
CLAIMS = "claims"
ADD_USERS = get_update_name(USERS)
ADD_PATS = get_update_name(PATS)
ADD_OPATS = get_update_name(OPATS)
ADD_CLAIMS = get_update_name(CLAIMS)
WALLET_GAINS = "wallet_gains"


# In[8]:


initial_conditions = {
    USERS: {0:{}}, # users are numerical ids and a dictionary of their current wallet
    PATS: [0], # pats are currently simply numerical ids
}


# ## update functions

# In[9]:


# create single user with empty wallet 
def create_users(params, step, sL, s):
    next_user_id = len(s[USERS])
    x = {ADD_USERS:[
        (next_user_id, {}),
         #{random.choice(s[PATS]):random.randint(1,10)}
    ]}
    return x


# In[10]:


def create_pat(params, step, sL, s):
    next_pat_id = len(s[PATS])
    x = {ADD_PATS:[next_pat_id,]}
    return x


# In[11]:


def user_actions(params, step, sL, s):
    gain = {}
    pats = s[PATS]
    for user in s[USERS]:
        for pat in random.sample(pats, random.randint(0, len(pats))):
            gain[(user, pat)] = 1
    return {WALLET_GAINS: gain}


# ## update variables

# In[12]:


def add_users(params, step, sL, s, _input):
    x = s[USERS].copy()
    for new_user_id, wallet in _input[ADD_USERS]:
        x[new_user_id] = wallet
    return (USERS, x)


# In[13]:


def update_user_wallets(params, step, sL, s, _input):
    x = s[USERS].copy()
    changes = _input[WALLET_GAINS]
    for (user, pat), gain in changes.items():
        x[user][pat] = x[user].get(pat, 0) + gain
    return (USERS, x)


# In[14]:


def add_pat(params, step, sL, s, _input):
    x = s[PATS].copy()
    x.extend(_input[ADD_PATS])
    return (PATS, x)    


# ## test of basic functions

# In[15]:


partial_state_update_blocks = [
    { 
        'policies': { 
            'create_users': create_users,
        },
        'variables': { 
            USERS: add_users,
        }
    },
    { 
        'policies': {
            'user_actions': user_actions,
        },
        'variables': {
            USERS: update_user_wallets,
        }
    },
    { 
        'policies': {
            'create_pat': create_pat,
        },
        'variables': {
            PATS: add_pat,
        }
    },    
]

config = Configuration(initial_state=initial_conditions, #dict containing variable names and initial values
                       partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
                       sim_config=simulation_parameters #dict containing simulation parameters
                      )

exec_mode = ExecutionMode()
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config]) # Pass the configuration object inside an array
raw_result, tensor = executor.execute()

df = pd.DataFrame(raw_result)
print(df)


# # Initial design V0

# In[34]:


initial_conditions = {
    USERS: {0:{}}, # users are numerical ids and a dictionary of their current wallet
    PATS: [0], # pats are currently simply numerical ids
    CLAIMS: {},
}


# In[41]:


def users_join(params, step, sL, s):
    """Each step one user joins the system"""
    next_user_id = len(s[USERS])
    x = {ADD_USERS:[
        (next_user_id, {}),
    ]}
    return x

def claim_pat(params, step, sL, s):
    """Each step each user creates a random amount of claims for a random selection of PATs"""
    maximum_number_of_actions = 10
    new_claims = {}
    pats = s[PATS]
    for user in s[USERS]:
        for pat in random.sample(pats, random.randint(0, min(len(pats), maximum_number_of_actions))):
            new_claims[(user, pat)] = 1
    return ({ADD_CLAIMS: new_claims})

def prove_claim(params, step, sL, s):
    """Each steps all claims are accepted with a certain probability"""
    acceptance_probability = 1
    gains = {}
    for (user, pat), gain in s[CLAIMS].items():
        if random.random() < acceptance_probability:
            gains[(user, pat)] = gain
    
    return {WALLET_GAINS:gains}

def create_new_pats(params, step, sL, s):
    """Each step one new PAT is added to the system"""
    next_pat_id = len(s[PATS])
    x = {ADD_PATS:[next_pat_id,]}
    return x


# In[69]:


def update_users(params, step, sL, s, _input):
    x = s[USERS] 
    
    # add new users
    for new_user_id, wallet in _input[ADD_USERS]:
        x[new_user_id] = wallet
    
    # update wallet according to proven claims
    changes = _input[WALLET_GAINS]
    for (user, pat), gain in changes.items():
        x[user][pat] = x[user].get(pat, 0) + gain
        
    return (USERS, x)

def update_pats(params, step, sL, s, _input):
    x = s[PATS] 
    x.extend(_input[ADD_PATS])
    return (PATS, x)

def update_claims(params, step, sL, s, _input):
    return (CLAIMS, _input[ADD_CLAIMS])


# In[70]:


# Initial Design V0
partial_state_update_blocks = [
    { 
        'policies': { 
            'users_join': users_join,
            'claim_pats': claim_pat,
            'prove_claim': prove_claim,
            'create_new_pats': create_new_pats
        },
        'variables': { 
            USERS: update_users,
            PATS: update_pats,
            CLAIMS: update_claims, 
        }
    },
]


# In[92]:


simulation_parameters = {
    'T': range(100), 
    'N': 1,
    'M': {}
}


# In[93]:


config = Configuration(initial_state=initial_conditions, #dict containing variable names and initial values
                       partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
                       sim_config=simulation_parameters #dict containing simulation parameters
                      )

exec_mode = ExecutionMode()
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config]) # Pass the configuration object inside an array
raw_result, tensor = executor.execute()

df = pd.DataFrame(raw_result)
#print(df)
print(raw_result[-1])


# # Analysis
# - Too many different Pats with too little token/activity per PAT
# - Multiple of same kind

# In[97]:


def calculate_total_tokens_per_pat(state):
    distribution = {pat:0 for pat in state[PATS]}
    for user_wallet in state[USERS].values():
        for pat, number_of_tokens in user_wallet.items():
            distribution[pat] += number_of_tokens
    return distribution

print(calculate_total_tokens_per_pat(raw_result[-1]))
pl.hist(calculate_total_tokens_per_pat(raw_result[-1]).values(), bins=300)
pl.show()

pl.scatter(calculate_total_tokens_per_pat(raw_result[-1]).keys(), 
           calculate_total_tokens_per_pat(raw_result[-1]).values())


# In[95]:


def calculate_active_user_per_pat(state):
    distribution = {pat:0 for pat in state[PATS]}
    for user_wallet in state[USERS].values():
        for pat, number_of_tokens in user_wallet.items():
            distribution[pat] += 1
    return distribution

print(calculate_active_user_per_pat(raw_result[-1]))
pl.hist(calculate_active_user_per_pat(raw_result[-1]).values(), bins=300)
pl.show()

pl.scatter(calculate_active_user_per_pat(raw_result[-1]).keys(), 
           calculate_active_user_per_pat(raw_result[-1]).values())


# In[96]:


def calculate_distributions_of_number_of_tokens(state):
    distribution = []
    for user_wallet in state[USERS].values():
        distribution.append(len(user_wallet))
    return distribution

print(calculate_distributions_of_number_of_tokens(raw_result[-1]))
pl.hist(calculate_distributions_of_number_of_tokens(raw_result[-1]), bins=300)
pl.show()


# # New Design (V1)
# - Req: Concentration/Focus/Emphasis on good PATs
# - Proposal: List of accepted/good/official PATs (using TCR -> new Token GOV)
# - Initial Approach, 1 GOV per User (democracy, one vote for each user)

# In[106]:


initial_conditions = {
    USERS: {0:{}}, # users are numerical ids and a dictionary of their current wallet
    PATS: [0], # pats are currently simply numerical ids
    OPATS: [],
    CLAIMS: {},
}


# In[162]:


def claim_pat_with_opats(params, step, sL, s):
    """Each step each user creates a random amount of claims for a random selection of PATs"""
    maximum_number_of_actions = 10
    probability_on_opat_actions = .9
    new_claims = {}
    pats = s[PATS]
    opats = s[OPATS]

    for user in s[USERS]:
        number_of_actions = random.randint(0, min(len(pats), maximum_number_of_actions))
        opat_actions = min(len(opats), int(number_of_actions*probability_on_opat_actions))
        usual_actions = number_of_actions - opat_actions
        
        for pat in random.sample(opats, opat_actions):
            new_claims[(user, pat)] = 1
        
        for pat in random.sample(pats, random.randint(0, usual_actions)):
            new_claims[(user, pat)] = 1
    return ({ADD_CLAIMS: new_claims})

def propose_opats(params, step, sL, s):
    if 5 < s[TIMESTEP] < 20:
        proposal_probability = .5
    else: 
        proposal_probability = .01
    pats = s[PATS]
    opats = s[OPATS]
    new_opats = []
    if random.random() < proposal_probability:
        next_opat = random.choice(pats)
        
        i = 0
        while next_opat in opats:
            i += 1
            if i >= 10:
                break
            next_opat = random.choice(pats)
        else:
            new_opats.append(next_opat)
    
    return {ADD_OPATS:new_opats}


# In[163]:


def update_opats(params, step, sL, s, _input):
    x = s[OPATS]
    x.extend(_input[ADD_OPATS])
    return (OPATS, x)


# In[164]:


# Design V1 with 
partial_state_update_blocks = [
    { 
        'policies': { 
            'users_join': users_join,
            'claim_pats': claim_pat_with_opats,
            'prove_claim': prove_claim,
            'create_new_pats': create_new_pats,
            'propose_opats': propose_opats,
        },
        'variables': { 
            USERS: update_users,
            PATS: update_pats,
            CLAIMS: update_claims, 
            OPATS: update_opats,
        }
    },
]


# In[165]:


simulation_parameters = {
    'T': range(100), 
    'N': 1,
    'M': {}
}


# In[166]:


config = Configuration(initial_state=initial_conditions, #dict containing variable names and initial values
                       partial_state_update_blocks=partial_state_update_blocks, #dict containing state update functions
                       sim_config=simulation_parameters #dict containing simulation parameters
                      )

exec_mode = ExecutionMode()
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config]) # Pass the configuration object inside an array
raw_result, tensor = executor.execute()

df = pd.DataFrame(raw_result)
#print(df)
print(raw_result[-1])


# # Analysis

# In[167]:


print(calculate_total_tokens_per_pat(raw_result[-1]))
pl.hist(calculate_total_tokens_per_pat(raw_result[-1]).values(), bins=300)
pl.show()

pl.scatter(calculate_total_tokens_per_pat(raw_result[-1]).keys(), 
           calculate_total_tokens_per_pat(raw_result[-1]).values())


# In[168]:


pl.hist(calculate_active_user_per_pat(raw_result[-1]).values(), bins=300)
pl.show()

pl.scatter(calculate_active_user_per_pat(raw_result[-1]).keys(), 
           calculate_active_user_per_pat(raw_result[-1]).values())


# In[169]:


print(calculate_distributions_of_number_of_tokens(raw_result[-1]))
pl.hist(calculate_distributions_of_number_of_tokens(raw_result[-1]), bins=300)
pl.show()


# # Analysis
# - It could work??
# - Vulnerability: Sybil attack
# - #Req: Introduction of REP as "Proof-of-work" for user actions

# In[ ]:


# new policy functions with REP


# In[ ]:


# Design V2 with 
partial_state_update_blocks = [
    { 
        'policies': { 
            'users_join': users_join,
            'claim_pats': claim_pat_with_opats,
            'prove_claim': prove_claim,
            'create_new_pats': create_new_pats
        },
        'variables': { 
            USERS: update_users,
            PATS: update_pats,
            CLAIMS: update_claims, 
        }
    },
    { 
        'policies': { 
            'propose_opats': propose_opats,
            'challenge_opats': challenge_opats,
            'vote_on_opats': vote_on_opats,
        },
        'variables': { 
            'proposals': update_proposals,
            'challenges': update_challenges,
            OPATS: update_opats,
            'failed_proposals': update_failed_proposals,
            'failed_challenges': update_failed_challenges,
        }
    },
]

