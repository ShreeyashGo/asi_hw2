OK_FORMAT = True

test = {
    "name": "Linear_Threshold_Model_Tests",
    "points": 10,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [
                # --- CASE 1: Direct Activation (Sanity Check) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 2, weight=0.6)
                    >>> thresholds = {1: 1.0, 2: 0.5}
                    >>> seeds = [1]
                    >>> 
                    >>> # 0.6 > 0.5, so 2 should activate
                    >>> result = linear_threshold(G, seeds, thresholds)
                    >>> 1 in result and 2 in result
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Direct activation failed (Weight > Threshold)."
                },

                # --- CASE 2: Insufficient Influence ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 2, weight=0.3)
                    >>> thresholds = {1: 1.0, 2: 0.5}
                    >>> seeds = [1]
                    >>> 
                    >>> # 0.3 < 0.5, so 2 should NOT activate
                    >>> result = linear_threshold(G, seeds, thresholds)
                    >>> 2 in result
                    False
                    """,
                    "hidden": False,
                    "failure_message": "Node activated incorrectly (Weight < Threshold)."
                },

                # --- CASE 3: Cumulative Influence (Summing Neighbors) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> G = nx.DiGraph()
                    >>> G.add_edge('A', 'C', weight=0.4)
                    >>> G.add_edge('B', 'C', weight=0.4)
                    >>> thresholds = {'A': 1.0, 'B': 1.0, 'C': 0.7}
                    >>> 
                    >>> # A+B = 0.8 >= 0.7. C should activate.
                    >>> result = linear_threshold(G, ['A', 'B'], thresholds)
                    >>> 'C' in result
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Cumulative influence failed. Weights from multiple neighbors were not summed correctly."
                },

                # --- CASE 4: Cascade (Chain Reaction) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 2, weight=1.0)
                    >>> G.add_edge(2, 3, weight=1.0)
                    >>> thresholds = {1: 0.5, 2: 0.5, 3: 0.5}
                    >>> 
                    >>> # 1 activates 2, 2 activates 3
                    >>> result = linear_threshold(G, [1], thresholds)
                    >>> 3 in result
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Cascading influence failed (1->2->3)."
                },

                # --- CASE 5: Randomized Integration Test 1 (Seed 12) ---
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> random.seed(12)
                    >>> G, node_threshold = generate_random_graph(num_nodes=70, edge_prob=0.2)
                    >>> result = linear_threshold(G, seed_set=[0, 1, 2, 3, 4], node_thresholds=node_threshold)
                    >>> 
                    >>> len(result)
                    69
                    >>> 12 in result
                    False
                    """,
                    "hidden": False,
                    "failure_message": "Randomized Graph Test 1 (Seed 12) failed. Expected 69 activated nodes and node 12 to remain inactive."
                },

                # --- CASE 6: Randomized Integration Test 2 (Isolated Seed Node) ---
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> random.seed(10)
                    >>> G, node_threshold = generate_random_graph(num_nodes=15, edge_prob=0.25)
                    >>> 
                    >>> # Force node 7 to be isolated (no incoming or outgoing edges)
                    >>> G.remove_edges_from(list(G.in_edges(7)))
                    >>> G.remove_edges_from(list(G.out_edges(7)))
                    >>> 
                    >>> result = linear_threshold(G, seed_set=[7], node_thresholds=node_threshold)
                    >>> 
                    >>> len(result)
                    1
                    >>> 7 in result
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Isolated seed node should not activate any other nodes."
                }

            ]
        }
    ]
}