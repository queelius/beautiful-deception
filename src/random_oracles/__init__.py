"""
Random Oracles: A Pedagogical Exploration

This package provides elegant implementations of cryptographic hash functions
and random oracles, emphasizing mathematical clarity and conceptual understanding.

Core Concepts:
- Cryptographic hash functions: {0,1}* → {0,1}^n
- Random oracles: {0,1}* → {0,1}^∞
- Lazy evaluation and codata
- Multiple approximations of theoretical ideals
"""

from .digest import (
    Digest,
    OracleDigest,
    LazyDigest,
    LazyHexDigest
)

from .hash import (
    Oracle,
    CryptoHash,
    OracleHash
)

__version__ = "0.1.0"

__all__ = [
    # Digest classes
    "Digest",
    "OracleDigest", 
    "LazyDigest",
    "LazyHexDigest",
    
    # Hash function classes
    "Oracle",
    "CryptoHash",
    "OracleHash",
]

# Mathematical type signatures for reference
TYPES = {
    "Digest": "{0,1}^n",
    "OracleDigest": "{0,1}^∞ (entropy-based)",
    "LazyDigest": "{0,1}^∞ (deterministic)",
    "CryptoHash": "{0,1}* → {0,1}^n",
    "OracleHash": "{0,1}* → {0,1}^∞",
    "Oracle": "{0,1}* → OracleDigest",
}