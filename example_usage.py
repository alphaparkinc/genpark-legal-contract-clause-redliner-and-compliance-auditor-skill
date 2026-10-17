"""Example usage for Legal Contract Clause Redliner & Compliance Auditor."""
from client import ContractClauseAuditor

if __name__ == "__main__":
    risky_clause = (
        "In no event shall Vendor have any limitation of liability for breaches. "
        "Customer shall not be liable for fees."
    )

    res = ContractClauseAuditor.audit_liability_clause(risky_clause, annual_contract_value=150000.0)
    print("Liability Audit Compliant:", res["compliant"])
    print("Risk Level:", res["overall_risk"])
    for f in res["findings"]:
        print(f"  - [{f['severity']}] {f['issue']}: {f['detail']}")
        print(f"    Redline: {f['redline_suggestion']}")
