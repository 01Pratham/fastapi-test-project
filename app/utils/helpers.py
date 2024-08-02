import re


class Helpers:
    def validate_not_empty(v):
        if v is None:
            return v
        v = " ".join(v.split())
        if not v:
            raise ValueError("All fields should be filled with keywords")
        return v

    def validate_email(v):
        if v is None:
            return v

        if "@" not in v:
            raise ValueError("Email must contain '@'")
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, v):
            raise ValueError("Email must contain a valid domain (e.g., '.com', '.net')")

        return v

    def validate_password(v: str) -> str:
        if v is None:
            return v
        has_digit = re.search(r"\d", v)
        has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', v)
        if not (has_digit and has_special_char):
            raise ValueError(
                "Password must contain at least one number and one special character."
            )
        return v
