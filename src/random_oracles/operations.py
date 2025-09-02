"""
Algebra of operations on lazy infinite sequences.

This module implements operations that combine and transform lazy sequences,
demonstrating how infinite objects can be manipulated algebraically without
materializing them.
"""

import hashlib
from .digest import LazyDigest, Digest


class LazyXorDigest(LazyDigest):
    """
    XOR of multiple lazy digests - security through diversity.
    
    Even if one hash algorithm is weakened or broken, the XOR of multiple
    independent algorithms remains secure as long as at least one is secure.
    This trades computational complexity for security margin.
    """
    
    def __init__(self, *digests):
        """
        Initialize with multiple lazy digests to XOR.
        
        :param digests: Variable number of LazyDigest instances
        """
        if not digests:
            raise ValueError("Need at least one digest to XOR")
        self.digests = digests
        
    def __getitem__(self, index):
        """
        Generate byte by XORing all constituent digests.
        
        Security property: If any single digest is cryptographically secure,
        the XOR remains secure. Breaking requires breaking ALL digests.
        """
        result = 0
        for digest in self.digests:
            result ^= digest[index]
        return result
    
    def __repr__(self):
        return f"LazyXorDigest({len(self.digests)} digests)"


class LazyXorMultiHash(LazyDigest):
    """
    XOR multiple hash functions with the same seed - maximum algorithm diversity.
    
    This is the "paranoid" construction: use every available hash algorithm
    and XOR them all. Even if multiple algorithms are broken, as long as
    one remains secure, the construction is secure.
    """
    
    def __init__(self, seed, hash_functions=None):
        """
        Initialize with seed and hash functions.
        
        :param seed: Common seed for all hash functions
        :param hash_functions: List of hash functions (default: all available)
        """
        super().__init__(seed)
        
        if hash_functions is None:
            # Use all available hash functions for maximum diversity
            self.hash_functions = [
                hashlib.sha256,
                hashlib.sha512,
                hashlib.sha3_256,
                hashlib.sha3_512,
                hashlib.blake2b,
                hashlib.blake2s,
            ]
        else:
            self.hash_functions = hash_functions
            
    def __getitem__(self, index):
        """
        XOR outputs from all hash functions.
        
        Computational cost: O(n) where n = number of hash functions
        Security: Requires breaking ALL n hash functions
        """
        result = 0
        for hash_fn in self.hash_functions:
            h = hash_fn()
            h.update(self.digest())
            h.update(str(index).encode('utf-8'))
            result ^= h.digest()[0]
        return result


class LazySliceDigest(LazyDigest):
    """
    Take every n-th element starting at offset - infinite subsequence.
    """
    
    def __init__(self, base_digest, start=0, step=1):
        """
        Initialize slice parameters.
        
        :param base_digest: Underlying lazy digest
        :param start: Starting index
        :param step: Step size
        """
        self.base_digest = base_digest
        self.start = start
        self.step = step
        
    def __getitem__(self, index):
        """Map slice index to base digest index."""
        base_index = self.start + (index * self.step)
        return self.base_digest[base_index]


class LazyInterleaveDigest(LazyDigest):
    """
    Interleave multiple lazy digests - creates complex patterns.
    
    Takes turns pulling from each digest, creating patterns that
    are hard to analyze even if individual digests are predictable.
    """
    
    def __init__(self, *digests):
        """
        Initialize with digests to interleave.
        
        :param digests: Variable number of LazyDigest instances
        """
        if not digests:
            raise ValueError("Need at least one digest to interleave")
        self.digests = digests
        
    def __getitem__(self, index):
        """Pull from digests in round-robin fashion."""
        digest_index = index % len(self.digests)
        position = index // len(self.digests)
        return self.digests[digest_index][position]


class LazyTransformDigest(LazyDigest):
    """
    Apply a transformation function to each element.
    
    This enables arbitrary transformations while maintaining laziness.
    """
    
    def __init__(self, base_digest, transform_fn):
        """
        Initialize with base digest and transformation.
        
        :param base_digest: Underlying lazy digest
        :param transform_fn: Function to apply to each byte
        """
        self.base_digest = base_digest
        self.transform_fn = transform_fn
        
    def __getitem__(self, index):
        """Apply transformation to base digest value."""
        value = self.base_digest[index]
        return self.transform_fn(value) & 0xFF  # Ensure byte result


