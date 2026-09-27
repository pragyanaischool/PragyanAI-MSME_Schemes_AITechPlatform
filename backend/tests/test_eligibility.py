import pytest
from services.eligibility_engine import eligibility_engine

class MockCompany:
    def __init__(self, sector, turnover, machinery, zone, state="Karnataka"):
        self.sector = sector
        self.turnover_lakhs = turnover
        self.plant_machinery_inv_lakhs = machinery
        self.zone = zone
        self.state = state

def test_karnataka_zone2_manufacturing_subsidy():
    company = MockCompany(
        sector="Manufacturing",
        turnover=50.0,
        machinery=30.0,
        zone="Zone 2 (Developing)"
    )
    matches = eligibility_engine.evaluate(company)
    assert len(matches) >= 2

    ka_scheme = next((m for m in matches if m["code"] == "KA-IPS-2025"), None)
    assert ka_scheme is not None
    assert ka_scheme["percentage"] == 25.0
    # 25% of 30.0 Lakhs = 7.5 Lakhs
    assert ka_scheme["calculated_amount_lakhs"] == 7.5

def test_zone3_no_capital_subsidy():
    company = MockCompany(
        sector="Manufacturing",
        turnover=50.0,
        machinery=30.0,
        zone="Zone 3 (Urbanized)"
    )
    matches = eligibility_engine.evaluate(company)
    ka_scheme = next((m for m in matches if m["code"] == "KA-IPS-2025"), None)
    assert ka_scheme is not None
    assert ka_scheme["percentage"] == 0.0
    assert ka_scheme["calculated_amount_lakhs"] == 0.0
