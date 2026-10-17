"""Legal Contract Clause Redliner and Compliance Auditor.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import re


class ContractClauseAuditor:
    """Audits contract clauses against standard corporate legal playbooks,
    flags liability and indemnity risks, and generates automated redline recommendations."""

    STANDARD_PLAYBOOK = {
        "limitation_of_liability": {
            "acceptable_cap_multipliers": [1.0, 1.5, 2.0],
            "required_consequential_waiver": True,
            "banned_phrases": ["unlimited liability", "no limitation of liability"],
        },
        "indemnification": {
            "allowed_scopes": ["third_party_ip_infringement", "gross_negligence"],
            "banned_scopes": ["breach_of_contract_general", "indirect_damages"],
        },
        "governing_law": {
            "preferred_jurisdictions": ["delaware", "new york", "california", "england and wales"],
        },
    }

    @classmethod
    def audit_liability_clause(cls, clause_text: str, annual_contract_value: float = 100000.0) -> Dict[str, Any]:
        """Scans limitation of liability clauses for uncapped liability and missing waivers."""
        text_lower = clause_text.lower()
        findings = []
        risk_level = "LOW"

        # Check for banned unlimited liability
        if any(phrase in text_lower for phrase in cls.STANDARD_PLAYBOOK["limitation_of_liability"]["banned_phrases"]):
            risk_level = "CRITICAL"
            findings.append({
                "issue": "UNCAPPED_LIABILITY",
                "severity": "CRITICAL",
                "detail": "Clause appears to waive limitation of liability caps completely.",
                "redline_suggestion": f"Replace with: 'Each party's total aggregate liability shall not exceed the amounts paid in the preceding 12 months (${annual_contract_value:,.2f}).'",
            })

        # Check for consequential damages waiver
        has_consequential_waiver = any(w in text_lower for w in ["consequential", "indirect", "punitive", "special damages"])
        if not has_consequential_waiver:
            if risk_level != "CRITICAL":
                risk_level = "HIGH"
            findings.append({
                "issue": "MISSING_CONSEQUENTIAL_DAMAGES_WAIVER",
                "severity": "HIGH",
                "detail": "No mutual waiver of indirect, special, or consequential damages detected.",
                "redline_suggestion": "Add: 'Neither party shall be liable for any indirect, incidental, special, or consequential damages.'",
            })

        # Check liability cap multiplier
        cap_match = re.search(r'(\d+)\s*(?:x|times)\s*(?:the\s+)?(?:fees|amounts paid)', text_lower)
        if cap_match:
            multiplier = float(cap_match.group(1))
            if multiplier > 2.0:
                if risk_level not in ["CRITICAL", "HIGH"]:
                    risk_level = "MEDIUM"
                findings.append({
                    "issue": "EXCESSIVE_LIABILITY_CAP",
                    "severity": "MEDIUM",
                    "detail": f"Liability cap is {multiplier}x annual fees, exceeding standard 2x playbook ceiling.",
                    "redline_suggestion": "Counter with standard 1x or 2x annual fee cap.",
                })

        compliant = len(findings) == 0
        return {
            "clause_type": "limitation_of_liability",
            "compliant": compliant,
            "overall_risk": risk_level if not compliant else "LOW",
            "findings": findings,
            "annual_contract_value": annual_contract_value,
        }

    @classmethod
    def audit_indemnification_clause(cls, clause_text: str) -> Dict[str, Any]:
        """Evaluates indemnification scope against broad general breach exposure."""
        text_lower = clause_text.lower()
        findings = []
        risk_level = "LOW"

        # Check for broad general breach indemnity
        if "any and all breaches" in text_lower or "breach of any representation" in text_lower:
            risk_level = "HIGH"
            findings.append({
                "issue": "OVERLY_BROAD_INDEMNITY",
                "severity": "HIGH",
                "detail": "Indemnity covers general contract breach rather than narrow 3rd-party IP infringement.",
                "redline_suggestion": "Limit indemnification exclusively to third-party claims alleging direct infringement of intellectual property.",
            })

        # Check for unilateral vs mutual
        if "vendor shall indemnify" in text_lower and "customer shall indemnify" not in text_lower:
            findings.append({
                "issue": "UNILATERAL_INDEMNIFICATION",
                "severity": "MEDIUM",
                "detail": "Indemnification obligation is one-sided.",
                "redline_suggestion": "Ensure mutual indemnification for customer content and acceptable use.",
            })

        compliant = len(findings) == 0
        return {
            "clause_type": "indemnification",
            "compliant": compliant,
            "overall_risk": risk_level if not compliant else "LOW",
            "findings": findings,
        }
