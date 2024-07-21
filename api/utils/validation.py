import re

pattern = re.compile(r'^\.|\.{2}|__.*__|/')

def contains_invalid_pattern(s: str) -> bool:
    return bool(pattern.search(s))