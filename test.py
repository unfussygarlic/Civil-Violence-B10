from agent.params import model_params_test as model_params
from agent.env import World

run = World(*model_params)

for i in range(100):
    run.step()