# 🥇 MSME Scheme & Subsidy AI Navigator

[![Backend CI](https://github.com/your-org/msme-scheme-ai-navigator/actions/workflows/backend-ci-render.yml/badge.svg)](https://github.com/your-org/msme-scheme-ai-navigator/actions)
[![Frontend CI](https://github.com/your-org/msme-scheme-ai-navigator/actions/workflows/frontend-ci-netlify.yml/badge.svg)](https://github.com/your-org/msme-scheme-ai-navigator/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An enterprise-grade, role-based platform designed to match Indian Micro, Small, and Medium Enterprises (MSMEs) with central schemes (CGTMSE, ZED, PMEGP) and state-specific industrial subsidies (such as the Karnataka Industrial Policy Investment Promotion Subsidy).

The system features sub-second eligibility evaluation, multilingual AI copilot advice, an automated document compliance vault, and complete back-office verification pipelines for District Industries Centres (DIC).

---

## 🏛️ System Architecture

```text
               ┌────────────────────────────────────────────────────────┐
               │              Netlify Edge Gateway (SPA)                │
               │   • MSME Profile Intake    • Dynamic Role Dashboards   │
               └───────────────────────────┬────────────────────────────┘
                                           │ (Reverse Proxy /api/*)
                                           ▼
┌─────────────────────────┐    ┌────────────────────────────────────────┐
│ Streamlit Admin Desk    │───▶│    FastAPI Backend Service (Render)     │
│ • State Analytics       │    │   • JWT Auth & Argon2 Hashing          │
│ • Company Verifications │    │   • Deterministic Eligibility Engine   │
│ • Claim Scrutiny        │    │   • LangGraph RAG Agent                │
└─────────────────────────┘    └───────────────────┬────────────────────┘
                                                   │
                        ┌──────────────────────────┴──────────────────────────┐
                        ▼                                                     ▼
         ┌──────────────────────────────┐                      ┌──────────────────────────────┐
         │ PostgreSQL Instance (Render) │                      │      Groq Inference Engine   │
         │ • Users & RBAC               │                      │   • Llama-3.3-70B-Versatile  │
         │ • Applications & Stages      │                      │   • Sub-second latency       │
         └──────────────────────────────┘                      └──────────────────────────────┘
