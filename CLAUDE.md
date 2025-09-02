# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **pedagogical project** exploring cryptographic hash functions and random oracles through elegant Python implementations. The code prioritizes clarity, mathematical understanding, and theoretical exposition over production robustness. Each class demonstrates fundamental cryptographic concepts in their purest form.

## Project Structure

- **digest.py**: Core digest classes implementing various digest types
  - `Digest`: Base class for cryptographic hash outputs
  - `OracleDigest`: Simulates a random oracle with lazy infinite output generation using entropy
  - `LazyDigest`: Deterministic infinite digest using hash function chaining
  - `LazyHexDigest`: Hexadecimal representation of lazy digests

- **hash.py**: Hash function adapters and oracle implementations
  - `Oracle`: Caches random oracle outputs for consistent responses
  - `CryptoHash`: Adapter for standard cryptographic hash functions
  - `OracleHash`: Approximates random oracle using cryptographic hash functions

## Development Commands

### Package Installation
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Install with visualization support
pip install -e ".[viz]"
```

### Running Demonstrations
```bash
# Interactive demo
python -m random_oracles.demo

# Property demonstrations
python -m random_oracles.properties

# Visual demonstrations
python -m random_oracles.visualize

# Algorithm explanations
python -m random_oracles.algorithms

# Run all demos
python -m random_oracles.demo all
```

### Testing
```bash
# Run tests with pytest
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=random_oracles

# Run specific test file
pytest tests/test_digest.py -v
```

### Building the Paper
```bash
cd paper/
pdflatex random_oracles.tex
# Or with latexmk
latexmk -pdf random_oracles.tex
```

## Key Implementation Details

### Digest Classes Architecture
- All digest classes inherit from `Digest` base class
- `OracleDigest` uses caching with entropy source (defaults to `hashlib.sha256(os.urandom(32))`)
- `LazyDigest` generates deterministic infinite sequences via `hash(seed || index)`
- Implements `__getitem__` for byte-level access to digest values

### Hash Function Adapters
- `CryptoHash` wraps standard hash functions (default: SHA-256)
- `Oracle` maintains cache for consistent random oracle simulation
- `OracleHash` combines `CryptoHash` with `LazyDigest` for infinite output

### Mathematical Foundations
- Random oracle: `{0,1}* → {0,1}^∞` (infinite output)
- Cryptographic hash: `{0,1}* → {0,1}^n` (fixed n-bit output)
- Lazy computation enables theoretical infinite outputs on finite machines

## Dependencies

Only standard library modules required:
- `hashlib`: Cryptographic hash functions
- `os`: Random number generation via `os.urandom()`

## Design Philosophy

- **Elegance over edge cases**: Code is intentionally simplified to highlight core concepts
- **Mathematical clarity**: Implementations directly reflect theoretical definitions
- **Pedagogical value**: Each class teaches a specific cryptographic concept
- **Theoretical exploration**: Demonstrates infinite outputs and lazy computation on finite machines

## Key Theoretical Concepts

- **Random Oracle**: A theoretical function `{0,1}* → {0,1}^∞` that returns random but consistent outputs
- **Lazy Computation**: Generates infinite sequences on-demand without pre-computation
- **Oracle Approximation**: `OracleDigest` simulates randomness via entropy; `LazyDigest` via deterministic chaining
- **Infinite Digests**: Conceptual exploration of unbounded output in practice