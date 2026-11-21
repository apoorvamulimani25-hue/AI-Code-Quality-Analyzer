import streamlit as st
import json

from analyzer import analyze_code
from ai_explainer import explain_issue
from report_generator import generate_report


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Code Quality Analyzer",
    page_icon="🔍",
    layout="wide"
)


# =====================================================
# HEADER
# =====================================================

st.title("🔍 AI-Assisted Code Quality Analyzer")

st.markdown(
    """
    This application analyzes Python code for code quality,
    coding style, and security problems.

    **Tools used:** Pylint | Flake8 | Bandit
    """
)

st.divider()


# =====================================================
# CODE INPUT
# =====================================================

code = st.text_area(
    "Enter your Python code:",
    height=300,
    placeholder="Write or paste your Python code here..."
)


# =====================================================
# ANALYSIS BUTTON
# =====================================================

if st.button("🚀 Analyze Code", use_container_width=True):

    if not code.strip():

        st.warning("Please enter Python code first.")

    else:

        with st.spinner("Analyzing code..."):

            results = analyze_code(code)

            # Extract analysis results
            pylint_issues = results.get("pylint", [])
            flake8_issues = results.get("flake8", [])
            bandit_issues = results.get("bandit", {}).get("results", [])

            # =================================================
            # WEIGHTED QUALITY SCORE
            # =================================================

            security_weight = 10
            pylint_weight = 3
            flake8_weight = 1

            total_penalty = (
                len(bandit_issues) * security_weight
                + len(pylint_issues) * pylint_weight
                + len(flake8_issues) * flake8_weight
            )

            quality_score = max(0, 100 - total_penalty)

            # =================================================
            # QUALITY STATUS
            # =================================================

            if quality_score >= 80:
                status = "Excellent"

            elif quality_score >= 60:
                status = "Good"

            elif quality_score >= 40:
                status = "Needs Improvement"

            else:
                status = "Poor"

            # Generate report
            report = generate_report(results)

            # Add score information to the report
            report["quality_score"] = quality_score
            report["quality_status"] = status

        st.success("Analysis completed successfully!")

        # =================================================
        # CODE QUALITY SUMMARY
        # =================================================

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

        st.markdown(
            f"### Overall Status: **{status}**"
        )

        st.progress(quality_score / 100)

        st.divider()

        # =================================================
        # ISSUE SEVERITY
        # =================================================

        st.subheader("🚨 Issue Severity")

        high_severity = len(bandit_issues)
        medium_severity = len(flake8_issues)
        low_severity = len(pylint_issues)

        severity_col1, severity_col2, severity_col3 = st.columns(3)

        severity_col1.metric(
            "🔴 High Severity",
            high_severity
        )

        severity_col2.metric(
            "🟠 Medium Severity",
            medium_severity
        )

        severity_col3.metric(
            "🟡 Low Severity",
            low_severity
        )

        st.divider()

        # =================================================
        # AI-ASSISTED EXPLANATIONS
        # =================================================

        st.subheader("🧠 AI-Assisted Explanations")

        all_issues = []

        # Pylint issues
        for issue in pylint_issues:

            message = issue.get("message", "")
            line = issue.get("line", "?")
            category = issue.get("type", "Pylint")

            all_issues.append(
                f"Pylint | Line {line} | {category} | {message}"
            )

        # Flake8 issues
        for issue in flake8_issues:

            message = issue.get("message", "")
            line = issue.get("line", "?")
            error_code = issue.get("code", "")

            all_issues.append(
                f"Flake8 | Line {line} | {error_code} | {message}"
            )

        # Bandit issues
        for issue in bandit_issues:

            message = issue.get("issue_text", "")
            line = issue.get("line_number", "?")
            severity = issue.get("issue_severity", "Unknown")

            all_issues.append(
                f"Bandit | Line {line} | {severity} | {message}"
            )

        # Display explanations
        if all_issues:

            for issue in all_issues:

                with st.expander(issue):

                    explanation = explain_issue(issue)

                    st.write(explanation)

        else:

            st.info("🎉 No issues detected!")

        st.divider()

        # =================================================
        # JSON REPORT
        # =================================================

        st.subheader("📄 JSON Report")

        json_report = json.dumps(
            report,
            indent=4
        )

        st.download_button(
            label="⬇️ Download JSON Report",
            data=json_report,
            file_name="quality_report.json",
            mime="application/json"
        )

        st.code(
            json_report,
            language="json"
        )

        st.success("Your analysis report is ready!")