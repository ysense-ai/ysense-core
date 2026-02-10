# Claude Code Instructions - YSenseAI Platform

**Project:** YSenseAI Platform v4.1
**Repository:** ysense-ai/ysense-core (PRIVATE)
**Command Central Hub:** creator35lwb-web/verifimind-genesis-mcp

---

## MACP Integration

This project is coordinated via Command Central Hub (verifimind-genesis-mcp).

### Session Start: Check MACP Inbox

At the start of every session, check for pending tasks:

Use the `macp_read_messages` MCP tool with:
- repository: `creator35lwb-web/verifimind-genesis-mcp`
- filters.to: `RNA`
- limit: 5

Or run `/macp-inbox`.

### Session End: Create Handoff

Use the `macp_create_handoff` MCP tool with:
- repository: `creator35lwb-web/verifimind-genesis-mcp`
- agent: `RNA`
- session_type: `development`
- All required fields (completed, decisions, artifacts, pending, blockers, next_agent)

---

## Session Start Checklist

When starting a new session, ALWAYS:

1. [ ] Read this CLAUDE.md file
2. [ ] **Check MACP inbox** for pending tasks
3. [ ] Check CHANGELOG.md for recent changes
4. [ ] Review recent git log for latest state

---

## Project Overview

YSenseAI Platform v4.1 is the core platform for the YSenseAI ecosystem. It includes:
- API services
- Database layer (Firestore)
- Authentication (Crypto auth)
- Cloud deployment (GCP Cloud Build)

### Key Technologies

- Python
- Google Cloud Platform (GCP)
- Firestore
- Cloud Build / Cloud Run

---

## Development Workflow

```
1. Check MACP inbox for tasks
2. Implement changes locally
3. Run tests
4. Commit with descriptive message
5. Push to origin/main
6. Create handoff record via macp_create_handoff
```

---

## Important Notes

- This is a PRIVATE repository under ysense-ai org
- Uses GCP for deployment (see cloudbuild.yaml)
- Never commit credentials or API keys
- Check API_CONFIGURATION_GUIDE.md for API setup

---

**Protocol:** MACP v2.0 | FLYWHEEL Level 2
