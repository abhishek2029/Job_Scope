# Contributing to Tech Jobs Aggregator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- Clear description of the feature
- Use case and benefits
- Any implementation ideas

### Code Contributions

1. **Fork the repository**
2. **Create a branch** for your feature/fix
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/job-aggregator.git
cd job-aggregator

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the application
cd ..
./start.sh
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing

Before submitting a PR:
- Test the scraping functionality
- Test the frontend UI
- Check for console errors
- Verify US location filtering works

## Adding Companies

To add more companies to scrape:

1. Edit `backend/fortune500_companies.py`
2. Add company to appropriate section (Greenhouse or Lever)
3. Test the scraping works
4. Submit PR with company name in title

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
