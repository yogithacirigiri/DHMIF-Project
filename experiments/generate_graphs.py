import csv
import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# ============================================================
# LOAD EXPERIMENT RESULTS
# ============================================================

base_dir = os.path.dirname(os.path.abspath(__file__))

csv_file = os.path.join(
    base_dir,
    "dhmif_experiment_results.csv"
)

output_dir = os.path.join(
    base_dir,
    "graphs"
)

os.makedirs(output_dir, exist_ok=True)


systems = [
    "Single Agent",
    "Static Multi-Agent",
    "DHMIF"
]

data = {
    system: {
        "verification": [],
        "confidence": [],
        "agents": [],
        "adaptation": [],
        "time": []
    }
    for system in systems
}


# ============================================================
# READ CSV
# ============================================================

with open(csv_file, "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        system = row["System"]

        data[system]["verification"].append(
            1 if row["Verification_Status"] == "PASSED" else 0
        )

        data[system]["confidence"].append(
            float(row["Confidence"])
        )

        data[system]["agents"].append(
            float(row["Average_Agents"])
        )

        data[system]["adaptation"].append(
            float(row["Adapted"])
        )

        data[system]["time"].append(
            float(row["Execution_Time_ms"])
        )


# ============================================================
# CALCULATE AVERAGES
# ============================================================

verification_rate = []
average_confidence = []
average_agents = []
adaptation_rate = []
average_time = []


for system in systems:

    verification_rate.append(
        sum(data[system]["verification"])
        / len(data[system]["verification"])
        * 100
    )

    average_confidence.append(
        sum(data[system]["confidence"])
        / len(data[system]["confidence"])
    )

    average_agents.append(
        sum(data[system]["agents"])
        / len(data[system]["agents"])
    )

    adaptation_rate.append(
        sum(data[system]["adaptation"])
        / len(data[system]["adaptation"])
        * 100
    )

    average_time.append(
        sum(data[system]["time"])
        / len(data[system]["time"])
    )


# ============================================================
# FUNCTION TO CREATE BAR CHARTS
# ============================================================

def create_bar_chart(values, ylabel, title, filename):

    plt.figure(figsize=(8, 5))

    bars = plt.bar(systems, values)

    plt.ylabel(ylabel)
    plt.title(title)

    plt.xticks(rotation=15)

    # Display values above bars
    for bar, value in zip(bars, values):

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    filepath = os.path.join(
        output_dir,
        filename
    )

    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Created: {filepath}")


# ============================================================
# GRAPH 1 — VERIFICATION RATE
# ============================================================

create_bar_chart(
    verification_rate,
    "Verification Rate (%)",
    "Verification Rate Comparison",
    "verification_rate.png"
)


# ============================================================
# GRAPH 2 — AVERAGE CONFIDENCE
# ============================================================

create_bar_chart(
    average_confidence,
    "Average Confidence",
    "Average Confidence Comparison",
    "average_confidence.png"
)


# ============================================================
# GRAPH 3 — AVERAGE NUMBER OF AGENTS
# ============================================================

create_bar_chart(
    average_agents,
    "Average Number of Agents",
    "Agent Utilization Comparison",
    "average_agents.png"
)


# ============================================================
# GRAPH 4 — EXECUTION TIME
# ============================================================

create_bar_chart(
    average_time,
    "Execution Time (ms)",
    "Execution Time Comparison",
    "execution_time.png"
)


# ============================================================
# GRAPH 5 — ADAPTATION RATE
# ============================================================

create_bar_chart(
    adaptation_rate,
    "Adaptation Rate (%)",
    "Workflow Adaptation Comparison",
    "adaptation_rate.png"
)


# ============================================================
# PRINT SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("GRAPH GENERATION COMPLETED")
print("=" * 60)

print(f"\nGraphs saved in:")
print(output_dir)

print("\nGenerated graphs:")

for filename in [
    "verification_rate.png",
    "average_confidence.png",
    "average_agents.png",
    "execution_time.png",
    "adaptation_rate.png"
]:

    print(f"✓ {filename}")