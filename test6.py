OK_FORMAT = True

test = {
    "name": "Load_Hospital_Graph_Tests",
    "points": 5,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [

                # --------------------------------------------------
                # CASE 1: Normal Scenario – Edge Weight Ranges
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> import random
                    >>> import networkx as nx
                    >>> 
                    >>> G, thresholds = load_hospital_graph('hospital.txt', scenario='normal', normalize=False)
                    >>> 
                    >>> # All edge weights should be in [0.4, 1.0] before normalization
                    >>> all(0.4 <= data['weight'] <= 1.0 for _, _, data in G.edges(data=True))
                    True
                    >>> 
                    >>> # Thresholds should be between 0 and 1
                    >>> all(0.0 <= t <= 1.0 for t in thresholds.values())
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Normal scenario: edge weights or thresholds are out of expected range."
                },

                # --------------------------------------------------
                # CASE 2: Lockdown Scenario – Edge Weight Regimes
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> random.seed(42)
                    >>> G, thresholds = load_hospital_graph('hospital.txt', scenario='lockdown', normalize=False)
                    >>> 
                    >>> def is_clinical_pair(u, v):
                    ...     return {G.nodes[u]['occupation'], G.nodes[v]['occupation']}.issubset({'MED', 'NUR'})
                    >>> 
                    >>> low_edges = []
                    >>> high_edges = []
                    >>> 
                    >>> for u, v, data in G.edges(data=True):
                    ...     if is_clinical_pair(u, v):
                    ...         low_edges.append(data['weight'])
                    ...     else:
                    ...         high_edges.append(data['weight'])
                    >>> 
                    >>> # Clinical-clinical edges should be low
                    >>> all(0.00 <= w <= 0.25 for w in low_edges)
                    True
                    >>> 
                    >>> # Others should be relatively high
                    >>> all(0.4 <= w <= 1.0 for w in high_edges)
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Lockdown scenario: incorrect edge weight regimes."
                },

                # --------------------------------------------------
                # CASE 3: Incoming Edge Normalization
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> random.seed(42)
                    >>> G, thresholds = load_hospital_graph('hospital.txt', scenario='lockdown')
                    >>>
                    >>> for node in G.nodes():
                    ...     in_edges = list(G.in_edges(node, data=True))
                    ...     total = sum(data['weight'] for _, _, data in in_edges)
                    ...     if len(in_edges) > 1:
                    ...         # Allow small floating point error
                    ...         assert abs(total - 1.0) < 1e-6 or total < 1.0 
                    """,
                    "hidden": False,
                    "failure_message": "Incoming edges are not properly normalized."
                },

                # --------------------------------------------------
                # CASE 4: Lockdown Threshold Assignment
                # --------------------------------------------------
                {
                    "code": r"""
                    >>> random.seed(42)
                    >>> G, thresholds = load_hospital_graph('hospital.txt', scenario='lockdown')
                    >>> 
                    >>> for node, data in G.nodes(data=True):
                    ...     t = thresholds[node]
                    ...     if data['occupation'] in ['MED', 'NUR', 'ADM']:
                    ...         assert 0.7 <= t <= 1.0
                    ...     else:  # PAT
                    ...         assert 0.3 <= t <= 0.6
                    """,
                    "hidden": False,
                    "failure_message": "Lockdown thresholds do not match occupation-based rules."
                }
            ]
        }
    ]
}