#!/usr/bin/env python3
"""
Interactive demonstration of random oracles and hash functions
"""

import hashlib
from .digest import Digest, OracleDigest, LazyDigest
from .hash import Oracle, CryptoHash, OracleHash
from .properties import run_all_properties
from .visualize import visualize_all


def interactive_demo():
    """
    Interactive demonstration of key concepts
    """
    print("\n" + "="*70)
    print("RANDOM ORACLES: Interactive Demonstration")
    print("="*70)
    
    print("\n1. Creating a traditional cryptographic hash:")
    print("-" * 40)
    crypto_hash = CryptoHash()
    input_data = b"Hello, Random Oracle!"
    digest = crypto_hash(input_data)
    print(f"Input: {input_data}")
    print(f"SHA-256: {digest.hexdigest()}")
    print(f"Length: {len(digest)} bytes (fixed)")
    
    print("\n2. Creating an infinite lazy digest:")
    print("-" * 40)
    lazy = LazyDigest(b"infinite_seed")
    print(f"Accessing sparse indices without computing all values:")
    for idx in [0, 100, 10000]:
        print(f"  lazy[{idx:5}] = 0x{lazy[idx]:02x}")
    
    print("\n3. Random oracle with entropy:")
    print("-" * 40)
    oracle_digest = OracleDigest(b"random_input")
    print(f"First 8 bytes: ", end="")
    for i in range(8):
        print(f"{oracle_digest[i]:02x}", end=" ")
    print("\n(Each OracleDigest instance is a different random function)")
    
    print("\n4. Truncation from infinite to finite:")
    print("-" * 40)
    oracle_hash = OracleHash()
    infinite_digest = oracle_hash(b"truncate_me")
    finite_16 = infinite_digest.truncate(16)
    finite_32 = infinite_digest.truncate(32)
    print(f"Infinite digest → truncate(16): {finite_16.hexdigest()}")
    print(f"Infinite digest → truncate(32): {finite_32.hexdigest()[:32]}...")
    
    print("\n5. Oracle consistency:")
    print("-" * 40)
    oracle = Oracle()
    digest1 = oracle(b"consistent")
    digest2 = oracle(b"consistent")
    print(f"First call:  oracle(b'consistent')[0] = 0x{digest1[0]:02x}")
    print(f"Second call: oracle(b'consistent')[0] = 0x{digest2[0]:02x}")
    print(f"Consistent: {digest1[0] == digest2[0]}")
    
    print("\n" + "="*70)
    print("Demo complete! Explore further with properties and visualizations.")
    print("="*70)


def main():
    """
    Main entry point for the demo
    """
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "properties":
            run_all_properties()
        elif sys.argv[1] == "visualize":
            visualize_all()
        elif sys.argv[1] == "all":
            interactive_demo()
            print("\n" + "Press Enter to continue to properties...")
            input()
            run_all_properties()
            print("\n" + "Press Enter to continue to visualizations...")
            input()
            visualize_all()
        else:
            print("Usage: random-oracles-demo [properties|visualize|all]")
    else:
        interactive_demo()


if __name__ == "__main__":
    main()