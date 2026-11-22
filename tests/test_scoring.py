from scoring import calculate_quality_score


def test_clean_code_score():
    score, status = calculate_quality_score([], [], [])

    assert score == 100
    assert status == "Excellent"


def test_security_issue_penalty():
    pylint = []
    flake8 = []
    bandit = [{}]

    score, status = calculate_quality_score(
        pylint,
        flake8,
        bandit
    )

    assert score == 90
    assert status == "Excellent"


def test_pylint_penalty():
    pylint = [{}, {}]
    flake8 = []
    bandit = []

    score, status = calculate_quality_score(
        pylint,
        flake8,
        bandit
    )

    assert score == 94
    assert status == "Excellent"


def test_flake8_penalty():
    pylint = []
    flake8 = [{}, {}, {}]
    bandit = []

    score, status = calculate_quality_score(
        pylint,
        flake8,
        bandit
    )

    assert score == 97
    assert status == "Excellent"


def test_poor_quality_status():
    pylint = [{}] * 20
    flake8 = [{}] * 10
    bandit = [{}] * 5

    score, status = calculate_quality_score(
        pylint,
        flake8,
        bandit
    )

    assert score == 0
    assert status == "Poor"