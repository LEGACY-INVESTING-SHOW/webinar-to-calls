"""Recurring example calculations for Roadmap 2.0 new content.

Every number here is an ASSUMPTION for teaching. Run:
    python3 tools/examples.py            # prints all tables
    python3 tools/examples.py --json     # machine-readable, used by QA
"""
import json, sys

def pmt(principal, annual_rate, years=30):
    r = annual_rate / 12
    n = years * 12
    return principal * r / (1 - (1 + r) ** -n)

def balance_after(principal, annual_rate, months, years=30):
    r = annual_rate / 12
    p = pmt(principal, annual_rate, years)
    return principal * (1 + r) ** months - p * ((1 + r) ** months - 1) / r

# ---------------------------------------------------------------- ARBITRAGE
ARB = dict(
    name="Alder Street unit (hypothetical)",
    rent_month=1950, adr=205, occupancy=0.70, avg_stay=3.0,
    cleaning_fee_charged=110, cleaner_cost=95, platform_fee=0.155,
    utilities_month=260, supplies_per_stay=14, insurance_year=1300,
    software_month=90, maintenance_month=120, permit_year=250,
)

def arb_model(a, adr=None, occ=None, rent=None, mgmt_pct=0.0):
    adr = a["adr"] if adr is None else adr
    occ = a["occupancy"] if occ is None else occ
    rent = a["rent_month"] if rent is None else rent
    nights = round(365 * occ)
    stays = round(nights / a["avg_stay"])
    nightly = nights * adr
    clean_in = stays * a["cleaning_fee_charged"]
    gross = nightly + clean_in
    fee = round(gross * a["platform_fee"])
    lines = {
        "Platform service fee (15.5% of nightly + cleaning)": fee,
        "Cleaner pay": stays * a["cleaner_cost"],
        "Utilities and internet": a["utilities_month"] * 12,
        "Supplies and consumables": stays * a["supplies_per_stay"],
        "STR liability insurance": a["insurance_year"],
        "Software (PMS, pricing, lock)": a["software_month"] * 12,
        "Repairs and replacement reserve": a["maintenance_month"] * 12,
        "Permit / registration": a["permit_year"],
    }
    if mgmt_pct:
        lines["Local manager fee"] = round(gross * mgmt_pct)
    lines["Rent"] = rent * 12
    total = sum(lines.values())
    return dict(adr=adr, occupancy=occ, nights=nights, stays=stays, nightly=nightly,
                cleaning_income=clean_in, gross=gross, lines=lines, total=total,
                net=gross - total, net_month=round((gross - total) / 12),
                rent_multiple=round(gross / (rent * 12), 2))

def arb_breakeven(a, adr=None, rent=None):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        # continuous version for break-even
        adr_ = a["adr"] if adr is None else adr
        rent_ = a["rent_month"] if rent is None else rent
        nights = 365 * mid
        stays = nights / a["avg_stay"]
        gross = nights * adr_ + stays * a["cleaning_fee_charged"]
        var = gross * a["platform_fee"] + stays * (a["cleaner_cost"] + a["supplies_per_stay"])
        fixed = (a["utilities_month"] + a["software_month"] + a["maintenance_month"] + rent_) * 12 + a["insurance_year"] + a["permit_year"]
        if gross - var - fixed > 0: hi = mid
        else: lo = mid
    return round(hi, 3)

# Sunk setup costs (money spent that you do not get back)
ARB_STARTUP = {
    "Furniture and decor": 9500,
    "Linens, kitchen, starter supplies": 1400,
    "Safety equipment (alarms, extinguisher, first aid, lock)": 450,
    "Professional photos": 450,
    "Permit / registration application": 250,
}
# Cash tied up but not spent
ARB_CASH_TIED = {
    "Security deposit (1 month, refundable if terms are met)": 1950,
    "First month's rent (prepaid operating cost)": 1950,
    "Operating reserve (2 months rent + utilities)": 2 * (1950 + 260),
}

