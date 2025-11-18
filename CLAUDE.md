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
**Status:** Active development - MVP phase
**Developer:** Solo project, limited free time, learning-focused
**Goal:** Interactive time-traveling world explorer for learning history and geography

### Purpose

Continuum is an interactive application that allows users to explore the globe and travel through time virtually, learning history and geography in a creative, visually rich, and dynamic manner. Users can click anywhere on Earth, select any time period, and discover what was happening at that location.

**Core Vision:**
- Explore any place on Earth at any point in time
- Learn endlessly with high-quality, targeted information
- Feel connected to the whole world and its history
- Experience a deep sense of awe about human civilization
- Be transparent about uncertainty ("I don't know" is acceptable)

**Inspired by:** Timelines of World History poster/book, but interactive and multidimensional

### Development Philosophy

**"See Progress Today, Improve Tomorrow"**

This project follows an incremental, learning-focused approach:
1. Build the simplest version that demonstrates the core idea
2. Get something working you can show and click
3. Add one improvement at a time
4. Learn modern web development gradually
5. Avoid complexity until it's needed

**Key Principles:**
- ✅ Simple is better than perfect
- ✅ Working is better than planned
- ✅ One feature at a time
- ✅ Learn by building
- ✅ Progress over perfection

### Technology Stack

**Current Stack (v0.1 - Simple Start):**
- **Language:** Python 3.8+
- **Backend:** Flask (simple, easy to learn)
- **Frontend:** Plain HTML + CSS + JavaScript (no frameworks yet)
- **Map:** Leaflet.js (simple 2D map via CDN)
- **Data Source:** Wikipedia API (real-time)
- **Database:** None yet (will add SQLite for caching in Phase 1)

**Why This Stack:**
- Matches developer's background (SQL, Java, C++, XSL)
- No build tools needed
- No npm/webpack complexity
- Can see changes immediately (just refresh browser)
- Easy to understand and debug
- Can upgrade to more powerful tools later

**Future Evolution:**
- Phase 1: Add SQLite for caching
- Phase 2: Improve data quality (Wikidata, curated sources)
- Phase 3: Upgrade to 3D globe (React-Globe.gl or Cesium)
- Phase 4: Advanced features (connections, timelines)
- Phase 5: Production-ready (PostgreSQL, proper deployment)

## Repository Structure

**Current Structure (v0.1):**

```
continuum/
├── app.py                      # Flask server (main backend logic)
├── templates/
│   └── index.html             # Frontend (map + UI)
├── requirements.txt           # Python dependencies
├── README.md                  # User-facing documentation
├── CLAUDE.md                  # This file - AI assistant guide
├── continuum_app_initial_idea.md  # Original vision document
└── GPT-1.rtf                  # Previous AI consultation notes
```

**Key Files:**

- **app.py** - Flask web server
  - `/` route serves the HTML page
  - `/explore` endpoint handles location queries
  - `get_nearest_city()` - maps coordinates to major cities
  - `fetch_historical_info()` - queries Wikipedia API
  - Simple confidence scoring logic

- **templates/index.html** - Complete frontend in one file
  - Leaflet.js map integration
  - Time slider (3000 BCE to 2024 CE)
  - Click handler for location queries
  - Knowledge category display
  - Confidence visualization

- **requirements.txt** - Just 2 dependencies
  - Flask (web server)
  - Wikipedia-API (data source)

**Future Structure (as project grows):**

```
continuum/
├── app.py
├── templates/
│   └── index.html
├── static/                    # CSS, JS files (when we split them out)
│   ├── css/
│   └── js/
├── data/                      # Cached data, SQLite database
│   └── continuum.db
├── utils/                     # Helper modules
│   ├── geocoding.py
│   ├── wikipedia_client.py
│   └── confidence.py
├── requirements.txt
└── README.md
```

**Note:** Keep it simple! Don't create these directories until you need them.

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

### Incremental Development Workflow

**CRITICAL:** This project follows an incremental, learn-as-you-go approach. Each session should:

1. **Start Small:** Pick ONE thing to add or fix
2. **Make It Work:** Get it functional, don't worry about perfect
3. **Test It:** Click around, see if it works
4. **Commit:** Save your progress
5. **Show Someone:** Even if it's just yourself tomorrow
6. **Pick Next Thing:** Choose one improvement for next session

**Example Session Progression:**

```
Session 1: Get the basic app running ✅
Session 2: Add SQLite caching for Wikipedia results
Session 3: Improve city detection (add more cities)
Session 4: Better confidence scoring algorithm
Session 5: Add "I don't know" messaging for low confidence
Session 6: Make UI prettier
Session 7: Add one more knowledge category
...and so on
```

### Working with AI Assistants (Critical!)

This project was kickstarted with AI help. Here's how to work with AI effectively:

#### ✅ DO: Be Specific and Incremental

**Good Prompts:**
- "Add a function to cache Wikipedia results in SQLite with location, year, and content fields"
- "Update the confidence scoring to consider article length and number of citations"
- "Add a new knowledge category called 'Economy' that extracts economic information"

