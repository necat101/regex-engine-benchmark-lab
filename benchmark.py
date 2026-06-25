#!/usr/bin/env python3
"""
Regex Engine Benchmark and Correctness Lab
Compares multiple regex engines with correctness checks before timing.
"""

import subprocess
import time
import json
import hashlib
import statistics
import sys
import re
import os
from pathlib import Path
from datetime import datetime

# Configuration
CORPUS_DIR = Path("corpus")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

TIMEOUT_SECONDS = 5.0
TRIALS = 3

# Test patterns organized by category
TEST_PATTERNS = {
    "literal": [
        ("Sherlock", False, False),
        ("test@example\\.com", False, False),
    ],
    "case_insensitive": [
        ("sherlock", True, False),
        ("ERROR", True, False),
    ],
    "character_classes": [
        ("[0-9]{3}-[0-9]{2}-[0-9]{4}", False, False),
        ("[a-zA-Z_][a-zA-Z0-9_]*", False, False),
    ],
    "alternations": [
        ("INFO|ERROR|WARN|DEBUG", False, False),
        ("https?://[^\\s]+", False, False),
    ],
    "dates": [
        ("\\d{4}-\\d{2}-\\d{2}", False, False),
        ("\\d{2}/\\d{2}/\\d{4}", False, False),
    ],
    "emails": [
        ("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", False, False),
    ],
    "word_boundaries": [
        ("\\btest\\b", False, False),
        ("\\b\\w+@\\w+\\.\\w+\\b", False, False),
    ],
}

# Backtracking-risk patterns (with strict timeouts)
RISKY_PATTERNS = {
    "quadratic": ("(a+)+b", "a" * 100 + "b"),
    "nested": ("(a+)+$", "a" * 50),
}

class EngineResult:
    def __init__(self, engine, pattern, file):
        self.engine = engine
        self.pattern = pattern
        self.file = file
        self.compile_time = None
        self.search_times = []
        self.match_count = None
        self.exit_code = None
        self.stderr = ""
        self.timeout = False
        self.skipped = False
        self.skip_reason = ""
        self.version = ""
        self.correctness_hash = ""
        
    def to_dict(self):
        return {
            "engine": self.engine,
            "pattern": self.pattern,
            "file": str(self.file),
            "compile_time_ms": self.compile_time,
            "search_times_ms": self.search_times,
            "search_median_ms": statistics.median(self.search_times) if self.search_times else None,
            "match_count": self.match_count,
            "exit_code": self.exit_code,
            "timeout": self.timeout,
            "skipped": self.skipped,
            "skip_reason": self.skip_reason,
            "version": self.version,
            "correctness_hash": self.correctness_hash,
        }

def get_tool_versions():
    """Get versions of available tools"""
    versions = {}
    
    tools = {
        "python": ["python3", "--version"],
        "grep": ["grep", "--version"],
        "rg": ["rg", "--version"],
        "perl": ["perl", "-v"],
        "node": ["node", "--version"],
    }
    
    for name, cmd in tools.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            output = result.stdout + result.stderr
            versions[name] = output.split('\n')[0].strip()
        except:
            versions[name] = "not available"
    
    return versions

def run_python_re(pattern, file_path, flags=0):
    """Benchmark Python re module"""
    import re as re_module
    
    # Compile separately to measure compile time
    start = time.perf_counter()
    try:
        compiled = re_module.compile(pattern, flags)
        compile_time = (time.perf_counter() - start) * 1000
    except Exception as e:
        return None, 0, f"Compile error: {e}", False
    
    # Read file
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Time search
    times = []
    match_count = 0
    for _ in range(TRIALS):
        start = time.perf_counter()
        matches = list(compiled.finditer(content))
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
        match_count = len(matches)
    
    # Correctness hash
    matches_text = "\n".join([f"{m.start()}:{m.end()}:{m.group()}" for m in matches[:100]])
    correctness_hash = hashlib.sha256(matches_text.encode()).hexdigest()[:16]
    
    return compile_time, times, match_count, "", False, correctness_hash

def run_grep(pattern, file_path, extended=False, ignore_case=False):
    """Benchmark GNU grep"""
    cmd = ["grep"]
    if extended:
        cmd.append("-E")
    if ignore_case:
        cmd.append("-i")
    cmd.extend(["-o", "-n", pattern, str(file_path)])
    
    times = []
    match_count = 0
    stderr_output = ""
    
    for _ in range(TRIALS):
        start = time.perf_counter()
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=TIMEOUT_SECONDS
            )
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            
            if result.returncode in (0, 1):  # 0=matches, 1=no matches
                match_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                stderr_output = result.stderr
            else:
                stderr_output = result.stderr
                break
        except subprocess.TimeoutExpired:
            return None, [], 0, "TIMEOUT", True
    
    # Correctness hash from output
    correctness_hash = hashlib.sha256(result.stdout.encode()).hexdigest()[:16] if 'result' in locals() else ""
    
    return None, times, match_count, stderr_output, False, correctness_hash

