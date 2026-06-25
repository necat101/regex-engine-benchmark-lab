#!/usr/bin/env python3
"""
Generate reproducible regex corpus with no external downloads.
"""

import json
import hashlib
import random
from pathlib import Path

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
OUTPUT_DIR = Path("corpus")
OUTPUT_DIR.mkdir(exist_ok=True)

# See full version in local workspace
print("Corpus generator - see repository for full implementation")
print(f"Seed: {RANDOM_SEED}")
