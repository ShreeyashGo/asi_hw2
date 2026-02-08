OK_FORMAT = True

test = {
    "name": "Greedy_Weighted_Degree_Tests",
    "points": 20,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [
                # --- CASE 1: Logic Verification (Sorting by Weighted Degree) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> 
                    >>> # Create a graph with distinct weighted out-degrees
                    >>> G = nx.DiGraph()
                    >>> # Node 1: Out-degree sum = 0.5 + 0.4 = 0.9
                    >>> G.add_edge(1, 2, weight=0.5)
                    >>> G.add_edge(1, 3, weight=0.4)
                    >>> 
                    >>> # Node 2: Out-degree sum = 0.2
                    >>> G.add_edge(2, 3, weight=0.2)
                    >>> 
                    >>> # Node 3: Out-degree sum = 5.0 (Highest)
                    >>> G.add_edge(3, 1, weight=5.0)
                    >>> 
                    >>> # Expected Order: 
                    >>> # 1. Node 3 (weight 5.0)
                    >>> # 2. Node 1 (weight 0.9)
                    >>> # 3. Node 2 (weight 0.2)
                    >>> 
                    >>> # Test k=1 (Should get top node)
                    >>> greedy_weighted_degree(G, 1)
                    [3]
                    >>> 
                    >>> # Test k=2 (Should get top 2 nodes in order)
                    >>> greedy_weighted_degree(G, 2)
                    [3, 1]
                    >>> 
                    >>> # Test k=3 (All nodes)
                    >>> greedy_weighted_degree(G, 3)
                    [3, 1, 2]
                    """,
                    "hidden": False,
                    "failure_message": "Failed to correctly sort nodes by weighted out-degree."
                },

                # --- CASE 2: Edge Cases (k=0, k > N) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 2, weight=1.0)
                    >>> 
                    >>> # k = 0 should return empty list
                    >>> greedy_weighted_degree(G, 0)
                    []
                    >>> 
                    >>> # k > num_nodes should return all nodes
                    >>> # (Sorting behavior handles the slice safely)
                    >>> res = greedy_weighted_degree(G, 100)
                    >>> len(res)
                    2
                    >>> set(res) == {1, 2}
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Failed to handle edge cases (k=0 or k > number of nodes)."
                },

                # --- CASE 3: Integration Test (Random Graph + Linear Threshold) ---
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> random.seed(42)
                    >>> # Assuming generate_random_graph is defined in your notebook
                    >>> G, node_thresholds = generate_random_graph(num_nodes=20, edge_prob=0.2)
                    >>> k = 5
                    >>> 
                    >>> # Select seeds
                    >>> seed_nodes = greedy_weighted_degree(G, k)
                    >>> 
                    >>> # Check resulting spread using linear_threshold
                    >>> result = linear_threshold(G, seed_set=seed_nodes, node_thresholds=node_thresholds)
                    >>> 
                    >>> len(result)
                    14
                    """,
                    "hidden": False,
                    "failure_message": "Integration test failed. Expected 14 activated nodes with seed 42."
                }
            ]
        }
    ]
}