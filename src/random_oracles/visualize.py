"""
Visual Demonstrations of Cryptographic Concepts

This module provides ASCII visualizations of hash functions and oracles,
making abstract concepts visually concrete.
"""

from digest import Digest, OracleDigest, LazyDigest
from hash import Oracle, CryptoHash, OracleHash
import hashlib


def visualize_finite_vs_infinite():
    """
    Visualize the difference between finite hashes and infinite oracles
    """
    print("\n" + "="*70)
    print("FINITE vs INFINITE DIGESTS")
    print("="*70)
    
    # Finite hash
    crypto_hash = CryptoHash()
    finite = crypto_hash(b"finite")
    
    print("\nFinite Hash (SHA-256): {0,1}^256")
    print("─" * 35)
    print(f"[{finite.hexdigest()[:8]}...{finite.hexdigest()[-8:]}]")
    print(f"Length: {len(finite)} bytes (fixed)")
    print("│")
    print("└─> Ends at byte 32")
    
    # Infinite oracle
    print("\nInfinite Oracle: {0,1}^∞")
    print("─" * 35)
    lazy = LazyDigest(b"infinite")
    visualization = ""
    for i in range(12):
        visualization += f"{lazy[i]:02x}"
    print(f"[{visualization}...")
    print("                      ↓")
    print(f"                    {lazy[100]:02x}")
    print("                      ↓")  
    print(f"                    {lazy[1000]:02x}")
    print("                      ↓")
    print("                     ∞")
    print("└─> Never ends (lazy evaluation)")


def visualize_oracle_family():
    """
    Visualize how each Oracle instance is different
    """
    print("\n" + "="*70)
    print("ORACLE FAMILY: Each Instance is a Different Random Function")
    print("="*70)
    
    input_data = b"test"
    
    print(f"\nInput: {input_data}")
    print("─" * 35)
    
    # Create 3 different oracle instances
    for i in range(3):
        oracle_instance = OracleDigest(input_data)
        bytes_preview = [oracle_instance[j] for j in range(8)]
        hex_preview = ''.join(f"{b:02x}" for b in bytes_preview)
        
        print(f"Oracle #{i+1}: [{hex_preview}...] ")
        print(f"           └─> Independent random function")
    
    print("\nProperty: Same input, different oracles → different outputs")
    print("Mathematical: Selecting from family {{f: {0,1}* → {0,1}^∞}}")


def visualize_lazy_computation():
    """
    Visualize how lazy evaluation works
    """
    print("\n" + "="*70)
    print("LAZY COMPUTATION: Generate On-Demand")
    print("="*70)
    
    seed = b"lazy_seed"
    lazy = LazyDigest(seed)
    
    print(f"\nSeed: {seed}")
    print("─" * 35)
    print("\nAccess Pattern → Computation:")
    print()
    
    # Show sparse access
    indices = [0, 5, 100, 1000]
    for idx in indices:
        value = lazy[idx]
        computation = f"h(seed || {idx})[0]"
        print(f"  lazy[{idx:4}] = 0x{value:02x}  ← computed via {computation}")
    
    print("\n✓ Note: We never computed indices 1-4, 6-99, 101-999!")
    print("  This is the power of lazy evaluation with codata")


def visualize_truncation_operation():
    """
    Visualize truncation from infinite to finite
    """
    print("\n" + "="*70)
    print("TRUNCATION: Bridge from Infinite to Finite")
    print("="*70)
    
    oracle_hash = OracleHash()
    infinite = oracle_hash(b"truncate_me")
    
    print("\nInfinite Oracle Output:")
    print("─" * 35)
    
    # Show first 40 bytes with visual truncation points
    visual = ""
    for i in range(40):
        if i == 16:
            visual += "│"
        elif i == 32:
            visual += "║"
        visual += f"{infinite[i]:02x}"
        if i == 15:
            visual += "│"
        elif i == 31:
            visual += "║"
    
    print(f"[{visual}...]")
    print(" " * 33 + "↑" + " " * 32 + "↑")
    print(" " * 30 + "16 bytes" + " " * 24 + "32 bytes")
    
    # Show truncations
    truncated_16 = infinite.truncate(16)
    truncated_32 = infinite.truncate(32)
    
    print("\nTruncation Results:")
    print(f"  truncate(16) → {truncated_16.hexdigest()} (MD5 size)")
    print(f"  truncate(32) → {truncated_32.hexdigest()[:32]}... (SHA-256 size)")
    
    print("\nMathematical: π_{n}: {0,1}^∞ → {0,1}^n (projection)")


def visualize_composition_paths():
    """
    Visualize different paths to achieve similar results
    """
    print("\n" + "="*70)
    print("COMPOSITION: Multiple Paths to Hash Functions")
    print("="*70)
    
    input_data = b"compose"
    
    print(f"\nInput: '{input_data.decode()}'")
    print("─" * 35)
    
    print("\nPath 1: Direct Cryptographic Hash")
    print("  input → [SHA-256] → {0,1}^256")
    crypto = CryptoHash()
    direct = crypto(input_data)
    print(f"  Result: {direct.hexdigest()[:16]}...")
    
    print("\nPath 2: Oracle + Truncation")
    print("  input → [Oracle] → {0,1}^∞ → [truncate(32)] → {0,1}^256")
    oracle = OracleHash()
    infinite = oracle(input_data)
    truncated = infinite.truncate(32)
    print(f"  Result: {truncated.hexdigest()[:16]}...")
    
    print("\nPath 3: Lazy Evaluation Chain")
    lazy_seed = hashlib.sha256(input_data).digest()
    lazy = LazyDigest(lazy_seed)
    print("  input → [SHA-256] → seed → [LazyDigest] → {0,1}^∞")
    print(f"  Can access lazy[10^9] without storing 10^9 bytes!")
    
    print("\n✓ Different paths demonstrate different theoretical properties")


def visualize_all():
    """
    Run all visualizations
    """
    print("\n" + "🔐" * 35)
    print("\nCRYPTOGRAPHIC CONCEPTS: VISUAL DEMONSTRATIONS")
    print("\n" + "🔐" * 35)
    
    visualize_finite_vs_infinite()
    visualize_oracle_family()
    visualize_lazy_computation()
    visualize_truncation_operation()
    visualize_composition_paths()
    
    print("\n" + "="*70)
    print("Visualizations complete! Abstract made concrete.")
    print("="*70)


if __name__ == "__main__":
    visualize_all()