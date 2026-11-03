class CalculationAgent:

    def run(self, task):
        return {
            "agent": "Calculation Agent",
            "task": task,
            "result": f"Calculation completed for: {task}",
            "confidence": 0.90
        }