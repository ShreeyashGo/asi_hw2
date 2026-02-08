OK_FORMAT = True

test = {
    "name": "Greedy_Hill_Climbing_Tests",
    "points": 20,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [
                # --- CASE 1: Marginal Gain Logic Check ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Create a scenario where the "best individual" node is NOT the best "second" node.
                    >>> # Graph structure:
                    >>> # A -> [1, 2, 3] (A influences 3 nodes)
                    >>> # B -> [1, 2, 3, 4] (B influences 4 nodes) - B is best single seed.
                    >>> # C -> [5, 6, 7] (C influences 3 nodes distinct from A and B)
                    >>> 
                    >>> G = nx.DiGraph()
                    >>> # Add edges with weight 1.0 (deterministic activation)
                    >>> for i in [1, 2, 3]: G.add_edge('A', i, weight=1.0)
                    >>> for i in [1, 2, 3, 4]: G.add_edge('B', i, weight=1.0)
                    >>> for i in [5, 6, 7]: G.add_edge('C', i, weight=1.0)
                    >>> 
                    >>> # Low thresholds to ensure activation
                    >>> thresholds = {n: 0.1 for n in G.nodes()}
                    >>> 
                    >>> # If k=1, B is best (covers 5 nodes: B + 1,2,3,4)
                    >>> seeds_1 = greedy_hill_climbing(G, 1, thresholds)
                    >>> 'B' in seeds_1
                    True
                    >>> 
                    >>> # If k=2, we already have B.
                    >>> # Adding A adds 0 new nodes (subset of B).
                    >>> # Adding C adds 3 new nodes.
                    >>> # So the algorithm MUST pick C, even though A individually is "tied" with C in raw power.
                    >>> seeds_2 = greedy_hill_climbing(G, 2, thresholds)
                    >>> set(seeds_2) == {'B', 'C'}
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Greedy logic failed. Ensure you are calculating marginal gain (New - Current) rather than total spread."
                },

                # --- CASE 2: K-Limit Check ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 2, weight=1.0)
                    >>> G.add_edge(3, 4, weight=1.0)
                    >>> thresholds = {n: 0.1 for n in G.nodes()}
                    >>> 
                    >>> # Request 0 seeds
                    >>> res_0 = greedy_hill_climbing(G, 0, thresholds)
                    >>> len(res_0)
                    0
                    >>> 
                    >>> # Request 2 seeds
                    >>> res_2 = greedy_hill_climbing(G, 2, thresholds)
                    >>> len(res_2)
                    2
                    """,
                    "hidden": False,
                    "failure_message": "Function did not return the correct number of seeds (k)."
                },

                # --- CASE 3: Integration Test (Random Graph) ---
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> random.seed(42)
                    >>> # Generate graph
                    >>> G, node_thresholds = generate_random_graph(num_nodes=20, edge_prob=0.2)
                    >>> 
                    >>> # Run greedy hill climbing
                    >>> seed_nodes = greedy_hill_climbing(G, 5, node_thresholds)
                    >>> 
                    >>> # Check total spread
                    >>> result = linear_threshold(G, seed_set=seed_nodes, node_thresholds=node_thresholds)
                    >>> len(result)
                    18
                    """,
                    "hidden": False,
                    "failure_message": "Integration test failed. Expected 18 activated nodes with seed 42."
                }
            ]
        }
    ]
}