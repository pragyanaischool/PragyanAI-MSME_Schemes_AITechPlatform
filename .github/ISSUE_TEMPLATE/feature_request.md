```markdown
---
name: Feature Request / Scheme Proposal
about: Suggest a new feature, platform enhancement, or new Central/State subsidy policy integration.
title: "[FEAT] "
labels: ["enhancement", "proposal"]
assignees: ""
---

## 💡 Feature Overview
Provide a clear and concise summary of the proposed enhancement, new scheme integration, or architectural upgrade.

---

## 👥 Target Stakeholder & Role
Select who benefits from this capability:

- [ ] **MSME Applicant** (Simplified questionnaire, document validation, roadmap tracking)
- [ ] **Nodal Entity / Policy Creator** (SIDBI, KVIC, commercial banks publishing custom schemes)
- [ ] **Government Administrator** (DIC Joint Directors, verification officers, sanction committee)
- [ ] **Developer / DevOps** (Performance, RAG indexing efficiency, automated testing)

---

## 🏛️ Policy & Regulatory Grounding
If this proposal integrates a new state or central scheme:
* **Scheme Title:** `[e.g., Karnataka Electric Vehicle & Clean Mobility Incentive Policy]`
* **Governing Body:** `[e.g., Department of Commerce & Industries / Ministry of Heavy Industries]`
* **Official Circular / Portal URL:** `[e.g., https://kum.karnataka.gov.in/...]`
* **Incentive Type:** `[e.g., Capital Subsidy / Interest Subvention / Stamp Duty Exemption]`

---

## 📐 Technical Architecture Proposal
Outline the intended implementation details across the decoupled platform:

### 1. Database Schema Impact
- [ ] Requires Alembic migration
- [ ] New model or table addition
- [ ] JSONB schema update (`schemes.required_documents` or `applications.attached_documents`)

```sql
-- Optional: Draft DDL or column updates here
