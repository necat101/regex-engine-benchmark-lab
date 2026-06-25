# Benchmark Results

Generated: 2026-06-25T17:09:15.922502

## Environment
- Python: Python 3.12.3
- Grep: grep (GNU grep) 3.11
- Ripgrep: ripgrep 14.1.1 (rev 4649aa9700)
- Perl: 
- Node: v22.22.3
- OS: Linux 6.17.0-1009-aws x86_64
- CPU: Intel Xeon Platinum 8259CL @ 2.50GHz
- Memory: 3.7GB

## Results Summary

| Engine | Pattern | File | Median (ms) | Matches | Status |
|--------|---------|------|-------------|---------|--------|
| python-re | Sherlock | large.txt | 0.19 | 0 | OK |
| grep-E | Sherlock | large.txt | 15.46 | 0 | OK |
| ripgrep | Sherlock | large.txt | 11.41 | 0 | OK |
| node | Sherlock | large.txt | 87.99 | 0 | OK |
| python-re | test@example\.com | large.txt | 0.29 | 200 | OK |
| grep-E | test@example\.com | large.txt | 14.42 | 200 | OK |
| ripgrep | test@example\.com | large.txt | 11.33 | 200 | OK |
| node | test@example\.com | large.txt | 87.73 | 200 | OK |
| python-re | sherlock | large.txt | 7.04 | 0 | OK |
| grep-E | sherlock | large.txt | 15.62 | 0 | OK |
| ripgrep | sherlock | large.txt | 11.75 | 0 | OK |
| node | sherlock | large.txt | 86.08 | 0 | OK |
| python-re | ERROR | large.txt | 5.52 | 425 | OK |
| grep-E | ERROR | large.txt | 16.45 | 425 | OK |
| ripgrep | ERROR | large.txt | 11.35 | 425 | OK |
| node | ERROR | large.txt | 85.57 | 425 | OK |
| python-re | [0-9]{3}-[0-9]{2}-[0-9]{4} | large.txt | 8.98 | 0 | OK |
| grep-E | [0-9]{3}-[0-9]{2}-[0-9]{4} | large.txt | 15.03 | 0 | OK |
| ripgrep | [0-9]{3}-[0-9]{2}-[0-9]{4} | large.txt | 11.87 | 0 | OK |
| node | [0-9]{3}-[0-9]{2}-[0-9]{4} | large.txt | 87.03 | 0 | OK |
| python-re | [a-zA-Z_][a-zA-Z0-9_]* | large.txt | 14.42 | 32656 | OK |
| grep-E | [a-zA-Z_][a-zA-Z0-9_]* | large.txt | 82.73 | 32656 | OK |
| ripgrep | [a-zA-Z_][a-zA-Z0-9_]* | large.txt | 32.57 | 32656 | OK |
| node | [a-zA-Z_][a-zA-Z0-9_]* | large.txt | 101.28 | 32656 | OK |
| python-re | INFO|ERROR|WARN|DEBUG | large.txt | 2.32 | 1005 | OK |
| grep-E | INFO|ERROR|WARN|DEBUG | large.txt | 15.39 | 1005 | OK |
| ripgrep | INFO|ERROR|WARN|DEBUG | large.txt | 11.74 | 1005 | OK |
| node | INFO|ERROR|WARN|DEBUG | large.txt | 90.73 | 1005 | OK |
| python-re | https?://[^\s]+ | large.txt | 0.22 | 13 | OK |
| grep-E | https?://[^\s]+ | large.txt | 18.86 | 10 | OK |
| ripgrep | https?://[^\s]+ | large.txt | 12.74 | 13 | OK |
| node | https?://[^\s]+ | large.txt | 93.03 | 13 | OK |
| python-re | \d{4}-\d{2}-\d{2} | large.txt | 10.23 | 1005 | OK |
| grep-E | \d{4}-\d{2}-\d{2} | large.txt | 14.89 | 0 | OK |
| ripgrep | \d{4}-\d{2}-\d{2} | large.txt | 19.59 | 1005 | OK |
| node | \d{4}-\d{2}-\d{2} | large.txt | 86.98 | 1005 | OK |
| python-re | \d{2}/\d{2}/\d{4} | large.txt | 10.22 | 0 | OK |
| grep-E | \d{2}/\d{2}/\d{4} | large.txt | 14.13 | 0 | OK |
| ripgrep | \d{2}/\d{2}/\d{4} | large.txt | 18.46 | 0 | OK |
| node | \d{2}/\d{2}/\d{4} | large.txt | 85.83 | 0 | OK |
| python-re | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | large.txt | 5083.16 | 228 | OK |
| grep-E | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | large.txt | 16.72 | 228 | OK |
| ripgrep | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | large.txt | 11.67 | 228 | OK |
| node | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | large.txt | 2943.15 | 228 | OK |
| python-re | \btest\b | large.txt | 11.32 | 5218 | OK |
| grep-E | \btest\b | large.txt | 23.60 | 5218 | OK |
| ripgrep | \btest\b | large.txt | 14.45 | 5218 | OK |
| node | \btest\b | large.txt | 85.77 | 5218 | OK |
| python-re | \b\w+@\w+\.\w+\b | large.txt | 15.62 | 228 | OK |
| grep-E | \b\w+@\w+\.\w+\b | large.txt | 15.50 | 228 | OK |
| ripgrep | \b\w+@\w+\.\w+\b | large.txt | 15.24 | 228 | OK |
| node | \b\w+@\w+\.\w+\b | large.txt | 87.60 | 228 | OK |
| python-re | Sherlock | medium.txt | 0.03 | 0 | OK |
| grep-E | Sherlock | medium.txt | 14.80 | 0 | OK |
| ripgrep | Sherlock | medium.txt | 10.66 | 0 | OK |
| node | Sherlock | medium.txt | 84.26 | 0 | OK |
| python-re | test@example\.com | medium.txt | 0.10 | 200 | OK |
| grep-E | test@example\.com | medium.txt | 14.31 | 200 | OK |
| ripgrep | test@example\.com | medium.txt | 10.99 | 200 | OK |
| node | test@example\.com | medium.txt | 85.30 | 200 | OK |
| python-re | sherlock | medium.txt | 1.52 | 0 | OK |
| grep-E | sherlock | medium.txt | 14.43 | 0 | OK |
| ripgrep | sherlock | medium.txt | 11.76 | 0 | OK |
| node | sherlock | medium.txt | 71.58 | 0 | OK |
| python-re | ERROR | medium.txt | 2.33 | 425 | OK |
| grep-E | ERROR | medium.txt | 9.89 | 425 | OK |
| ripgrep | ERROR | medium.txt | 7.70 | 425 | OK |
| node | ERROR | medium.txt | 76.09 | 425 | OK |
| python-re | [0-9]{3}-[0-9]{2}-[0-9]{4} | medium.txt | 3.79 | 0 | OK |
| grep-E | [0-9]{3}-[0-9]{2}-[0-9]{4} | medium.txt | 7.17 | 0 | OK |
| ripgrep | [0-9]{3}-[0-9]{2}-[0-9]{4} | medium.txt | 8.85 | 0 | OK |
| node | [0-9]{3}-[0-9]{2}-[0-9]{4} | medium.txt | 73.50 | 0 | OK |
| python-re | [a-zA-Z_][a-zA-Z0-9_]* | medium.txt | 6.01 | 9620 | OK |
| grep-E | [a-zA-Z_][a-zA-Z0-9_]* | medium.txt | 26.43 | 9620 | OK |
| ripgrep | [a-zA-Z_][a-zA-Z0-9_]* | medium.txt | 14.46 | 9620 | OK |
| node | [a-zA-Z_][a-zA-Z0-9_]* | medium.txt | 81.47 | 9620 | OK |
| python-re | INFO|ERROR|WARN|DEBUG | medium.txt | 1.41 | 1005 | OK |
| grep-E | INFO|ERROR|WARN|DEBUG | medium.txt | 8.98 | 1005 | OK |
| ripgrep | INFO|ERROR|WARN|DEBUG | medium.txt | 7.83 | 1005 | OK |
| node | INFO|ERROR|WARN|DEBUG | medium.txt | 78.47 | 1005 | OK |
| python-re | https?://[^\s]+ | medium.txt | 0.05 | 13 | OK |
| grep-E | https?://[^\s]+ | medium.txt | 14.45 | 10 | OK |
| ripgrep | https?://[^\s]+ | medium.txt | 12.02 | 13 | OK |
| node | https?://[^\s]+ | medium.txt | 81.71 | 13 | OK |
| python-re | \d{4}-\d{2}-\d{2} | medium.txt | 2.65 | 1005 | OK |
| grep-E | \d{4}-\d{2}-\d{2} | medium.txt | 14.53 | 0 | OK |
| ripgrep | \d{4}-\d{2}-\d{2} | medium.txt | 19.32 | 1005 | OK |
| node | \d{4}-\d{2}-\d{2} | medium.txt | 84.96 | 1005 | OK |
| python-re | \d{2}/\d{2}/\d{4} | medium.txt | 2.23 | 0 | OK |
| grep-E | \d{2}/\d{2}/\d{4} | medium.txt | 13.93 | 0 | OK |
| ripgrep | \d{2}/\d{2}/\d{4} | medium.txt | 18.12 | 0 | OK |
| node | \d{2}/\d{2}/\d{4} | medium.txt | 83.21 | 0 | OK |
| python-re | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | medium.txt | 15.88 | 228 | OK |
| grep-E | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | medium.txt | 15.45 | 228 | OK |
| ripgrep | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | medium.txt | 11.09 | 228 | OK |
| node | [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.- | medium.txt | 101.17 | 228 | OK |
| python-re | \btest\b | medium.txt | 2.81 | 218 | OK |
| grep-E | \btest\b | medium.txt | 15.41 | 218 | OK |
| ripgrep | \btest\b | medium.txt | 11.21 | 218 | OK |
| node | \btest\b | medium.txt | 85.68 | 218 | OK |
| python-re | \b\w+@\w+\.\w+\b | medium.txt | 3.96 | 228 | OK |
| grep-E | \b\w+@\w+\.\w+\b | medium.txt | 15.56 | 228 | OK |
| ripgrep | \b\w+@\w+\.\w+\b | medium.txt | 15.53 | 228 | OK |
| node | \b\w+@\w+\.\w+\b | medium.txt | 82.49 | 228 | OK |

## Notes

- **104 total benchmarks** run (4 engines × 13 patterns × 2 files)
- **Key semantic difference**: grep -E doesn't support `\d` (POSIX ERE) - shows 0 matches vs 1005 for others on date patterns
- **Pathological case**: Email regex shows 435x difference between Python re (5083ms) and ripgrep (11.67ms) on large.txt
- **Process overhead**: CLI tools include ~10-15ms startup time vs Python's in-process execution
