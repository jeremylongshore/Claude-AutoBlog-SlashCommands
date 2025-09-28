# Security Policy

## Supported Versions

We provide security updates for the following versions of Content-Nuke-Claude:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

### Security Contact

If you discover a security vulnerability in Content-Nuke-Claude, please report it responsibly:

- **Email**: jeremy@intentsolutions.io
- **Subject**: [SECURITY] Content-Nuke-Claude Vulnerability Report

### What to Include

Please include the following information in your report:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** and affected components
4. **Suggested fix** (if you have one)
5. **Your contact information** for follow-up

### Response Timeline

- **Acknowledgment**: Within 24 hours
- **Initial Assessment**: Within 72 hours
- **Status Updates**: Weekly during investigation
- **Resolution**: Target within 30 days for high-severity issues

### Security Considerations

#### API Credentials
- Never commit API credentials to version control
- Use environment variables for all sensitive data
- Rotate API tokens regularly (X OAuth tokens expire every 2 hours)
- Monitor API usage for unusual activity

#### Script Execution
- All automation scripts run with minimal required permissions
- Review generated content before publishing
- Verify deployment targets before executing commands
- Use read-only tokens where possible

#### Data Privacy
- Analytics data is stored locally only
- No personal data is transmitted to third parties
- Command history includes only metadata, not content
- Users control all data retention and deletion

### Vulnerability Disclosure Policy

We follow coordinated disclosure:

1. **Private reporting** to our security team
2. **Investigation and fix** development
3. **Security update release** with fix
4. **Public disclosure** after users have time to update
5. **Credit to reporter** (if desired)

### Security Best Practices

When using Content-Nuke-Claude:

- **Review all generated content** before publishing
- **Use separate API credentials** for testing vs production
- **Enable two-factor authentication** on all connected accounts
- **Monitor published content** for any unauthorized changes
- **Keep the tool updated** to the latest version
- **Use version control** to track all content changes

### Reporting Non-Security Issues

For non-security bugs and feature requests, please use:
- [GitHub Issues](https://github.com/jeremylongshore/content-nuke-claude/issues)

Thank you for helping keep Content-Nuke-Claude secure!