# Security Policy

This document explains how security, privacy, and responsible reporting are handled for EconKit.

EconKit is a Python toolkit for economics data analysis, macroeconomic diagnostics, scenario simulation, forecasting, lightweight econometrics, and automated reporting.

Although EconKit is not a web service and does not store user accounts, security still matters because users may run the toolkit on local datasets, research files, classroom materials, or policy-related data.

---

## Supported Versions

The current actively maintained version is:

| Version | Supported |
|---|---|
| 1.1.x | Yes |
| 1.0.x | Limited stability support |
| < 1.0 | No |

Security and reliability fixes should target the latest version whenever possible.

---

## Scope

This security policy applies to:

- source code in `src/`
- command-line interface code
- test files
- documentation examples
- sample data
- GitHub Actions workflows
- packaging configuration
- project scripts
- generated example workflows

This policy is especially relevant for:

```text
src/econkit.py
src/econkit_cli.py
.github/workflows/tests.yml
requirements.txt
pyproject.toml
```

---

## What Counts as a Security Issue?

Please report issues such as:

- code execution vulnerabilities
- unsafe file handling
- path traversal risks
- accidental exposure of private files
- unsafe use of external input
- dependency security problems
- malicious pull requests
- suspicious workflow changes
- accidental inclusion of credentials
- accidental inclusion of private datasets
- unsafe examples in documentation
- commands that overwrite unexpected files
- commands that read files outside the intended path
- generated reports that expose private data unexpectedly

---

## What Does Not Usually Count as a Security Issue?

The following are usually normal bugs or feature requests rather than security issues:

- incorrect economic interpretation
- wrong chart label
- typo in documentation
- failing test
- unsupported file format
- missing CLI option
- slow performance on large files
- minor formatting problem
- disagreement about macroeconomic thresholds
- request for a new forecasting model

These can be reported through normal GitHub issues.

---

## Reporting a Security Issue

If you find a security issue, please report it carefully.

Preferred process:

1. Do not publicly post sensitive details if the issue could expose data or allow abuse.
2. Contact the project maintainer through GitHub or the contact method listed on the repository profile.
3. Include enough detail to reproduce the issue.
4. Include the affected file, command, or workflow.
5. Include whether private data, credentials, or unsafe file access may be involved.

Example report:

```text
Security issue: possible unsafe output path handling

File:
src/econkit_cli.py

Command:
python src/econkit_cli.py report data/sample.csv --output-dir ../../unexpected_folder

Concern:
The command may write outside the intended project directory.

Expected:
The CLI should clearly document or restrict output path behavior.
```

---

## Information to Include

A useful report should include:

- affected version or commit
- operating system
- Python version
- command used
- dataset type if relevant
- exact error message if available
- expected behavior
- actual behavior
- whether private data was exposed
- whether credentials were involved
- whether the issue is reproducible

Avoid sending private datasets unless absolutely necessary.

If possible, reproduce the issue with a small synthetic dataset.

---

## Responsible Disclosure

Please give the maintainer reasonable time to investigate and fix the issue before publishing detailed exploit information.

Suggested process:

1. Report the issue privately or carefully.
2. Allow time for confirmation.
3. Work with the maintainer on a fix if possible.
4. After a fix is available, public documentation can summarize the issue without exposing sensitive details.

---

## Data Privacy

EconKit is usually run locally.

The project itself does not intentionally collect, transmit, or store user data.

However, users may run EconKit on datasets that contain sensitive information.

Do not commit or share:

- private research datasets
- personally identifiable information
- student records
- financial account data
- confidential policy documents
- licensed datasets
- API keys
- access tokens
- passwords
- private configuration files

---

## Safe Dataset Guidelines

For examples, tests, and documentation, use:

- synthetic data
- small toy datasets
- public-domain data
- clearly licensed public data
- manually created sample data

Avoid using real private data in:

```text
data/
examples/
tests/
docs/
README.md
issues
pull requests
screenshots
```

---

## Credential Safety

Never commit credentials.

Do not commit:

```text
.env
.env.local
*.pem
*.key
credentials.json
token.json
id_rsa
id_ed25519
```

Do not paste credentials into:

- GitHub issues
- pull requests
- README examples
- documentation
- test files
- code comments

If a credential is accidentally committed, rotate it immediately.

Deleting it from the latest commit is not always enough because Git history may still contain it.

---

## File Handling Safety

EconKit commands can write outputs to folders such as:

```text
outputs/
outputs/report/
outputs/risk/
outputs/policy/
outputs/scenarios/
outputs/package/
```

When changing file-handling code:

- create output directories explicitly
- avoid deleting user files
- avoid overwriting unrelated files
- avoid reading unexpected paths
- avoid hidden network calls
- avoid executing files from datasets
- keep generated outputs predictable

---

## CLI Safety

The CLI should be predictable and transparent.

Good CLI behavior:

```text
- print what was generated
- save files in the requested output directory
- fail with a clear error message
- avoid destructive actions
- avoid hidden side effects
```

Bad CLI behavior:

