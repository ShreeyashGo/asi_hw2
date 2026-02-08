OK_FORMAT = True

test = {
    "name": "LP_Linear_Threshold_Tests",
    "points": 10,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [

                # --- CASE 1: Single Chain Full Cascade ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Chain: 0 -> 1 -> 2 -> 3 (deterministic)
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(0, 1, weight=1.0)
                    >>> G.add_edge(1, 2, weight=1.0)
                    >>> G.add_edge(2, 3, weight=1.0)
                    >>> 
                    >>> node_thresholds = {0: 0.01, 1: 1.0, 2: 1.0, 3: 1.0}
                    >>> 
                    >>> seeds = lp_linear_threshold(G, seed_budget=1, time_steps=3, node_thresholds=node_thresholds)
                    >>> 
                    >>> set(seeds)
                    {0}
                    """,
                    "hidden": False,
                    "failure_message": "LP failed to select the correct seed for full cascade in a simple chain graph."
                },

                # --- CASE 2: No Propagation Possible ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Graph with isolated nodes only
                    >>> G = nx.DiGraph()
                    >>> G.add_nodes_from([0, 1, 2])
                    >>> 
                    >>> node_thresholds = {0: 0.01, 1: 1.0, 2: 1.0}
                    >>> 
                    >>> seeds = lp_linear_threshold(G, seed_budget=1, time_steps=2, node_thresholds=node_thresholds)
                    >>> 
                    >>> len(seeds)
                    1
                    """,
                    "hidden": False,
                    "failure_message": "LP should select exactly one seed when no propagation is possible."
                },

                # --- CASE 3: Budget Enforcement ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Two separate chains
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(0, 1, weight=1.0)
                    >>> G.add_edge(2, 3, weight=1.0)
                    >>> 
                    >>> node_thresholds = {0: 0.1, 1: 1.0, 2: 0.1, 3: 1.0}
                    >>> 
                    >>> seeds = lp_linear_threshold(G, seed_budget=1, time_steps=2, node_thresholds=node_thresholds)
                    >>> 
                    >>> len(seeds)
                    1
                    """,
                    "hidden": False,
                    "failure_message": "LP violated the seed budget constraint."
                },

                # --- CASE 4: Multi-Step Propagation Required ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Longer chain requires multiple timesteps
                    >>> G = nx.DiGraph()
                    >>> for i in range(5):
                    ...     G.add_edge(i, i+1, weight=1.0)
                    >>> 
                    >>> node_thresholds = {i: (0.01 if i == 0 else 1.0) for i in range(6)}
                    >>> 
                    >>> seeds = lp_linear_threshold(G, seed_budget=1, time_steps=5, node_thresholds=node_thresholds)
                    >>> 
                    >>> set(seeds)
                    {0}
                    """,
                    "hidden": False,
                    "failure_message": "LP failed to propagate influence across multiple time steps."
                },

                # --- CASE 5: Weighted Threshold Logic ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Node 2 requires combined influence from 0 and 1
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(0, 2, weight=0.5)
                    >>> G.add_edge(1, 2, weight=0.5)
                    >>> 
                    >>> node_thresholds = {0: 0.01, 1: 0.01, 2: 1.0}
                    >>> 
                    >>> seeds = lp_linear_threshold(G, seed_budget=2, time_steps=1, node_thresholds=node_thresholds)
                    >>> 
                    >>> set(seeds) == {0, 1}
                    True
                    """,
                    "hidden": False,
                    "failure_message": "LP failed to enforce weighted threshold activation correctly."
                },

                # --- CASE 6: Randomized Small Graph Sanity Check ---
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> random.seed(42)
                    >>> G, node_thresholds = generate_random_graph(num_nodes=12, edge_prob=0.3)
                    >>> 
                    >>> seeds = lp_linear_threshold(G, seed_budget=2, time_steps=3, node_thresholds=node_thresholds)
                    >>> 
                    >>> len(seeds) <= 2
                    True
                    """,
                    "hidden": False,
                    "failure_message": "LP returned more seeds than allowed by the budget."
                }

            ]
        }
    ]
}
