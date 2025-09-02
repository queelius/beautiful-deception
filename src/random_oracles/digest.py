import hashlib
import os

class Digest:
    """
    A digest is the output from a hash function, such as SHA-256. This class
    provides a common interface to access the hash function output, regardless
    of which hash function generated the digest.
    
    Mathematical Type: {0,1}^n (finite bit string of length n)
    """
    
    __type__ = "{0,1}^n"

    def truncate(self, length):
        """
        Truncate the digest to the given length. If the length is greater than
        the digest length, the original digest is returned.

        :param length: The length to truncate the digest to.
        """
        if length < 0:
            raise ValueError("Length must be non-negative.")
        return Digest(self.digest()[:min(len(self), length)])

    def __len__(self):
        """
        Get the length of the digest.

        :return: The length of the digest.
        """
        return len(self._digest)

    def __init__(self, digest):
        """
        Initialize with the given digest.

        :param digest: The digest from a hash function (or other source)
        """
        self._digest = bytes.fromhex(digest) if isinstance(digest, str) else digest

    def __getitem__(self, index):
        """
        Get the byte at the given index in the digest.

        :param index: The index of the byte to get.
        :return: The byte at the given index.
        :raises IndexError: If the index is out of bounds.
        """
        if index < 0 or index >= len(self):
            raise IndexError("Index out of bounds.")
        return self.digest()[index]

    def __str__(self):
        """
        Get a string representation of the digest.

        :return: A string representation of the digest.
        """
        return self.hexdigest()
    
    def __repr__(self):
        """
        Get a serialized representation of the digest.

        :return: A serialized representation of the digest.
        """
        return f"{self.__class__.__name__}({self.digest()!r})"
    
    def digest(self):
        """
        Get the digest as a bytes object.

        :return: The digest as a bytes object.
        """
        return self._digest
    
    def hexdigest(self):
        """
        Get the digest as a hex string.

        :return: The digest as a hex string.
        """
        return self.digest().hex()
        
class OracleDigest(Digest):
    """
    A random oracle digest is an infinite digest output by a random oracle.
    We lazily generate the digest values on demand, using an entropy source
    to generate random bytes.

    This class is a pedagogical device used to illustrate the concept of a
    random oracle, which is a function of type

    $$
    {0,1}^* -> {0,1}^\infty
    $$

    with the property that the first time an input is seen, the output is
    generated randomly, but thereafter the same output is returned for the
    same input.
    
    Mathematical Type: {0,1}^∞ (infinite bit string, accessed lazily)

    Random oracles are non-computable theoretical objects. However, this class
    provides very good approximation if `entropy_source` is a true random number
    generator. It is an approximation even if `entropy_source` is a true
    random number generator because the cache is finite and so eventually the
    property of returning the same output for the same input will be violated.
    """

    def __init__(self,
                 input,
                 entropy = None):
        """
        Initialize the object with the given input and entropy source.
        If no entropy source is provided, we use a cryptographic hash function
        to generate random bytes, seeded by a PRNG `os.urandom`.

        :param input: The input to the random oracle. We assume that the input.
        :param entropy_source: A function that generates random bytes.
        """
        super().__init__(input)

        if entropy is None:
            entropy = lambda : hashlib.sha256(os.urandom(32)).digest()
        self.entropy = entropy

        # The cache is a dictionary that maps each index to the byte at that index.
        # We use a simple dictionary to store the cache. In practice, we would
        # want to use a more sophisticated data structure to handle large indexes,
        # such as a LRU cache, but this is sufficient for pedagogical purposes.
        #
        # We use this cache to try to ensure that the same byte is returned for
        # the same index, as long as the RandomOracleDigest object is not
        # re-initialized. So, each time we create a new RandomOracleDigest object,
        # we get a different random oracle in the family of random oracles.
        self.cache = {}

    def __getitem__(self, index):
        """
        Get the byte at the given index in the digest.

        :param index: The index of the byte to get.
        :return: The byte at the given index.
        """
        if index not in self.cache:
            # Sample from entropy source to generate a random byte
            self.cache[index] = self.entropy()[0]

        return self.cache[index]

    def __repr__(self):
        """
        Get a serialized representation of the digest.

        :return: A serialized representation of the digest.
        """
        return f"OracleDigest(input={self.digest()}, " + \
               f"entropy_source={repr(self.entropy_source)}), " + \
               f"cache={repr(self.cache)})"
    