```text
- silently deleting files
- writing outside the requested folder without explanation
- running external commands from user input
- downloading remote content without user intent
- executing arbitrary code from a dataset
```

---

## Dependency Safety

EconKit should keep dependencies minimal.

Core dependencies:

```text
numpy
pandas
matplotlib
tabulate
pytest
```

Before adding a new dependency, consider:

- Is it necessary?
- Is it actively maintained?
- Is it widely used?
- Does it introduce security risk?
- Can it be optional?
- Will it make installation harder?

Optional file-format dependencies such as Excel or Parquet support should remain optional when possible.

---

## GitHub Actions Safety

Workflow files should be reviewed carefully.

Important file:

```text
.github/workflows/tests.yml
```

Workflow changes should avoid:

- exposing secrets
- running untrusted commands
- installing from suspicious URLs
- uploading private data
- using unnecessary permissions
- modifying releases without review

A test workflow should generally:

- check out code
- set up Python
- install dependencies
- run tests

---

## Generated Output Safety

EconKit generates reports, charts, CSV files, and JSON diagnostics.

Generated outputs may include values from the input dataset.

Before sharing generated outputs publicly, users should check whether they contain sensitive information.

This applies to:

```text
economic_report.md
monetary_policy_report.md
data_quality_report.md
diagnostics.json
scenario_comparison.csv
indicator_forecasts.csv
regression_result.json
regression_report.md
```

---

## Documentation Safety

Documentation should not encourage unsafe behavior.

Avoid examples that:

- include private data
- include credentials
- download suspicious files
- run unknown scripts
- overwrite system folders
- imply investment advice
- imply official policy recommendations

Good examples should use:

```text
data/sample_economic_data.csv
outputs/
synthetic data
clear educational notes
```

---

## Economic Safety and Misuse

EconKit includes tools for:

- macro risk analysis
- monetary policy analysis
- business-cycle diagnosis
- inflation pressure analysis
- forecasting
- scenario simulation
- regression

These tools are simplified and transparent.

They should not be used as:

- official forecasts
- investment advice
- central-bank decisions
- automated trading signals
- professional policy recommendations
- proof of causal relationships without research design

Security includes reducing misuse caused by misleading claims.

Documentation and code comments should clearly state limitations.

---

## Maintainer Response Process

When a security report is received, maintainers should:

1. Acknowledge receipt.
2. Reproduce the issue if possible.
3. Assess severity.
4. Identify affected files and versions.
5. Create a fix.
6. Add or update tests when possible.
7. Update documentation if needed.
8. Release a patch if appropriate.
9. Credit the reporter if they want credit.

---

## Severity Guidelines

### Low Severity

Examples:

- documentation suggests unsafe path accidentally
- generated report includes more metadata than expected
- minor dependency warning with no known exploit

### Medium Severity

Examples:

- output path behavior could overwrite unexpected project files
- workflow permissions are broader than needed
- dependency has known vulnerability but limited project exposure

### High Severity

Examples:

- arbitrary code execution
- credential exposure
- private data exposure
- malicious workflow execution
- path traversal that reads or writes sensitive files

---

## Security Checklist for Contributors

Before submitting changes, check:

- [ ] No credentials are included.
- [ ] No private datasets are included.
- [ ] No unsafe shell commands are added.
- [ ] No hidden network calls are added.
- [ ] File output paths are predictable.
- [ ] Documentation examples use safe sample paths.
- [ ] Generated outputs are clearly described.
- [ ] New dependencies are justified.
- [ ] Tests pass.
- [ ] Economic limitations are documented when relevant.

---

## Security Checklist for Releases

Before creating a release, check:

- [ ] GitHub Actions tests pass.
- [ ] `requirements.txt` looks clean.
- [ ] `pyproject.toml` looks clean.
- [ ] No private files are committed.
- [ ] No accidental large files are committed.
- [ ] No credentials are committed.
- [ ] README examples are safe.
- [ ] CLI documentation is safe.
- [ ] Release notes do not expose sensitive information.

---

## Known Limitations

EconKit does not currently provide:

- sandboxed execution
- encrypted data storage
- user authentication
- access-control management
- cloud-hosted data protection
- professional audit logging
- automatic secret scanning
- advanced dependency vulnerability scanning

Users should apply normal local security practices when running EconKit.

---

## Recommended Local Practices

Users should:

- use synthetic data for public examples
- avoid putting private data into public repositories
- review generated outputs before sharing
- use virtual environments
- keep dependencies updated
- avoid running unknown code from forks
- avoid committing `outputs/` if it contains private analysis
- avoid publishing screenshots that reveal sensitive values

---

## Educational Disclaimer

EconKit is for educational and exploratory economic analysis.

It is not:

- an official forecasting system
- a central-bank policy model
- investment advice
- a substitute for professional econometric software
- a substitute for secure enterprise analytics infrastructure

Use EconKit responsibly.

---

## Contact

For security concerns, contact the repository maintainer through GitHub.

Repository:

```text
https://github.com/car6770/econkit
```

When reporting a security issue, include enough detail to reproduce the problem without sharing private data unnecessarily.
