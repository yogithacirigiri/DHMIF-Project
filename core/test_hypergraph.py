from hypergraph import Hypergraph


graph = Hypergraph()

# Add nodes
graph.add_node("Task", "TASK")
graph.add_node("ResearchAgent", "AGENT")
graph.add_node("AnalysisAgent", "AGENT")
graph.add_node("VerificationAgent", "AGENT")
graph.add_node("KnowledgeBase", "KNOWLEDGE")

# Create many-to-many relationships
graph.add_hyperedge(
    "H1",
    ["Task", "ResearchAgent", "KnowledgeBase"]
)

graph.add_hyperedge(
    "H2",
    ["Task", "ResearchAgent", "AnalysisAgent"]
)

graph.add_hyperedge(
    "H3",
    ["AnalysisAgent", "VerificationAgent", "KnowledgeBase"]
)

graph.display()