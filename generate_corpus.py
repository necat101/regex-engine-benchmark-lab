#!/usr/bin/env python3
"""
Generate reproducible regex corpus with no external downloads.
Creates small, medium, and large haystacks with various content types.
"""

import os
import json
import hashlib
import random
from pathlib import Path

# Fixed seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

OUTPUT_DIR = Path("corpus")
OUTPUT_DIR.mkdir(exist_ok=True)

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

# Sample data components
ASCII_LOGS = """2024-01-15 10:23:45 INFO User login successful for user123
2024-01-15 10:24:12 ERROR Failed to connect to database at 192.168.1.100:5432
2024-01-15 10:25:03 WARN High memory usage detected: 87%
2024-01-15 10:26:45 INFO Request processed in 234ms - /api/v1/users
2024-01-15 10:27:12 DEBUG Cache hit for key: user_profile_12345
"""

UNICODE_TEXT = """Привет мир! Это тестовый текст на русском языке.
你好世界！这是一个中文测试文本。
こんにちは世界！これは日本語のテストテキストです。
مرحبا بالعالم! هذا نص اختبار باللغة العربية.
Emoji test: 😀 🎉 🚀 💻 🐱 🍕 🌟 ⚡ 🔥
"""

SOURCE_CODE = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.data = []
    
    def process(self, items):
        return [x * 2 for x in items if x > 0]
"""

JSON_LOGS = """{"timestamp":"2024-01-15T10:23:45Z","level":"INFO","message":"User login","user_id":"12345","ip":"192.168.1.1"}
{"timestamp":"2024-01-15T10:24:12Z","level":"ERROR","message":"DB connection failed","error":"timeout","retry_count":3}
{"timestamp":"2024-01-15T10:25:03Z","level":"WARN","message":"High memory","usage":87,"threshold":80}
"""

CSV_DATA = """id,name,email,age,city
1,Alice Smith,alice@example.com,28,New York
2,Bob Jones,bob@test.org,34,San Francisco
3,Carol White,carol@company.net,29,Chicago
4,David Brown,david@email.com,41,Boston
"""

MARKDOWN_SAMPLE = """# Test Document

This is a **markdown** file with [links](https://example.com) and `code`.

## Section 2

- Item 1 with email@test.com
- Item 2 with http://test.org/path
- Item 3 with API_KEY=sk-12345abcdef

```python
print("Hello world")
```
"""

URL_EMAIL_KEYS = """
Contact us at support@example.com or admin@test.org
Visit https://example.com or http://test.org/path?query=value
API keys: sk-1234567890abcdef, pk_live_abc123, AKIAIOSFODNN7EXAMPLE
GitHub: https://github.com/user/repo
"""

def generate_small_corpus():
    """Small corpus (~10KB)"""
    content = []
    content.append("=== ASCII LOGS ===\n" + ASCII_LOGS * 5)
    content.append("\n=== UNICODE ===\n" + UNICODE_TEXT * 3)
    content.append("\n=== SOURCE CODE ===\n" + SOURCE_CODE * 2)
    content.append("\n=== JSON LOGS ===\n" + JSON_LOGS * 10)
    content.append("\n=== CSV ===\n" + CSV_DATA * 5)
    content.append("\n=== MARKDOWN ===\n" + MARKDOWN_SAMPLE * 2)
    content.append("\n=== URLS/EMAILS ===\n" + URL_EMAIL_KEYS * 3)
    
    # Add file with no matches
    content.append("\n=== NO MATCHES ===\n" + "xyz\n" * 100)
    
    # Add file with many matches
    content.append("\n=== MANY MATCHES ===\n" + "test@example.com\n" * 200)
    
    return "\n".join(content)

def generate_medium_corpus():
    """Medium corpus (~100KB)"""
    small = generate_small_corpus()
    # Repeat and add variations
    content = [small]
    for i in range(5):
        content.append(f"\n=== REPEAT BLOCK {i} ===\n")
        content.append(ASCII_LOGS * 20)
        content.append(JSON_LOGS * 30)
        content.append("random data: " + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=1000)) + "\n")
    return "\n".join(content)

def generate_large_corpus():
    """Large corpus (~1MB)"""
    medium = generate_medium_corpus()
    content = [medium]
    
    # Add long lines
    content.append("\n=== LONG LINES ===\n")
    for i in range(10):
        long_line = "A" * 10000 + f" pattern_{i} " + "B" * 10000 + "\n"
        content.append(long_line)
    
    # Add many short lines
    content.append("\n=== MANY SHORT LINES ===\n")
    for i in range(5000):
        content.append(f"line_{i}: test data {i % 100}\n")
    
    # Add repeated boilerplate
    boilerplate = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10 + "\n"
    content.append("\n=== BOILERPLATE ===\n" + boilerplate * 100)
    
    return "".join(content)

def generate_backtracking_cases():
    """Generate files designed to test backtracking behavior"""
    cases = {}
    
    # Quadratic-like pattern: a+a+a+ on long string of a's
    cases["quadratic_a"] = "a" * 1000 + "b"
    
    # Nested quantifiers
    cases["nested"] = "a" * 500 + "!" + "b" * 500
    
    # Alternation explosion
    cases["alternation"] = ("a" * 100 + "b") * 10
    
    return cases

def main():
    print("Generating reproducible corpus...")
    print(f"Random seed: {RANDOM_SEED}")
    
    # Generate corpora
    corpora = {
        "small.txt": generate_small_corpus(),
        "medium.txt": generate_medium_corpus(),
        "large.txt": generate_large_corpus(),
    }
    
    # Write main corpora
    manifest = {
        "seed": RANDOM_SEED,
        "files": {},
        "generated_at": "2026-06-25T17:06:00Z"
    }
    
    for name, content in corpora.items():
        path = OUTPUT_DIR / name
        write_file(path, content)
        size = len(content.encode('utf-8'))
        sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()
        manifest["files"][name] = {
            "size_bytes": size,
            "sha256": sha256,
            "lines": content.count('\n')
        }
        print(f"  {name}: {size} bytes, {content.count(chr(10))} lines")
    
    # Generate backtracking test cases
    bt_dir = OUTPUT_DIR / "backtracking"
    bt_cases = generate_backtracking_cases()
    for name, content in bt_cases.items():
        path = bt_dir / f"{name}.txt"
        write_file(path, content)
        manifest["files"][f"backtracking/{name}.txt"] = {
            "size_bytes": len(content),
            "sha256": hashlib.sha256(content.encode()).hexdigest(),
            "lines": 1
        }
    
    # Write manifest
    manifest_path = OUTPUT_DIR / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nCorpus generated in {OUTPUT_DIR}/")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
