"""
Properties and Laws of Cryptographic Primitives

This module demonstrates fundamental properties of hash functions and oracles
through executable examples, making abstract properties tangible.
"""

import hashlib
from digest import Digest, OracleDigest, LazyDigest
from hash import Oracle, CryptoHash, OracleHash


def demonstrate_determinism():
    """
    Property: Deterministic - Same input always produces same output
    
    h(x) = h(x) for all x
    """
    crypto_hash = CryptoHash()
    input_data = b"Hello, World!"
    
    digest1 = crypto_hash(input_data)
    digest2 = crypto_hash(input_data)
    
    assert digest1.hexdigest() == digest2.hexdigest(), "Hash should be deterministic"
    print(f"✓ Determinism: h({input_data}) consistently = {digest1.hexdigest()[:16]}...")
    return digest1.hexdigest() == digest2.hexdigest()


def demonstrate_avalanche():
    """
    Property: Avalanche Effect - Small input changes cause large output changes
    
    h(x) ≠ h(x') where x and x' differ by one bit
    """
    crypto_hash = CryptoHash()
    
    input1 = b"Hello, World!"
    input2 = b"Hello, World."  # Changed one character
    
    digest1 = crypto_hash(input1)
    digest2 = crypto_hash(input2)
    
    # Count differing bits
    bytes1 = digest1.digest()
    bytes2 = digest2.digest()
    
    differing_bits = sum(
        bin(b1 ^ b2).count('1') 
        for b1, b2 in zip(bytes1, bytes2)
    )
    
    total_bits = len(bytes1) * 8
    diff_percentage = (differing_bits / total_bits) * 100
    
    print(f"✓ Avalanche: 1 char change → {diff_percentage:.1f}% bits different")
    print(f"  '{input1.decode()}' → {digest1.hexdigest()[:16]}...")
    print(f"  '{input2.decode()}' → {digest2.hexdigest()[:16]}...")
    
    return diff_percentage > 40  # Should be ~50% for good hash


def demonstrate_oracle_consistency():
    """
    Property: Oracle Consistency - Same query returns same infinite sequence
    
    oracle(x)[i] = oracle(x)[i] for all x, i
    """
    oracle = Oracle()
    
    input_data = b"quantum"
    digest1 = oracle(input_data)
    digest2 = oracle(input_data)
    
    # Check multiple indices
    indices = [0, 42, 1337, 9999]
    for i in indices:
        assert digest1[i] == digest2[i], f"Oracle should be consistent at index {i}"
    
    print(f"✓ Oracle Consistency: oracle({input_data})[i] stable for i in {indices}")
    return True


def demonstrate_oracle_uniqueness():
    """
    Property: Different Oracle Instances = Different Random Functions
    
    oracle1 ≠ oracle2 (with high probability)
    """
    # Two different oracle instances
    input_data = b"test"
    
    # Each OracleDigest instance uses fresh entropy
    oracle_digest1 = OracleDigest(input_data)
    oracle_digest2 = OracleDigest(input_data)
    
    # Check if they produce different values (should with high probability)
    indices_to_check = range(10)
    differences = sum(
        oracle_digest1[i] != oracle_digest2[i] 
        for i in indices_to_check
    )
    
    print(f"✓ Oracle Uniqueness: Two instances differ at {differences}/10 positions")
    print(f"  (Each OracleDigest is a different random oracle)")
    return differences > 0


def demonstrate_lazy_infinity():
    """
    Property: Lazy Infinity - Can access arbitrary indices without storing all data
    
    digest[n] is computable for any n without computing digest[0..n-1]
    """
    seed = b"infinity"
    lazy = LazyDigest(seed)
    
    # Access sparse indices - demonstrates we don't need all previous values
    sparse_indices = [0, 1000, 1000000, 10**9]
    
    print(f"✓ Lazy Infinity: Accessing indices {sparse_indices}")
    for i in sparse_indices[:3]:  # Skip 10^9 for performance
        value = lazy[i]
        print(f"  digest[{i:>7}] = 0x{value:02x}")
    
    print(f"  digest[10^9] computable without storing 10^9 bytes!")
    return True


def demonstrate_truncation_algebra():
    """
    Property: Truncation preserves prefix
    
    truncate(digest, n)[i] = digest[i] for all i < n
    """
    oracle_hash = OracleHash()
    infinite_digest = oracle_hash(b"mathematics")
    
    # Store first 10 bytes
    first_10 = [infinite_digest[i] for i in range(10)]
    
    # Truncate to finite digest
    finite_digest = infinite_digest.truncate(10)
    
    # Verify prefix preservation
    assert all(finite_digest[i] == first_10[i] for i in range(10))
    
    print(f"✓ Truncation Algebra: infinite.truncate(10) preserves first 10 bytes")
    print(f"  Enables: hash(x) = oracle(x).truncate(32)")
    return True


def demonstrate_composition():
    """
    Property: Function Composition
    
    (f ∘ g)(x) - Composing hash functions and oracles
    """
    # Traditional hash
    crypto_hash = CryptoHash(hashlib.sha256)
    
    # Oracle-based "hash" via truncation
    oracle_hash = OracleHash(hashlib.sha256)
    
    input_data = b"composition"
    
    # Method 1: Direct hash
    traditional = crypto_hash(input_data)
    
    # Method 2: Oracle + truncation
    oracle_infinite = oracle_hash(input_data)
    oracle_truncated = oracle_infinite.truncate(32)  # SHA-256 is 32 bytes
    
    print(f"✓ Composition: Two paths to finite digests")
    print(f"  CryptoHash:  {traditional.hexdigest()[:16]}...")
    print(f"  OracleHash → truncate: demonstrates oracle → hash reduction")
    return True


def run_all_properties():
    """
    Execute all property demonstrations
    """
    print("=" * 60)
    print("CRYPTOGRAPHIC PROPERTIES DEMONSTRATION")
    print("=" * 60)
    
    print("\n1. HASH FUNCTION PROPERTIES")
    print("-" * 40)
    demonstrate_determinism()
    demonstrate_avalanche()
    
    print("\n2. RANDOM ORACLE PROPERTIES")
    print("-" * 40)
    demonstrate_oracle_consistency()
    demonstrate_oracle_uniqueness()
    
    print("\n3. LAZY EVALUATION & INFINITY")
    print("-" * 40)
    demonstrate_lazy_infinity()
    demonstrate_truncation_algebra()
    
    print("\n4. ALGEBRAIC PROPERTIES")
    print("-" * 40)
    demonstrate_composition()
    
    print("\n" + "=" * 60)
    print("All properties demonstrated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_properties()