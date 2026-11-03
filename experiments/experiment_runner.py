import sys
import os
import time
import csv

# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from agents.analysis_agent import AnalysisAgent
from agents.research_agent import ResearchAgent
from agents.calculation_agent import CalculationAgent
from verification.verification_agent import VerificationAgent
from core.orchestrator import DHMIFOrchestrator


# ============================================================
# 30 EXPERIMENT TASKS
# ============================================================

tasks = [

    # LOW COMPLEXITY
    ("L01", "Explain artificial intelligence."),
    ("L02", "Explain machine learning."),
    ("L03", "What is deep learning?"),
    ("L04", "Explain cloud computing."),
    ("L05", "What is data science?"),
    ("L06", "Explain neural networks."),
    ("L07", "What is natural language processing?"),
    ("L08", "Explain computer vision."),
    ("L09", "What is an autonomous agent?"),
    ("L10", "Explain cybersecurity."),

    # MEDIUM COMPLEXITY
    ("M01", "Analyze the impact of artificial intelligence on education."),
    ("M02", "Compare supervised and unsupervised machine learning."),
    ("M03", "Evaluate the advantages of cloud computing."),
    ("M04", "Analyze the challenges of data privacy."),
    ("M05", "Compare traditional AI systems and agentic AI."),
    ("M06", "Evaluate the role of machine learning in healthcare."),
    ("M07", "Analyze the effects of automation on employment."),
    ("M08", "Compare centralized and decentralized systems."),
    ("M09", "Evaluate the performance of machine learning models."),
    ("M10", "Analyze the role of natural language processing."),

    # HIGH COMPLEXITY
    ("H01", "Design a distributed multi-agent system for intelligent task execution."),
    ("H02", "Design an adaptive AI architecture with dynamic workflow optimization."),
    ("H03", "Analyze and evaluate scalability of a distributed multi-agent framework."),
    ("H04", "Design a multi-agent system including memory, verification, and self-reflection."),
    ("H05", "Evaluate performance and accuracy of an adaptive intelligent workflow."),
    ("H06", "Design a secure distributed AI system including privacy and verification."),
    ("H07", "Develop an architecture for dynamic agent selection and workflow optimization."),
    ("H08", "Design a scalable multi-agent framework for complex reasoning tasks."),
    ("H09", "Evaluate consistency and reliability of distributed agent reasoning."),
    ("H10", "Design and evaluate a hypergraph-based multi-agent reasoning system.")
]


# ============================================================
# SINGLE AGENT
# ============================================================

def run_single_agent(task):

    agent = AnalysisAgent()

    start_time = time.perf_counter()

    result = agent.run(task)

    elapsed_time = (
        time.perf_counter() - start_time
    ) * 1000

    verification = VerificationAgent().verify([result])

    return {
        "verification": verification,
        "confidence": verification["confidence"],
        "agents": 1,
        "adapted": 0,
        "time_ms": elapsed_time
    }


# ============================================================
# STATIC MULTI-AGENT
# ============================================================

def run_static_multi_agent(task):

    research_agent = ResearchAgent()
    analysis_agent = AnalysisAgent()
    calculation_agent = CalculationAgent()
    verification_agent = VerificationAgent()

    start_time = time.perf_counter()

    research_result = research_agent.run(task)

    analysis_result = analysis_agent.run(
        task,
        research_result
    )

    calculation_result = calculation_agent.run(task)

    results = [
        research_result,
        analysis_result,
        calculation_result
    ]

    verification = verification_agent.verify(results)

    elapsed_time = (
        time.perf_counter() - start_time
    ) * 1000

    return {
        "verification": verification,
        "confidence": verification["confidence"],
        "agents": 4,
        "adapted": 0,
        "time_ms": elapsed_time
    }


# ============================================================
# DHMIF
# ============================================================

def run_dhmif(task):

    dhmif = DHMIFOrchestrator()

    start_time = time.perf_counter()

    result = dhmif.run(task)

    elapsed_time = (
        time.perf_counter() - start_time
    ) * 1000

    # Determine initial confidence from complexity
    if result["complexity"] == "LOW":
        initial_confidence = 0.90

    elif result["complexity"] == "MEDIUM":
        initial_confidence = 0.75

    else:
        initial_confidence = 0.60

    final_confidence = result["verification"]["confidence"]

    adapted = (
        1
        if final_confidence != initial_confidence
        else 0
    )

    return {
        "verification": result["verification"],
        "confidence": final_confidence,
        "agents": len(result["agents"]),
        "adapted": adapted,
        "time_ms": elapsed_time
    }


# ============================================================
# RUN EXPERIMENT
# ============================================================

results = []

print("\n")
print("=" * 70)
print("DHMIF EXPERIMENT")
print("=" * 70)

print(f"\nTotal tasks: {len(tasks)}")

print("\nSystems compared:")
print("1. Single Agent")
print("2. Static Multi-Agent")
print("3. DHMIF")


# ============================================================
# PROCESS ALL TASKS
# ============================================================

