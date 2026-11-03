from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.calculation_agent import CalculationAgent
from verification.verification_agent import VerificationAgent
from core.task_analyzer import TaskAnalyzer
from core.hypergraph import Hypergraph
from memory.memory_manager import MemoryManager


class DHMIFOrchestrator:

    def __init__(self):
        self.analyzer = TaskAnalyzer()
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.calculation_agent = CalculationAgent()
        self.verification_agent = VerificationAgent()
        self.hypergraph = Hypergraph()
        self.memory = MemoryManager()

    def run(self, task):

        print("\n========== DHMIF STARTED ==========")
        print(f"Task: {task}")

        # ==========================================
        # 1. RETRIEVE PREVIOUS CONTEXT
        # ==========================================

        previous_context = self.memory.retrieve(task)

        print("\n========== MEMORY ==========")

        if previous_context:
            print(f"Previous related tasks found: {len(previous_context)}")
        else:
            print("No previous context found.")

        # ==========================================
        # 2. TASK ANALYSIS
        # ==========================================

        analysis = self.analyzer.analyze(task)

        print(f"\nInitial Complexity: {analysis['complexity']}")
        print(f"Initial Confidence: {analysis['confidence']}")
        print(f"Agents selected: {analysis['required_agents']}")

        selected_agents = analysis["required_agents"].copy()

        # ==========================================
        # 3. CREATE HYPERGRAPH
        # ==========================================

        self.hypergraph.add_node("Task", "TASK")

        for agent in selected_agents:
            self.hypergraph.add_node(agent, "AGENT")

        # ==========================================
        # 4. EXECUTE RESEARCH AGENT
        # ==========================================

        results = []

        if "Research Agent" in selected_agents:

            result = self.research_agent.run(task)

            results.append(result)

            print("✓ Research Agent completed")

        # ==========================================
        # 5. EXECUTE ANALYSIS AGENT
        # ==========================================

        if "Analysis Agent" in selected_agents:

            research = results[-1] if results else None

            result = self.analysis_agent.run(
                task,
                research
            )

            results.append(result)

            print("✓ Analysis Agent completed")

        # ==========================================
        # 6. EXECUTE CALCULATION AGENT
        # ==========================================

        if "Calculation Agent" in selected_agents:

            result = self.calculation_agent.run(task)

            results.append(result)

            print("✓ Calculation Agent completed")

        # ==========================================
        # 7. FIRST VERIFICATION
        # ==========================================

        verification = self.verification_agent.verify(results)

        print("\n========== FIRST VERIFICATION ==========")

        print(f"Status: {verification['status']}")
        print(f"Confidence: {verification['confidence']}")

        # ==========================================
        # 8. ADAPTIVE RE-PLANNING
        # ==========================================

        if verification["confidence"] < 0.85:

            print("\n⚠ Confidence below threshold.")
            print("DHMIF is adapting the workflow...")

            if "Research Agent" not in selected_agents:

                selected_agents.append("Research Agent")

                self.hypergraph.add_node(
                    "Research Agent",
                    "AGENT"
                )

                print("→ Adding Research Agent")

                extra_result = self.research_agent.run(
                    f"Verify and investigate: {task}"
                )

                results.append(extra_result)

                print("✓ Additional Research Agent completed")

            # Re-verification

            verification = self.verification_agent.verify(results)

            print("\n========== SECOND VERIFICATION ==========")

            print(f"Status: {verification['status']}")
            print(f"Confidence: {verification['confidence']}")

        # ==========================================
        # 9. CREATE ADAPTIVE HYPEREDGE
        # ==========================================

        self.hypergraph.add_hyperedge(
            "AdaptiveWorkflow",
            ["Task"] + selected_agents
        )

        # ==========================================
        # 10. DISPLAY HYPERGRAPH
        # ==========================================

        self.hypergraph.display()

        # ==========================================
        # 11. STORE RESULT IN MEMORY
        # ==========================================

        self.memory.store(
            task,
            {
                "agents": selected_agents,
                "verification": verification
            }
        )

        print("✓ Task stored in persistent memory")

        # ==========================================
        # 12. COMPLETION
        # ==========================================

        print("\n========== DHMIF COMPLETED ==========\n")

        return {

            "task": task,

            "complexity": analysis["complexity"],

            "agents": selected_agents,

            "results": results,

            "verification": verification

        }