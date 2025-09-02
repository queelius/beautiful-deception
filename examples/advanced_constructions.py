#!/usr/bin/env python3
"""
Advanced LazyDigest constructions demonstrating security enhancements.

This script shows various ways to extend the basic LazyDigest:
- Hierarchical seeding for extended cycle length
- Rekeying for forward security
- XOR construction for algorithm diversity
- Sponge construction with tunable capacity
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from random_oracles.extended_lazy import (
    HierarchicalLazyDigest,
    RekeyingLazyDigest,
    SpongeLazyDigest,
    XorMultiHashLazyDigest
)


def main():
    print("=" * 60)
    print("Advanced LazyDigest Constructions")
    print("=" * 60)
    
    master_seed = b"master secret key"
    
    # Example 1: Hierarchical Seeding
    print("\n1. Hierarchical LazyDigest")
    print("-" * 40)
    hier = HierarchicalLazyDigest(master_seed)
    print("Structure: Three-level tree (epoch/chunk/position)")
    print(f"Byte at index 0: {hier[0]}")
    print(f"Byte at index 2^20: {hier[2**20]}")
    print(f"Byte at index 2^40: {hier[2**40]}")
    print("Benefit: Extended effective cycle length (~2^316)")
    
    # Example 2: Rekeying for Forward Security
    print("\n2. Rekeying LazyDigest")
    print("-" * 40)
    rekey = RekeyingLazyDigest(master_seed, rekey_interval=1000)
    print("Rekeying every 1000 indices")
    print(f"Byte at index 0 (epoch 0): {rekey[0]}")
    print(f"Byte at index 999 (epoch 0): {rekey[999]}")
    print(f"Byte at index 1000 (epoch 1): {rekey[1000]}")
    print(f"Byte at index 2000 (epoch 2): {rekey[2000]}")
    print("Benefit: Forward security - compromise of epoch n")
    print("         doesn't reveal data from epochs 0..n-1")
    
    # Example 3: XOR Multi-Hash Construction
    print("\n3. XOR Multi-Hash LazyDigest")
    print("-" * 40)
    xor_digest = XorMultiHashLazyDigest(master_seed)
    print("XORing outputs from SHA-256, SHA-512, SHA3-256, BLAKE2b")
    print(f"Byte at index 0: {xor_digest[0]}")
    print(f"Byte at index 100: {xor_digest[100]}")
    print("Benefit: Security even if 3 out of 4 algorithms broken")
    print("Trade-off: 4x computation cost")
    
    # Example 4: Sponge Construction
    print("\n4. Sponge LazyDigest")
    print("-" * 40)
    sponge = SpongeLazyDigest(master_seed, capacity=256)
    print(f"Capacity: 256 bits (never exposed)")
    print(f"Byte at index 0: {sponge[0]}")
    print(f"Byte at index 1000: {sponge[1000]}")
    print("Benefit: Tunable security via capacity parameter")
    print("         Higher capacity = stronger security")
    
    # Example 5: Comparing Security Properties
    print("\n5. Security Properties Comparison")
    print("-" * 40)
    print("Construction        | Cycle Length | Special Property")
    print("-" * 52)
    print("Basic LazyDigest    | ~2^128       | Simple, fast")
    print("Hierarchical        | ~2^316       | Extended state space")
    print("Rekeying           | Undetectable | Forward security")
    print("XOR Multi-Hash     | ~2^128 × 4   | Algorithm diversity")
    print("Sponge             | ~2^capacity  | Tunable security")
    
    # Example 6: Performance Demonstration
    print("\n6. Performance Comparison")
    print("-" * 40)
    import time
    
    constructions = [
        ("Basic", LazyDigest(master_seed)),
        ("Hierarchical", HierarchicalLazyDigest(master_seed)),
        ("Rekeying", RekeyingLazyDigest(master_seed)),
        ("XOR Multi", XorMultiHashLazyDigest(master_seed)),
        ("Sponge", SpongeLazyDigest(master_seed))
    ]
    
    n_accesses = 1000
    print(f"Time to access {n_accesses} sequential bytes:")
    
    for name, digest in constructions:
        start = time.perf_counter()
        for i in range(n_accesses):
            _ = digest[i]
        elapsed = time.perf_counter() - start
        print(f"  {name:12s}: {elapsed*1000:.2f} ms")
    
    print("\n" + "=" * 60)
    print("Key Insight: Different constructions offer different")
    print("             security/performance trade-offs!")
    print("=" * 60)


if __name__ == "__main__":
    main()