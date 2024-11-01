import digest
import hashlib

class Oracle:
    """
    A lazy function that approximates a random oracle. A random oracle
    is a function of the form $h: {0,1}^* -> {0,1}^n$ that is indistinguishable
    from a random function, but with the property that the same input always
    produces the same output. More concretely,

    $$
    [Byte] -> OracleDigest,
    $$

    where for the same input we always get the same OracleDigest (using
    a simple cache to store the lazy results of the function calls).
    """
    
    def __init__(self):
        """
        Initialize the oracle with the given seed.
        
        :param seed: The seed.
        """
        self.cache = {}

    def __call__(self, x):
        """
        Get the digest of the given input.
        
        :param x: The input.
        :return: The digest of the input.
        """
        
        if x not in self.cache:
            self.cache[x] = digest.OracleDigest(x)
        return self.cache[x]


class CryptoHash:
    """
    A cryptographic hash function adapter. It is a function of type
    $h: {0,1}^* -> {0,1}^n$, where $n$ is the digest size in bytes.
    More concretely,

    $$
    [Byte] -> Digest.
    $$
    """

    def __init__(self, hash_fn = hashlib.sha256):
        """
        Initialize the crypto hash function adapter with the given hash function.

        :param hash_fn: The hash function.
        """

        self.hash_fn = hash_fn

    def __call__(self, x):
        """
        Get the digest of the given input.

        :param x: The input.
        :return: The digest of the input.
        """
        return digest.Digest(self.hash_fn(x).digest())


class OracleHash(CryptoHash):
    """
    A lazy function that approximates a random oracle using a cryptographic hash function.

    It's a function of type ${0,1}^* -> {0,1}^\infty$, or more concretely:
    `Hashable -> LazyDigest`.
    """

    def __call__(self, x):
        """
        Get the digest of the given input.

        :param x: The input.
        :return: The infinite lazy digest of the input.
        """
        return digest.LazyDigest(self.hash_fn(x).digest(), self.hash_fn)