class LazyConcatFiniteDigest(LazyDigest):
    """
    Concatenate finite prefix with infinite suffix.
    
    This allows prepending known data to an infinite stream.
    """
    
    def __init__(self, finite_prefix, infinite_suffix):
        """
        Initialize with finite prefix and infinite suffix.
        
        :param finite_prefix: Finite bytes to prepend
        :param infinite_suffix: LazyDigest for tail
        """
        self.prefix = bytes(finite_prefix)
        self.suffix = infinite_suffix
        
    def __getitem__(self, index):
        """Return from prefix if available, else from suffix."""
        if index < len(self.prefix):
            return self.prefix[index]
        else:
            return self.suffix[index - len(self.prefix)]


class LazyWindowDigest(Digest):
    """
    Extract a finite window from a lazy digest - lazy to concrete.
    
    This is a concrete operation that materializes a portion of
    the infinite sequence.
    """
    
    def __init__(self, lazy_digest, start, length):
        """
        Initialize window extraction.
        
        :param lazy_digest: Source lazy digest
        :param start: Starting index
        :param length: Number of bytes to extract
        """
        data = bytes([lazy_digest[start + i] for i in range(length)])
        super().__init__(data)


def demonstrate_xor_security():
    """
    Demonstrate how XOR provides security through algorithm diversity.
    """
    print("=" * 60)
    print("XOR SECURITY: Algorithm Diversity")
    print("=" * 60)
    
    seed = b"security_test"
    
    # Create individual digests with different algorithms
    sha256_digest = LazyDigest(seed, hashlib.sha256)
    sha512_digest = LazyDigest(seed, hashlib.sha512)
    sha3_digest = LazyDigest(seed, hashlib.sha3_256)
    blake2_digest = LazyDigest(seed, hashlib.blake2b)
    
    # XOR them together
    xor_digest = LazyXorDigest(sha256_digest, sha512_digest, sha3_digest, blake2_digest)
    
    print("\nIndividual algorithm outputs at index 0:")
    print(f"  SHA-256:  0x{sha256_digest[0]:02x}")
    print(f"  SHA-512:  0x{sha512_digest[0]:02x}")
    print(f"  SHA3-256: 0x{sha3_digest[0]:02x}")
    print(f"  BLAKE2b:  0x{blake2_digest[0]:02x}")
    print(f"  XOR all:  0x{xor_digest[0]:02x}")
    
    print("\nSecurity properties:")
    print("- If SHA-256 is broken: XOR still secure via SHA-512, SHA3, BLAKE2")
    print("- If SHA-2 family broken: XOR still secure via SHA3, BLAKE2")
    print("- If 3 of 4 are broken: XOR still secure via remaining algorithm")
    print("- Only fails if ALL algorithms are simultaneously broken")
    
    print("\nComputational trade-off:")
    print(f"- Single hash: 1x computation")
    print(f"- XOR of {len(xor_digest.digests)}: {len(xor_digest.digests)}x computation")
    print(f"- Security margin: Exponentially stronger")
    
    # Demonstrate paranoid construction
    print("\n" + "-" * 40)
    print("PARANOID CONSTRUCTION: All Available Hashes")
    print("-" * 40)
    
    paranoid = LazyXorMultiHash(seed)
    print(f"Using {len(paranoid.hash_functions)} hash functions:")
    for fn in paranoid.hash_functions:
        print(f"  - {fn.__name__}")
    
    print(f"\nOutput at index 0: 0x{paranoid[0]:02x}")
    print("This value is the XOR of ALL hash functions above.")
    print("Breaking this requires finding a simultaneous collision in ALL algorithms.")


