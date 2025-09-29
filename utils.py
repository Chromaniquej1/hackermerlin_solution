import re

def extract_password(response_text):
    # Common patterns for revealed passwords
    patterns = [
        r"password[:\s]*([A-Za-z0-9]+)",
        r"secret[:\s]*([A-Za-z0-9]+)",
        r"the word is[:\s]*([A-Za-z0-9]+)",
        r"passcode[:\s]*([A-Za-z0-9]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None