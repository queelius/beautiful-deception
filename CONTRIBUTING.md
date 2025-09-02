# Contributing to The Beautiful Deception

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🎯 Areas of Interest

We welcome contributions in the following areas:

### Research & Theory
- Additional LazyDigest constructions with novel properties
- Formal verification of security properties (Coq, Isabelle, Lean)
- Quantum-resistant variants and post-quantum analysis
- Connections to other areas of mathematics and computer science

### Implementation
- Performance optimizations (while maintaining clarity)
- Additional language implementations (Rust, Go, Haskell)
- GPU/parallel implementations
- WebAssembly version for browser demos

### Education
- Interactive visualizations
- Jupyter notebooks with tutorials
- Additional examples and use cases
- Translations of documentation

### Documentation
- Clarifications and improvements to existing docs
- Additional mathematical proofs and explanations
- Real-world application examples
- Blog posts and tutorials

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   gh repo fork queelius/beautiful-deception --clone
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Run tests to ensure everything works**
   ```bash
   pytest tests/
   ```

## 📝 Development Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/quantum-resistant-lazy`
- `fix/cycle-detection-bug`
- `docs/add-tutorial-merkle-trees`

### 2. Write Your Code

Follow these principles:

- **Clarity over cleverness**: This is a pedagogical project
- **Document your code**: Add docstrings and comments
- **Maintain consistency**: Follow existing code style
- **Test your changes**: Add tests for new functionality

### 3. Code Style

We use Black for formatting and Ruff for linting:

```bash
# Format code
black src/ tests/

# Check linting
ruff check src/ tests/

# Type checking
mypy src/
```

### 4. Testing

All new code should include tests:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=random_oracles --cov-report=html

# Run specific test
pytest tests/test_digest.py::TestLazyDigest -v
```

### 5. Documentation

- Update docstrings for any modified functions
- Update README.md if adding new features
- Add examples to the `examples/` directory
- Update the paper if making theoretical contributions

## 🔄 Pull Request Process

1. **Ensure all tests pass**
   ```bash
   pytest tests/
   black --check src/ tests/
   ruff check src/ tests/
   ```

2. **Update documentation**
   - Add/update docstrings
   - Update README if needed
   - Add your contribution to CHANGELOG (if exists)

3. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what changes you made and why
   - Include examples of how to use new features

4. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   - [ ] Theoretical contribution

   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests for changes
   - [ ] Coverage maintained/improved

   ## Checklist
   - [ ] Code follows project style
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No sensitive information included
   ```

## 🤔 Philosophy

This project values:

1. **Pedagogical clarity**: Code should teach concepts
2. **Mathematical rigor**: Claims should be precise
3. **Practical demonstration**: Theory should be implementable
4. **Philosophical depth**: Explore fundamental questions

## 💡 Specific Contribution Ideas

### Easy (Good First Issues)
- Add more examples to `examples/`
- Improve error messages and validation
- Add type hints to existing code
- Write additional unit tests

### Medium
- Implement LazyDigest in another language
- Create interactive web demo
- Add benchmarking suite
- Implement additional hash function adapters

### Advanced
- Formal verification of properties
- Quantum resistance analysis
- Novel LazyDigest constructions
- Theoretical contributions to the paper

## 📚 Resources

### Understanding the Codebase
1. Read the paper: `paper/beautiful_deception.pdf`
2. Run the demos: `python -m random_oracles.demo`
3. Study the tests: `tests/test_digest.py`

### Background Reading
- [Random Oracles are Practical](https://cseweb.ucsd.edu/~mihir/papers/ro.html)
- [The Random Oracle Methodology, Revisited](https://arxiv.org/abs/cs/9807028)
- [Cryptographic Hash Functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function)

## ❓ Questions?

- Open an issue for bugs or feature requests
- Start a discussion for theoretical questions
- Email the author for collaboration opportunities

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make cryptographic concepts more accessible and understandable! 🎭