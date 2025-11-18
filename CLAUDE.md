# CLAUDE.md - AI Assistant Guide for Continuum

This document provides comprehensive guidance for AI assistants working on the Continuum project. It outlines the codebase structure, development workflows, conventions, and best practices.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Development Workflow](#development-workflow)
- [Code Conventions](#code-conventions)
- [Testing Strategy](#testing-strategy)
- [Documentation Standards](#documentation-standards)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## Project Overview

**Project Name:** Continuum
**Repository:** spellbind3r/continuum
**Status:** Initial setup phase

### Purpose

[To be filled: Brief description of what this project does and its main objectives]

### Technology Stack

[To be filled: List of main technologies, frameworks, and tools used]

Example structure:
- **Language:** [e.g., Python, JavaScript, TypeScript, Go]
- **Framework:** [e.g., React, Django, FastAPI, Express]
- **Database:** [e.g., PostgreSQL, MongoDB, Redis]
- **Testing:** [e.g., Jest, pytest, Go test]
- **Build Tools:** [e.g., webpack, vite, make]
- **CI/CD:** [e.g., GitHub Actions, GitLab CI]

## Repository Structure

```
continuum/
├── .git/                  # Git metadata
├── CLAUDE.md             # This file - AI assistant guide
├── README.md             # Project documentation
├── [src/]                # Source code (to be created)
├── [tests/]              # Test files (to be created)
├── [docs/]               # Additional documentation (to be created)
├── [config/]             # Configuration files (to be created)
└── [scripts/]            # Build and utility scripts (to be created)
```

### Key Directories

**Update this section as the project structure evolves:**

- **src/** - Main application source code
  - Core business logic
  - API endpoints / handlers
  - Data models
  - Utilities and helpers

- **tests/** - Test suites
  - Unit tests
  - Integration tests
  - End-to-end tests
  - Test fixtures and mocks

- **docs/** - Documentation
  - API documentation
  - Architecture diagrams
  - Design decisions
  - Deployment guides

- **config/** - Configuration files
  - Environment-specific configs
  - Application settings
  - External service configurations

## Development Workflow

### Branch Strategy

- **Main Branch:** `main` (or `master`)
  - Protected branch
  - Contains production-ready code
  - Requires PR approval before merging

- **Feature Branches:** `claude/claude-md-*` or `feature/*`
  - Created for each new feature or bug fix
  - Named descriptively: `feature/user-authentication`, `bugfix/login-error`
  - Should be short-lived and focused

- **Development Branch:** [Specify if applicable]

### Git Workflow

1. **Starting Work:**
   ```bash
   git fetch origin
   git checkout -b feature/your-feature-name
   ```

2. **Making Changes:**
   ```bash
   # Make your changes
   git add .
   git commit -m "Clear, descriptive commit message"
   ```

3. **Pushing Changes:**
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. **Creating Pull Request:**
   - Use clear, descriptive PR titles
   - Include summary of changes
   - Reference related issues
   - Add test plan

### Commit Message Conventions

Follow conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements

**Examples:**
- `feat(auth): add JWT token authentication`
- `fix(api): resolve null pointer in user endpoint`
- `docs(readme): update installation instructions`
- `refactor(db): optimize query performance`

## Code Conventions

### General Principles

1. **Clarity over Cleverness:** Write code that is easy to understand
2. **DRY (Don't Repeat Yourself):** Extract common patterns into reusable functions
3. **SOLID Principles:** Follow object-oriented design principles where applicable
4. **Error Handling:** Always handle errors gracefully
5. **Security First:** Validate inputs, sanitize outputs, avoid common vulnerabilities

### Language-Specific Conventions

[Update based on your primary language]

#### For Python:
- Follow PEP 8 style guide
- Use type hints for function signatures
- Docstrings for all public functions/classes
- Maximum line length: 100 characters
- Use `black` for formatting
- Use `pylint` or `flake8` for linting

#### For JavaScript/TypeScript:
- Follow ESLint configuration
- Use TypeScript for type safety
- Prefer `const` over `let`, avoid `var`
- Use async/await over callbacks
- JSDoc comments for public APIs
- Maximum line length: 100 characters

#### For Go:
- Follow `gofmt` formatting
- Use `golint` and `go vet`
- Write idiomatic Go code
- Handle all errors explicitly
- Use meaningful variable names

### Naming Conventions

- **Files:** Use lowercase with hyphens or underscores (e.g., `user-service.ts`, `user_service.py`)
- **Functions:** Use camelCase (JavaScript) or snake_case (Python)
- **Classes:** Use PascalCase
- **Constants:** Use UPPER_SNAKE_CASE
- **Variables:** Use descriptive names (avoid single letters except in loops)

### Code Comments

- Write comments for **why**, not **what**
- Keep comments up-to-date with code changes
- Use TODO comments with context: `// TODO(name): Description`
- Document complex algorithms or business logic
- Remove commented-out code before committing

## Testing Strategy

### Testing Pyramid

1. **Unit Tests (70%)**
   - Test individual functions/methods
   - Mock external dependencies
   - Fast execution
   - High coverage goal: >80%

2. **Integration Tests (20%)**
   - Test component interactions
   - Use test databases/services
   - Verify API contracts

3. **End-to-End Tests (10%)**
   - Test critical user flows
   - Run in staging environment
   - Focus on happy paths and critical edge cases

### Test Organization

```
tests/
├── unit/
│   ├── test_auth.py
│   └── test_users.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── e2e/
    └── test_user_flows.py
```

### Running Tests

[Update with actual commands]

```bash
# Run all tests
npm test              # or: pytest, go test ./...

# Run specific test file
npm test user.test.js # or: pytest tests/test_user.py

# Run with coverage
npm test -- --coverage # or: pytest --cov=src

# Run integration tests only
npm test:integration   # or: pytest tests/integration/
```

### Test Writing Guidelines

- **Arrange-Act-Assert (AAA)** pattern
- One assertion per test (when possible)
- Descriptive test names: `test_user_creation_with_valid_email`
- Use fixtures/factories for test data
- Clean up resources after tests
- Mock external services (APIs, databases in unit tests)

## Documentation Standards

### Code Documentation

- **README.md:** Project overview, setup instructions, basic usage
- **API Documentation:** Use OpenAPI/Swagger, JSDoc, or similar
- **Inline Comments:** Explain complex logic, business rules
- **Architecture Docs:** System design, data flow diagrams

### Updating Documentation

When making changes:
1. Update relevant README sections
2. Update API documentation if endpoints change
3. Update CLAUDE.md for workflow changes
4. Keep changelog updated

### Documentation Tools

[Specify tools used]
- API Docs: [e.g., Swagger, Postman, JSDoc]
- Code Docs: [e.g., Sphinx, TypeDoc, GoDoc]
- Diagrams: [e.g., Mermaid, PlantUML, Draw.io]

## Common Tasks

### Setting Up Development Environment

```bash
# Clone repository
git clone <repository-url>
cd continuum

# Install dependencies
[npm install | pip install -r requirements.txt | go mod download]

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations (if applicable)
[npm run migrate | python manage.py migrate | make migrate]

# Start development server
[npm run dev | python app.py | go run main.go]
```

### Running the Application

```bash
# Development mode
[npm run dev | python app.py --dev | go run main.go]

# Production mode
[npm start | gunicorn app:app | ./continuum]
```

### Building for Production

```bash
# Build application
[npm run build | python -m build | go build]

# Run production build
[npm run start:prod | gunicorn app:app | ./continuum]
```

### Database Operations

```bash
# Create migration
[npm run migration:create | python manage.py makemigrations]

# Run migrations
[npm run migration:run | python manage.py migrate | make migrate]

# Rollback migration
[npm run migration:rollback | python manage.py migrate <previous>]

# Seed database
[npm run seed | python manage.py loaddata | make seed]
```

### Linting and Formatting

```bash
# Run linter
[npm run lint | pylint src/ | golint ./...]

# Fix auto-fixable issues
[npm run lint:fix | black src/ | go fmt ./...]

# Run formatter
[npm run format | black . | gofmt -w .]
```

## Key Files and Their Purpose

[Update as files are created]

- **package.json / requirements.txt / go.mod:** Dependencies
- **.env.example:** Template for environment variables
- **.gitignore:** Files to exclude from version control
- **Makefile / scripts/:** Build and automation scripts
- **docker-compose.yml:** Local development environment
- **.github/workflows/:** CI/CD pipelines

## Security Considerations

### Best Practices

1. **Never commit secrets:** Use environment variables
2. **Validate all inputs:** Prevent injection attacks
3. **Sanitize outputs:** Prevent XSS attacks
4. **Use HTTPS:** For all external communications
5. **Keep dependencies updated:** Regular security patches
6. **Principle of least privilege:** Minimal permissions needed
7. **Authentication & Authorization:** Verify user identity and permissions

### Common Vulnerabilities to Avoid

- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Command Injection
- Path Traversal
- Insecure Deserialization
- Hardcoded Secrets

## Troubleshooting

### Common Issues

[Update with actual issues as they arise]

**Issue:** [Description]
**Solution:** [Steps to resolve]

**Issue:** [Description]
**Solution:** [Steps to resolve]

### Debug Mode

```bash
# Enable debug logging
[DEBUG=* npm run dev | export DEBUG=1 && python app.py]
```

### Getting Help

1. Check existing documentation in `/docs`
2. Review related issues in issue tracker
3. Check commit history for context: `git log --grep="keyword"`
4. Ask team members or project maintainers

## Performance Optimization

### Guidelines

- Profile before optimizing
- Focus on bottlenecks identified by profiling
- Consider caching strategies (Redis, in-memory)
- Optimize database queries (indexes, query optimization)
- Use lazy loading where appropriate
- Minimize external API calls
- Consider async/parallel processing

### Monitoring

[Specify monitoring tools and practices]
- Application monitoring: [e.g., New Relic, DataDog]
- Error tracking: [e.g., Sentry, Rollbar]
- Logging: [e.g., ELK stack, CloudWatch]

## Deployment

### Environments

- **Development:** Local development environment
- **Staging:** Pre-production environment for testing
- **Production:** Live environment

### Deployment Process

[Update with actual deployment process]

1. Ensure all tests pass
2. Create release branch/tag
3. Deploy to staging
4. Run smoke tests
5. Deploy to production
6. Monitor for errors
7. Rollback if needed

### CI/CD Pipeline

[Describe automated processes]
- Automated testing on PR
- Automated builds
- Deployment triggers
- Health checks

## Contributing

### For AI Assistants

When working on this codebase:

1. **Read this file first** to understand conventions
2. **Maintain consistency** with existing code style
3. **Write tests** for new functionality
4. **Update documentation** when making changes
5. **Follow git workflow** as described above
6. **Ask questions** if conventions are unclear
7. **Consider security** implications of changes
8. **Run tests** before committing
9. **Keep commits focused** on single concerns
10. **Update this file** if workflows change

### Code Review Checklist

Before submitting PR:
- [ ] Code follows project conventions
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Error handling implemented
- [ ] Performance considered
- [ ] Backwards compatibility maintained
- [ ] Commit messages are clear
- [ ] No debugging code left in
- [ ] Dependencies justified and minimal

## Maintenance

### Regular Tasks

- **Weekly:** Update dependencies, review security advisories
- **Monthly:** Review and clean up unused code, update documentation
- **Quarterly:** Review architecture, plan refactoring

### Technical Debt

Track technical debt items and prioritize regularly:
- Code that needs refactoring
- Missing tests
- Documentation gaps
- Performance bottlenecks
- Security updates needed

## Additional Resources

### External Documentation

[Add links to relevant resources]
- Project Wiki: [URL]
- API Documentation: [URL]
- Design Documents: [URL]
- Team Guidelines: [URL]

### Learning Resources

[Add relevant learning materials]
- Technology-specific docs
- Best practices guides
- Tutorial videos
- Related projects

---

## Document Maintenance

**Last Updated:** 2025-11-18
**Maintained By:** Project maintainers and AI assistants

**Note to AI Assistants:** Keep this document up-to-date as the project evolves. Update sections when you make significant changes to the codebase structure, add new workflows, or identify new conventions.

### Changelog

- 2025-11-18: Initial CLAUDE.md creation for Continuum project

---

## Quick Reference

### Essential Commands

```bash
# Development
[start dev server command]

# Testing
[run tests command]

# Building
[build command]

# Deployment
[deploy command]
```

### Important Paths

- Source: `[src/]`
- Tests: `[tests/]`
- Config: `[config/]`
- Docs: `[docs/]`

### Contact

- Project Lead: [Name/Email]
- Repository: spellbind3r/continuum
- Issues: [Issue tracker URL]

---

**This is a living document. Update it as the project grows and evolves.**
