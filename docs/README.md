<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021

SPDX-License-Identifier: CC-BY-4.0
-->

# Personal Finance Coach

A Flask application that helps users manage their personal finances with Auth0 authentication.

## Environment Setup

### Auth0 Configuration

1. Create an Auth0 account at [auth0.com](https://auth0.com)
2. Create a new Application:
   - Go to Applications > Applications
   - Click "Create Application"
   - Name it "Personal Finance Coach"
   - Choose "Regular Web Application"

3. Configure Application URLs:
   ```
   Allowed Callback URLs:
   http://localhost:5000/callback
   https://${CODESPACE_NAME}-5000.app.github.dev/callback

   Allowed Logout URLs:
   http://localhost:5000
   https://${CODESPACE_NAME}-5000.app.github.dev

   Allowed Web Origins:
   http://localhost:5000
   https://${CODESPACE_NAME}-5000.app.github.dev
   ```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```properties
# Auth0 Configuration
AUTH0_CLIENT_ID='your-client-id'
AUTH0_CLIENT_SECRET='your-client-secret'
AUTH0_DOMAIN='your-domain.us.auth0.com'
APP_SECRET_KEY='your-secret-key'

# GitHub Codespace Configuration
CODESPACE_NAME='your-codespace-name'  # Optional: Only needed for Codespace development
```

Replace the placeholder values:
- `AUTH0_CLIENT_ID`: Found in Auth0 Application Settings
- `AUTH0_CLIENT_SECRET`: Found in Auth0 Application Settings
- `AUTH0_DOMAIN`: Your Auth0 domain (e.g., `dev-xxx.us.auth0.com`)
- `APP_SECRET_KEY`: Generate with `python -c 'import secrets; print(secrets.token_hex())'`
- `CODESPACE_NAME`: Your GitHub Codespace name (only if using Codespaces)

### Running in GitHub Codespaces

When running in GitHub Codespaces:
1. The `CODESPACE_NAME` environment variable is automatically set
2. Update your Auth0 Application URLs with your Codespace URL
3. The application will be available at `https://${CODESPACE_NAME}-5000.app.github.dev`

---

## Contributor Guidance

If you contribute to this repository, **please make sure to review and follow the community standards and reference the following files**:

- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md): Outlines the standards for behavior and participation in this community.  
  _Please read and follow the Code of Conduct to help maintain a welcoming environment for all contributors._

- [`CONTRIBUTING.md`](CONTRIBUTING.md): Provides detailed guidelines on how to contribute to this project, including how to submit issues and pull requests, coding standards, and commit message conventions.  
  _Please review these instructions before contributing to ensure your submissions align with the project's workflow and expectations._

- [`SECURITY.md`](SECURITY.md): Contains the process for reporting security vulnerabilities or concerns.  
  _If you discover a security issue, please follow the instructions in this file to report it responsibly._

We appreciate your attention to these documents to help keep the project collaborative, secure, and compliant.

---

## License

**Source code** in this repository is licensed under the [GNU General Public License v3.0 or later (GPL-3.0-or-later)](https://www.gnu.org/licenses/gpl-3.0.html).

**Documentation** (including the README, all files in the `docs/` directory, and all files in the `.github` directory) is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

For code files, you may see the following SPDX identifier at the top:
```
SPDX-License-Identifier: GPL-3.0-or-later
```
For documentation files, you may see:
```
SPDX-License-Identifier: CC-BY-4.0
```

If you contribute, you agree that your contributions will be licensed under these terms.
