class Hypergraph:

    def __init__(self):
        self.nodes = {}
        self.hyperedges = {}

    def add_node(self, node_id, node_type, data=None):
        self.nodes[node_id] = {
            "type": node_type,
            "data": data
        }

    def add_hyperedge(self, edge_id, connected_nodes):
        self.hyperedges[edge_id] = connected_nodes

    def display(self):
        print("\n========== DHMIF HYPERGRAPH ==========")

        print("\nNodes:")
        for node_id, node in self.nodes.items():
            print(f"  {node_id} [{node['type']}]")

        print("\nHyperedges:")
        for edge_id, nodes in self.hyperedges.items():
            print(f"  {edge_id}: {' <-> '.join(nodes)}")

        print("======================================\n")