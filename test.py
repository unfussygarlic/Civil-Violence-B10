from agent.env import World

N = 100
gridsize = 10
run = World(N,gridsize)

for i in range(100):
    run.step()