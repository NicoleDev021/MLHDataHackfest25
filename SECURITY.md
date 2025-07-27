<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021

SPDX-License-Identifier: CC-BY-4.0
-->

# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.1   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of MLHDataHackfest25 seriously. If you believe you have found a security vulnerability, please report it to us responsibly.

### How to Report

**Preferred Method:**
- Open a new [GitHub Issue](../../issues/new?template=security_report.md) with the label ![security](https://img.shields.io/badge/security-ac1401?style=flat&labelColor=ac1401&color=ac1401)
- Please provide as much detail as possible while omitting sensitive exploit details from the public issue body
- If needed, you can request further private discussion in your issue

**Alternative Methods:**
1. If you do not wish to disclose details publicly, please mention in your issue that you'd like to provide more information privately
2. A project maintainer will reach out to coordinate a private discussion
3. For highly sensitive vulnerabilities, contact the maintainer directly

### Information to Include

When reporting a vulnerability, please include the following information:
- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

## Handling of Vulnerabilities

### Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Update**: Within 7 days with preliminary assessment
- **Resolution**: Security fixes will be prioritized and released as soon as possible

### Security Update Process

1. Vulnerability assessment and verification
2. Development of security patch
3. Testing of the patch
4. Coordinated disclosure (if applicable)
5. Release of security update
6. Public disclosure in release notes

All security issues will be reviewed promptly. If a vulnerability is confirmed, we will work to address it as quickly as possible and will communicate updates in the related issue.

### Security Best Practices

When contributing to this project, please follow these security guidelines:

#### Authentication & Authorization
- Never hardcode credentials or API keys
- Use environment variables for sensitive configuration
- Implement proper session management
- Follow OAuth2/OIDC best practices with Auth0

#### Input Validation
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Sanitize data before processing
- Implement proper error handling

#### Dependencies
- Keep dependencies updated
- Monitor for security advisories
- Use tools like `safety` and `bandit` for security scanning
- Review dependency licenses

#### Data Protection
- Encrypt sensitive data at rest and in transit
- Follow GDPR/privacy regulations
- Implement proper logging (avoid logging sensitive data)
- Use HTTPS for all communications

### Automated Security Measures

This repository includes automated security measures:

- **Dependabot**: Automated dependency updates
- **CodeQL**: Automated code security analysis
- **Security Workflow**: Regular vulnerability scanning
- **Secrets Detection**: Prevents accidental credential commits

### Security Tools Integration

We use the following security tools:

- **Safety**: Python dependency vulnerability scanner
- **Bandit**: Python security linter
- **Semgrep**: Static analysis security scanner
- **TruffleHog**: Secrets detection
- **CodeQL**: GitHub's semantic code analysis

### Acknowledgments

We appreciate the security research community and will acknowledge researchers who responsibly disclose vulnerabilities (with their permission).

Thank you for helping to keep this project and its users safe!

---

**Note**: This security policy is a living document and will be updated as our security practices evolve.