class LazyDigest(Digest):
    """
    A lazy digest is an infinite digest whose values at indexes are generated
    lazily (computed on demand).
    
    It's defined by a seed value and a hash function. The digest is generated by
    hashing the seed value concatenated with the index. It is a pedagogical
    device that approximates the concept of a random oracle.
    
    It is based on cryptographic hash functions, which are deterministic
    functions that take an input and produce a fixed-size output that appears
    uniformly random and uncorrelated with the input. To an adversary, the
    output of a cryptographic hash function should be indistinguishable from
    random noise. To extend the output of a hash function to an infinite
    sequence, we can use the hash function to generate a sequence of outputs
    by hashing the seed value concatenated with an index.

    If the hash function is a cryptographic hash function, then concatenating
    the seed value with an index and hashing the result should produce a
    sequence of outputs that appears random and uncorrelated with the input
    that ostensibly generated the LazyDigest object, i.e.,

    $$
    h(seed || 0) || h(seed || 1) || h(seed || 2) || \ldots
    $$

    should appear random and uncorrelated with the input that generated the
    seed value. Conceputally, then, using LazyDigest,

    $$
    oracle(x) = lambda x: LazyDigest(h(x), h) : {0,1}^* -> {0,1}^\infty
    $$

    is a good approximation of a random oracle, where $h$ is a cryptographic
    hash function.

    We can recover a non-lazy digest by truncating the LazyDigest to a finite
    length:

    $$
    hash(x) = lambda x: oracle(x).truncate(n) : {0,1}^* -> {0,1}^n
    $$

    where $n$ is the desired length of the digest in bytes.
    """

    def __init__(self, seed, hash_fn = hashlib.sha256):
        """
        Initialize the lazy digest with the given bytes object and hash function.

        :param seed: The bytes object.
        :param hash_fn: The hash function.
        """
        super().__init__(seed)
        self.hash_fn = hash_fn

    def __getitem__(self, index):
        """
        Get the byte at the given index in the digest.
        
        This implements the core algorithm for extending a finite seed into
        an infinite sequence:
        
        Algorithm: ExtendedOutput(seed, index)
        ─────────────────────────────────────
        1. h ← HashFunction()
        2. h.update(seed || index)
        3. return h.digest()[0]
        
        This creates a deterministic pseudo-random sequence where:
        - Each byte is computed independently (no need to compute previous bytes)
        - The sequence appears random to computationally bounded adversaries
        - The same (seed, index) pair always produces the same byte
        
        This is how we approximate a random oracle's infinite output:
        oracle(x) = [h(seed||0), h(seed||1), h(seed||2), ...]
        where seed = h(x)
        """
        h = self.hash_fn()
        h.update(self.digest())  # self.digest() is our seed
        h.update(str(index).encode('utf-8'))  # Concatenate with index
        return h.digest()[0]  # Return first byte of hash output
    
    def __repr__(self):
        """
        Get a serialized representation of the digest.

        :return: A serialized representation of the digest.
        """
        return f"LazyDigest(seed={self.digest()}, hash_fn={repr(self.hash_fn)})"
    
    def hexdigest(self):
        """
        Get the digest as a hex string.

        :return: The digest as a hex string.
        """
        return LazyHexDigest(self)
    
class LazyHexDigest(LazyDigest):

    def __getitem__(self, index):
        return super().__getitem__(index).hex()

    def hexdigest(self):
        return self
    
    def __repr__(self):
        return f"LazyHexDigest(seed={self.digest()}, hash_fn={repr(self.hash_fn)})"
