import streamlit as st
import json

from analyzer import analyze_code
from ai_explainer import explain_issue
from report_generator import generate_report
from scoring import calculate_quality_score


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Code Quality Analyzer",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🔍 Code Analyzer")

    st.divider()

    st.subheader("📌 Project Information")

    st.write("**Project:**")
    st.write("AI-Assisted Code Quality Analysis")

    st.write("**Analysis Tools:**")
    st.write("🔹 Pylint")
    st.write("🔹 Flake8")
    st.write("🔹 Bandit")

    st.write("**Framework:**")
    st.write("Streamlit")

    st.divider()

    st.subheader("📊 Quality Score")

    st.write(
        "The quality score is calculated using a weighted "
        "penalty system. Security issues receive higher penalties."
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.title("🛡️ AI-Assisted Code Quality Analyzer")

st.markdown(
    """
    Analyze Python code for **quality problems, coding-style
    violations, and security vulnerabilities** using automated
    analysis tools.
    """
)

st.divider()


# =========================================================
# CODE INPUT
# =========================================================

st.subheader("📝 Python Code Input")

code = st.text_area(
    "Paste your Python code below:",
    height=300,
    placeholder="Enter your Python code here..."
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("🚀 Analyze Code", use_container_width=True):

    if not code.strip():

        st.warning("Please enter Python code before analyzing.")

    else:

        with st.spinner("Analyzing your code..."):

            results = analyze_code(code)

            pylint_issues = results.get("pylint", [])
            flake8_issues = results.get("flake8", [])
            bandit_issues = results.get("bandit", {}).get(
                "results", []
            )

            # Calculate score using scoring.py
            quality_score, status = calculate_quality_score(
                pylint_issues,
                flake8_issues,
                bandit_issues
            )

            # Generate report
            report = generate_report(results)

            # Add score and status
            report["quality_score"] = quality_score
            report["quality_status"] = status

            # Add summary
            report["summary"] = {
                "pylint_issues": len(pylint_issues),
                "flake8_issues": len(flake8_issues),
                "security_issues": len(bandit_issues)
            }

            # Save complete report
            with open(
                "quality_report.json",
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(report, file, indent=4)

        st.success("✅ Analysis completed successfully!")


        # =================================================
        # CODE QUALITY SUMMARY
        # =================================================

        st.subheader("📊 Code Quality Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Quality Score", f"{quality_score}/100")
        col2.metric("Pylint Issues", len(pylint_issues))
        col3.metric("Flake8 Issues", len(flake8_issues))
        col4.metric("Security Issues", len(bandit_issues))


        # =================================================
        # QUALITY STATUS
        # =================================================

        st.subheader("Overall Quality Status")

        if quality_score >= 80:
            st.success(f"🟢 Status: {status}")

        elif quality_score >= 60:
            st.info(f"🔵 Status: {status}")

        elif quality_score >= 40:
            st.warning(f"🟠 Status: {status}")

        else:
            st.error(f"🔴 Status: {status}")

        st.progress(quality_score / 100)

        st.write(f"Your code quality score is **{quality_score}%**.")

        st.divider()


        # =================================================
        # ISSUE SEVERITY SUMMARY
        # =================================================

        st.subheader("🚨 Issue Severity Summary")

        high_severity = len(bandit_issues)
        medium_severity = len(flake8_issues)
        low_severity = len(pylint_issues)

        severity_col1, severity_col2, severity_col3 = st.columns(3)

        severity_col1.metric("🔴 High Severity", high_severity)
        severity_col2.metric("🟠 Medium Severity", medium_severity)
        severity_col3.metric("🟡 Low Severity", low_severity)

        st.divider()


        # =================================================
        # ISSUE DETAILS AND EXPLANATIONS
        # =================================================

        st.subheader("🧠 AI-Assisted Explanations")

        all_issues = []

        # Pylint
        for issue in pylint_issues:

            all_issues.append({
                "tool": "Pylint",
                "line": issue.get("line", "?"),
                "category": issue.get("type", "Pylint"),
                "message": issue.get("message", "")
            })

        # Flake8
        for issue in flake8_issues:

            all_issues.append({
                "tool": "Flake8",
                "line": issue.get("line", "?"),
                "category": issue.get("code", "Flake8"),
                "message": issue.get("message", "")
            })

        # Bandit
        for issue in bandit_issues:

            all_issues.append({
                "tool": "Bandit",
                "line": issue.get("line_number", "?"),
                "category": issue.get("issue_severity", "Security"),
                "message": issue.get("issue_text", "")
            })

        # Display issues
        if all_issues:

            for issue in all_issues:

                title = (
                    f"{issue['tool']} | "
                    f"Line {issue['line']} | "
                    f"{issue['category']} | "
                    f"{issue['message']}"
                )

                with st.expander(title):

                    st.write("**Tool:**", issue["tool"])
                    st.write("**Line:**", issue["line"])
                    st.write("**Issue:**", issue["message"])

                    explanation = explain_issue(issue["message"])

                    st.write("**Explanation:**")
                    st.info(explanation)

        else:

            st.success("🎉 No issues detected!")

        st.divider()


        # =================================================
        # JSON REPORT
        # =================================================

        st.subheader("📄 JSON Analysis Report")

        json_report = json.dumps(report, indent=4)

        st.download_button(
            label="⬇️ Download JSON Report",
            data=json_report,
            file_name="quality_report.json",
            mime="application/json",
            use_container_width=True
        )

        with st.expander("View JSON Report"):

            st.json(report)

        st.success("📁 Your analysis report is ready!")