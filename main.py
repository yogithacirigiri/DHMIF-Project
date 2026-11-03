from core.orchestrator import DHMIFOrchestrator


def main():

    dhmif = DHMIFOrchestrator()

    task = input("\nEnter your task: ")

    result = dhmif.run(task)

    print("\nFINAL RESULT")
    print("----------------------------")
    print(f"Task: {result['task']}")
    print(f"Complexity: {result['complexity']}")
    print(f"Agents Used: {', '.join(result['agents'])}")
    print(f"Verification: {result['verification']['status']}")
    print(f"Final Confidence: {result['verification']['confidence']}")


if __name__ == "__main__":
    main()