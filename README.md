# Modelling Civil Violence: A Multi Agent Simulation
We have two actors in the model, ‘cops’ which are forces of central authority and the decentralised ‘agents’ who rebel as per their own grievance. Each agent’s grievance is calculated using the product of its perceived hardship and it’s own illegitimacy, i.e unwillingness to abide by the law. Reason for using their product is to depict the fact that, if legitimacy is high (meaning illegitimacy becomes zero), then grievance becomes zero, and no amount of hardship will ever induce any political grievance. However, it is interesting to know that the decision to rebel is not only dependent onmere grievance, but also on the agent’s estimated probability of arrest, and their risk aversion. Thisarrest probability is then determined by cops to active agents ratio, such that the higher the ratio,the more probable is the agent’s arrest if it goes active.

## Files
- `agent/authority.py` : Contains Cops/Central authority agent class.
- `agent/env.py` : Primary environment in which placement and operations of agents take place.
- `agent/params.py` : Parameters including sliders and various constants.
- `agent/people.py` : Contains Citizen agent class.
- `agent/server.py` : Sets up server and visualization.
- `run.py` : Opens the server and port for visualization.

## How To Run
> 1. Clone the repository
> 2. Install `requirements.txt`
> 3. Run using `python run.py`