**Bad Prompts:**
- "Make the app better"
- "Implement all the features from the architecture"
- "Refactor everything"

#### ✅ DO: Protect Against Over-Refactoring

Always include this in your prompts when fixing bugs:

```
"ONLY fix this specific error. Do NOT refactor, rename functions,
or change file structure. Make the MINIMAL change needed."
```

#### ✅ DO: Define the Interface First

```
"I want to add caching. First, just show me what the function
signature and database schema should look like. Don't implement
everything yet."
```

Then review, adjust, and ask for implementation.

#### ❌ DON'T: Let AI Rewrite Large Chunks

If AI suggests rewriting more than ~50 lines at once, stop and ask:
- "Can we do this in smaller steps?"
- "What's the minimal change to make X work?"

#### ❌ DON'T: Accept Solutions You Don't Understand

If AI gives you code you can't follow:
- "Explain this code line by line"
- "Is there a simpler way to do this?"
- "Can you add comments explaining what each part does?"

### Commit Message Conventions

Keep it simple for this project:

```
<type>: <what you did>
```

**Examples:**
- `feat: add SQLite caching for Wikipedia results`
- `fix: city detection now works for southern hemisphere`
- `improve: better confidence scoring algorithm`
- `ui: made the info panel prettier`
- `docs: updated README with new features`

**No need for complex conventional commits** - just make it clear what changed!

## Code Conventions

### Keep It Simple

For this learning project, don't worry about perfect code style. Focus on:

1. **Readable:** Can you understand it when you come back tomorrow?
2. **Functional:** Does it work?
3. **Commented:** Did you explain the tricky parts?

### Python Conventions (Loose Guidelines)

- Use snake_case for functions: `get_historical_info()`
- Use descriptive variable names: `confidence_score` not `cs`
- Add comments when something is non-obvious
- Handle errors with try/except when calling external APIs
- Keep functions short (under 50 lines when possible)

### JavaScript/HTML Conventions (In templates/index.html)

- Use camelCase for JavaScript variables: `currentYear`
- Use kebab-case for HTML ids: `year-display`
- Keep JavaScript simple - no fancy frameworks yet
- Comment any complex logic

### When to Refactor

**Don't refactor** until:
- You've copy-pasted the same code 3+ times
- A function is over 100 lines
- You can't understand your own code from last week

**Then refactor** by:
- Extracting repeated code into a function
- Breaking big functions into smaller ones
- Adding helpful comments

## Content Philosophy

### Transparent Uncertainty

Continuum embraces **"I don't know"** as a feature, not a bug.

**Core Principles:**

1. **Scholarly Consensus First**
   - Wikipedia and peer-reviewed sources prioritized
   - Multiple sources increase confidence
   - Contemporary accounts valued highly

2. **Honest About Gaps**
   - Low confidence = explicitly state "Limited information"
   - Empty regions stay dark (low brightness)
   - Better to say "unknown" than to guess

3. **Interesting > Boring (But Labeled)**
   - Apocryphal facts are OK if labeled clearly
   - Example: "It was long believed that... but actually..."
   - Engage with stories, but always follow with truth

4. **Balanced Views on Controversies**
   - Present multiple perspectives on disputed events
   - Weight by scholarly consensus
   - Show confidence breakdown (e.g., "68% of scholars support view A")
   - Avoid fringe theories unless in special "controversy mode"

### Confidence Scoring

**Current Simple Algorithm:**
```python
confidence = min(0.9, 0.5 + len(article_text) / 2000)
```

**Confidence Levels:**
- **0.8-1.0:** "Well-documented" (bright on map)
- **0.6-0.8:** "Generally accepted" (medium brightness)
- **0.4-0.6:** "Limited evidence" (dim)
- **0.0-0.4:** "Speculative" / "Unknown" (dark)

**Future Improvements:**
- Factor in number of sources
- Check for cross-referencing
- Temporal proximity (contemporary sources score higher)
- Source quality (peer-reviewed > general web)

### Knowledge Categories

**Current Categories:**
1. **Overview** - General information about the place/time
2. **Politics** - Government, rulers, empires
3. **Culture** - Language, art, literature
4. **Religion** - Beliefs, temples, practices

**Future Categories:**
5. **Science & Technology** - Discoveries, inventions, tools
6. **Economy** - Trade, agriculture, resources
7. **Diplomacy** - Allies, enemies, relations
8. **Society** - Social structure, customs, daily life
9. **Food & Agriculture** - Diet, crops, cuisine
10. **Interesting Facts** - Notable events, legends, mysteries

### Handling Controversial Topics

**Examples:**

**Palestine/Kashmir/Other Territorial Disputes:**
- Show historical evolution of boundaries
- Present perspectives from all sides
- Label based on year and source
- Scholarly consensus weighted most

**Cultural/Historical Controversies:**
- Present mainstream scholarly view first
- Note alternative interpretations exist
- Provide source counts for each view
- Allow "Explore controversy" mode (future feature)

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
