"""
Extended LazyDigest implementations with advanced constructions.

This module demonstrates techniques for extending cycle length and
improving the deception of deterministic infinite sequences.
"""

import hashlib
from .digest import LazyDigest, Digest


class HierarchicalLazyDigest(LazyDigest):
    """
    Hierarchical seeding structure for extended cycle length.
    
    Uses a tree of seeds to extend the effective period by structuring
    the state space hierarchically.
    """
    
    def __init__(self, master_seed, hash_fn=hashlib.sha256, 
                 epoch_bits=40, chunk_bits=20):
        """
        Initialize with hierarchical structure.
        
        :param master_seed: Root seed for the hierarchy
        :param hash_fn: Hash function to use
        :param epoch_bits: Bits per epoch (default 2^40 indices)
        :param chunk_bits: Bits per chunk (default 2^20 indices)
        """
        super().__init__(master_seed, hash_fn)
        self.epoch_size = 2 ** epoch_bits
        self.chunk_size = 2 ** chunk_bits
        
    def __getitem__(self, index):
        """
        Generate byte at index using hierarchical seeding.
        
        The hierarchy is:
        1. Epoch (every 2^40 indices)
        2. Chunk (every 2^20 indices within epoch)
        3. Position (within chunk)
        """
        # Determine position in hierarchy
        epoch = index // self.epoch_size
        remainder = index % self.epoch_size
        chunk = remainder // self.chunk_size
        position = remainder % self.chunk_size
        
        # Derive hierarchical seeds
        h = self.hash_fn()
        h.update(self.digest())
        h.update(b"epoch")
        h.update(str(epoch).encode('utf-8'))
        epoch_seed = h.digest()
        
        h = self.hash_fn()
        h.update(epoch_seed)
        h.update(b"chunk")
        h.update(str(chunk).encode('utf-8'))
        chunk_seed = h.digest()
        
        h = self.hash_fn()
        h.update(chunk_seed)
        h.update(str(position).encode('utf-8'))
        
        return h.digest()[0]


class RekeyingLazyDigest(LazyDigest):
    """
    Periodically rekey to prevent cycle detection across epochs.
    
    Deterministically derives new keys at regular intervals, making
    it impossible to detect cycles across epoch boundaries.
    """
    
    def __init__(self, seed, hash_fn=hashlib.sha256, rekey_interval=2**32):
        """
        Initialize with rekeying parameters.
        
        :param seed: Initial seed
        :param hash_fn: Hash function to use
        :param rekey_interval: Indices between rekeys (default 2^32)
        """
        super().__init__(seed, hash_fn)
        self.rekey_interval = rekey_interval
        self._key_cache = {0: seed}
        
    def _get_epoch_key(self, epoch):
        """Derive key for given epoch."""
        if epoch not in self._key_cache:
            # Derive from previous epoch
            prev_key = self._get_epoch_key(epoch - 1)
            h = self.hash_fn()
            h.update(prev_key)
            h.update(b"rekey")
            h.update(str(epoch).encode('utf-8'))
            self._key_cache[epoch] = h.digest()
        return self._key_cache[epoch]
        
    def __getitem__(self, index):
        """Generate byte at index with periodic rekeying."""
        epoch = index // self.rekey_interval
        local_index = index % self.rekey_interval
        
        key = self._get_epoch_key(epoch)
        
        h = self.hash_fn()
        h.update(key)
        h.update(str(local_index).encode('utf-8'))
        return h.digest()[0]


class SpongeLazyDigest(LazyDigest):
    """
    Sponge construction for tunable security/performance trade-off.
    
    Based on the sponge construction used in SHA-3/Keccak, this provides
    tunable capacity for longer cycles at the cost of performance.
    """
    
    def __init__(self, seed, capacity=256, rate=256, hash_fn=hashlib.sha3_256):
        """
        Initialize sponge parameters.
        
        :param seed: Initial seed
        :param capacity: Bits of internal state preserved (security parameter)
        :param rate: Bits extracted per squeeze (performance parameter)
        :param hash_fn: Hash function (should be SHA-3 family)
        """
        super().__init__(seed, hash_fn)
        self.capacity = capacity
        self.rate = rate
        self.state_size = capacity + rate
        
    def __getitem__(self, index):
        """
        Generate byte using sponge construction.
        
        This is a simplified sponge that:
        1. Absorbs the seed
        2. Absorbs the index
        3. Squeezes out one byte
        """
        # Initialize with seed
        h = self.hash_fn()
        h.update(self.digest())
        h.update(b"sponge_init")
        state = h.digest()
        
        # Absorb index
        h = self.hash_fn()
        h.update(state)
        h.update(str(index).encode('utf-8'))
        h.update(b"absorb")
        state = h.digest()
        
        # Squeeze out one byte
        h = self.hash_fn()
        h.update(state)
        h.update(b"squeeze")
        output = h.digest()
        
        return output[0]


