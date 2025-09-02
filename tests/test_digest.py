"""
Tests for digest classes - focusing on mathematical properties
"""

import hashlib
import pytest
from random_oracles.digest import Digest, OracleDigest, LazyDigest, LazyHexDigest


def test_digest_initialization():
    """Test Digest can be initialized with bytes or hex string"""
    # From bytes
    digest_bytes = Digest(b"test")
    assert digest_bytes.digest() == b"test"
    
    # From hex string
    digest_hex = Digest("74657374")  # "test" in hex
    assert digest_hex.digest() == b"test"
    assert digest_hex.hexdigest() == "74657374"


def test_digest_truncation():
    """Test truncation preserves prefix property"""
    original = Digest(b"abcdefghijklmnop")
    truncated = original.truncate(8)
    
    assert len(truncated) == 8
    assert truncated.digest() == b"abcdefgh"
    
    # Truncating beyond length returns original
    over_truncated = original.truncate(100)
    assert over_truncated.digest() == original.digest()


def test_oracle_digest_consistency():
    """Test that OracleDigest returns consistent values"""
    oracle = OracleDigest(b"seed")
    
    # Same index should return same value
    value1 = oracle[42]
    value2 = oracle[42]
    assert value1 == value2
    
    # Different indices should (likely) return different values
    values = [oracle[i] for i in range(10)]
    assert len(set(values)) > 1  # At least some different values


def test_oracle_digest_independence():
    """Test that different OracleDigest instances are independent"""
    oracle1 = OracleDigest(b"seed")
    oracle2 = OracleDigest(b"seed")
    
    # Same input, different instances should give different outputs
    # (with high probability due to different entropy)
    differences = sum(oracle1[i] != oracle2[i] for i in range(10))
    assert differences > 0  # Should have at least some differences


def test_lazy_digest_determinism():
    """Test LazyDigest is deterministic"""
    lazy1 = LazyDigest(b"seed", hashlib.sha256)
    lazy2 = LazyDigest(b"seed", hashlib.sha256)
    
    # Same seed and hash function should give same results
    for i in [0, 42, 1000]:
        assert lazy1[i] == lazy2[i]


def test_lazy_digest_computation():
    """Test LazyDigest computes h(seed || index)"""
    seed = b"test_seed"
    lazy = LazyDigest(seed, hashlib.sha256)
    
    # Manually compute what index 0 should be
    h = hashlib.sha256()
    h.update(seed)
    h.update(b"0")
    expected = h.digest()[0]
    
    assert lazy[0] == expected


def test_lazy_hex_digest():
    """Test LazyHexDigest returns hex strings"""
    seed = b"hex_test"
    lazy_hex = LazyHexDigest(seed)
    
    # Should return hex string, not bytes
    result = lazy_hex[0]
    assert isinstance(result, str)
    assert len(result) == 2  # Two hex characters per byte
    assert all(c in "0123456789abcdef" for c in result)


def test_digest_indexing():
    """Test __getitem__ access"""
    digest = Digest(b"abcdef")
    
    assert digest[0] == ord(b'a')
    assert digest[5] == ord(b'f')
    
    with pytest.raises(IndexError):
        _ = digest[6]  # Out of bounds
    
    with pytest.raises(IndexError):
        _ = digest[-1]  # Negative index