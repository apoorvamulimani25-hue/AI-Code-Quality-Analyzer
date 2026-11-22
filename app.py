import streamlit as st
import json
from datetime import datetime

from analyzer import analyze_code
from ai_explainer import explain_issue
from report_generator import generate_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Code Quality Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background-color: #1c2333;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303b52;
}

[data-testid="stMetricLabel"] {
    color: #aab8d0;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
}

.custom-card {
    background-color: #1c2333;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303b52;
    margin-bottom: 15px;
}

.status-excellent {
    background-color: #123d2b;
    color: #4ade80;
    padding: 12px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

.status-good {
    background-color: #183b50;
    color: #38bdf8;
    padding: 12px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

.status-improvement {
    background-color: #493519;
    color: #facc15;
    padding: 12px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

.status-poor {
    background-color: #491e25;
    color: #fb7185;
    padding: 12px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🔍 Code Analyzer")

    st.markdown("---")

    st.subheader("📌 Project Information")

    st.write("**Project:**")
    st.write("AI-Assisted Code Quality Analysis")

    st.write("**Analysis Tools:**")
    st.write("🔹 Pylint")
    st.write("🔹 Flake8")
    st.write("🔹 Bandit")

    st.write("**Framework:**")
    st.write("Streamlit")

    st.markdown("---")

    st.subheader("📊 Quality Score")

    st.write("""
    The quality score is calculated using a weighted
    penalty system. Security issues receive higher penalties.
    """)

    st.markdown("---")

    st.caption("Mini Project | Python | DevOps | CI/CD")


# =========================================================
# HEADER
# =========================================================

st.title("🛡️ AI-Assisted Code Quality Analyzer")

st.markdown("""
Analyze Python code for **quality problems, coding-style violations,
and security vulnerabilities** using automated analysis tools.
""")

st.markdown("---")


# =========================================================
# CODE INPUT
# =========================================================

st.subheader("📝 Python Code Input")

code = st.text_area(
    "Paste your Python code below:",
    height=280,
    placeholder="Enter your Python code here..."
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("🚀 Analyze Code", use_container_width=True):

    if not code.strip():

        st.warning("⚠️ Please enter Python code before analyzing.")

    else:

        with st.spinner("🔎 Analyzing your code..."):

            results = analyze_code(code)

            pylint_issues = results.get("pylint", [])
            flake8_issues = results.get("flake8", [])
            bandit_issues = results.get("bandit", {}).get("results", [])

            # -----------------------------------------------
            # QUALITY SCORE
            # -----------------------------------------------

            total_penalty = (
                len(bandit_issues) * 10
                + len(pylint_issues) * 3
                + len(flake8_issues)
            )

            quality_score = max(0, 100 - total_penalty)

            # -----------------------------------------------
            # STATUS
            # -----------------------------------------------

            if quality_score >= 80:
                status = "Excellent"
                status_class = "status-excellent"

            elif quality_score >= 60:
                status = "Good"
                status_class = "status-good"

            elif quality_score >= 40:
                status = "Needs Improvement"
                status_class = "status-improvement"

            else:
                status = "Poor"
                status_class = "status-poor"

            # -----------------------------------------------
            # REPORT
            # -----------------------------------------------

            report = generate_report(results)

            report["quality_score"] = quality_score
            report["quality_status"] = status

            report["summary"] = {
                "pylint_issues": len(pylint_issues),
                "flake8_issues": len(flake8_issues),
                "security_issues": len(bandit_issues)
            }

            # Save the complete report to JSON
            with open(
                "quality_report.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(report, file, indent=4)

            # Save results to session state
            st.session_state["analysis_results"] = results
            st.session_state["quality_score"] = quality_score
            st.session_state["quality_status"] = status
            st.session_state["status_class"] = status_class
            st.session_state["report"] = report


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "analysis_results" in st.session_state:

    results = st.session_state["analysis_results"]

    quality_score = st.session_state["quality_score"]

    status = st.session_state["quality_status"]

    status_class = st.session_state["status_class"]

    report = st.session_state["report"]

    pylint_issues = results.get("pylint", [])

    flake8_issues = results.get("flake8", [])

    bandit_issues = results.get("bandit", {}).get("results", [])

    st.success("✅ Analysis completed successfully!")

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3 = st.tabs([
        "📊 Overview",
        "🧠 Issues & Explanations",
        "📄 JSON Report"
    ])


    # =====================================================
    # TAB 1 - OVERVIEW
    # =====================================================

    with tab1:

        st.subheader("📊 Code Quality Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Quality Score",
            f"{quality_score}/100"
        )

        col2.metric(
            "Pylint Issues",
            len(pylint_issues)
        )

        col3.metric(
            "Flake8 Issues",
            len(flake8_issues)
        )

        col4.metric(
            "Security Issues",
            len(bandit_issues)
        )

        st.markdown("### Overall Quality Status")

        st.markdown(
            f'<div class="{status_class}">Status: {status}</div>',
            unsafe_allow_html=True
        )

        st.progress(quality_score / 100)

        st.write(f"Your code quality score is **{quality_score}%**.")

        st.markdown("---")

        # -----------------------------------------------
        # SEVERITY
        # -----------------------------------------------

        st.subheader("🚨 Issue Severity Summary")

        severity_col1, severity_col2, severity_col3 = st.columns(3)

        severity_col1.metric(
            "🔴 High Severity",
            len(bandit_issues)
        )

        severity_col2.metric(
            "🟠 Medium Severity",
            len(flake8_issues)
        )

        severity_col3.metric(
            "🟡 Low Severity",
            len(pylint_issues)
        )

        st.markdown("---")

        # -----------------------------------------------
        # TOOL INFORMATION
        # -----------------------------------------------

        st.subheader("🛠️ Analysis Tools")

        tool_col1, tool_col2, tool_col3 = st.columns(3)

        with tool_col1:

            st.markdown("### 🔎 Pylint")

            st.write("Checks Python code quality.")

            st.metric(
                "Issues Found",
                len(pylint_issues)
            )

        with tool_col2:

            st.markdown("### 📏 Flake8")

            st.write("Checks coding style and formatting.")

            st.metric(
                "Issues Found",
                len(flake8_issues)
            )

        with tool_col3:

            st.markdown("### 🔐 Bandit")

            st.write("Detects potential security problems.")

            st.metric(
                "Issues Found",
                len(bandit_issues)
            )


    # =====================================================
    # TAB 2 - ISSUES & EXPLANATIONS
    # =====================================================

    with tab2:

        st.subheader("🧠 Issues & Explanations")

        all_issues = []

        # -----------------------------------------------
        # PYLINT
        # -----------------------------------------------

        for issue in pylint_issues:

            all_issues.append({
                "tool": "Pylint",
                "line": issue.get("line", "?"),
                "type": issue.get("type", "Code Quality"),
                "message": issue.get("message", "")
            })

        # -----------------------------------------------
        # FLAKE8
        # -----------------------------------------------

        for issue in flake8_issues:

            all_issues.append({
                "tool": "Flake8",
                "line": issue.get("line", "?"),
                "type": issue.get("code", "Style"),
                "message": issue.get("message", "")
            })

        # -----------------------------------------------
        # BANDIT
        # -----------------------------------------------

        for issue in bandit_issues:

            all_issues.append({
                "tool": "Bandit",
                "line": issue.get("line_number", "?"),
                "type": issue.get("issue_severity", "Security"),
                "message": issue.get("issue_text", "")
            })

        # -----------------------------------------------
        # DISPLAY
        # -----------------------------------------------

        if all_issues:

            st.write(
                f"Total findings reported by tools: **{len(all_issues)}**"
            )

            for index, issue in enumerate(all_issues, start=1):

                title = (
                    f"{index}. {issue['tool']} | "
                    f"Line {issue['line']} | "
                    f"{issue['type']} | "
                    f"{issue['message']}"
                )

                with st.expander(title):

                    st.markdown(
                        f"**Analysis Tool:** {issue['tool']}"
                    )

                    st.markdown(
                        f"**Line Number:** {issue['line']}"
                    )

                    st.markdown(
                        f"**Issue Type:** {issue['type']}"
                    )

                    st.markdown(
                        f"**Description:** {issue['message']}"
                    )

                    st.markdown("---")

                    st.markdown("### 💡 Explanation")

                    explanation = explain_issue(
                        f"{issue['tool']} {issue['type']} {issue['message']}"
                    )

                    st.info(explanation)

        else:

            st.success("🎉 No issues detected! Your code looks clean.")


    # =====================================================
    # TAB 3 - JSON REPORT
    # =====================================================

    with tab3:

        st.subheader("📄 JSON Analysis Report")

        json_report = json.dumps(
            report,
            indent=4
        )

        st.download_button(
            label="⬇️ Download JSON Report",
            data=json_report,
            file_name="quality_report.json",
            mime="application/json",
            use_container_width=True
        )

        st.markdown("---")

        st.write("### Report Preview")

        st.json(report)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI-Assisted Code Quality Analyzer | "
    "Python | Pylint | Flake8 | Bandit | Streamlit"
)