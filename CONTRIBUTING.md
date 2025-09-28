# Contributing to Content-Nuke-Claude

Thank you for your interest in contributing to Content-Nuke-Claude! This document provides guidelines for contributing to this next-generation content automation platform.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Types](#contribution-types)
- [Development Workflow](#development-workflow)
- [Testing Requirements](#testing-requirements)
- [Documentation Guidelines](#documentation-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## 📜 Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [jeremy@intentsolutions.io](mailto:jeremy@intentsolutions.io).

## 🚀 Getting Started

### Prerequisites

- **Claude Code CLI** (v1.0.123+)
- **Git** with SSH keys configured
- **Python 3.8+** for automation scripts
- **Node.js 18+** for documentation site
- **Blog platform** (Hugo, Jekyll, Gatsby, Next.js, or WordPress)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/content-nuke-claude.git
cd content-nuke-claude

# Install commands
cp commands/*.md ~/.claude/commands/

# Test command discovery
cd ~/test-project
/content-nuke --help
```

## 🛠️ Development Setup

### Environment Configuration

1. **Set up Waygate MCP** for credential management:
   ```bash
   # Configure API credentials in Waygate .env
   X_CLIENT_ID=your_oauth2_client_id
   X_CLIENT_SECRET=your_oauth2_client_secret
   X_API_KEY=your_api_key
   X_API_SECRET=your_api_secret
   ```

2. **Configure analytics database**:
   ```bash
   # Ensure analytics directory exists
   mkdir -p /home/jeremy/analytics/databases/
   ```

3. **Set up blog platforms** (see [Platform Setup Guide](docs/platform-setup.html))

### Dependencies

```bash
# Python dependencies for automation scripts
pip install requests requests-oauthlib python-dotenv

# Node.js dependencies for documentation
npm install -g hugo
```

## 🎯 Contribution Types

We welcome contributions in several areas:

### 1. **New Platform Templates**
- Support for additional blog platforms
- Enhanced deployment pipelines
- Custom build configurations

### 2. **Enhanced Analytics**
- Improved tracking and insights
- New metrics and visualizations
- Performance optimization

### 3. **API Integrations**
- Additional social media platforms
- Enhanced OAuth flows
- Better error handling

### 4. **Bug Fixes**
- Error handling improvements
- Edge case resolution
- Performance optimizations

### 5. **Documentation**
- Setup guides and tutorials
- API documentation
- Example configurations

### 6. **Command Improvements**
- New slash command templates
- Enhanced content generation
- Better cross-platform integration

## 🔄 Development Workflow

### Branching Strategy

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Create platform template branch
git checkout -b platform/platform-name

# Create bugfix branch
git checkout -b fix/issue-description
```

### Commit Message Format

Use conventional commits for clear history:

```
type(scope): description

feat(commands): add WordPress REST API integration
fix(analytics): resolve duplicate post tracking
docs(platform): update Hugo setup guide
refactor(scripts): improve OAuth error handling
```

### Testing Your Changes

1. **Test command functionality**:
   ```bash
   cd ~/test-project
   /your-new-command
   ```

2. **Verify analytics tracking**:
   ```bash
   python3 scripts/test_analytics.py
   ```

3. **Test cross-platform deployment**:
   ```bash
   /content-nuke
   ```

## 🧪 Testing Requirements

### Command Testing

All new commands must include:

1. **Functional testing** with real blog platforms
2. **Error handling** for common failure scenarios
3. **Analytics integration** verification
4. **Documentation** with usage examples

### Script Testing

Python scripts require:

1. **Unit tests** for core functions
2. **Integration tests** with external APIs
3. **Error handling** for network failures
4. **OAuth flow** validation

## 📝 Pull Request Process

### Before Submitting

1. **Test thoroughly** on your local environment
2. **Update documentation** for any new features
3. **Add tests** for new functionality
4. **Check analytics integration** works properly
5. **Verify command discovery** in Claude Code

### Review Process

1. **Automated checks** must pass
2. **Manual testing** by maintainers
3. **Documentation review** for completeness
4. **Security review** for API integrations
5. **Merge approval** from project maintainers

## 🚨 Security Guidelines

### API Credentials

- **Never commit** API keys or tokens
- **Use environment variables** only
- **Test with test credentials** during development
- **Document security requirements** clearly

### OAuth Implementation

- **Use secure flows** (OAuth 2.0 with PKCE)
- **Implement token refresh** automatically
- **Handle errors gracefully** without exposing credentials
- **Validate all inputs** and sanitize outputs

## 📞 Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: [jeremy@intentsolutions.io](mailto:jeremy@intentsolutions.io) for security issues

### Getting Help

1. **Check documentation** first
2. **Search existing issues** for similar problems
3. **Create detailed issue** with reproduction steps
4. **Join discussions** for feature ideas

---

**Thank you for contributing to Content-Nuke-Claude!** Your contributions help make content automation more accessible and powerful for the entire Claude Code community.

For questions about contributing, reach out to [jeremy@intentsolutions.io](mailto:jeremy@intentsolutions.io) or create an issue in this repository.