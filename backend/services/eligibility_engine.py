import os
import json
from typing import List, Dict, Any

class EligibilityEngine:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_path = os.path.join(base_dir, "data", "schemes_karnataka.json")

    def load_schemes(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.data_path):
            return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate(self, company) -> List[Dict[str, Any]]:
        schemes = self.load_schemes()
        results = []

        for s in schemes:
            if company.sector not in s.get("target_sector", []):
                continue
            if company.turnover_lakhs > s.get("max_turnover_lakhs", 999999):
                continue
            if s.get("level") == "State" and s.get("state") != company.state:
                continue

            incentives = s.get("incentive_structure", {})
            zone_info = incentives.get(company.zone, incentives.get("All Zones", {"percentage": 0, "cap_lakhs": 0}))
            
            pct = zone_info.get("percentage", 0.0)
            cap = zone_info.get("cap_lakhs", 0.0)

            calculated = round((pct / 100.0) * company.plant_machinery_inv_lakhs, 2)
            final_val = min(calculated, cap) if cap > 0 else calculated

            results.append({
                "code": s["id"],
                "name": s["name"],
                "level": s["level"],
                "authority": s["authority"],
                "percentage": pct,
                "calculated_amount_lakhs": final_val,
                "max_cap": cap,
                "documents_required": s.get("documents_required", []),
                "portal": s.get("portal_url", "#")
            })
        return results

eligibility_engine = EligibilityEngine()
