from analyzer import analyze_code


def test_analyzer_returns_all_tools():
    code = "print('Hello World')"

    results = analyze_code(code)

    assert "pylint" in results
    assert "flake8" in results
    assert "bandit" in results


def test_analyzer_handles_empty_code():
    code = ""

    results = analyze_code(code)

    assert isinstance(results, dict)


def test_analyzer_detects_security_issue():
    code = """
password = "admin123"
print(password)
"""

    results = analyze_code(code)

    assert "bandit" in results
    assert isinstance(results["bandit"], dict)