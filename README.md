# genpark-legal-contract-clause-redliner-and-compliance-auditor-skill

Contract clause deviation detector, indemnity risk scorer, and automated redlining auditor for enterprise legal workflows.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Limitation of Liability Auditing**: Detects uncapped liabilities, excessive cap multipliers, and missing mutual waivers of indirect/consequential damages.
- **Indemnification Scope Governance**: Flags over-broad representations and unilateral indemnity obligations, producing targeted contract redlines.
- **Enterprise Legal Playbook Integration**: Automatically suggests compliant substitute language based on standard corporate risk tolerances.

## Architecture

```
[Contract Clause (Liability / Indemnity / Jurisdiction)]
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│              ContractClauseAuditor                  │
│  - Playbook Rule Evaluator                          │
│  - Liability Cap & Waiver Scanner                   │
│  - Broad Breach Indemnity Detector                  │
└─────────────────────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
[Compliance Assessment]         [Actionable Redlines]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `audit_liability_clause`: Scans limitation of liability clauses for uncapped liability, excessive multipliers, and missing consequential waivers.
- `audit_indemnification_clause`: Evaluates indemnification clauses for over-broad general breach obligations and unilateral risks.

## Quickstart (Python API)

```python
from client import ContractClauseAuditor

clause = "Vendor shall have unlimited liability for any breach of this agreement."
res = ContractClauseAuditor.audit_liability_clause(clause, annual_contract_value=50000.0)
print("Risk:", res["overall_risk"])
print("Suggested Redline:", res["findings"][0]["redline_suggestion"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
