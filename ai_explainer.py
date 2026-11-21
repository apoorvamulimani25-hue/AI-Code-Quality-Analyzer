def explain_issue(issue):
    message = str(issue).lower()

    if "unused-import" in message or "unused import" in message:
        return (
            "This import is not being used in the program. "
            "Removing it can make the code cleaner."
        )

    elif "undefined-variable" in message or "undefined name" in message:
        return (
            "This variable may not have been declared before use. "
            "Check its spelling and ensure it is initialized."
        )

    elif "line-too-long" in message:
        return (
            "This line is longer than the recommended length. "
            "Consider breaking it into smaller lines."
        )

    elif "indentation" in message:
        return (
            "The indentation appears incorrect. Python uses indentation "
            "to define code blocks."
        )

    elif "password" in message or "hardcoded" in message:
        return (
            "A password or sensitive value may be hardcoded. "
            "Avoid storing secrets directly in source code."
        )

    elif "eval" in message:
        return (
            "The eval() function can execute dynamically supplied code "
            "and may introduce security risks."
        )

    elif "sql" in message:
        return (
            "This code may be vulnerable to SQL injection. "
            "Use parameterized queries instead of directly combining "
            "SQL statements with user input."
        )

    else:
        return (
            "Review this issue carefully. Improving this code may "
            "increase readability, reliability, or security."
        )