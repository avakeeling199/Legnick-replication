import numpy as np
import mesa
import random
from agents import Household, Firm

class LegnickModel(mesa.Model):
    """the Legnick model"""
    
    def __init__(self, n_households = 1000, n_firms = 100, seed=333, alpha = 0.9, n = 7, ld = 3, chi = 0.1):
        super().__init__(rng=seed)
        self.n_households = n_households
        self.n_firms = n_firms
        self.counter = 0
        self.alpha = alpha
        self.n = n
        self.ld = ld
        self.chi = chi
        

        # create agents
        Household.create_agents(model=self, n=n_households)
        Firm.create_agents(model=self, n=n_firms)

        Households = self.agents.select(agent_type = Household)
        firms = list(self.agents.select(agent_type = Firm))

        # initialise trading connectons (type a)

        for h in Households:
            
            type_a = random.sample(firms, 7)
            h.type_a_connections = type_a

    def step(self):
        Households = self.agents.select(agent_type = Household)
        firms = list(self.agents.select(agent_type = Firm))
        self.counter += 1
        if self.counter % 21 == 1:
            # beginning of month
            # firms:
            # each decide how to set w_f
            # each decide p_f if i_f unsatisfactory level
            # households:
            # each search for better type_a connections
            # if type_b_connection = None, go to random f to search for open position
            # decide how much m_h to spend on consumption goods
            for h in Households:
                prices = 0
                alpha = self.alpha
                for a in h.type_a_connections:
                    prices += a.p_f
                p_i_h = prices / len(h.type_a_connections)
                h.c_r_h = min((h.m_h / p_i_h)**alpha, h.m_h / p_i_h)
        # daily: 
        # households:
        # use their m_h to buy goods from random type_a connection
        # demand is equally spread thru month
        
        for h in Households:
            demand = h.c_r_h / 21
            og_demand = demand
            shops = random.sample(h.type_a_connections, len(h.type_a_connections))
            for shop in shops[:self.n]:
                shop = random.choice(h.type_a_connections)
                if shop.i_f >= demand and h.m_h >= (shop.p_f * demand):
                    h.m_h -= shop.p_f * demand
                    shop.m_f += shop.p_f * demand
                    shop.i_f -= demand
                    demand = 0
                elif h.m_h < (shop.p_f * demand):
                    demand_new = h.m_h / shop.p_f
                    h.m_h -= shop.p_f * demand_new
                    shop.m_f += shop.p_f * demand_new
                    shop.i_f -= demand_new
                    demand -= demand_new
                elif shop.i_f < demand:
                    h.m_h -= shop.p_f * shop.i_f
                    shop.m_f += shop.p_f * shop.i_f
                    demand -= shop.i_f
                    shop.i_f = 0
                if demand <= 0.05 * og_demand:
                    break
        # firms produce
        for f in firms:
            f.l_f += self.ld * f.l_f


        if self.counter % 21 == 0:
            # end of month:
            # firms:
            # use their m_f to pay wages, build buffer and pay profits
            
            for f in firms:
                buffer = 0
                if f.m_f >= f.w_f * f.l_f:
                    for h in Households:
                        if h.type_b_connection == f:
                            f.m_f -= f.w_f
                            h.m_h += f.w_f
                            # store income
                            h.income = f.w_f
                else:
                    new_wage = f.m_f / f.l_f
                    for h in Households:
                        if h.type_b_connection == f:
                            f.m_f -= new_wage
                            h.m_h += new_wage
                            # store income
                            h.income = new_wage
                    
                if f.m_f > self.chi * f.w_f * f.l_f:
                    # add to buffer - full amount
                    buffer += self.chi * f.w_f * f.l_f
                    f.m_f -= self.chi * f.w_f * f.l_f
                elif f.m_f > 0:
                    # add to buffer - not full amount
                    buffer += f.m_f
                    f.m_f = 0

                if f.m_f > 0:
                    # distribute profit for each house proportional to m_h
                    total_liquid = 0
                    for h in Households:
                        total_liquid += h.m_h
                    for h in Households:
                        h.m_h += (f.m_f / total_liquid) * h.m_h
                f.m_f = buffer

            # households:
            # adjust w_h depending on income
            for h in Households:
                if h.income > h.w_h:
                    h.w_h = h.income
                if h.income == 0:
                    h.w_h = h.w_h * 0.9


            



