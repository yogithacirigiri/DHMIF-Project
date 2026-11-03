"""DHMIF Research Console — polished Streamlit dashboard.

Run from the DHMIF project root:
    streamlit run dhmif_professional_app.py

This is a presentation/UI layer. When the project backend is unavailable, the app
uses clearly labelled illustrative fallback values rather than claiming a real run.
"""

from pathlib import Path
import time

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Optional project integrations -------------------------------------------------
try:
    from core.task_analyzer import TaskAnalyzer
except (ImportError, AttributeError):
    TaskAnalyzer = None

try:
    from core.orchestrator import Orchestrator
except (ImportError, AttributeError):
    try:
        from core.orchestrator import MetaCognitiveOrchestrator as Orchestrator
    except (ImportError, AttributeError):
        Orchestrator = None

ROOT = Path(__file__).resolve().parent
RESULTS_FILE = ROOT / "experiments" / "dhmif_experiment_results.csv"

st.set_page_config(
    page_title="DHMIF | Research Console",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Visual system ----------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --bg:#080d18; --panel:#101827; --panel2:#121e30; --line:#24334a;
            --text:#edf4ff; --muted:#93a4bd; --cyan:#45e0d0; --blue:#6b8cff; --violet:#b18cff; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background: radial-gradient(ellipse at 15% 0%, #14243d 0%, transparent 38%),
                         radial-gradient(ellipse at 90% 12%, #1b1536 0%, transparent 32%), var(--bg); color:var(--text); }
    [data-testid="stHeader"] { background:rgba(8,13,24,.72); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#0d1524 0%,#0a111e 100%); border-right:1px solid var(--line); }
    [data-testid="stSidebar"] * { color:var(--text); }
    .block-container { max-width:1500px; padding-top:1.6rem; padding-bottom:2.5rem; }
    h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif !important; color:var(--text) !important; letter-spacing:-.035em; }
    p, label, .stMarkdown { color:var(--text); }
    [data-testid="stCaptionContainer"] { color:var(--muted); }
    .eyebrow { color:var(--cyan); text-transform:uppercase; letter-spacing:.19em; font-size:.72rem; font-weight:700; }
    .hero { position:relative; overflow:hidden; border:1px solid #2b3c56; border-radius:24px;
            padding:30px 34px; margin:0 0 24px; background:linear-gradient(115deg,rgba(18,33,53,.96),rgba(18,22,43,.92));
            box-shadow:0 22px 70px rgba(0,0,0,.22); }
    .hero:after { content:''; position:absolute; width:310px; height:310px; right:-100px; top:-170px;
                  border-radius:50%; border:1px solid rgba(69,224,208,.22); box-shadow:0 0 0 35px rgba(69,224,208,.035),0 0 0 75px rgba(107,140,255,.035); }
    .hero h1 { font-size:clamp(1.8rem,3vw,3rem); line-height:1.06; margin:.45rem 0 .7rem; }
    .hero-copy { max-width:760px; color:#aebed4; font-size:1rem; line-height:1.65; }
    .pill { display:inline-block; border:1px solid rgba(69,224,208,.35); background:rgba(69,224,208,.08); color:var(--cyan);
            border-radius:999px; padding:6px 11px; font-size:.72rem; font-weight:700; letter-spacing:.08em; }
    .section-head { display:flex; align-items:center; gap:10px; margin:24px 0 12px; font-family:'Space Grotesk',sans-serif; font-size:1.12rem; font-weight:600; }
    .section-head span { width:8px; height:8px; border-radius:3px; background:var(--cyan); box-shadow:0 0 14px rgba(69,224,208,.55); display:inline-block; }
    [data-testid="stMetric"] { background:linear-gradient(145deg,rgba(18,30,48,.98),rgba(13,23,37,.98)); border:1px solid var(--line);
       border-radius:17px; padding:17px 19px; box-shadow:0 10px 25px rgba(0,0,0,.12); }
    [data-testid="stMetricLabel"] { color:#9eafc7 !important; font-size:.82rem; }
    [data-testid="stMetricValue"] { color:var(--text) !important; font-family:'Space Grotesk',sans-serif; font-size:1.9rem; }
    [data-testid="stMetricDelta"] { font-size:.76rem; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--line) !important; border-radius:18px !important; }
    .stButton>button, .stFormSubmitButton>button { border:1px solid #3e6e86; border-radius:11px; color:#06131c;
       background:linear-gradient(105deg,var(--cyan),#8be8dc); font-weight:700; min-height:2.7rem; transition:all .18s ease; }
    .stButton>button:hover, .stFormSubmitButton>button:hover { border-color:var(--cyan); box-shadow:0 0 22px rgba(69,224,208,.2); transform:translateY(-1px); }
    .stTextArea textarea, .stTextInput input, [data-baseweb="select"] > div { background:#0b1422 !important; color:var(--text) !important; border-color:#2b3d55 !important; border-radius:10px !important; }
    [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--line); }
    [data-baseweb="tab"] { background:transparent; border-radius:9px 9px 0 0; color:#9aabc2; }
    [aria-selected="true"][data-baseweb="tab"] { color:var(--cyan) !important; }
    [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
    .status-note { background:rgba(69,224,208,.06); border:1px solid rgba(69,224,208,.18); border-radius:12px; padding:12px 14px; color:#b9d6dd; font-size:.86rem; }
    .small-muted { color:var(--muted); font-size:.82rem; }
    hr { border-color:var(--line); }
    footer { visibility:hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


def assess_complexity(task: str) -> str:
    """Use the project's analyzer if available; otherwise provide a transparent heuristic."""
    if TaskAnalyzer:
        try:
            analyzer = TaskAnalyzer()
            if hasattr(analyzer, "analyze_complexity"):
                result = analyzer.analyze_complexity(task)
                if result:
                    return str(result).title()
        except Exception:
            pass
    words = len(task.split())
    signals = ("compare", "calculate", "verify", "analyze", "evaluate", "multiple", "risk", "evidence")
    score = words + sum(8 for token in signals if token in task.lower())
    return "Low" if score < 18 else ("Medium" if score < 38 else "High")


def build_topology(complexity: str, mode: str) -> go.Figure:
    """Create a clear workflow topology illustration for the selected architecture."""
    graph = nx.DiGraph()
    nodes = ["Task Intake", "Complexity Analyzer", "Meta-Cognitive\nController"]
    if mode == "Single Agent":
        nodes += ["General Agent", "Response"]
    elif mode == "Static Multi-Agent":
        nodes += ["Research Agent", "Analysis Agent", "Calculation Agent", "Verification", "Response"]
    else:
        nodes += ["Research Agent", "Independent Verifier", "Context Memory", "Response"]
        if complexity in ("Medium", "High"):
            nodes.insert(nodes.index("Independent Verifier"), "Analysis Agent")
        if complexity == "High":
            nodes.insert(nodes.index("Independent Verifier"), "Calculation Agent")
    graph.add_nodes_from(nodes)
    edges = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
    # Adaptive branches are represented explicitly instead of forcing a straight pipeline.
    if mode == "DHMIF (Proposed)" and "Context Memory" in nodes:
        edges += [("Context Memory", "Meta-Cognitive\nController"), ("Independent Verifier", "Response")]
    graph.add_edges_from(edges)
    pos = nx.spring_layout(graph, seed=21, k=1.25, iterations=100)

    edge_x, edge_y = [], []
    for start, end in graph.edges():
        x0, y0 = pos[start]; x1, y1 = pos[end]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", hoverinfo="skip",
        line=dict(width=1.6, color="rgba(93,157,191,.65)"))

    palette = {"Task Intake": "#6b8cff", "Complexity Analyzer": "#6b8cff",
               "Meta-Cognitive\nController": "#45e0d0", "Independent Verifier": "#b18cff",
               "Context Memory": "#b18cff", "Response": "#45e0d0"}
    colors = [palette.get(n, "#3e7196") for n in graph.nodes()]
    node_trace = go.Scatter(
        x=[pos[n][0] for n in graph.nodes()], y=[pos[n][1] for n in graph.nodes()],
        mode="markers+text", text=list(graph.nodes()), textposition="bottom center",
        textfont=dict(family="DM Sans", size=11, color="#08A9E4"),
        hovertemplate="<b>%{text}</b><extra></extra>",
        marker=dict(size=25, color=colors, line=dict(width=1.5, color="#83bbed"),
                    opacity=.98, symbol="circle"),
    )
    fig = go.Figure([edge_trace, node_trace])
    fig.update_layout(
        height=410, margin=dict(l=12, r=12, t=15, b=18), showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        hoverlabel=dict(bgcolor="#D0DAEE", font_color="#7603e0", bordercolor="#2b3c56"),
    )
    return fig


def load_benchmarks() -> pd.DataFrame:
    if RESULTS_FILE.exists():
        try:
            return pd.read_csv(RESULTS_FILE)
        except Exception:
            pass
    return pd.DataFrame({
        "System Architecture": ["Single Agent", "Static Multi-Agent", "DHMIF (Proposed)"],
        "Verification Rate": ["100%", "100%", "100%"],
        "Mean Confidence": [0.820, 0.860, 0.839],
        "Avg Agents/Task": [1.00, 4.00, 2.67],
        "Workflow Adapted": ["No", "No", "Yes"],
        "Execution Time": ["0.001890 ms", "0.008980 ms", "3.359123 ms"],
    })


def run_task(task: str, mode: str, complexity: str) -> dict:
    """Call the real orchestrator where possible; otherwise label results as illustrative."""
    if Orchestrator:
        try:
            engine = Orchestrator()
            if hasattr(engine, "execute_task"):
                result = engine.execute_task(task, mode)
                if isinstance(result, dict):
                    return {
                        "confidence": float(result.get("confidence", 0.0)),
                        "agents": int(result.get("agents_used", 1)),
                        "source": "Project orchestrator",
                        "verification": str(result.get("verification_status", "Not reported")),
                        "details": result,
                    }
        except Exception as exc:
            return {"confidence": 0.0, "agents": 0, "source": f"Backend error: {exc}",
                    "verification": "Not run", "details": {}}
    # Clearly labelled UI fallback; these values are not measured execution results.
    agents = 1 if mode == "Single Agent" else (4 if mode == "Static Multi-Agent" else (2 if complexity == "Low" else 3))
    confidence = 0.82 if mode == "Single Agent" else (0.86 if mode == "Static Multi-Agent" else 0.839)
    return {"confidence": confidence, "agents": agents, "source": "Illustrative UI fallback",
            "verification": "Not connected", "details": {}}


# Sidebar -----------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div style='padding:8px 0 18px'><span class='pill'>◈ RESEARCH CONSOLE</span></div>", unsafe_allow_html=True)
    st.markdown("## DHMIF")
    st.caption("Distributed intelligence · Adaptive orchestration")
    st.divider()
    st.markdown("**WORKSPACE**")
    page = st.radio("Workspace navigation", ["Overview", "Run an experiment", "Benchmark results", "About DHMIF"],
                    label_visibility="collapsed")
    st.divider()
    st.markdown("**ENGINE CONFIGURATION**")
    mode = st.selectbox("Architecture", ["DHMIF (Proposed)", "Static Multi-Agent", "Single Agent"], index=0)
    task = st.text_area(
        "Task prompt",
        value="Analyze quarterly market trends, estimate risk factors, and verify consistency across the reasoning steps.",
        height=135,
        help="Enter the task you want the selected architecture to process.",
    )
    run = st.button("▶  Execute workflow", use_container_width=True, type="primary")
    st.divider()
    st.markdown("<div class='small-muted'>PROJECT · Phase I<br>AI & Machine Learning<br>Malla Reddy University</div>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted' style='margin-top:14px'>DHMIF prototype interface · v1.1</div>", unsafe_allow_html=True)

# Hero --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Distributed intelligence / research prototype</div>
      <h1>Meta-Cognitive<br>Intelligence Fabric<span style="color:#45e0d0">.</span></h1>
      <div class="hero-copy">A research console for exploring adaptive multi-agent workflows, contextual memory,
      and verification-aware orchestration. Inspect the workflow topology, run tasks, and compare system behaviour.</div>
      <div style="margin-top:19px;display:flex;gap:9px;flex-wrap:wrap">
        <span class="pill">ADAPTIVE WORKFLOWS</span><span class="pill">HYPERGRAPH-INSPIRED</span><span class="pill">VERIFICATION LOOP</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Run only on an explicit click; keep last result visible across reruns.
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if run:
    if not task.strip():
        st.warning("Enter a task prompt before executing the workflow.")
    else:
        with st.spinner("Assessing task and preparing workflow…"):
            complexity_now = assess_complexity(task)
            st.session_state.last_result = {
                "task": task,
                "mode": mode,
                "complexity": complexity_now,
                "result": run_task(task, mode, complexity_now),
                "timestamp": time.strftime("%d %b %Y · %H:%M:%S"),
            }

last = st.session_state.last_result

if page == "Overview":
    st.markdown("<div class='section-head'><span></span>System overview</div>", unsafe_allow_html=True)
    benchmarks = load_benchmarks()
    last_complexity = last["complexity"] if last else "Awaiting task"
    last_agents = last["result"]["agents"] if last else "—"
    last_conf = last["result"]["confidence"] if last else None
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Workflow status", "Ready" if last else "Standby", "Prototype")
    with c2: st.metric("Task complexity", last_complexity)
    with c3: st.metric("Agents selected", str(last_agents))
    with c4: st.metric("Confidence estimate", f"{last_conf:.3f}" if last_conf is not None else "—")

    left, right = st.columns([1.45, 1], gap="large")
    with left:
        st.markdown("<div class='section-head'><span></span>Workflow topology</div>", unsafe_allow_html=True)
        topology_complexity = last["complexity"] if last else "High"
        st.plotly_chart(build_topology(topology_complexity, mode), use_container_width=True, config={"displayModeBar": False})
        st.caption("Illustrative topology for the selected architecture and complexity level; inspect the backend implementation for execution truth.")
    with right:
        st.markdown("<div class='section-head'><span></span>Execution snapshot</div>", unsafe_allow_html=True)
        with st.container(border=True):
            if last:
                st.markdown(f"**Last task**  \n{last['task']}")
                st.markdown(f"<span class='pill'>{last['mode']}</span> &nbsp; <span class='pill'>{last['complexity'].upper()} COMPLEXITY</span>", unsafe_allow_html=True)
                st.write("")
                st.markdown(f"**Run time:** {last['timestamp']}")
                st.markdown(f"**Result source:** {last['result']['source']}")
                st.markdown(f"**Verification:** {last['result']['verification']}")
                if last["result"]["source"] == "Illustrative UI fallback":
                    st.markdown("<div class='status-note'>Backend integration was not detected. Values shown for this run are illustrative and are not measured experiment results.</div>", unsafe_allow_html=True)
            else:
                st.markdown("### No workflow executed yet")
                st.write("Choose an architecture and enter a task in the sidebar, then select **Execute workflow**.")
                st.markdown("<div class='status-note'>The dashboard will show the latest task, selected agents, complexity estimate, and result source here.</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-head'><span></span>Core capabilities</div>", unsafe_allow_html=True)
        st.markdown("- **Meta-cognitive control** — adapt the workflow to task complexity\n- **Agent collaboration** — route work to specialized agents\n- **Verification loop** — make validation a visible stage\n- **Context memory** — retain useful task context where implemented")

elif page == "Run an experiment":
    st.markdown("<div class='section-head'><span></span>Experiment workspace</div>", unsafe_allow_html=True)
    st.write("Configure the architecture and task from the sidebar, then execute. This page reports the latest run and distinguishes real backend output from fallback UI values.")
    if last:
        a, b, c = st.columns(3)
        a.metric("Complexity", last["complexity"])
        b.metric("Agents selected", last["result"]["agents"])
        c.metric("Confidence estimate", f"{last['result']['confidence']:.3f}")
        st.markdown("#### Submitted task")
        st.code(last["task"], language=None)
        st.markdown("#### Run metadata")
        st.json({"architecture": last["mode"], "timestamp": last["timestamp"],
                 "source": last["result"]["source"], "verification": last["result"]["verification"]})
        if last["result"]["details"]:
            st.markdown("#### Backend response")
            st.json(last["result"]["details"])
    else:
        st.info("No experiment has been run in this session yet. Use the sidebar to start one.")

elif page == "Benchmark results":
    st.markdown("<div class='section-head'><span></span>Architecture benchmark</div>", unsafe_allow_html=True)
    df = load_benchmarks()
    if RESULTS_FILE.exists():
        st.markdown(f"<div class='status-note'>Loaded benchmark data from <code>{RESULTS_FILE.relative_to(ROOT)}</code>.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-note'>No experiment CSV found at <code>experiments/dhmif_experiment_results.csv</code>. Showing illustrative sample values until the experiment runner creates the file.</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    # Render a confidence comparison only when the relevant numeric column exists.
    confidence_col = next((col for col in df.columns if col.lower() in ("mean confidence", "avg confidence", "average confidence")), None)
    name_col = next((col for col in df.columns if "architecture" in col.lower() or "system" in col.lower()), None)
    if confidence_col and name_col:
        try:
            chart_df = df[[name_col, confidence_col]].copy()
            chart_df[confidence_col] = pd.to_numeric(chart_df[confidence_col], errors="coerce")
            chart_df = chart_df.dropna()
            if not chart_df.empty:
                fig = go.Figure(go.Bar(x=chart_df[name_col], y=chart_df[confidence_col],
                    marker=dict(color=["#6b8cff", "#b18cff", "#45e0d0"]),
                    text=[f"{v:.3f}" for v in chart_df[confidence_col]], textposition="outside"))
                fig.update_layout(height=330, margin=dict(l=10,r=10,t=20,b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#14a0dc"), yaxis=dict(gridcolor="#dae1ea", title="Mean confidence"),
                    xaxis=dict(title="Architecture"), showlegend=False)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            pass
    if RESULTS_FILE.exists():
        st.download_button("Download benchmark CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name="dhmif_benchmark_results.csv", mime="text/csv")

else:
    st.markdown("<div class='section-head'><span></span>About the framework</div>", unsafe_allow_html=True)
    st.markdown("""
    DHMIF is a prototype concept for dynamically composing and supervising multiple agents rather than relying only on a fixed pipeline.

    **Design goals**
    - **Distributed coordination:** represent relationships among tasks, agents, tools, and knowledge sources.
    - **Meta-cognitive orchestration:** assess task complexity and adapt agent composition at runtime.
    - **Contextual continuity:** reuse stored context when the memory component is connected.
    - **Verification-aware output:** expose validation as a stage rather than hiding it behind the final answer.

    **Research note:** a polished dashboard is not itself evidence of system performance. For a paper, report results generated by repeatable experiments, explain the dataset and metrics, and avoid presenting fallback values as measured outcomes.
    """)

st.divider()
st.markdown("<div class='small-muted'>DHMIF Research Console · Prototype interface · Validate metrics against experiment logs before publication.</div>", unsafe_allow_html=True)
