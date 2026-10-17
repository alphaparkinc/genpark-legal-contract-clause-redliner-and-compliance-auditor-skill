"""MCP server for Legal Contract Clause Redliner & Compliance Auditor."""
import sys
import json
from client import ContractClauseAuditor


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "audit_liability_clause",
                    "description": "Scans limitation of liability clauses for uncapped liability, excessive multipliers, and missing consequential waivers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "clause_text": {"type": "string"},
                            "annual_contract_value": {"type": "number", "default": 100000.0},
                        },
                        "required": ["clause_text"],
                    },
                },
                {
                    "name": "audit_indemnification_clause",
                    "description": "Evaluates indemnification clauses for over-broad general breach obligations and unilateral risks",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "clause_text": {"type": "string"},
                        },
                        "required": ["clause_text"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "audit_liability_clause":
            res = ContractClauseAuditor.audit_liability_clause(
                args.get("clause_text", ""),
                annual_contract_value=args.get("annual_contract_value", 100000.0),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "audit_indemnification_clause":
            res = ContractClauseAuditor.audit_indemnification_clause(
                args.get("clause_text", "")
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