# ---------------------------------------------------------------- OWNERSHIP
OWN = dict(
    name="Cedar Ridge house (hypothetical)",
    price=385000, down_pct=0.25, adr=300, occupancy=0.58, avg_stay=3.5,
    cleaning_fee_charged=175, cleaner_cost=150, platform_fee=0.155,
    tax_year=3850, insurance_year=3200, utilities_month=450, software_month=100,
    supplies_per_stay=25, maint_pct=0.05, capex_pct=0.05, cohost_pct=0.18, oncall_month=150,
    furnishing=32000, closing_cost_pct=0.03,
    dscr_rate=0.0725, dscr_points=0.01, conv_rate=0.06875, conv_points=0.0,
)

def own_ops(o, adr=None, occ=None, cohost=False):
    adr = o["adr"] if adr is None else adr
    occ = o["occupancy"] if occ is None else occ
    nights = round(365 * occ)
    stays = round(nights / o["avg_stay"])
    gross = nights * adr + stays * o["cleaning_fee_charged"]
    lines = {
        "Platform service fee (15.5%)": round(gross * o["platform_fee"]),
        "On-call handyman / inspection retainer": o["oncall_month"] * 12,
        "Cleaner pay": stays * o["cleaner_cost"],
        "Utilities, internet, trash": o["utilities_month"] * 12,
        "Supplies": stays * o["supplies_per_stay"],
        "Software": o["software_month"] * 12,
        "Repairs and maintenance (5%)": round(gross * o["maint_pct"]),
        "Capital reserve (5%)": round(gross * o["capex_pct"]),
        "Property tax": o["tax_year"],
        "STR insurance": o["insurance_year"],
    }
    if cohost:
        lines["Local co-host (18% of booking revenue)"] = round(gross * o["cohost_pct"])
    opex = sum(lines.values())
    return dict(adr=adr, occupancy=occ, nights=nights, stays=stays, gross=gross,
                lines=lines, opex=opex, noi=gross - opex)

def own_finance(o, rate, points, down_pct=None):
    down_pct = o["down_pct"] if down_pct is None else down_pct
    loan = round(o["price"] * (1 - down_pct))
    down = o["price"] - loan
    pi = pmt(loan, rate)
    closing = round(o["price"] * o["closing_cost_pct"]) + round(loan * points)
    ti_month = (o["tax_year"] + o["insurance_year"]) / 12
    pitia = pi + ti_month
    return dict(loan=loan, down=down, rate=rate, points=points, pi=round(pi), pitia=round(pitia),
                debt_service_year=round(pi * 12), closing=closing,
                principal_paid_y1=round(loan - balance_after(loan, rate, 12)))

