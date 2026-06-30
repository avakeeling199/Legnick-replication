from agents import Household, Firm
from model import LegnickModel

model = LegnickModel()
for i in range(1000):
    model.step()
    if i % 21 == 0:
        households = model.agents.select(agent_type=Household)
        firms = model.agents.select(agent_type=Firm)
        employed = sum(1 for h in households if h.type_b_connection is not None)
        avg_price = sum(f.p_f for f in firms) / len(list(firms))
        print(f"Month {i//21}: employed={employed}, avg_price={avg_price:.2f}")

        firms = list(model.agents.select(agent_type=Firm))
        prices = [f.p_f for f in firms]
        print(f"min price: {min(prices)}, max price: {max(prices)}, unique: {len(set(prices))}")

        sample_household = households[0]
        print(f"m_h={sample_household.m_h}, c_r_h={sample_household.c_r_h}, daily_demand={sample_household.c_r_h/21}")