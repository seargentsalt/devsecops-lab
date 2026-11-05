# DevSecOps Learning Lab: Flask + Semgrep + Gitleaks + pip-audit

> Intentionally vulnerable training application. Run only on localhost. Never deploy it to a public or company network.

## What this lab demonstrates

| Category | Tool | Expected lesson |
|---|---|---|
| SAST | Semgrep | Detect unsafe SQL construction |
| Secrets | Gitleaks | Detect a synthetic fake key in files and Git history |
| SCA | pip-audit | Identify known vulnerabilities in pinned Python dependencies |

## Prerequisites

- A personal GitHub account and a **public** practice repository.
- GitHub Actions enabled for the repository.
- Python 3.10+ for local execution (the vulnerable dependency set may not work on every modern Python version).
- A browser.

## Project structure

```text
devsecops-learning-lab/
├── .github/workflows/secure-ci.yml
├── app.py
├── config.py
├── database.py
├── templates/index.html
├── requirements.txt
├── gitleaks.toml
└── README.md
```

## Run locally (optional)

Use an isolated virtual environment. Do not install these deliberately old dependencies into your normal Python environment.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python database.py
python app.py
```

Open http://127.0.0.1:5000.

If the old Flask/Werkzeug combination does not run on your installed Python version, that is a compatibility issue in this deliberately old dependency set. The CI SCA job audits the requirements file; it does not need to run the application.

## Demonstrate the SQL injection (localhost only)

The search form builds SQL by concatenating untrusted input. Try a normal search first, then try:

```text
' OR '1'='1' --
```

This is an educational demonstration against the local SQLite database seeded by `database.py`. Do not use these tests against any other system.

## Synthetic secret

`config.py` contains a deliberately fake marker, not a usable credential:

```text
LAB_FAKE_0123456789ABCDEF
```

The custom Gitleaks rule in `gitleaks.toml` detects this marker. It is intentionally not an AWS/GitHub/cloud credential and cannot authenticate to a service.

## CI workflow

The workflow in `.github/workflows/secure-ci.yml` runs three independent jobs:

- `secrets`: Gitleaks scans the checked-out repository history.
- `sast`: Semgrep scans Python code and writes SARIF; the SARIF upload step publishes findings to GitHub Code scanning on a supported public repository.
- `sca`: pip-audit checks the pinned packages in `requirements.txt`.

The workflow uses major-version action tags to make this starter easier to follow. For production, verify and pin every action to its full 40-character commit SHA, then maintain those pins through a controlled update process. GitHub documents why full-SHA pinning is the immutable reference: https://docs.github.com/en/actions/reference/security/secure-use

## Important behaviour

- A scanner finding and a failed CI job are related but not identical. The scanner must return a non-zero exit code for the job to fail.
- `semgrep ... --error` makes Semgrep return a failing exit code when it finds findings.
- `pip-audit` returns non-zero when it identifies vulnerable dependencies (or encounters certain audit errors).
- Gitleaks fails when it detects a secret matching its rules.
- The GitHub SARIF upload is for code-scanning visibility. It does not itself enforce a merge gate.
- Required status checks in branch protection enforce the gate.

## Safety

All vulnerabilities and the synthetic secret are intentional. Do not add real credentials, connect this app to production data, expose it to the internet, or reuse the fake marker as a real secret.