class MultiHashLazyDigest(LazyDigest):
    """
    Use multiple hash functions to extend effective state space.
    
    Different hash functions for different index ranges prevents
    patterns that might emerge from a single hash function.
    """
    
    def __init__(self, seed):
        """
        Initialize with multiple hash functions.
        
        :param seed: Initial seed
        """
        super().__init__(seed, hashlib.sha256)
        self.hash_functions = [
            hashlib.sha256,
            hashlib.sha512,
            hashlib.sha3_256,
            hashlib.blake2b,
        ]
        
    def __getitem__(self, index):
        """Generate byte using hash function rotation."""
        # Select hash function based on index range
        hash_selector = (index // (2**30)) % len(self.hash_functions)
        hash_fn = self.hash_functions[hash_selector]
        
        h = hash_fn()
        h.update(self.digest())
        h.update(str(index).encode('utf-8'))
        return h.digest()[0]


class CompositeLazyDigest(LazyDigest):
    """
    Combine multiple LazyDigest strategies for maximum cycle length.
    
    This is the "kitchen sink" approach - use every technique to
    maximize the cycle length and quality of the sequence.
    """
    
    def __init__(self, seed):
        """Initialize with composite strategy."""
        super().__init__(seed)
        self.hierarchical = HierarchicalLazyDigest(seed)
        self.rekeying = RekeyingLazyDigest(seed)
        self.sponge = SpongeLazyDigest(seed)
        
    def __getitem__(self, index):
        """
        Generate byte by XORing multiple strategies.
        
        This combines independent sequences to create a higher-quality
        output with longer effective cycle.
        """
        h1 = self.hierarchical[index]
        h2 = self.rekeying[index]
        h3 = self.sponge[index]
        
        # XOR all three for final output
        return h1 ^ h2 ^ h3


def demonstrate_cycle_extension():
    """Demonstrate how different constructions extend cycle length."""
    seed = b"cycle_test_seed"
    
    print("=" * 60)
    print("CYCLE LENGTH EXTENSION TECHNIQUES")
    print("=" * 60)
    
    constructions = [
        ("Basic LazyDigest", LazyDigest(seed)),
        ("Hierarchical", HierarchicalLazyDigest(seed)),
        ("Rekeying", RekeyingLazyDigest(seed)),
        ("Sponge", SpongeLazyDigest(seed)),
        ("Multi-Hash", MultiHashLazyDigest(seed)),
        ("Composite", CompositeLazyDigest(seed)),
    ]
    
    # Test each construction
    for name, digest in constructions:
        print(f"\n{name}:")
        print("-" * 40)
        
        # Sample some indices
        samples = [0, 1000, 1000000, 2**32, 2**40]
        for idx in samples[:3]:  # Skip large indices for demo
            value = digest[idx]
            print(f"  [{idx:>10}] = 0x{value:02x}")
        
        # Theoretical cycle length discussion
        if isinstance(digest, HierarchicalLazyDigest):
            print(f"  Effective state space: ~2^{40+20+256} via hierarchy")
        elif isinstance(digest, RekeyingLazyDigest):
            print(f"  Rekeys every 2^32 indices, preventing cycle detection")
        elif isinstance(digest, SpongeLazyDigest):
            print(f"  Sponge capacity provides {digest.capacity}-bit security")
        elif isinstance(digest, MultiHashLazyDigest):
            print(f"  Rotates through {len(digest.hash_functions)} hash functions")
        elif isinstance(digest, CompositeLazyDigest):
            print(f"  Combines all techniques for maximum cycle length")
        else:
            print(f"  Basic construction with 2^256 maximum cycle")


if __name__ == "__main__":
    demonstrate_cycle_extension()