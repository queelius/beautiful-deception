"""
Formal Algorithm Descriptions and Their Implementations

This module presents the mathematical algorithms underlying our random oracle
and hash function implementations, connecting theory to practice.
"""

from .digest import Digest, OracleDigest, LazyDigest
from .hash import Oracle, CryptoHash, OracleHash
import hashlib


def describe_algorithms():
    """
    Present formal algorithm descriptions with their implementations
    """
    print("=" * 70)
    print("ALGORITHMS: From Mathematical Description to Implementation")
    print("=" * 70)


def algorithm_extended_output():
    """
    Algorithm 1: Extended Output Generation
    
    This is the core algorithm for transforming a finite seed into an
    infinite pseudo-random sequence.
    """
    print("\n" + "─" * 70)
    print("ALGORITHM 1: Extended Output Generation")
    print("─" * 70)
    
    print("""
    Mathematical Description:
    ════════════════════════
    ExtendedOutput(seed, index) → byte
    
    Input:  seed ∈ {0,1}*, index ∈ ℕ
    Output: byte ∈ {0,1}^8
    
    1. h ← CryptoHashFunction()
    2. h.update(seed || index)
    3. digest ← h.finalize()
    4. return digest[0]
    
    Properties:
    • Deterministic: Same (seed, index) → same output
    • Independent: Can compute byte i without computing bytes 0..i-1
    • Pseudo-random: Output appears random to bounded adversaries
    """)
    
    print("\n    Python Implementation in LazyDigest:")
    print("    ─────────────────────────────────")
    print("""
    def __getitem__(self, index):
        h = self.hash_fn()                    # Step 1: Initialize hash
        h.update(self.digest())                # Step 2a: Add seed
        h.update(str(index).encode('utf-8'))   # Step 2b: Add index
        return h.digest()[0]                   # Steps 3-4: Get first byte
    """)
    
    # Demonstration
    print("\n    Live Demonstration:")
    print("    ──────────────────")
    seed = b"demo_seed"
    lazy = LazyDigest(seed)
    
    print(f"    seed = {seed}")
    print(f"    lazy[0]   = 0x{lazy[0]:02x}  ← h(seed || '0')[0]")
    print(f"    lazy[100] = 0x{lazy[100]:02x}  ← h(seed || '100')[0]")
    print(f"    lazy[0]   = 0x{lazy[0]:02x}  ← Same input, same output (deterministic)")


def algorithm_random_oracle():
    """
    Algorithm 2: Random Oracle Simulation
    
    Shows how we approximate a true random oracle using entropy.
    """
    print("\n" + "─" * 70)
    print("ALGORITHM 2: Random Oracle Simulation")
    print("─" * 70)
    
    print("""
    Mathematical Description:
    ════════════════════════
    RandomOracle(input) → {0,1}^∞
    
    Input:  x ∈ {0,1}*
    Output: infinite sequence ∈ {0,1}^∞
    
    On first query for x:
    1. For each index i requested:
    2.   output[i] ← Random({0,1}^8)
    3.   cache[(x,i)] ← output[i]
    4. return output
    
    On repeated query for x:
    1. return cache[(x,*)]
    
    Properties:
    • Consistency: Same input → same infinite output
    • Randomness: Each new input gets fresh random output
    • Independence: Different oracle instances are independent
    """)
    
    print("\n    Python Implementation in OracleDigest:")
    print("    ──────────────────────────────────")
    print("""
    def __getitem__(self, index):
        if index not in self.cache:
            # First access: generate random byte
            self.cache[index] = self.entropy()[0]
        return self.cache[index]  # Consistent on repeated access
    """)
    
    # Demonstration
    print("\n    Live Demonstration:")
    print("    ──────────────────")
    
    oracle1 = OracleDigest(b"test")
    oracle2 = OracleDigest(b"test")
    
    print(f"    Two oracle instances with same input b'test':")
    print(f"    oracle1[0] = 0x{oracle1[0]:02x}")
    print(f"    oracle2[0] = 0x{oracle2[0]:02x}")
    print(f"    Different? {oracle1[0] != oracle2[0]} (each instance is independent)")
    print(f"    ")
    print(f"    But within same instance:")
    print(f"    oracle1[0] first  = 0x{oracle1[0]:02x}")
    print(f"    oracle1[0] second = 0x{oracle1[0]:02x}")
    print(f"    Consistent? {oracle1[0] == oracle1[0]}")