def run_ripgrep(pattern, file_path, ignore_case=False):
    """Benchmark ripgrep"""
    cmd = ["rg", "--no-heading", "-o", "-n"]
    if ignore_case:
        cmd.append("-i")
    cmd.extend([pattern, str(file_path)])
    
    times = []
    match_count = 0
    
    for _ in range(TRIALS):
        start = time.perf_counter()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            match_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except subprocess.TimeoutExpired:
            return None, [], 0, "TIMEOUT", True
    
    correctness_hash = hashlib.sha256(result.stdout.encode()).hexdigest()[:16] if 'result' in locals() else ""
    return None, times, match_count, "", False, correctness_hash

def run_perl(pattern, file_path, ignore_case=False):
    """Benchmark Perl"""
    flags = "i" if ignore_case else ""
    perl_code = f"""
    $count = 0;
    while (<>) {{
        $count += () = /{pattern}/{flags}g;
    }}
    print $count;
    """
    
    times = []
    match_count = 0
    
    for _ in range(TRIALS):
        start = time.perf_counter()
        try:
            result = subprocess.run(
                ["perl", "-e", perl_code, str(file_path)],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS
            )
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            if result.returncode == 0:
                match_count = int(result.stdout.strip() or 0)
        except subprocess.TimeoutExpired:
            return None, [], 0, "TIMEOUT", True
        except ValueError:
            match_count = 0
    
    return None, times, match_count, "", False, ""

def run_node(pattern, file_path, ignore_case=False):
    """Benchmark Node.js"""
    flags = "gi" if ignore_case else "g"
    node_code = f"""
    const fs = require('fs');
    const content = fs.readFileSync(process.argv[1], 'utf8');
    const regex = new RegExp(process.argv[2], '{flags}');
    const matches = content.match(regex);
    console.log(matches ? matches.length : 0);
    """
    
    times = []
    match_count = 0
    
    for _ in range(TRIALS):
        start = time.perf_counter()
        try:
            result = subprocess.run(
                ["node", "-e", node_code, str(file_path), pattern],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS
            )
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
            if result.returncode == 0:
                match_count = int(result.stdout.strip() or 0)
        except subprocess.TimeoutExpired:
            return None, [], 0, "TIMEOUT", True
        except:
            match_count = 0
    
    return None, times, match_count, "", False, ""

def benchmark_engine(engine_name, pattern, file_path, ignore_case=False):
    """Run benchmark for a specific engine"""
    result = EngineResult(engine_name, pattern, file_path.name)
    
    try:
        if engine_name == "python-re":
            flags = re.IGNORECASE if ignore_case else 0
            compile_time, times, count, stderr, timeout, chash = run_python_re(
                pattern, file_path, flags
            )
            result.compile_time = compile_time
            result.search_times = times
            result.match_count = count
            result.stderr = stderr
            result.timeout = timeout
            result.correctness_hash = chash
            
        elif engine_name == "grep-E":
            _, times, count, stderr, timeout, chash = run_grep(
                pattern, file_path, extended=True, ignore_case=ignore_case
            )
            result.search_times = times
            result.match_count = count
            result.stderr = stderr
            result.timeout = timeout
            result.correctness_hash = chash
            
        elif engine_name == "ripgrep":
            _, times, count, stderr, timeout, chash = run_ripgrep(
                pattern, file_path, ignore_case=ignore_case
            )
            result.search_times = times
            result.match_count = count
            result.stderr = stderr
            result.timeout = timeout
            result.correctness_hash = chash
            
        elif engine_name == "perl":
            _, times, count, stderr, timeout, _ = run_perl(
                pattern, file_path, ignore_case=ignore_case
            )
            result.search_times = times
            result.match_count = count
            result.stderr = stderr
            result.timeout = timeout
            
        elif engine_name == "node":
            _, times, count, stderr, timeout, _ = run_node(
                pattern, file_path, ignore_case=ignore_case
            )
            result.search_times = times
            result.match_count = count
            result.stderr = stderr
            result.timeout = timeout
            
        else:
            result.skipped = True
            result.skip_reason = "Engine not implemented"
            
    except Exception as e:
        result.stderr = str(e)
        result.exit_code = -1
    
    return result

