# Modelling civil disobedience using wealth in agents

We are trying to model the grievance behaviour of citizens as a measure of varying parameters such as democracy, wealth, employment and corruption. We would then deduce what amount of central forces are required to control the active agents. We aim to model the agents' behaviour in the presence of cops and how they become active or inactive as a measure of their risk aversion and their surrounding agents' total grievance. Finally, we also try to understand if wealth can also play a role in agents' civil disobedience.

## Table of content

- [Modelling Civil Violence: A Multi Agent Simulation](#modelling-civil-disobedience-using-wealth-in-agents)
- [Implementation Description(Beta)](#implementation-description)
  - [Model Details](#model-details)
- [Files](#files)
- [How To Run](#how-to-run)
- [Repository Structure](#repository-structure)

## Implementation Description

In the present implemenation, there are two main agents(i.e. Citizen and Cops). The task of Citizen is to revolt if the grievance is above a threshold and the task of Cops is to imprison the citizen who are in revolt state. The Cops can also eliminate the citizen based on the number of times it has been imprisoned in the past.

There are three categories in **Citizen** agent(**Poor, Middle, & Rich**) which essentially tell us about the economic status of that agent. Simultaneously, the parameters that affect the Citizen are **Democracy, Employment, Corruption**.

### Model Details

- **Citizen**

  Citizens are the core agents whose behaviour is varied during each time step depending on the change in behaviour of Central authority. The simulation is initially filled with a
  certain population ratio of citizens of varying economic status. The property of Citizen is:
    - It can revolt against the Central Authority
    - The grievance of a citizen is decided by the three global parameters(i.e. Democracy, Employment, Corruption), its economic status, its confidence.
    - It can inspect upto a certain number of cells in each direction (N, S, E and W).
    - It can perceive its neighbor(as citizen or cops)
    
- **Cops**
  
  Cops represent the central authority and are influenced by the local behaviour. Cops can:
    - Jail revolting citizen
    - Elinimate excessive revolting citizen based on a threshold(*kill_threshold*).

## Results

Description of colors agents will take(all agents are circles):
revolt agent will be gray
cop agent will be black
rich class agent will be a tone of sour cherry
middle class agent will be red
poor class agent will be yellow
any agent that gets jailed becomes a black square
colors

## Files
- `agent/authority.py` : Contains Cops/Central authority agent class.
- `agent/env.py` : Primary environment in which placement and operations of agents take place.
- `agent/params.py` : Parameters including sliders and various constants.
- `agent/people.py` : Contains Citizen agent class.
- `agent/server.py` : Sets up server and visualization.
- `run.py` : Opens the server and port for visualization.

## How To Run
> 1. Clone the repository
> 2. Install `requirements.txt` via pip package manager using `$ pip install -r requirements.txt`
> 3. Run using `python run.py`

## Repository structure
```shell
.
├── README.md
├── agent
│   ├── __init__.py
│   ├── authority.py
│   ├── env.py
│   ├── params.py
│   ├── people.py
│   ├── portrayal.py
│   └── server.py
├── requirements.txt
└── run.py
```
