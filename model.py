import numpy as np
import mesa
import random
from agents import Household, Firm

class LegnickModel(mesa.Model):
    """the Legnick model"""
    
    def __init__(self, n_households = 1000, n_firms = 100, seed=333):
        super().__init__(rng=seed)
        self.n_households = n_households
        self.n_firms = n_firms

        # create agents
        Household.create_agents(model=self, n=n_households)
        Firm.create_agents(model=self, n=n_firms)

        Households = self.agents.select(agent_type = Household)
        firms = list(self.agents.select(agent_type = Firm))

        # initialise trading connectons (type a)

        for h in Households:
            
            type_a = random.sample(firms, 7)
            h.type_a_connections = type_a

