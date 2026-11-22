def calculate_quality_score(
    pylint_issues,
    flake8_issues,
    bandit_issues
):
    security_weight = 10
    pylint_weight = 3
    flake8_weight = 1

    total_penalty = (
        len(bandit_issues) * security_weight
        + len(pylint_issues) * pylint_weight
        + len(flake8_issues) * flake8_weight
    )

    score = max(0, 100 - total_penalty)

    if score >= 80:
        status = "Excellent"
    elif score >= 60:
        status = "Good"
    elif score >= 40:
        status = "Needs Improvement"
    else:
        status = "Poor"

    return score, status