def demonstrate_operations():
    """Demonstrate various operations on lazy sequences."""
    print("\n" + "=" * 60)
    print("LAZY OPERATIONS ALGEBRA")
    print("=" * 60)
    
    seed1 = b"first_seed"
    seed2 = b"second_seed"
    
    lazy1 = LazyDigest(seed1)
    lazy2 = LazyDigest(seed2)
    
    # Demonstrate operations
    print("\nBase digests:")
    print(f"  lazy1[0..3] = {[lazy1[i] for i in range(4)]}")
    print(f"  lazy2[0..3] = {[lazy2[i] for i in range(4)]}")
    
    # XOR
    xor = LazyXorDigest(lazy1, lazy2)
    print(f"\nXOR:")
    print(f"  xor[0..3] = {[xor[i] for i in range(4)]}")
    
    # Slice
    slice_digest = LazySliceDigest(lazy1, start=10, step=3)
    print(f"\nSlice (start=10, step=3):")
    print(f"  Maps: [0,1,2,3] -> [10,13,16,19] in lazy1")
    print(f"  slice[0..3] = {[slice_digest[i] for i in range(4)]}")
    
    # Interleave
    interleave = LazyInterleaveDigest(lazy1, lazy2)
    print(f"\nInterleave:")
    print(f"  interleave[0..5] = {[interleave[i] for i in range(6)]}")
    print(f"  Pattern: lazy1[0], lazy2[0], lazy1[1], lazy2[1], ...")
    
    # Transform
    rotate = LazyTransformDigest(lazy1, lambda x: (x << 1) | (x >> 7))
    print(f"\nTransform (rotate left 1 bit):")
    print(f"  original[0] = 0x{lazy1[0]:02x} = {lazy1[0]:08b}")
    print(f"  rotated[0]  = 0x{rotate[0]:02x} = {rotate[0]:08b}")
    
    # Finite concatenation
    prefix = b"HEADER"
    concat = LazyConcatFiniteDigest(prefix, lazy1)
    print(f"\nConcatenate finite prefix:")
    print(f"  First 10 bytes: {bytes([concat[i] for i in range(10)])}")
    print(f"  (First 6 are 'HEADER', rest from lazy1)")


def analyze_composition_laws():
    """Analyze algebraic properties of operations."""
    print("\n" + "=" * 60)
    print("ALGEBRAIC PROPERTIES")
    print("=" * 60)
    
    seed1 = b"A"
    seed2 = b"B"
    seed3 = b"C"
    
    A = LazyDigest(seed1)
    B = LazyDigest(seed2)
    C = LazyDigest(seed3)
    
    # Commutativity of XOR
    xor_AB = LazyXorDigest(A, B)
    xor_BA = LazyXorDigest(B, A)
    
    print("\nCommutativity of XOR:")
    print(f"  A ⊕ B = {[xor_AB[i] for i in range(4)]}")
    print(f"  B ⊕ A = {[xor_BA[i] for i in range(4)]}")
    print(f"  Equal: {all(xor_AB[i] == xor_BA[i] for i in range(100))}")
    
    # Associativity of XOR
    xor_AB_C = LazyXorDigest(LazyXorDigest(A, B), C)
    xor_A_BC = LazyXorDigest(A, LazyXorDigest(B, C))
    
    print("\nAssociativity of XOR:")
    print(f"  (A ⊕ B) ⊕ C = {[xor_AB_C[i] for i in range(4)]}")
    print(f"  A ⊕ (B ⊕ C) = {[xor_A_BC[i] for i in range(4)]}")
    print(f"  Equal: {all(xor_AB_C[i] == xor_A_BC[i] for i in range(100))}")
    
    # Identity element (zeros)
    class ZeroDigest(LazyDigest):
        def __getitem__(self, index):
            return 0
    
    Z = ZeroDigest(b"")
    xor_AZ = LazyXorDigest(A, Z)
    
    print("\nIdentity element (zero stream):")
    print(f"  A     = {[A[i] for i in range(4)]}")
    print(f"  A ⊕ 0 = {[xor_AZ[i] for i in range(4)]}")
    print(f"  Equal: {all(A[i] == xor_AZ[i] for i in range(100))}")
    
    # Self-inverse property
    xor_AA = LazyXorDigest(A, A)
    
    print("\nSelf-inverse property:")
    print(f"  A ⊕ A = {[xor_AA[i] for i in range(4)]}")
    print(f"  All zeros: {all(xor_AA[i] == 0 for i in range(100))}")


if __name__ == "__main__":
    demonstrate_xor_security()
    demonstrate_operations()
    analyze_composition_laws()