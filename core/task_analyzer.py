class TaskAnalyzer:

    def analyze(self, task):

        task_lower = task.lower()

        # HIGH complexity:
        # Multiple requirements, architecture/design,
        # distributed systems, scalability, or complex evaluation.
        high_keywords = [
            "design",
            "architecture",
            "distributed",
            "multi-agent",
            "scalability",
            "framework",
            "optimize",
            "optimization",
            "implementation",
            "evaluate and compare",
            "multiple",
            "including",
            "consistency",
            "performance and",
            "accuracy and",
            "privacy and security"
        ]

        # MEDIUM complexity:
        # Analysis, comparison, evaluation, impact studies, etc.
        medium_keywords = [
            "analyze",
            "analysis",
            "compare",
            "comparison",
            "evaluate",
            "evaluation",
            "impact",
            "advantages",
            "disadvantages",
            "challenges",
            "predict",
            "prediction",
            "role",
            "effects"
        ]

        # LOW complexity:
        # Simple explanations or definitions.
        low_keywords = [
            "what is",
            "define",
            "explain",
            "meaning",
            "list",
            "name"
        ]

        # Determine complexity
        if any(keyword in task_lower for keyword in high_keywords):
            complexity = "HIGH"

        elif any(keyword in task_lower for keyword in medium_keywords):
            complexity = "MEDIUM"

        elif any(keyword in task_lower for keyword in low_keywords):
            complexity = "LOW"

        else:
            # Fallback based on task length
            words = task_lower.split()

            if len(words) <= 8:
                complexity = "LOW"
            elif len(words) <= 18:
                complexity = "MEDIUM"
            else:
                complexity = "HIGH"

        # Select agents dynamically
        required_agents = []

        if any(word in task_lower for word in [
            "research",
            "explain",
            "information",
            "education",
            "privacy",
            "impact",
            "background",
            "challenges",
            "advantages",
            "disadvantages"
        ]):
            required_agents.append("Research Agent")

        if any(word in task_lower for word in [
            "analyze",
            "analysis",
            "compare",
            "comparison",
            "evaluate",
            "evaluation",
            "design",
            "system",
            "architecture",
            "performance",
            "prediction",
            "predict",
            "role",
            "impact"
        ]):
            required_agents.append("Analysis Agent")

        if any(word in task_lower for word in [
            "calculate",
            "calculation",
            "number",
            "metric",
            "metrics",
            "percentage",
            "accuracy",
            "score",
            "performance"
        ]):
            required_agents.append("Calculation Agent")

        # Verification is always included
        required_agents.append("Verification Agent")

        # Remove duplicates while preserving order
        required_agents = list(dict.fromkeys(required_agents))

        # Initial confidence based on estimated complexity
        if complexity == "LOW":
            confidence = 0.90

        elif complexity == "MEDIUM":
            confidence = 0.75

        else:
            confidence = 0.60

        return {
            "task": task,
            "complexity": complexity,
            "required_agents": required_agents,
            "confidence": confidence
        }