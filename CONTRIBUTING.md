# Contributing to E-Ink To-Do List Display

Thank you for considering contributing to this project! 

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your hardware (Pi model, display version)
- Raspberry Pi OS version
- Error messages or logs

### Suggesting Features

Feature requests are welcome! Please open an issue describing:
- What you'd like to see
- Why it would be useful
- Potential implementation ideas (optional)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test on actual hardware if possible
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Add comments for complex logic
- Update documentation if needed
- Test on Raspberry Pi hardware when possible

### Testing

Before submitting:
- [ ] Code runs without errors
- [ ] Works with both V1 and V2 displays (if display-related)
- [ ] Doesn't break existing functionality
- [ ] Documentation is updated

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/eink-todo-display.git
cd eink-todo-display

# Create a branch
git checkout -b feature/your-feature

# Make changes and test
python3 test_connection.py
python3 todo_display.py

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/your-feature
```

## Questions?

Feel free to open an issue for any questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