def algorithm_truncation():
    """
    Algorithm 3: Truncation (Projection from Infinite to Finite)
    
    Shows how we bridge infinite oracles to finite hashes.
    """
    print("\n" + "─" * 70)
    print("ALGORITHM 3: Truncation / Projection")
    print("─" * 70)
    
    print("""
    Mathematical Description:
    ════════════════════════
    Truncate_n: {0,1}^∞ → {0,1}^n
    
    Input:  digest ∈ {0,1}^∞, n ∈ ℕ
    Output: digest' ∈ {0,1}^n
    
    1. output ← empty
    2. for i from 0 to n-1:
    3.   output[i] ← digest[i]
    4. return output
    
    Properties:
    • Prefix preservation: truncate(d,n)[i] = d[i] for all i < n
    • Enables: hash(x) = truncate(oracle(x), n)
    • Projection: π_n: {0,1}^∞ → {0,1}^n
    """)
    
    print("\n    Python Implementation:")
    print("    ─────────────────")
    print("""
    def truncate(self, length):
        return Digest(self.digest()[:min(len(self), length)])
    """)
    
    # Demonstration
    print("\n    Live Demonstration:")
    print("    ──────────────────")
    
    oracle_hash = OracleHash()
    infinite = oracle_hash(b"truncation_demo")
    
    # Show truncation preserves prefix
    print(f"    Infinite oracle output for b'truncation_demo':")
    print(f"    Position 0: 0x{infinite[0]:02x}")
    print(f"    Position 1: 0x{infinite[1]:02x}")
    print(f"    Position 2: 0x{infinite[2]:02x}")
    
    truncated = infinite.truncate(3)
    print(f"\n    After truncate(3):")
    print(f"    Finite digest: {truncated.hexdigest()}")
    print(f"    Length: {len(truncated)} bytes")
    print(f"    Preserves prefix: {all(truncated[i] == infinite[i] for i in range(3))}")


def algorithm_oracle_composition():
    """
    Algorithm 4: Oracle Composition
    
    Shows how we compose hash functions to create oracle approximations.
    """
    print("\n" + "─" * 70)
    print("ALGORITHM 4: Oracle Composition")
    print("─" * 70)
    
    print("""
    Mathematical Description:
    ════════════════════════
    OracleHash: {0,1}* → {0,1}^∞
    
    Input:  x ∈ {0,1}*
    Output: lazy_digest ∈ {0,1}^∞
    
    1. seed ← CryptoHash(x)
    2. return LazyDigest(seed, CryptoHash)
    
    Expands to:
    OracleHash(x)[i] = CryptoHash(CryptoHash(x) || i)[0]
    
    Properties:
    • Deterministic approximation of random oracle
    • Computable: Uses only hash functions
    • Infinite output from finite computation
    """)
    
    print("\n    Python Implementation:")
    print("    ─────────────────")
    print("""
    class OracleHash(CryptoHash):
        def __call__(self, x):
            seed = self.hash_fn(x).digest()  # Step 1: Hash input to seed
            return LazyDigest(seed, self.hash_fn)  # Step 2: Create lazy sequence
    """)
    
    # Demonstration
    print("\n    Live Demonstration:")
    print("    ──────────────────")
    
    oracle_hash = OracleHash(hashlib.sha256)
    input_data = b"composition"
    result = oracle_hash(input_data)
    
    print(f"    Input: {input_data}")
    print(f"    Step 1: seed = SHA256({input_data}) = {hashlib.sha256(input_data).hexdigest()[:16]}...")
    print(f"    Step 2: LazyDigest(seed) generates infinite sequence")
    print(f"    ")
    print(f"    Access any index:")
    print(f"    result[0]      = 0x{result[0]:02x}")
    print(f"    result[1000]   = 0x{result[1000]:02x}")
    print(f"    result[1000000] computable without storing 1MB!")


def algorithm_family_selection():
    """
    Algorithm 5: Random Oracle Family Selection
    
    Shows how each oracle instance selects from the family of all oracles.
    """
    print("\n" + "─" * 70)
    print("ALGORITHM 5: Oracle Family Selection")
    print("─" * 70)
    
    print("""
    Mathematical Description:
    ════════════════════════
    SelectOracle() → Oracle_i
    
    Oracle family: F = {f | f: {0,1}* → {0,1}^∞}
    
    1. entropy_source ← FreshEntropy()
    2. Oracle_i ← new Oracle(entropy_source)
    3. return Oracle_i
    
    Each Oracle_i behaves as:
    - Oracle_i(x)[j] = entropy_source_i(x, j)
    
    Properties:
    • |F| = 2^∞ (uncountably infinite family)
    • Pr[Oracle_i = Oracle_j] = 0 for i ≠ j
    • Each instance approximates a different random function
    """)
    
    print("\n    Demonstration of Independence:")
    print("    ─────────────────────────────")
    
    # Create multiple oracle instances
    oracles = [OracleDigest(b"same_input") for _ in range(3)]
    
    print(f"    Three oracle instances with same input b'same_input':")
    for i, oracle in enumerate(oracles):
        bytes_sample = [oracle[j] for j in range(4)]
        hex_string = ''.join(f"{b:02x}" for b in bytes_sample)
        print(f"    Oracle_{i}: [{hex_string}...] ← Independent random function")
    
    print(f"\n    Each selects a different function from the infinite family F")


def run_all_algorithms():
    """
    Execute all algorithm demonstrations
    """
    describe_algorithms()
    algorithm_extended_output()
    algorithm_random_oracle()
    algorithm_truncation()
    algorithm_oracle_composition()
    algorithm_family_selection()
    
    print("\n" + "=" * 70)
    print("Algorithms demonstrated! Theory connected to implementation.")
    print("=" * 70)


if __name__ == "__main__":
    run_all_algorithms()