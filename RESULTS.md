# Benchmark Results

Generated: 2026-06-25T17:09:15 UTC

## Environment
- OS: Linux 6.17.0-1009-aws x86_64
- CPU: Intel Xeon Platinum 8259CL @ 2.50GHz (2 cores)
- Python: 3.12.3
- grep: GNU grep 3.11
- ripgrep: 14.1.1
- Node.js: v22.22.3

## Summary

104 benchmarks run across 4 engines and 2 files (medium.txt, large.txt).

### Key Findings

1. **Process startup overhead dominates**
   - Python re: 0.03-0.29ms (in-process)
   - grep/ripgrep: 10-16ms (process spawn)
   - Node.js: 71-101ms (Node startup)

2. **Semantic differences invalidate comparisons**
   - `grep -E` with `\d`: 0 matches (POSIX ERE doesn't support `\d`)
   - Others: 1005 matches
   - Cannot compare timing - different work being done

3. **Pathological patterns show extreme differences**
   - Email regex on large.txt:
     - ripgrep: 11.67ms
     - Python re: 5,083ms
     - **435x difference** - backtracking vs DFA

4. **Literal optimizations work well**
   - All engines handle simple literals efficiently
   - Character classes with many matches (32,656) still perform reasonably

## Full Results

See the repository for complete benchmark data and methodology.

**Repository**: https://github.com/necat101/regex-engine-benchmark-lab
