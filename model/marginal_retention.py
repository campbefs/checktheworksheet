"""Marginal retention: of the NEXT dollar the payor earns, how much does he keep?

Uses the transcribed worksheet (worksheet.py) and the verified tax model (net_position.py)
at the submission's fact pattern. Increments payor gross by STEP and measures the change in
what he keeps after federal/state/payroll tax and the resulting order. Recipient income,
children, premiums and any claimed child care are held fixed.

Run: .venv/bin/python model/marginal_retention.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net_position as npos  # noqa: E402
import worksheet as w  # noqa: E402

RECIP_WEEKLY = 570.0
RECIP_GROSS = RECIP_WEEKLY * 52.0
KIDS, KIDS_UNDER_13 = 3, 2
STEP = 10_000.0


def keep(payor_gross, cc_total_wk, box=1):
    per = cc_total_wk / 3.0
    r = w.run(box=box, a_gross=RECIP_WEEKLY, b_gross=payor_gross / 52.0, children_under18=KIDS,
              a_health=33.0, b_health=43.0, a_childcare=(per, per, per), b_childcare=(0, 0, 0))
    p = npos.analyze(payor_gross, RECIP_GROSS, KIDS, r["7d"], cc_total_wk, 0.0, kids_under_13=KIDS_UNDER_13)
    k = [v for kname, v in p.items() if "payor" in kname and ("keep" in kname or "spend" in kname or "after" in kname)]
    if not k:
        raise SystemExit(f"could not find payor keep key in {sorted(p)}")
    return r["7d"] * 52.0, k[0]


def main():
    print("Marginal retention on the next $%s of payor gross (recipient $570/wk, 3 children, Box 1 shared)\n" % f"{STEP:,.0f}")
    print(f"{'payor gross':>12} {'child care/wk':>13} {'order/yr':>10} {'keeps/yr':>10} | {'marginal order':>14} {'marginal tax':>12} {'KEEPS of next $1':>16}")
    for cc in (0.0, 300.0):
        for g in (150_000.0, 201_000.0, 250_000.0, 300_000.0):
            o0, k0 = keep(g, cc); o1, k1 = keep(g + STEP, cc)
            d_order = (o1 - o0) / STEP
            d_keep = (k1 - k0) / STEP
            d_tax = 1.0 - d_order - d_keep
            print(f"{g:>12,.0f} {cc:>13,.0f} {o0:>10,.0f} {k0:>10,.0f} | {d_order:>13.1%} {d_tax:>12.1%} {d_keep:>15.1%}")
        print()
    print("Reading: at each row, of one more dollar earned, 'marginal order' goes to the order, 'marginal tax' to")
    print("federal, state and payroll tax, and the remainder is what the payor keeps. Average retention at $201,000")
    print("with $300/wk child care is keeps/yr divided by gross.")


if __name__ == "__main__":
    main()
