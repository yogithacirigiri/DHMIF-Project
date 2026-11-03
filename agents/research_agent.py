class ResearchAgent:

    def run(self, task):

        result = f"""
Research Agent analyzed the task:

{task}

The task requires gathering relevant information,
identifying important factors, and providing
supporting knowledge for the analysis stage.
"""

        return {
            "agent": "Research Agent",
            "task": task,
            "result": result,
            "confidence": 0.85
        }