# 🔐 SecureFlow — Autonomous Vulnerability Triage & Fix Agent

> **GitLab AI Hackathon 2026 Submission**  
> Built with GitLab Duo Agent Platform + Anthropic Claude Sonnet 4

[![GitLab Duo](https://img.shields.io/badge/GitLab%20Duo-Agent%20Platform-orange)](https://docs.gitlab.com/user/duo_agent_platform/)
[![Anthropic Claude](https://img.shields.io/badge/Anthropic-Claude%20Sonnet%204-blueviolet)](https://www.anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is SecureFlow?

SecureFlow is a **GitLab Custom Flow** that autonomously triages security vulnerabilities, analyzes affected code, generates fixes, and creates merge requests — all triggered by a simple mention in an issue or MR comment.

**Mention `@ai-secureflow` on any vulnerability issue → SecureFlow handles the rest.**

## 🚀 Demo

```
Developer: @ai-secureflow please triage and fix the critical vulnerabilities in this project

SecureFlow:
  1. 🔍 Listed 23 vulnerabilities (4 CRITICAL, 7 HIGH, 12 MEDIUM)
  2. 📋 Analyzed top 4 critical vulnerabilities
  3. 🔎 Located affected code in src/auth/login.py, src/api/users.py
  4. 🔧 Generated fixes for SQL injection + hardcoded secret
  5. ✅ Created MR !47 "fix: resolve critical security vulnerabilities"
  6. 🔗 Linked vulnerabilities #CV-001, #CV-002 to MR !47
  7. 💬 Posted detailed security report as MR comment
```

## 🏗️ Architecture

```
GitLab Issue/MR Comment
        │
        ▼ (mention trigger)
┌─────────────────────────┐
│   SecureFlow Custom     │
│   Flow (YAML config)    │
│                         │
│  Step 1: Triage         │──► List Vulnerabilities
│  Step 2: Analyze        │──► Get Vulnerability Details
│  Step 3: Locate Code    │──► Grep + Read File
│  Step 4: Generate Fix   │──► Claude Sonnet 4 (built-in)
│  Step 5: Apply Fix      │──► Edit File / Create File
│  Step 6: Create MR      │──► Create Merge Request
│  Step 7: Link & Report  │──► Link Vulnerability to MR
│                         │    Create MR Note
└─────────────────────────┘
```

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| `List Vulnerabilities` | Enumerate all security vulnerabilities in the project |
| `Get Vulnerability Details` | Deep-dive into specific vulnerability CVE data |
| `Grep` | Search codebase for vulnerable patterns |
| `Read File` | Read affected source files for context |
| `Edit File` | Apply security fixes directly |
| `Create File With Contents` | Create new security configuration files |
| `Create Merge Request` | Open fix MR with proper description |
| `Link Vulnerability To Merge Request` | Connect vuln tracking to the fix |
| `Create Merge Request Note` | Post detailed security analysis report |
| `Get Pipeline Errors` | Check if CI/CD security scans are failing |
| `List Merge Request Diffs` | Review the proposed changes |

## 📋 Setup Instructions

### Prerequisites
- GitLab Premium or Ultimate tier
- GitLab Duo enabled for your group
- Maintainer or Owner role on the project

### 1. Create the Custom Flow

1. Navigate to your project → **Automate > Flows**
2. Select **New flow**
3. Enter:
   - **Display name**: `SecureFlow`
   - **Description**: `Autonomous vulnerability triage and fix agent`
   - **Visibility**: Public
4. Paste the contents of [`.gitlab/duo/secureflow.yml`](.gitlab/duo/secureflow.yml) into the Flow editor
5. Select **Create flow**

### 2. Enable the Flow

1. From the flow detail page, select **Enable**
2. Choose your **Group** and **Project**
3. Set triggers:
   - ✅ **Mention** (when `@ai-secureflow-<group>` is mentioned)
   - ✅ **Assign** (when the service account is assigned to an issue)
4. Select **Enable**

### 3. Use SecureFlow

In any issue or MR comment:
```
@ai-secureflow-mygroupname triage and fix critical vulnerabilities
```

Or assign the `ai-secureflow-mygroupname` user to a security issue.

## 📁 Repository Structure

```
secureflow/
├── README.md                          # This file
├── AGENTS.md                          # Agent capabilities documentation
├── .gitlab/
│   └── duo/
│       ├── secureflow.yml             # Custom Flow YAML config
│       └── agent-config.yml           # Custom Agent config (alternative)
├── .gitlab-ci.yml                     # CI/CD pipeline with security scanning
├── demo/
│   ├── vulnerable-app/                # Demo vulnerable application
│   │   ├── src/
│   │   │   ├── auth.py               # Contains intentional vulns for demo
│   │   │   └── api.py                # Contains intentional vulns for demo
│   │   └── requirements.txt
│   └── screenshots/                   # Demo screenshots
├── docs/
│   ├── architecture.md               # Detailed architecture
│   ├── security-report-template.md   # Report format
│   └── setup-guide.md                # Extended setup guide
└── LICENSE
```

## 🔒 Security Report Format

SecureFlow generates structured security reports:

```markdown
## 🔐 SecureFlow Security Analysis

**Vulnerabilities Triaged**: 4 CRITICAL, 7 HIGH
**Fix MR**: !47
**Risk Reduction**: 85% (critical vulns resolved)

### Critical Findings

#### 1. 🚨 SQL Injection — src/auth/login.py:45
**CVE**: CVE-2024-XXXX | **CVSS**: 9.8
**Fix Applied**: Parameterized queries implemented
**Status**: ✅ Fixed in MR !47

#### 2. 🚨 Hardcoded Secret — src/config.py:12  
**Type**: AWS Access Key exposed in source
**Fix Applied**: Moved to environment variable
**Status**: ✅ Fixed in MR !47

### CI/CD Recommendations
- Added SAST scanning to pipeline
- Secret detection enabled
- Dependency scanning configured
```

## 🏆 Hackathon Track

This submission targets:
- **Grand Prize** ($15K) — Most impactful use of GitLab Duo Agent Platform
- **Anthropic Bonus Track** ($10K) — Native Claude Sonnet 4 via GitLab AI Gateway
- **Most Impactful** ($5K) — Directly reduces security risk in production codebases

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*Built for the [GitLab AI Hackathon 2026](https://gitlab.devpost.com/) by the SecureFlow team.*
