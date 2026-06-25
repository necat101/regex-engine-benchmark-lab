# Regex Engine Benchmark Lab

A local, reproducible regex engine benchmark and correctness lab inspired by BurntSushi's rebar and the Hacker News discussion about "A Regex Barometer".

## Overview

This lab addresses the key concerns raised in the HN thread:
- Single geometric-mean summaries can be misleading
- Higher/lower must be explicit
- Not every engine can run every benchmark
- Capture offsets and Unicode make comparisons unfair
- Different engine types have different semantics
- Catastrophic patterns need timeouts
- Compile time vs search time must be separated
- One large file ≠ many small files
- Regex may be overkill for simple cases

## Quick Start

```bash
# Generate deterministic corpus (no downloads)
python3 generate_corpus.py

# Run benchmarks
python3 benchmark.py
```

## Results

See RESULTS.md for benchmark results from the initial run.

Key finding: On a complex email regex, ripgrep (11.67ms) was ~435x faster than Python re (5083ms) due to backtracking differences.

## Files

- `generate_corpus.py` - Creates reproducible test corpus
- `benchmark.py` - Runs benchmarks with correctness checks
- `README.md` - This file
- `RESULTS.md` - Benchmark results

Inspired by BurntSushi/rebar: https://github.com/BurntSushi/rebar
