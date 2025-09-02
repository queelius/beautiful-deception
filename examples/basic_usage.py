#!/usr/bin/env python3
"""
Basic usage examples for the Beautiful Deception library.

This script demonstrates the fundamental difference between:
1. OracleDigest - A true random oracle (impossible to implement correctly)
2. LazyDigest - A deterministic function that pretends to be random
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from random_oracles import LazyDigest, OracleDigest, Digest
import hashlib


def main():
    print("=" * 60)
    print("The Beautiful Deception: Basic Usage Examples")
    print("=" * 60)
    
    # Example 1: Basic Digest
    print("\n1. Basic Digest (finite, traditional hash)")
    print("-" * 40)
    data = b"Hello, World!"
    hash_output = hashlib.sha256(data).digest()
    digest = Digest(hash_output)
    print(f"Input: {data}")
    print(f"SHA-256 digest: {digest.hexdigest()[:32]}...")
    print(f"First byte: {digest.digest()[0]}")
    
    # Example 2: OracleDigest (true random oracle - fails)
    print("\n2. OracleDigest (true random oracle)")
    print("-" * 40)
    oracle = OracleDigest(b"test input")
    print(f"Byte at index 0: {oracle[0]}")
    print(f"Byte at index 100: {oracle[100]}")
    print(f"Byte at index 0 again: {oracle[0]} (consistent!)")
    print(f"Cache size: {len(oracle.cache)} entries")
    print("⚠️  Warning: Cache grows unbounded with each new index!")
    
    # Example 3: LazyDigest (the beautiful deception)
    print("\n3. LazyDigest (deterministic infinite digest)")
    print("-" * 40)
    seed = b"my secret seed"
    lazy = LazyDigest(seed)
    print(f"Seed: {seed}")
    print(f"Byte at index 0: {lazy[0]}")
    print(f"Byte at index 1000000: {lazy[1000000]}")
    print(f"First 16 bytes: {lazy.truncate(16).hex()}")
    print("✅ Memory usage: O(1) - no cache needed!")
    
    # Example 4: Reproducibility
    print("\n4. Reproducibility Comparison")
    print("-" * 40)
    
    # Two LazyDigests with same seed
    lazy1 = LazyDigest(b"shared seed")
    lazy2 = LazyDigest(b"shared seed")
    print(f"LazyDigest 1, byte 42: {lazy1[42]}")
    print(f"LazyDigest 2, byte 42: {lazy2[42]}")
    print(f"Are they equal? {lazy1[42] == lazy2[42]} ✅")
    
    # Two OracleDigests with same input
    oracle1 = OracleDigest(b"shared input")
    oracle2 = OracleDigest(b"shared input")
    print(f"\nOracleDigest 1, byte 42: {oracle1[42]}")
    print(f"OracleDigest 2, byte 42: {oracle2[42]}")
    print(f"Are they equal? {oracle1[42] == oracle2[42]} ❌")
    print("(Different random values - not reproducible!)")
    
    # Example 5: The Deception in Action
    print("\n5. The Deception: Finite Pretending to be Infinite")
    print("-" * 40)
    lazy = LazyDigest(b"finite seed")
    
    # Access "infinite" sequence
    indices = [0, 10, 100, 1000, 10000, 100000, 1000000]
    print("Accessing bytes at exponentially growing indices:")
    for i in indices:
        print(f"  Index {i:7d}: byte value {lazy[i]:3d}")
    
    print("\n🎭 The Beautiful Deception:")
    print("  - Appears: Infinite random sequence")
    print("  - Reality: Deterministic function with 256 bits of state")
    print("  - Memory:  Constant O(1) regardless of access pattern")
    print("  - Secret:  hash(seed || index) for each byte")
    
    print("\n" + "=" * 60)
    print("Key Insight: We're not storing randomness,")
    print("             we're computing it on demand!")
    print("=" * 60)


if __name__ == "__main__":
    main()