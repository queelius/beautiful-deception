"""
Tests for hash function classes - focusing on mathematical properties
"""

import hashlib
from random_oracles.hash import Oracle, CryptoHash, OracleHash
from random_oracles.digest import Digest, LazyDigest


def test_crypto_hash_determinism():
    """Test CryptoHash is deterministic"""
    crypto = CryptoHash(hashlib.sha256)
    
    input_data = b"deterministic"
    digest1 = crypto(input_data)
    digest2 = crypto(input_data)
    
    assert digest1.hexdigest() == digest2.hexdigest()


def test_crypto_hash_returns_digest():
    """Test CryptoHash returns Digest instances"""
    crypto = CryptoHash()
    result = crypto(b"test")
    
    assert isinstance(result, Digest)
    assert len(result) == 32  # SHA-256 default


def test_oracle_consistency():
    """Test Oracle returns same digest for same input"""
    oracle = Oracle()
    
    input_data = b"consistent_input"
    digest1 = oracle(input_data)
    digest2 = oracle(input_data)
    
    # Should be the exact same object (cached)
    assert digest1 is digest2
    
    # Values should be consistent
    for i in range(10):
        assert digest1[i] == digest2[i]


def test_oracle_different_inputs():
    """Test Oracle returns different digests for different inputs"""
    oracle = Oracle()
    
    digest1 = oracle(b"input1")
    digest2 = oracle(b"input2")
    
    # Should be different objects
    assert digest1 is not digest2
    
    # Values should (likely) differ
    differences = sum(digest1[i] != digest2[i] for i in range(10))
    assert differences > 0


def test_oracle_hash_returns_lazy_digest():
    """Test OracleHash returns LazyDigest instances"""
    oracle_hash = OracleHash()
    result = oracle_hash(b"test")
    
    assert isinstance(result, LazyDigest)
    
    # Should be able to access arbitrary indices
    _ = result[0]
    _ = result[1000000]  # Large index should work


def test_oracle_hash_determinism():
    """Test OracleHash is deterministic for same input"""
    oracle_hash = OracleHash(hashlib.sha256)
    
    input_data = b"deterministic"
    lazy1 = oracle_hash(input_data)
    lazy2 = oracle_hash(input_data)
    
    # Should produce same values at same indices
    for i in [0, 42, 1337]:
        assert lazy1[i] == lazy2[i]


def test_hash_function_composition():
    """Test composition of hash functions"""
    # Path 1: Direct hash
    crypto = CryptoHash(hashlib.sha256)
    direct = crypto(b"compose")
    
    # Path 2: Oracle + truncation
    oracle = OracleHash(hashlib.sha256)
    infinite = oracle(b"compose")
    truncated = infinite.truncate(32)
    
    # Both should be valid 32-byte digests
    assert len(direct) == 32
    assert len(truncated) == 32
    
    # They won't be equal (different methods) but both are valid