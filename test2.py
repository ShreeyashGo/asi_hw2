OK_FORMAT = True

test = {
    "name": "Independent_Cascade_Tests",
    "points": 15,
    "suites": [
        {
            "type": "doctest",
            "scored": True,
            "setup": "",
            "teardown": "",
            "cases": [
                # --- CASE 1: Deterministic Propagation (Weight = 1.0) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> import random
                    >>> 
                    >>> # Create a chain: 1 -> 2 -> 3 with 100% activation probability
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 2, weight=1.0)
                    >>> G.add_edge(2, 3, weight=1.0)
                    >>> 
                    >>> # Seed 1 should activate 2, which activates 3
                    >>> seeds = [1]
                    >>> result = independent_cascade(G, seeds)
                    >>> 
                    >>> set(result) == {1, 2, 3}
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Failed to propagate influence across edges with 100% probability (weight=1.0)."
                },

                # --- CASE 2: No Propagation (Weight = 0.0) ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> import random
                    >>> 
                    >>> # Create A -> B with 0% activation probability
                    >>> G = nx.DiGraph()
                    >>> G.add_edge('A', 'B', weight=0.0)
                    >>> 
                    >>> seeds = ['A']
                    >>> result = independent_cascade(G, seeds)
                    >>> 
                    >>> # Should contain 'A' (seed) but NOT 'B'
                    >>> 'A' in result
                    True
                    >>> 'B' in result
                    False
                    """,
                    "hidden": False,
                    "failure_message": "Incorrectly activated a node across an edge with 0% probability (weight=0.0)."
                },

                # --- CASE 3: Multiple Seeds Logic ---
                {
                    "code": r"""
                    >>> import networkx as nx
                    >>> # Graph: 1->3 (1.0), 2->4 (1.0)
                    >>> # Disconnected components, multiple seeds
                    >>> G = nx.DiGraph()
                    >>> G.add_edge(1, 3, weight=1.0)
                    >>> G.add_edge(2, 4, weight=1.0)
                    >>> 
                    >>> seeds = [1, 2]
                    >>> result = independent_cascade(G, seeds)
                    >>> 
                    >>> len(result)
                    4
                    >>> set(result) == {1, 2, 3, 4}
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Failed to handle multiple seed nodes correctly."
                },

                # --- CASE 4: Monte Carlo Average Test ---
                {
                    "code": r"""
                    >>> import random
                    >>> import time
                    >>> import networkx as nx
                    >>> 
                    >>> # Perform a statistical test over multiple runs
                    >>> 
                    >>> avg_result = 0
                    >>> num_runs = 50  # 50 runs is sufficient for grading speed
                    >>> 
                    >>> # Use a fixed starting seed for the loop to ensure consistency across grading runs
                    >>> # but allow variation inside the loop
                    >>> random.seed(999) 
                    >>> 
                    >>> for _ in range(num_runs):
                    ...     # Generate graph (dense enough to likely cascade)
                    ...     G, _ = generate_random_graph(num_nodes=100, edge_prob=0.15, mode='independent')
                    ...     
                    ...     # Run IC
                    ...     result = independent_cascade(G, seed_set=[0, 1, 2, 3, 4])
                    ...     avg_result += len(result)
                    >>> 
                    >>> final_avg = avg_result / num_runs
                    >>> 
                    >>> # We expect ~90. We set a loose bound to account for RNG variance.
                    >>> # If logic is broken, this usually drops to < 10 or stays at 5 (seeds only).
                    >>> final_avg > 70
                    True
                    """,
                    "hidden": False,
                    "failure_message": "Monte Carlo simulation failed. The average cascade size was too small, suggesting the propagation logic is broken."
                }
            ]
        }
    ]
}