class VerificationAgent:

    def verify(self, results):

        if not results:
            return {
                "status": "FAILED",
                "confidence": 0.0,
                "message": "No agent results available."
            }

        average_confidence = sum(
            result["confidence"] for result in results
        ) / len(results)

        if average_confidence >= 0.70:
            status = "PASSED"
        else:
            status = "REQUIRES_REVIEW"

        return {
            "status": status,
            "confidence": round(average_confidence, 2),
            "agents_verified": len(results)
        }