def main():
    print("Regex Engine Benchmark Lab")
    print("=" * 50)
    
    # Check corpus exists
    if not CORPUS_DIR.exists():
        print("ERROR: Corpus not found. Run generate_corpus.py first.")
        sys.exit(1)
    
    # Get versions
    versions = get_tool_versions()
    print("\nTool Versions:")
    for tool, version in versions.items():
        print(f"  {tool}: {version}")
    
    # Find test files
    test_files = sorted(CORPUS_DIR.glob("*.txt"))
    if not test_files:
        print("ERROR: No test files found in corpus/")
        sys.exit(1)
    
    print(f"\nTest files: {[f.name for f in test_files]}")
    
    # Engines to test (only available ones)
    engines = []
    if versions["python"] != "not available":
        engines.append("python-re")
    if "grep" in versions and versions["grep"] != "not available":
        engines.append("grep-E")
    if "rg" in versions and "ripgrep" in versions["rg"].lower():
        engines.append("ripgrep")
    if versions.get("perl", "").startswith("This is perl"):
        engines.append("perl")
    if versions.get("node", "").startswith("v"):
        engines.append("node")
    
    print(f"Engines to test: {engines}")
    
    # Run benchmarks
    all_results = []
    
    for file_path in test_files[:2]:  # Limit to small/medium for initial run
        print(f"\n--- Testing {file_path.name} ---")
        
        file_size = file_path.stat().st_size
        print(f"File size: {file_size} bytes")
        
        for category, patterns in TEST_PATTERNS.items():
            for pattern, ignore_case, _ in patterns[:2]:  # Limit patterns for speed
                print(f"\n  Pattern [{category}]: {pattern[:40]}")
                
                for engine in engines:
                    result = benchmark_engine(engine, pattern, file_path, ignore_case)
                    result.version = versions.get(engine.split('-')[0], "")
                    all_results.append(result)
                    
                    if result.skipped:
                        print(f"    {engine}: SKIPPED - {result.skip_reason}")
                    elif result.timeout:
                        print(f"    {engine}: TIMEOUT")
                    elif result.search_times:
                        median = statistics.median(result.search_times)
                        print(f"    {engine}: {median:.2f}ms ({result.match_count} matches)")
                    else:
                        print(f"    {engine}: FAILED - {result.stderr[:50]}")
    
    # Save results
    timestamp = datetime.now().isoformat()
    results_data = {
        "timestamp": timestamp,
        "versions": versions,
        "config": {
            "trials": TRIALS,
            "timeout_seconds": TIMEOUT_SECONDS,
            "corpus_dir": str(CORPUS_DIR),
        },
        "results": [r.to_dict() for r in all_results]
    }
    
    results_file = RESULTS_DIR / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"\n\nResults saved to: {results_file}")
    print(f"Total benchmarks run: {len(all_results)}")
    
    # Generate summary
    generate_markdown_summary(results_data, versions)

def generate_markdown_summary(results_data, versions):
    """Generate markdown summary of results"""
    output = []
    output.append("# Benchmark Results")
    output.append(f"\nGenerated: {results_data['timestamp']}")
    output.append("\n## Environment")
    output.append(f"- Python: {versions.get('python', 'unknown')}")
    output.append(f"- Grep: {versions.get('grep', 'unknown')}")
    output.append(f"- Ripgrep: {versions.get('rg', 'unknown')}")
    output.append(f"- Perl: {versions.get('perl', 'unknown').split(chr(10))[0]}")
    output.append(f"- Node: {versions.get('node', 'unknown')}")
    
    output.append("\n## Results Summary")
    output.append("\n| Engine | Pattern | File | Median (ms) | Matches | Status |")
    output.append("|--------|---------|------|-------------|---------|--------|")
    
    for r in results_data['results']:
        if r['skipped']:
            status = "SKIPPED"
            median = "-"
        elif r['timeout']:
            status = "TIMEOUT"
            median = "-"
        elif r['search_median_ms']:
            status = "OK"
            median = f"{r['search_median_ms']:.2f}"
        else:
            status = "FAIL"
            median = "-"
        
        output.append(
            f"| {r['engine']} | {r['pattern'][:30]} | {r['file']} | "
            f"{median} | {r['match_count'] or 0} | {status} |"
        )
    
    # Write to RESULTS.md
    with open("RESULTS.md", "w") as f:
        f.write("\n".join(output))
    
    print("Summary written to RESULTS.md")

if __name__ == "__main__":
    main()
