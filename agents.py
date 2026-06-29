import numpy as np
import mesa

class Household(mesa.Agent):
    """Household agents"""

    def __init__(self, model):
        # pass the params to parent class
        super().__init__(model)

        self.w_h = 1.0 # reservation wage
        self.m_h = 0.0 # liquidity
        self.type_a_connections = [] # list of firms 
        self.type_b_connection = None # employment
        self.c_r_h = 0 # demand
        self.income = 0 #income from last month


class Firm(mesa.Agent):
    """Firm agents"""

    def __init__(self, model):
        super().__init__(model)

        self.m_f = 0.0 # liquidity
        self.i_f = 0.0 # inventory
        self.p_f = 1.0 # goods price
        self.w_f = 1.0 # wage rate
        self.l_f = 0 # no of workers?

