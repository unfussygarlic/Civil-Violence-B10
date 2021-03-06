# Modelling civil disobedience using wealth in agents

We are trying to model the grievance behaviour of citizens as a measure of varying parameters such as legitimacy, wealth, and hardship. We would then deduce what amount of central forces are required to control the active agents. We aim to model the agents' behaviour in the presence of cops and how they become active or inactive as a measure of their risk aversion and their surrounding agents' total grievance. Finally, we also try to understand if wealth can also play a role in agents' civil disobedience.

## Table of content

- [Modelling Civil Violence: A Multi Agent Simulation](#modelling-civil-disobedience-using-wealth-in-agents)
- [How To Run](#how-to-run)
- [Implementation Description](#implementation-description)
  - [Model Details](#model-details)
- [Results](#results)
- [Files](#files)
- [Repository Structure](#repository-structure)

## How To Run
1. Clone the repository
2. Install `requirements.txt` via pip package manager using `$ pip install -r requirements.txt`
3. Run using `python run.py`

## Implementation Description

In the beta implementation, there are two main agents(i.e. Citizen and Cops). The task of Citizen is to revolt if the grievance is above a threshold and the task of Cops is to imprison the citizen who is in revolt state. The Cops can also eliminate the citizen based on the number of times it has been imprisoned in the past.

There are three categories in **Citizen** agent(**Poor, Middle, & Rich**) which essentially tell us about the economic status of that agent. Simultaneously, the parameters that affect the Citizen are **Hardship, Legitimacy, Wealth**.

### Model Details

- **Citizen**

  Citizens are the core agents whose behaviour is varied during each time step depending on the change in behaviour of Central authority. The simulation is initially filled with a
  certain population ratio of citizens of varying economic status. The property of Citizen is:
    - It can revolt against the Central Authority
    - The grievance of a citizen is decided by the three global parameters(i.e. Legitimacy, Hardship, Wealth), its economic status, its confidence.
    - It can inspect up to a certain number of cells in each direction (N, S, E and W).
    - It can perceive its neighbour(as citizen or cops).
    - Agents cop can be eliminated if they are outnumbered by revolting citizen under given conditions.
    
- **Cops**
  
  Cops represent the central authority and are influenced by local behaviour. Cops can:
    - Jail revolting citizen
    - Eliminate excessive revolting citizen based on a threshold(*kill_threshold*).

## Parameters
<p align="center">
  <img src="./images/parameters.PNG" alt="Graph" width="200">
</p>

- **Cop Density** describes the number of cops deployed in the experiment.

- **Citizen Density** describes the number of citizen agents in the scene.

- **Legitimacy** describes how legitimate the central authority acts.

- **Reduction Constant** specifies the constant by which the legitimacy is decreased in an experiment to test different scenarios surrounding it.

- **Active Threshold** specifies the constant by which agents turn from 'calm' state to 'revolt'.

- **Include Wealth** is a toggle switch which provides a way to introduce our wealth parameter in the experiment.

- **Rich Threshold** defines the threshold above which rich will turn active in civil unrest.

## Results

- The grid at one step in the experiment:

   Description of colours agents will take(all agents are circles):
   
    1. Revolt agent will be grey
    2. Cop agent will be black 
    3. Rich class agent will be a tone of sour cherry
    4. Middle class agent will be red
    5. Poor class agent will be yellow
    6. Any agent that gets jailed becomes a black square
    
<p align="center">
  <img src="./images/grid.PNG" alt="Graph" width="400">
</p>

- The grid shows grievance levels of citizen. For display purpose only:
<p align="center">
  <img src="./images/grid2.PNG" alt="Graph" width="400">
</p>

- The graph which shows the grievance and the number of steps: 
<p align="center">
  <img src="./images/grievance.PNG" alt="Graph" width="400">
</p>

## Files
- `agents/authority.py` : Contains Cops/Central authority agent class.
- `agents/citizen.py` : Contains Citizen agent class.
- `utils/gradient.py` : show the grievance levels of agents. Only for display.
- `utils/params.py` : Parameters including sliders and various constants.
- `utils/portrayal.py` : Descriptions of colors agents will take.
- `env.py` : Primary environment in which placement and operations of agents take place.
- `server.py` : Sets up server and visualization.
- `run.py` : Opens the server and port for visualization.


## Repository structure
```shell
.
├── README.md
├── agents
│   ├── __init__.py
│   ├── authority.py
│   └── citizen.py
├── images
│   ├── Graph.png
│   ├── grid.png
│   └── parameters.png
├── utils
│   ├── __init__.py
│   ├── gradient.py
│   ├── params.py
│   └── portrayal.py
├── requirements.txt
└── env.py
└── run.py
└── server.py
```
