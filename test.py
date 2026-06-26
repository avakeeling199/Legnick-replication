from agents import Household, Firm
from model import LegnickModel

model = LegnickModel()
households = model.agents.select(agent_type=Household)
h = households[0]
print(h.type_a_connections)
print(h.type_b_connection)