def main():
    out = {}
    base = arb_model(ARB)
    stress = arb_model(ARB, adr=round(ARB["adr"] * 0.88), occ=0.60)
    rent_up = arb_model(ARB, rent=2150)
    mgr = arb_model(ARB, mgmt_pct=0.20)
    startup = sum(ARB_STARTUP.values())
    out["arb"] = dict(base=base, stress=stress, rent_up=rent_up, with_manager_20=mgr,
                      breakeven_occ=arb_breakeven(ARB),
                      breakeven_occ_stress_adr=arb_breakeven(ARB, adr=round(ARB["adr"] * 0.88)),
                      startup=ARB_STARTUP, startup_total=startup,
                      cash_tied=ARB_CASH_TIED, cash_tied_total=sum(ARB_CASH_TIED.values()),
                      cash_needed_total=startup + sum(ARB_CASH_TIED.values()),
                      payback_months=round(startup / base["net_month"], 1))
    ob = own_ops(OWN); ow = own_ops(OWN, adr=265, occ=0.50); oc = own_ops(OWN, cohost=True)
    dscr = own_finance(OWN, OWN["dscr_rate"], OWN["dscr_points"])
    conv = own_finance(OWN, OWN["conv_rate"], OWN["conv_points"])
    for tag, f in (("dscr", dscr), ("conv", conv)):
        # NOI here already includes tax+insurance, so cash flow = NOI - P&I
        f["cash_flow_base"] = ob["noi"] - f["debt_service_year"]
        f["cash_flow_weak"] = ow["noi"] - f["debt_service_year"]
        f["cash_flow_with_cohost"] = oc["noi"] - f["debt_service_year"]
        f["cash_to_close"] = f["down"] + f["closing"]
        f["total_cash_in"] = f["cash_to_close"] + OWN["furnishing"]
    # Lender-style gross-rent DSCR (one common definition): gross rents / PITIA
    gross_dscr_base = round(ob["gross"] / (dscr["pitia"] * 12), 2)
    gross_dscr_weak = round(ow["gross"] / (dscr["pitia"] * 12), 2)
    # Lender haircut: many lenders discount projected STR income (assume 80%)
    haircut_dscr = round(ob["gross"] * 0.80 / (dscr["pitia"] * 12), 2)
    # NOI-based coverage (investor view): NOI before tax/ins / PITIA
    noi_before_ti = ob["noi"] + OWN["tax_year"] + OWN["insurance_year"]
    noi_dscr = round(noi_before_ti / (dscr["pitia"] * 12), 2)
    for f in (dscr, conv):
        f["cash_on_cash_base"] = round(f["cash_flow_base"] / f["total_cash_in"], 3)
    out["own"] = dict(base=ob, weak=ow, with_cohost=oc, dscr=dscr, conv=conv,
                      gross_dscr_base=gross_dscr_base, gross_dscr_weak=gross_dscr_weak,
                      haircut_dscr_base=haircut_dscr, noi_dscr_base=noi_dscr)
    # Depreciation illustration
    closing_basis = 6000  # capitalized acquisition costs, assumption
    land_pct = 0.20
    basis = OWN["price"] + closing_basis
    land = round(basis * land_pct)
    bldg = basis - land
    sl_39 = round(bldg / 39); sl_275 = round(bldg / 27.5)
    short_life_pct = 0.22  # cost seg reclass share, assumption
    short_life = round(bldg * short_life_pct)
    remaining = bldg - short_life
    yr1_bonus = short_life + OWN["furnishing"]  # if eligible for 100% bonus
    rem_39_first_year_fraction = 0.5  # simplify; real mid-month convention depends on month placed in service
    out["tax"] = dict(basis=basis, land=land, building=bldg, sl_39=sl_39, sl_275=sl_275,
                      short_life=short_life, furnishing=OWN["furnishing"],
                      bonus_year1=yr1_bonus, remaining_building=remaining,
                      remaining_39_full_year=round(remaining / 39),
                      illustrative_rate=0.32,
                      illustrative_tax_effect=round((yr1_bonus + remaining / 39) * 0.32))
    # Refinance after year 2 and exit after year 5
    val2 = round(OWN["price"] * 1.03 ** 2); val5 = round(OWN["price"] * 1.03 ** 5)
    bal2 = round(balance_after(dscr["loan"], OWN["dscr_rate"], 24))
    bal5 = round(balance_after(dscr["loan"], OWN["dscr_rate"], 60))
    new_loan = round(val2 * 0.75)
    refi_cost = round(new_loan * 0.025)
    cash_out = new_loan - bal2 - refi_cost
    new_pi = pmt(new_loan, 0.07)
    new_pitia = new_pi + (OWN["tax_year"] + OWN["insurance_year"]) / 12
    out["refi"] = dict(value_y2=val2, balance_y2=bal2, new_loan_75=new_loan, refi_cost=refi_cost,
                       cash_out=cash_out, new_rate=0.07, new_pi=round(new_pi), new_pitia=round(new_pitia),
                       cash_flow_after=round(ob["noi"] - new_pi * 12),
                       cash_flow_after_weak=round(ow["noi"] - new_pi * 12),
                       gross_dscr_after=round(ob["gross"] / (new_pitia * 12), 2))
    sale_cost = round(val5 * 0.07)
    out["exit"] = dict(value_y5=val5, balance_y5=bal5, sale_costs_7pct=sale_cost,
                       net_before_tax=val5 - bal5 - sale_cost)
    return out

if __name__ == "__main__":
    r = main()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1)); sys.exit()
    print(json.dumps(r, indent=1))
