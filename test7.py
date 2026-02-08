OK_FORMAT = True

test = {
    "name": "Load_Flu_Graph_Tests",
    "points": 5,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [

                # --------------------------------------------------
                # CASE 1: Normal Scenario – Edge Weight Bounds
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> random.seed(42)
                    >>> G, thresholds = load_flu_graph('flu.txt', scenario='normal')
                    >>> 
                    >>> edges = list(G.edges(data=True))
                    >>> sampled_edges = random.sample(edges, min(50, len(edges)))
                    >>> 
                    >>> # All sampled edge weights must be valid probabilities
                    >>> all(0.0 <= data['weight'] <= 1.0 for _, _, data in sampled_edges)
                    True
                    >>> 
                    >>> # Mean probability is clipped to [0.01, 0.2]
                    >>> # Therefore sampled weights should never exceed 1.5 * 0.2 = 0.3
                    >>> all(data['weight'] <= 0.3 for _, _, data in sampled_edges)
                    True
                    """,
                    "hidden": False,
                    "failure_message": (
                        "Normal scenario: sampled edge weights are out of expected bounds "
                        "or do not respect the clipped mean probability."
                    )
                },

                # --------------------------------------------------
                # CASE 2: Mitigation Scenario – Scaling Applied
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> import random
                    >>> random.seed(42)
                    >>> G_normal, _ = load_flu_graph('flu.txt', scenario='normal')
                    >>> random.seed(42)
                    >>> G_mitigate, _ = load_flu_graph('flu.txt', scenario='mitigation')
                    >>> 
                    >>> normal_edges = list(G_normal.edges(data=True))
                    >>> mitigate_edges = list(G_mitigate.edges(data=True))
                    >>> 
                    >>> idxs = random.sample(range(len(normal_edges)), min(50, len(normal_edges)))
                    >>> 
                    >>> # Mitigation weights should be strictly smaller
                    >>> all(
                    ...     mitigate_edges[i][2]['weight'] < normal_edges[i][2]['weight']
                    ...     for i in idxs
                    ... )
                    True
                    """,
                    "hidden": False,
                    "failure_message": (
                        "Mitigation scenario: sampled edge weights are not properly scaled down."
                    )
                },

                # --------------------------------------------------
                # CASE 3: Mitigation Scaling Factor (≈ 0.3)
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> import random
                    >>> random.seed(123)
                    >>> G_normal, _ = load_flu_graph('flu.txt', scenario='normal')
                    >>> random.seed(123)
                    >>> G_mitigate, _ = load_flu_graph('flu.txt', scenario='mitigation')
                    >>> 
                    >>> edges = list(G_normal.edges())
                    >>> sampled_edges = random.sample(edges, min(50, len(edges)))
                    >>> 
                    >>> ratios = [
                    ...     G_mitigate[u][v]['weight'] / G_normal[u][v]['weight']
                    ...     for u, v in sampled_edges
                    ...     if G_normal[u][v]['weight'] > 0
                    ... ]
                    >>> 
                    >>> all(0.25 <= r <= 0.35 for r in ratios)
                    True
                    """,
                    "hidden": False,
                    "failure_message": (
                        "Mitigation scaling factor is incorrect. Expected approximately 0.3×."
                    )
                },

                # --------------------------------------------------
                # CASE 4: Node Thresholds
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> import random
                    >>> random.seed(99)
                    >>> G, thresholds = load_flu_graph('flu.txt')
                    >>> 
                    >>> nodes = list(G.nodes())
                    >>> sampled_nodes = random.sample(nodes, min(50, len(nodes)))
                    >>> 
                    >>> # One threshold per sampled node
                    >>> all(n in thresholds for n in sampled_nodes)
                    True
                    >>> 
                    >>> # Thresholds must be valid probabilities
                    >>> all(0.0 <= thresholds[n] <= 1.0 for n in sampled_nodes)
                    True
                    """,
                    "hidden": False,
                    "failure_message": (
                        "Node thresholds are missing or outside the [0, 1] range."
                    )
                }
            ]
        }
    ]
}
