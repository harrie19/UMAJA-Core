# Contributing to UMAJA-Core

Thank you for your interest in contributing to UMAJA-Core! This document provides comprehensive guidelines for contributing to the project. We welcome contributions from everyone and appreciate your efforts to improve this project.

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)
- [Translation Guide](#translation-guide)
- [Archetype Proposal Process](#archetype-proposal-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)
- [Testing Guidelines](#testing-guidelines)
- [Performance Standards](#performance-standards)
- [Security Best Practices](#security-best-practices)
- [Code Review Checklist](#code-review-checklist)
- [Contributor Recognition](#contributor-recognition)
- [Community Guidelines](#community-guidelines)

---

## Ways to Contribute

There are many ways to contribute to UMAJA-Core:

### 📝 Content Contributions
- **Archetype Development**: Create or enhance character archetypes with cultural insights
- **Story Content**: Add narrative elements, quests, or character backstories
- **Cultural Research**: Contribute authentic cultural references and context
- **Lore Building**: Expand the UMAJA universe with consistent world-building

### 💻 Code Contributions
- **Feature Development**: Implement new features and functionality
- **Bug Fixes**: Identify and resolve issues in the codebase
- **Performance Optimization**: Improve application speed and efficiency
- **Refactoring**: Enhance code quality and maintainability
- **API Development**: Build or improve backend services

### 📚 Documentation
- **User Guides**: Create tutorials and how-to documentation
- **API Documentation**: Document endpoints, parameters, and responses
- **Code Comments**: Improve inline documentation
- **README Updates**: Keep project information current
- **Wiki Contributions**: Expand the knowledge base

### 🎨 Design Contributions
- **UI/UX Design**: Improve user interface and experience
- **Visual Assets**: Create icons, illustrations, or graphics
- **Accessibility**: Enhance design for users with disabilities
- **Responsive Design**: Optimize layouts for various devices

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18.x or higher)
- **npm** or **yarn** package manager
- **Git** for version control
- A code editor (VS Code, WebStorm, etc.)

### Setup Instructions

1. **Fork the Repository**
   ```bash
   # Click the 'Fork' button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/UMAJA-Core.git
   cd UMAJA-Core
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/harrie19/UMAJA-Core.git
   ```

4. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

5. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

6. **Start Development Server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Project Structure

```
UMAJA-Core/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Application pages
│   ├── services/       # API and service logic
│   ├── utils/          # Utility functions
│   ├── styles/         # CSS/SCSS files
│   ├── locales/        # Translation files
│   └── archetypes/     # Character archetype definitions
├── public/             # Static assets
├── tests/              # Test files
├── docs/               # Documentation
└── scripts/            # Build and utility scripts
```

---

## Code Style Guidelines

### General Principles

- **Clarity over Cleverness**: Write code that is easy to understand
- **Consistency**: Follow existing patterns in the codebase
- **DRY**: Don't Repeat Yourself - extract common functionality
- **SOLID Principles**: Apply object-oriented design principles where appropriate

### JavaScript/TypeScript

```javascript
// Use ES6+ features
const greeting = (name) => `Hello, ${name}!`;

// Use descriptive variable names
const userAge = 25;
const isAuthenticated = true;

// Use PascalCase for components
const UserProfile = ({ user }) => {
  return <div>{user.name}</div>;
};

// Use camelCase for functions and variables
function calculateTotalScore(scores) {
  return scores.reduce((sum, score) => sum + score, 0);
}

// Use UPPER_SNAKE_CASE for constants
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.umaja.org';
```

### Formatting

- **Indentation**: 2 spaces (no tabs)
- **Line Length**: Maximum 100 characters
- **Semicolons**: Use semicolons consistently
- **Quotes**: Use single quotes for strings, except in JSON
- **Trailing Commas**: Use trailing commas in multi-line objects/arrays

### Linting

Run the linter before committing:

```bash
npm run lint
npm run lint:fix  # Auto-fix issues
```

### Comments

```javascript
// Good: Explain WHY, not WHAT
// Cache results to avoid expensive API calls on re-renders
const cachedData = useMemo(() => processData(rawData), [rawData]);

// Bad: Obvious comments
// Set x to 5
const x = 5;

/**
 * Calculate character stats based on archetype and level
 * @param {Object} archetype - Character archetype data
 * @param {number} level - Current character level
 * @returns {Object} Calculated stats object
 */
function calculateStats(archetype, level) {
  // Implementation
}
```

---

## Commit Message Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without changing functionality
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates
- **ci**: CI/CD configuration changes
- **revert**: Reverting previous commits

### Examples

```bash
# Feature
feat(archetypes): add Swahili warrior archetype

# Bug fix
fix(auth): resolve token expiration issue

# Documentation
docs(readme): update installation instructions

# Performance
perf(rendering): optimize character list rendering with virtualization

# Multiple changes
feat(i18n): add French translation support

- Add French locale files
- Update language selector component
- Add translation helper utilities

Closes #123
```

### Scope Examples

- `archetypes`: Character archetype system
- `i18n`: Internationalization/translations
- `auth`: Authentication system
- `ui`: User interface components
- `api`: Backend API
- `db`: Database-related changes
- `tests`: Testing infrastructure

### Rules

- Use imperative mood: "add feature" not "added feature"
- Don't capitalize first letter
- No period at the end of subject
- Limit subject line to 72 characters
- Reference issues and PRs in footer

---

## Pull Request Process

### Before Submitting

1. **Update Your Branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run Tests**
   ```bash
   npm test
   npm run test:coverage
   ```

3. **Check Code Quality**
   ```bash
   npm run lint
   npm run type-check  # For TypeScript
   ```

4. **Update Documentation**
   - Update relevant README sections
   - Add/update JSDoc comments
   - Update CHANGELOG.md if applicable

### Submitting a Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Use a descriptive title following commit conventions
   - Fill out the PR template completely
   - Link related issues (e.g., "Closes #123")
   - Add screenshots/videos for UI changes
   - Describe testing performed

3. **PR Template**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

### Test Environment
- OS: [e.g., macOS, Windows, Linux]
- Browser: [e.g., Chrome 100, Firefox 95]
- Node version: [e.g., 18.x]

## Screenshots/Videos
[If applicable]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Dependent changes merged
```

### Review Process

1. **Automated Checks**: CI/CD pipeline must pass
2. **Code Review**: At least one maintainer approval required
3. **Address Feedback**: Make requested changes promptly
4. **Final Review**: Maintainer performs final check
5. **Merge**: Maintainer merges the PR

### After Merge

- Delete your feature branch
- Update your local repository
- Celebrate! 🎉

---

## Translation Guide

We use JSON-based i18n for multi-language support. Translations live in `src/locales/`.

### Directory Structure

```
src/locales/
├── en/
│   ├── common.json
│   ├── archetypes.json
│   ├── ui.json
│   └── errors.json
├── sw/
│   ├── common.json
│   ├── archetypes.json
│   ├── ui.json
│   └── errors.json
└── ... (other languages)
```

### Adding a New Language

1. **Create Language Directory**
   ```bash
   mkdir src/locales/[language-code]
   ```

2. **Copy Base Files**
   ```bash
   cp src/locales/en/*.json src/locales/[language-code]/
   ```

3. **Translate Content**
   - Keep keys identical to English version
   - Translate only the values
   - Maintain placeholders and formatting

4. **Register Language**
   
   Update `src/i18n/config.js`:
   ```javascript
   export const supportedLanguages = {
     en: { name: 'English', nativeName: 'English' },
     sw: { name: 'Swahili', nativeName: 'Kiswahili' },
     fr: { name: 'French', nativeName: 'Français' },
     // Add your language here
   };
   ```

### JSON Schema Examples

#### common.json
```json
{
  "app": {
    "name": "UMAJA",
    "tagline": "Unity Through Stories"
  },
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "create": "Create",
    "confirm": "Confirm"
  },
  "navigation": {
    "home": "Home",
    "archetypes": "Archetypes",
    "profile": "Profile",
    "settings": "Settings"
  }
}
```

#### archetypes.json
```json
{
  "archetypes": {
    "warrior": {
      "name": "Warrior",
      "description": "A brave fighter skilled in combat",
      "traits": {
        "strength": "Strength",
        "courage": "Courage",
        "honor": "Honor"
      }
    },
    "healer": {
      "name": "Healer",
      "description": "A wise caretaker who mends wounds",
      "traits": {
        "wisdom": "Wisdom",
        "compassion": "Compassion",
        "patience": "Patience"
      }
    }
  },
  "stats": {
    "health": "Health",
    "energy": "Energy",
    "experience": "Experience",
    "level": "Level"
  }
}
```

#### ui.json
```json
{
  "forms": {
    "labels": {
      "username": "Username",
      "email": "Email",
      "password": "Password"
    },
    "placeholders": {
      "enterUsername": "Enter your username",
      "enterEmail": "Enter your email address"
    },
    "validation": {
      "required": "This field is required",
      "invalidEmail": "Please enter a valid email",
      "minLength": "Minimum {{count}} characters required"
    }
  },
  "messages": {
    "success": "Operation completed successfully",
    "error": "An error occurred",
    "loading": "Loading..."
  }
}
```

#### errors.json
```json
{
  "errors": {
    "network": {
      "offline": "You appear to be offline",
      "timeout": "Request timed out",
      "serverError": "Server error occurred"
    },
    "authentication": {
      "unauthorized": "You are not authorized",
      "sessionExpired": "Your session has expired",
      "invalidCredentials": "Invalid username or password"
    },
    "validation": {
      "fieldRequired": "{{field}} is required",
      "invalidFormat": "Invalid {{field}} format",
      "outOfRange": "{{field}} must be between {{min}} and {{max}}"
    }
  }
}
```

### Translation Best Practices

1. **Context Matters**: Understand the context where text appears
2. **Cultural Sensitivity**: Adapt idioms and expressions appropriately
3. **Consistency**: Use consistent terminology throughout
4. **Placeholders**: Don't translate placeholder syntax (e.g., `{{variable}}`)
5. **Formatting**: Maintain HTML tags and special characters
6. **Length**: Be mindful of text length for UI elements
7. **Testing**: Test translations in the actual UI

### Plural Forms

```json
{
  "items": {
    "zero": "No items",
    "one": "{{count}} item",
    "other": "{{count}} items"
  }
}
```

### Gender-Specific Translations

```json
{
  "welcome": {
    "male": "Welcome, Mr. {{name}}",
    "female": "Welcome, Ms. {{name}}",
    "neutral": "Welcome, {{name}}"
  }
}
```

---

## Archetype Proposal Process

Character archetypes are central to UMAJA. Follow this process to propose new archetypes:

### 1. Research Phase

- **Cultural Background**: Research the cultural context
- **Historical Accuracy**: Verify historical/mythological sources
- **Unique Traits**: Identify distinguishing characteristics
- **Community Consultation**: Engage with cultural community members

### 2. Proposal Template

Create a proposal document in `docs/proposals/archetypes/`:

```markdown
# Archetype Proposal: [Archetype Name]

## Overview
Brief description of the archetype

## Cultural Context
- **Origin**: Geographic/cultural origin
- **Historical Period**: Time period or mythological era
- **Cultural Significance**: Role in society/mythology
- **Sources**: References and citations

## Character Attributes

### Base Stats
- Strength: [1-10]
- Agility: [1-10]
- Intelligence: [1-10]
- Wisdom: [1-10]
- Charisma: [1-10]
- Endurance: [1-10]

### Special Abilities
1. **Ability Name**: Description
2. **Ability Name**: Description
3. **Ability Name**: Description

### Starting Equipment
- Item 1
- Item 2
- Item 3

## Visual Design

### Appearance Description
Detailed description of visual characteristics

### Color Palette
- Primary: #XXXXXX
- Secondary: #XXXXXX
- Accent: #XXXXXX

### Reference Images
[Links or attachments]

## Gameplay Integration

### Starting Quest
Brief description of introductory quest

### Skill Tree
- Branch 1: [Skills]
- Branch 2: [Skills]
- Branch 3: [Skills]

### Character Arc
Potential character development path

## Cultural Sensitivity Review

- [ ] Consulted with cultural representatives
- [ ] Avoided stereotypes
- [ ] Respectful representation
- [ ] Authentic details verified

## Implementation Checklist

- [ ] JSON data structure created
- [ ] Translations added (all supported languages)
- [ ] Visual assets created/sourced
- [ ] Abilities implemented
- [ ] Tests written
- [ ] Documentation updated

## Additional Notes
Any other relevant information
```

### 3. JSON Schema for Archetypes

```json
{
  "id": "unique-archetype-id",
  "version": "1.0.0",
  "metadata": {
    "name": {
      "en": "Archetype Name",
      "sw": "Jina la Archetype"
    },
    "description": {
      "en": "Detailed description",
      "sw": "Maelezo ya kina"
    },
    "culture": "Cultural origin",
    "region": "Geographic region",
    "era": "Historical period or 'mythological'"
  },
  "stats": {
    "base": {
      "strength": 7,
      "agility": 6,
      "intelligence": 5,
      "wisdom": 8,
      "charisma": 6,
      "endurance": 7
    },
    "growth": {
      "strength": 1.2,
      "agility": 1.1,
      "intelligence": 1.0,
      "wisdom": 1.3,
      "charisma": 1.1,
      "endurance": 1.2
    }
  },
  "abilities": [
    {
      "id": "ability-1",
      "name": {
        "en": "Ability Name",
        "sw": "Jina la Uwezo"
      },
      "description": {
        "en": "What the ability does",
        "sw": "Kinachofanya uwezo"
      },
      "type": "active|passive",
      "cooldown": 60,
      "energyCost": 25,
      "unlockLevel": 1
    }
  ],
  "equipment": {
    "starting": [
      {
        "id": "item-1",
        "slot": "weapon|armor|accessory",
        "quantity": 1
      }
    ]
  },
  "appearance": {
    "defaultSkin": "skin-id",
    "colorScheme": {
      "primary": "#8B4513",
      "secondary": "#DAA520",
      "accent": "#FF6347"
    },
    "assets": {
      "portrait": "/assets/archetypes/archetype-id/portrait.png",
      "fullBody": "/assets/archetypes/archetype-id/fullbody.png",
      "icon": "/assets/archetypes/archetype-id/icon.png"
    }
  },
  "quests": {
    "introQuest": "quest-id-1",
    "classQuests": ["quest-id-2", "quest-id-3"]
  },
  "skillTree": {
    "branches": [
      {
        "id": "branch-1",
        "name": {
          "en": "Branch Name",
          "sw": "Jina la Tawi"
        },
        "skills": ["skill-1", "skill-2", "skill-3"]
      }
    ]
  },
  "lore": {
    "backstory": {
      "en": "Rich backstory text",
      "sw": "Maandishi ya historia"
    },
    "culturalNotes": {
      "en": "Cultural context and significance",
      "sw": "Muktadha na umuhimu wa kitamaduni"
    }
  }
}
```

### 4. Review Process

1. **Community Feedback**: Open proposal for community comments (1 week)
2. **Cultural Review**: Verification by cultural consultants
3. **Technical Review**: Code/implementation review by maintainers
4. **Approval**: Final approval from core team
5. **Implementation**: Merge into main branch
6. **Announcement**: Promote new archetype to community

---

## Bug Reports

Found a bug? Help us fix it!

### Before Submitting

1. **Check Existing Issues**: Search for similar bug reports
2. **Update to Latest**: Verify bug exists in latest version
3. **Reproduce**: Confirm you can consistently reproduce the bug
4. **Simplify**: Create minimal reproduction case

### Bug Report Template

```markdown
## Bug Description
Clear and concise description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Screenshots/Videos
If applicable, add media to help explain the problem

## Environment
- **OS**: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- **Browser**: [e.g., Chrome 108, Firefox 107, Safari 16]
- **Device**: [e.g., Desktop, iPhone 14, Samsung Galaxy S22]
- **Screen Resolution**: [e.g., 1920x1080]
- **App Version**: [e.g., 1.2.3]

## Console Output
```
Paste any relevant console errors or logs
```

## Additional Context
Any other context about the problem

## Possible Solution
(Optional) Suggest a fix if you have one

## Priority
- [ ] Critical (app is unusable)
- [ ] High (major feature broken)
- [ ] Medium (minor feature broken)
- [ ] Low (cosmetic issue)
```

### Severity Levels

- **Critical**: App crashes, data loss, security vulnerabilities
- **High**: Major features unusable, significant functionality broken
- **Medium**: Minor features broken, workarounds available
- **Low**: Cosmetic issues, minor inconveniences

---

## Feature Requests

Have an idea for UMAJA? We'd love to hear it!

### Feature Request Template

```markdown
## Feature Description
Clear and concise description of the feature

## Problem Statement
What problem does this feature solve?
Example: "I'm always frustrated when..."

## Proposed Solution
Detailed description of how the feature should work

## Alternative Solutions
Other approaches you've considered

## Use Cases
Examples of how this feature would be used:
1. Use case 1
2. Use case 2
3. Use case 3

## Benefits
- Benefit 1
- Benefit 2
- Benefit 3

## Drawbacks/Risks
Potential downsides or challenges

## User Stories
- As a [user type], I want to [action] so that [benefit]
- As a [user type], I want to [action] so that [benefit]

## UI/UX Mockups
(Optional) Add sketches, wireframes, or mockups

## Technical Considerations
Any technical details or implementation notes

## Success Metrics
How will we measure if this feature is successful?

## Priority
- [ ] Must Have
- [ ] Should Have
- [ ] Nice to Have

## Related Issues
Links to related issues or discussions

## Additional Context
Any other information about the feature request
```

### Feature Evaluation Criteria

Features are evaluated based on:
- **Impact**: How many users will benefit?
- **Alignment**: Does it fit project vision?
- **Feasibility**: Can we implement it with available resources?
- **Maintenance**: Long-term support requirements
- **Community Interest**: Level of community support

---

## Testing Guidelines

Quality code requires thorough testing.

### Testing Stack

- **Unit Tests**: Jest
- **Component Tests**: React Testing Library
- **E2E Tests**: Cypress or Playwright
- **Coverage**: nyc/istanbul

### Writing Tests

#### Unit Test Example

```javascript
// src/utils/stats.test.js
import { calculateStats } from './stats';

describe('calculateStats', () => {
  it('should calculate basic stats correctly', () => {
    const archetype = {
      stats: { base: { strength: 10 }, growth: { strength: 1.1 } }
    };
    const level = 5;
    
    const result = calculateStats(archetype, level);
    
    expect(result.strength).toBe(14); // 10 + (4 * 1.1)
  });

  it('should handle invalid input', () => {
    expect(() => calculateStats(null, 5)).toThrow();
  });

  it('should not allow negative levels', () => {
    const archetype = { stats: { base: {}, growth: {} } };
    expect(() => calculateStats(archetype, -1)).toThrow();
  });
});
```

#### Component Test Example

```javascript
// src/components/CharacterCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import CharacterCard from './CharacterCard';

describe('CharacterCard', () => {
  const mockCharacter = {
    id: '1',
    name: 'Test Hero',
    level: 5,
    archetype: 'warrior'
  };

  it('renders character information', () => {
    render(<CharacterCard character={mockCharacter} />);
    
    expect(screen.getByText('Test Hero')).toBeInTheDocument();
    expect(screen.getByText('Level 5')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const handleSelect = jest.fn();
    render(<CharacterCard character={mockCharacter} onSelect={handleSelect} />);
    
    fireEvent.click(screen.getByRole('button'));
    
    expect(handleSelect).toHaveBeenCalledWith(mockCharacter.id);
  });
});
```

#### E2E Test Example

```javascript
// cypress/e2e/character-creation.cy.js
describe('Character Creation Flow', () => {
  beforeEach(() => {
    cy.visit('/create-character');
  });

  it('creates a new character successfully', () => {
    cy.get('[data-cy=archetype-select]').select('warrior');
    cy.get('[data-cy=character-name]').type('Brave Hero');
    cy.get('[data-cy=create-button]').click();
    
    cy.url().should('include', '/character/');
    cy.contains('Brave Hero').should('be.visible');
  });

  it('validates required fields', () => {
    cy.get('[data-cy=create-button]').click();
    
    cy.contains('Name is required').should('be.visible');
  });
});
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run specific test file
npm test -- stats.test.js
```

### Test Coverage Requirements

- **Minimum Overall Coverage**: 80%
- **Critical Paths**: 100% coverage
- **New Features**: Must include tests
- **Bug Fixes**: Add regression test

### Testing Best Practices

1. **AAA Pattern**: Arrange, Act, Assert
2. **One Assertion**: Test one thing per test (when possible)
3. **Descriptive Names**: Use clear test descriptions
4. **Independent Tests**: Tests should not depend on each other
5. **Mock External Dependencies**: Use mocks/stubs for APIs, databases
6. **Test Edge Cases**: Include boundary conditions and error cases
7. **Fast Tests**: Keep unit tests quick (< 100ms)

---

## Performance Standards

UMAJA must be fast and responsive.

### Performance Metrics

#### Load Time
- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Time to Interactive (TTI)**: < 3.5s
- **Total Blocking Time (TBT)**: < 300ms

#### Runtime Performance
- **Frame Rate**: Maintain 60 FPS
- **Input Latency**: < 50ms response time
- **Memory Usage**: < 100MB for typical session
- **Bundle Size**: 
  - Initial bundle: < 200KB (gzipped)
  - Total assets: < 1MB (gzipped)

### Performance Best Practices

#### Code Optimization

```javascript
// ❌ Bad: Inefficient re-renders
function CharacterList({ characters }) {
  return characters.map(char => (
    <div onClick={() => selectCharacter(char.id)}>
      {char.name}
    </div>
  ));
}

// ✅ Good: Optimized with memoization
const CharacterList = memo(({ characters, onSelect }) => {
  return characters.map(char => (
    <CharacterItem 
      key={char.id} 
      character={char} 
      onSelect={onSelect} 
    />
  ));
});
```

#### Asset Optimization

- **Images**: Use WebP format, lazy loading
- **Code Splitting**: Dynamic imports for routes
- **Tree Shaking**: Remove unused code
- **Minification**: Compress JavaScript and CSS

#### Lazy Loading

```javascript
// Lazy load routes
const Archetypes = lazy(() => import('./pages/Archetypes'));
const Profile = lazy(() => import('./pages/Profile'));

// Lazy load images
<img 
  src={thumbnail} 
  loading="lazy" 
  alt="Character portrait" 
/>
```

#### Measuring Performance

```bash
# Lighthouse audit
npm run lighthouse

# Bundle analysis
npm run analyze

# Performance profiling
npm run profile
```

### Performance Checklist

- [ ] Images optimized and lazy-loaded
- [ ] Code split by route
- [ ] Memoization used for expensive computations
- [ ] Virtual scrolling for long lists
- [ ] Service worker for offline caching
- [ ] Critical CSS inlined
- [ ] Fonts optimized (woff2, font-display)
- [ ] No blocking JavaScript
- [ ] API responses cached appropriately
- [ ] Database queries optimized with indexes

---

## Security Best Practices

Security is paramount for protecting our users.

### Security Principles

1. **Defense in Depth**: Multiple layers of security
2. **Least Privilege**: Minimum necessary permissions
3. **Fail Securely**: Default to secure state on error
4. **Never Trust Input**: Validate and sanitize all input
5. **Security by Design**: Built-in, not bolted-on

### Common Vulnerabilities

#### XSS Prevention

```javascript
// ❌ Bad: Vulnerable to XSS
function UserComment({ comment }) {
  return <div dangerouslySetInnerHTML={{ __html: comment }} />;
}

// ✅ Good: Safe rendering
function UserComment({ comment }) {
  return <div>{comment}</div>;
}

// ✅ Good: Sanitized HTML (if HTML needed)
import DOMPurify from 'dompurify';

function UserComment({ comment }) {
  const sanitized = DOMPurify.sanitize(comment);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

#### SQL Injection Prevention

```javascript
// ❌ Bad: SQL injection vulnerability
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Good: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.execute(query, [userId]);
```

#### Authentication

```javascript
// ✅ Secure password hashing
import bcrypt from 'bcrypt';

const saltRounds = 12;
const hashedPassword = await bcrypt.hash(password, saltRounds);

// ✅ JWT with expiration
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// ✅ Secure session management
app.use(session({
  secret: process.env.SESSION_SECRET,
  secure: true, // HTTPS only
  httpOnly: true, // No JavaScript access
  sameSite: 'strict',
  maxAge: 3600000 // 1 hour
}));
```

#### CSRF Protection

```javascript
// Use CSRF tokens
import csrf from 'csurf';
app.use(csrf());

// Include token in forms
<input type="hidden" name="_csrf" value={csrfToken} />
```

### Data Protection

#### Sensitive Data

- **Never Log**: Passwords, tokens, API keys
- **Encrypt at Rest**: Use encryption for sensitive database fields
- **Encrypt in Transit**: HTTPS everywhere
- **Secure Storage**: Use environment variables for secrets

```javascript
// ❌ Bad: Exposing sensitive data
console.log('User password:', password);

// ✅ Good: Avoid logging sensitive data
console.log('User authenticated:', userId);

// ❌ Bad: Hardcoded secrets
const apiKey = 'sk_live_abc123...';

// ✅ Good: Environment variables
const apiKey = process.env.API_KEY;
```

#### Personal Information

- **Data Minimization**: Collect only necessary data
- **User Consent**: Explicit consent for data collection
- **Right to Delete**: Allow users to delete their data
- **Data Portability**: Allow users to export their data

### Security Checklist

- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries to prevent SQL injection
- [ ] HTTPS enforced (no HTTP)
- [ ] Secure headers configured (CSP, HSTS, etc.)
- [ ] Authentication using secure methods
- [ ] Authorization checks on all protected resources
- [ ] CSRF protection enabled
- [ ] Rate limiting implemented
- [ ] Dependencies regularly updated
- [ ] Security scanning in CI/CD
- [ ] Secrets managed securely (not in code)
- [ ] Error messages don't leak sensitive info
- [ ] File uploads validated and scanned
- [ ] API endpoints authenticated and authorized

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead, email security concerns to: **security@umaja.org**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours.

---

## Code Review Checklist

### For Authors

Before requesting review:

- [ ] Code compiles and runs without errors
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No debug code or console.logs
- [ ] Commit messages follow conventions
- [ ] PR description is complete
- [ ] Screenshots/videos added (if UI changes)

### For Reviewers

#### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs

#### Code Quality
- [ ] Code is readable and maintainable
- [ ] Functions are focused and not too long
- [ ] No unnecessary complexity
- [ ] DRY principle followed
- [ ] Naming is clear and consistent
- [ ] Comments explain "why", not "what"

#### Testing
- [ ] Tests cover new functionality
- [ ] Tests are meaningful
- [ ] Edge cases are tested
- [ ] Test names are descriptive

#### Performance
- [ ] No performance regressions
- [ ] Efficient algorithms used
- [ ] Database queries optimized
- [ ] No unnecessary renders (React)

#### Security
- [ ] Input is validated
- [ ] No security vulnerabilities
- [ ] Sensitive data is protected
- [ ] Authorization is checked

#### Documentation
- [ ] Public APIs are documented
- [ ] README updated if needed
- [ ] Breaking changes noted
- [ ] Migration guide provided (if needed)

### Review Etiquette

#### For Reviewers

- **Be Kind**: Critique code, not people
- **Be Specific**: Point to exact issues
- **Explain Why**: Help author understand reasoning
- **Suggest Solutions**: Offer constructive alternatives
- **Ask Questions**: Use questions to prompt thought
- **Praise Good Work**: Acknowledge excellent code

Example comments:

```
❌ "This is wrong."
✅ "This might cause issues when X is null. Consider adding a null check."

❌ "Bad naming."
✅ "The name 'handleClick' is generic. Consider 'handleArchetypeSelection' for clarity."

❌ "Rewrite this."
✅ "This could be simplified using Array.map(). Example: [code snippet]"

✅ "Nice use of memoization here! This will improve performance significantly."
```

#### For Authors

- **Be Open**: Accept feedback graciously
- **Ask for Clarification**: If you don't understand, ask
- **Explain Reasoning**: Help reviewers understand your approach
- **Respond Promptly**: Address feedback in a timely manner
- **Show Appreciation**: Thank reviewers for their time

---

## Contributor Recognition

We value every contribution to UMAJA!

### Recognition Levels

#### Bronze Contributors
- First merged PR
- Listed in CONTRIBUTORS.md
- Bronze badge in community Discord

#### Silver Contributors
- 5+ merged PRs
- Listed in CONTRIBUTORS.md with highlights
- Silver badge in community Discord
- Mentioned in release notes

#### Gold Contributors
- 20+ merged PRs or major feature contributions
- Featured in CONTRIBUTORS.md
- Gold badge in community Discord
- Invited to contributor meetings
- Listed in "About" section of app

#### Platinum Contributors
- 50+ merged PRs or critical contributions
- Permanent recognition in app credits
- Platinum badge in community Discord
- Voting rights on major decisions
- Co-author status on publications

### Special Recognition

- **Archetype Creator**: Create 3+ approved archetypes
- **Translation Master**: Complete translation for a language
- **Bug Hunter**: Report 10+ valid bugs
- **Documentation Hero**: Major documentation contributions
- **Community Champion**: Outstanding community support

### Hall of Fame

Outstanding contributors will be featured in:
- Project website
- Annual blog posts
- Conference presentations
- Academic publications

### Rewards

While UMAJA is open source and volunteer-driven:
- **Swag**: Stickers, t-shirts for significant contributors
- **Conference Tickets**: Sponsorship for relevant conferences
- **Letters of Recommendation**: For job/school applications
- **LinkedIn Endorsements**: Skill endorsements from maintainers

---

## Community Guidelines

### Our Pledge

We pledge to make participation in UMAJA a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

#### Positive Behavior

- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

#### Unacceptable Behavior

- Harassment, trolling, or discriminatory comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Spam or promotional content
- Other conduct inappropriate in a professional setting

### Communication Channels

- **GitHub Discussions**: Feature discussions, questions
- **Discord**: Real-time chat, community support
- **Email**: security@umaja.org for security issues
- **Twitter**: @UMAJAProject for announcements

### Mentorship

New contributors can request mentorship:
- Pair programming sessions
- Code review walkthroughs
- Architecture discussions
- Career guidance

Contact maintainers via Discord or GitHub Discussions.

### Conflict Resolution

If you experience or witness unacceptable behavior:

1. **Direct Resolution**: Politely address the person directly (if comfortable)
2. **Report to Maintainers**: Contact via conduct@umaja.org
3. **Provide Details**: Include links, screenshots, context
4. **Confidentiality**: Reports will be kept confidential
5. **Action**: Maintainers will investigate and take appropriate action

### Enforcement

Violations may result in:
- Warning
- Temporary ban from community spaces
- Permanent ban from community spaces

All community members are expected to comply immediately with moderation requests.

---

## Questions?

Need help? Have questions?

- 📖 **Documentation**: Check our [Wiki](https://github.com/harrie19/UMAJA-Core/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/harrie19/UMAJA-Core/discussions)
- 💭 **Discord**: Join our [community server](https://discord.gg/umaja)
- 📧 **Email**: contact@umaja.org

---

## License

By contributing to UMAJA-Core, you agree that your contributions will be licensed under the same license as the project.

---

## Thank You!

Thank you for contributing to UMAJA! Your efforts help build a platform that celebrates cultural diversity and brings communities together through storytelling. Every contribution, no matter how small, makes a difference.

**Together, we build UMAJA - Unity Through Stories** 🌍✨

---

*Last updated: 2026-01-01*
