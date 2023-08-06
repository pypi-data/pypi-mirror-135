# Qatalyst Package

## What is Qatalyst?

The Qatalyst software product from Quantum Computing Inc. (QCI) consists 
of a fast, quantum-ready solver for constrained-optimization problems and 
a collection of compute-intense (NP-hard) graph algorithms (QGraph).  
Most of this software runs as a service in the cloud
but a small portion of the software, this package, runs on a user's client system.  
The APIs are Python3-based.

Python API to the QCI cloud service.

## Fundamental Components

There are two basic components in Qatalyst: 

1. The **Core** module that handles constrained optimizations problems with binary variables and 
2. **QGraph**, an extension of the popular [NetworkX](https://networkx.github.io/) package.  

### Qatalyst Core 

A Python API to submit QUBO and constrained optimization problems to the Qatalyst cloud service. 
A sampler will be called in the server based on user input. The default sampler is 
QCI's `csample` tabu solver. 

**Available interfaces**

* `sample_lagrange_optimization`: Given `C` and `A` as in `sample_constraint_problem`, this algorithm optimizes Lagrangian multiplier, `constraint_penalties`, in 
order to return solutions that provide near-optimal cost while simultaneously satisfying the constraints. 
* `sample_constraint_problem`: An objective function, `C`, constrained by a system of linear equations, `A`, the two can be combined to form a QUBO,  
`Q = C + constraint_penalties * A^t A + offset`. The Lagrangian multiplier,`constraint_penalties`, balances the importance of the constraints and the objective function and must be chosen so that both the constraints are satisfied while also minimizing the objective.
* `sample_qubo`: Given a quadratic unconstrained binary optimization (QUBO) problem [[1]](#1) in the form of a symmetric matrix or Python dictionary, the sampler returns minimum or near-minimal energy solutions.

### QGraph

A Python API to submit compute-intense graph problems to the Qatalyst cloud service. 

**Available interfaces**

* `community_detection`: Partition the vertices of a graph `G` into `num_communities` communities using a *modularity metric* [[2]](#2) and [[3]](#3).
* `minumum_clique_cover`: In graph theory, a clique cover or partition into cliques of a given undirected graph is a 
partition of the vertices in the graph into cliques, which form subsets of vertices where every two vertices are adjacent [[4]](#4). A minimum clique cover is a clique cover that uses as few cliques as possible. 
* `partition`: For a fixed integer `num_partitions`, the graph partitioning problem is to find a 
  partition of the vertex set `V` into `num_partitions` equal parts such that the number
  of cut edges is minimized [[5]](#5).  

## Documentation

The Qatalyst documentation is visible at `https://docs.qci-prod.com/`.

## Installation

### Dependencies

Standard Python numeric libraries 
([NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [NetworkX](https://networkx.github.io/), 
plus `requests` and `PyYAML`. See the Dependencies section of the online docs for details or the `requirements.txt` file.

### Installation

* `pip3 install qatalyst`

## Usage

Qatalyst aims to provide a minimal interface for the user. The following examples demonstrate how to use `qgraph` and `qatalyst core`.

For a QUBO problem, the following will send the (symmetric) objective function, `obj`, to the cloud service to sample solutions. We ask for 10 solutions 
to be returned in the `response` object by specifying `num_solutions=10`.

```python
import numpy as np
from qatalyst import qcore

obj = np.array([[-6, 10, 0, 0], 
                [10, -8, 2, 8], 
                [0, 2, -3, 4], 
                [0, 8, 4, -5]])

resp = qcore.sample_qubo(obj, num_solutions=10)

# Result
# samples
# [[1. 0. 0. 1.]
# [1. 0. 1. 0.]
# ...
# [0. 0. 1. 1.]]
# energies
# [-11.  -9.  -8.  -7.  -6.  -6.  -5.  -3.   0.   0.]
# counts
# [1 1 1 1 1 1 1 1 1 1]
```

Given a NetworkX graph, `G`, we show the use of the `partition` function, with `num_partitions` set to 2.

```python
import networkx as nx
from qatalyst import qgraph as qg

G = nx.barbell_graph(4, 2)

resp = qg.partition(G, num_partitions=2)

# GraphResult
# samples
# [{'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 0, '7': 0, '8': 0, '9': 0}, ..., 
#  {'0': 1, '1': 1, '2': 1, '3': 0, '4': 0, '5': 0, '6': 0, '7': 1, '8': 1, '9': 1}]
# energies
# [-48 -48]
# counts
# [ 684 1812]
```
Since the graph is a barbell graph there are two symmetric, optimal solutions with identical energy.

## License

This software is a Python client enabling access to the cloud-resident Qatalyst service.
Both the client and the service are licensed to users and organizations under the terms
of the End-User License Agreement, a copy of which is visible in this package or in the
online documentation.

## References
<a id="1">[1]</a> 
Fred Glover, Gary Kochenberger, and Yu Du, "Quantum Bridge Analytics I: A Tutorial on Formulating and Using QUBO Models", arXiv:1811.11538, 2018.

<a id="2">[2]</a> 
M. E. J. Newman, "Modularity and community structure in networks",
PNAS June 6, 2006 103 (23) 8577-8582; https://doi.org/10.1073/pnas.0601602103.  

<a id="3">[3]</a>
Christian Negre, Hayato Ushijima-Mwesigwa, and Susan M. Mniszewski, "Detecting Multiple Communities Using Quantum Annealing on the D-Wave System", arXiv:1901.09756v1, 2019.

<a id="4">[4]</a>
R. Dridi, H. Alghassi, "Homology computation of large point clouds using quantum annealing", arXiv:1512.09328v3, 2016.

<a id="5">[5]</a>
Andrew Lucas, "Ising formulations of many NP problems". Frontiers in Physics, Volume 2, Article 5, 2014.