for task_id, task in tasks:

    print("\n")
    print("-" * 70)
    print(f"Task {task_id}: {task}")
    print("-" * 70)

    # -------------------------
    # Single Agent
    # -------------------------

    single = run_single_agent(task)

    print(
        f"Single Agent -> "
        f"Confidence: {single['confidence']:.2f}, "
        f"Time: {single['time_ms']:.6f} ms"
    )

    results.append([
        task_id,
        "Single Agent",
        single["verification"]["status"],
        single["confidence"],
        single["agents"],
        single["adapted"],
        single["time_ms"]
    ])


    # -------------------------
    # Static Multi-Agent
    # -------------------------

    static = run_static_multi_agent(task)

    print(
        f"Static Multi-Agent -> "
        f"Confidence: {static['confidence']:.2f}, "
        f"Time: {static['time_ms']:.6f} ms"
    )

    results.append([
        task_id,
        "Static Multi-Agent",
        static["verification"]["status"],
        static["confidence"],
        static["agents"],
        static["adapted"],
        static["time_ms"]
    ])


    # -------------------------
    # DHMIF
    # -------------------------

    dhmif = run_dhmif(task)

    print(
        f"DHMIF -> "
        f"Confidence: {dhmif['confidence']:.2f}, "
        f"Agents: {dhmif['agents']}, "
        f"Time: {dhmif['time_ms']:.6f} ms, "
        f"Adapted: {dhmif['adapted']}"
    )

    results.append([
        task_id,
        "DHMIF",
        dhmif["verification"]["status"],
        dhmif["confidence"],
        dhmif["agents"],
        dhmif["adapted"],
        dhmif["time_ms"]
    ])


# ============================================================
# SAVE CSV
# ============================================================

output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dhmif_experiment_results.csv"
)

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Task_ID",
        "System",
        "Verification_Status",
        "Confidence",
        "Average_Agents",
        "Adapted",
        "Execution_Time_ms"
    ])

    writer.writerows(results)


# ============================================================
# OVERALL RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("OVERALL EXPERIMENT SUMMARY")
print("=" * 70)

systems = [
    "Single Agent",
    "Static Multi-Agent",
    "DHMIF"
]

for system in systems:

    system_results = [
        row
        for row in results
        if row[1] == system
    ]

    verification_rate = (
        sum(
            1
            for row in system_results
            if row[2] == "PASSED"
        )
        / len(system_results)
        * 100
    )

    average_confidence = (
        sum(row[3] for row in system_results)
        / len(system_results)
    )

    average_agents = (
        sum(row[4] for row in system_results)
        / len(system_results)
    )

    adaptation_rate = (
        sum(row[5] for row in system_results)
        / len(system_results)
        * 100
    )

    average_time = (
        sum(row[6] for row in system_results)
        / len(system_results)
    )

    print(f"\n{system}")

    print(
        f"Verification Rate : "
        f"{verification_rate:.2f}%"
    )

    print(
        f"Average Confidence: "
        f"{average_confidence:.3f}"
    )

    print(
        f"Average Time      : "
        f"{average_time:.6f} ms"
    )

    print(
        f"Average Agents    : "
        f"{average_agents:.2f}"
    )

    print(
        f"Adaptation Rate   : "
        f"{adaptation_rate:.2f}%"
    )


# ============================================================
# COMPLEXITY-WISE DHMIF RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("COMPLEXITY-WISE DHMIF RESULTS")
print("=" * 70)


complexity_groups = {

    "LOW": [
        f"L{i:02d}"
        for i in range(1, 11)
    ],

    "MEDIUM": [
        f"M{i:02d}"
        for i in range(1, 11)
    ],

    "HIGH": [
        f"H{i:02d}"
        for i in range(1, 11)
    ]
}


for complexity, task_ids in complexity_groups.items():

    dhmif_results = [

        row
        for row in results

        if row[0] in task_ids
        and row[1] == "DHMIF"

    ]

    verification_rate = (

        sum(
            1
            for row in dhmif_results
            if row[2] == "PASSED"
        )

        / len(dhmif_results)
        * 100
    )


    average_confidence = (

        sum(
            row[3]
            for row in dhmif_results
        )

        / len(dhmif_results)
    )


    average_agents = (

        sum(
            row[4]
            for row in dhmif_results
        )

        / len(dhmif_results)
    )


    adaptation_rate = (

        sum(
            row[5]
            for row in dhmif_results
        )

        / len(dhmif_results)
        * 100
    )


    average_time = (

        sum(
            row[6]
            for row in dhmif_results
        )

        / len(dhmif_results)
    )


    print("\n")
    print(f"{complexity} COMPLEXITY")

    print(
        f"Verification Rate : "
        f"{verification_rate:.2f}%"
    )

    print(
        f"Average Confidence: "
        f"{average_confidence:.3f}"
    )

    print(
        f"Average Agents    : "
        f"{average_agents:.2f}"
    )

    print(
        f"Adaptation Rate   : "
        f"{adaptation_rate:.2f}%"
    )

    print(
        f"Average Time      : "
        f"{average_time:.6f} ms"
    )


# ============================================================
# FINISHED
# ============================================================

print("\n")
print("=" * 70)
print("EXPERIMENT COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nCSV file:")
print(output_file)

print("\n")