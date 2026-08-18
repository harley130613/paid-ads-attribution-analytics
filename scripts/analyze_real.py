"""
Analysis of REAL BUTL data exported from MMP (Airbridge), 01/06/2026 - 17/08/2026.

IMPORTANT — data handling:
  - Raw CSVs live in real_data/ (private, real company data — NOT included in the
    public GitHub package).
  - This script writes TWO outputs:
      output/real_summary_private.json  -> full real numbers (VND), for Loan's own
                                            reference only, never published.
      output/real_summary_public.json   -> anonymized version (revenue/cost turned
                                            into % share / index, never raw VND) —
                                            this is what the public dashboard reads.
"""
import json
import pandas as pd
import numpy as np

RD = "/home/claude/marketing_attribution_project/real_data"
OUT = "/home/claude/marketing_attribution_project/output"

TEST_CHANNELS = {"ooh"}  # keep everything except obvious SDK test noise (filtered below)

# ---------- load ----------
install = pd.read_csv(f"{RD}/daily_install_os_channel.csv")
revenue = pd.read_csv(f"{RD}/daily_revenue.csv")
fraud = pd.read_csv(f"{RD}/fraud_touchpoint.csv")
events = pd.read_csv(f"{RD}/total_event_traffic.csv")

install.columns = [c.strip() for c in install.columns]
revenue.columns = [c.strip() for c in revenue.columns]
fraud.columns = [c.strip() for c in fraud.columns]
events.columns = [c.strip() for c in events.columns]

# drop internal SDK test rows
fraud = fraud[~fraud["Channel"].astype(str).str.startswith("airbridge_sdk_test")]
install = install[~install["Channel"].astype(str).str.startswith("airbridge_sdk_test")]
revenue = revenue[~revenue["Channel"].astype(str).str.startswith("airbridge_sdk_test")]

# ---------- 1. Channel install performance (clicks -> installs) ----------
install["clicks_eff"] = install[["Clicks", "Clicks (Channel)"]].max(axis=1)
by_channel_install = install.groupby("Channel", as_index=False).agg(
    clicks=("clicks_eff", "sum"),
    installs=("Installs (App)", "sum"),
    install_users=("Install Users (App)", "sum"),
)
by_channel_install["install_rate"] = by_channel_install["installs"] / by_channel_install["clicks"].replace(0, np.nan)
by_channel_install = by_channel_install.sort_values("installs", ascending=False)

# OS split
by_os = install.groupby("OS Name", as_index=False).agg(installs=("Installs (App)", "sum"))
by_os = by_os[by_os["OS Name"].notna() & (by_os["OS Name"] != "")]
by_os["share_pct"] = by_os["installs"] / by_os["installs"].sum() * 100
by_os = by_os.sort_values("installs", ascending=False)

# ---------- 2. Channel revenue / cost economics ----------
by_channel_rev = revenue.groupby("Channel", as_index=False).agg(
    orders=("Order Complete (App)", "sum"),
    order_users=("Order Complete Users (App)", "sum"),
    revenue_vnd=("Revenue (App)", "sum"),
    cost_vnd=("Cost (Channel)", "sum"),
)
by_channel_rev["roas"] = by_channel_rev["revenue_vnd"] / by_channel_rev["cost_vnd"].replace(0, np.nan)
by_channel_rev["cac_vnd"] = by_channel_rev["cost_vnd"] / by_channel_rev["order_users"].replace(0, np.nan)
by_channel_rev["arppu_vnd"] = by_channel_rev["revenue_vnd"] / by_channel_rev["order_users"].replace(0, np.nan)
by_channel_rev = by_channel_rev.sort_values("cost_vnd", ascending=False)

# only paid channels have meaningful CAC/ROAS (organic/unattributed has ~0 cost)
paid_mask = ~by_channel_rev["Channel"].isin(["unattributed", "referral", "qr", "fanpage.facebook", "tiktok.video"])
paid_rev = by_channel_rev[paid_mask & (by_channel_rev["cost_vnd"] > 0)].copy()

# ---------- 3. Fraud / re-install quality ----------
fraud["reinstall_rate_pct"] = fraud["Re-installs (App)"] / fraud["Installs (App)"].replace(0, np.nan) * 100
fraud_sorted = fraud.sort_values("Installs (App)", ascending=False)

# ---------- 4. App-wide product activity (aggregate events) ----------
# NOTE: these are period-level EVENT TOTALS, not a single-cohort funnel — "Sign-up"
# only counts NEW registrations in the window while "Order Complete" includes orders
# from both new and pre-existing users, so events don't strictly nest (e.g. Order
# Complete > Sign-up is expected, not a funnel "leak"). Reported as activity VOLUME,
# not as sequential conversion %, to avoid implying a cohort funnel the data can't support.
ev = events.set_index("Event Category")["Events (App)"].to_dict()
activity_steps = [
    ("Install", ev.get("Install (App)", 0)),
    ("Sign-up (mới trong kỳ)", ev.get("Sign-up (App)", 0)),
    ("Product View", ev.get("Product View (App)", 0)),
    ("Xem báo giá", ev.get("price_estimate_viewed (App)", 0)),
    ("Initiate Checkout", ev.get("Initiate Checkout (App)", 0)),
    ("Order Complete", ev.get("Order Complete (App)", 0)),
]
funnel = [{"step": name, "events": int(val)} for name, val in activity_steps]

no_driver_found = int(ev.get("no_driver_found (App)", 0))
order_cancel = int(ev.get("Order Cancel (App)", 0))
order_complete = int(ev.get("Order Complete (App)", 0))
voucher_applied = int(ev.get("voucher_applied (App)", 0))
voucher_viewed = int(ev.get("voucher_viewed (App)", 0))

# ---------- print (private / for CV drafting) ----------
print("=" * 70)
print("CHANNEL INSTALL PERFORMANCE (clicks -> installs)")
print(by_channel_install.to_string(index=False))
print("\nOS SPLIT")
print(by_os.to_string(index=False))
print("\nCHANNEL REVENUE/COST (real VND — PRIVATE, do not publish raw)")
print(by_channel_rev.to_string(index=False))
print("\nFRAUD / RE-INSTALL RATE BY CHANNEL")
print(fraud_sorted.to_string(index=False))
print("\nAPP FUNNEL")
for s in funnel:
    print(s)
print(f"\nno_driver_found: {no_driver_found} | order_cancel: {order_cancel} | order_complete: {order_complete}")
print(f"voucher_applied: {voucher_applied} | voucher_viewed: {voucher_viewed} | apply_rate: {voucher_applied/voucher_viewed*100:.1f}%")

total_cost = by_channel_rev["cost_vnd"].sum()
total_revenue = by_channel_rev["revenue_vnd"].sum()
paid_cost = paid_rev["cost_vnd"].sum()
paid_revenue = paid_rev["revenue_vnd"].sum()
print(f"\nTotal cost (all channels, 78 days): {total_cost:,.0f} VND")
print(f"Total revenue (all channels, 78 days): {total_revenue:,.0f} VND")
print(f"Blended ROAS (bao gồm unattributed, cost=0 -> không phản ánh đúng hiệu quả paid): {total_revenue/total_cost:.2f}x")
print(f"Paid-only ROAS (chỉ 4 kênh có chi phí): {paid_revenue/paid_cost:.2f}x")
print(f"Paid channels' share of total installs: {by_channel_install[by_channel_install['Channel'].isin(paid_rev['Channel'])]['installs'].sum() / by_channel_install['installs'].sum() * 100:.1f}%")

best_roas = paid_rev.iloc[paid_rev["roas"].argmax()]
worst_roas = paid_rev.iloc[paid_rev["roas"].argmin()]
print(f"\nBest ROAS (paid): {best_roas['Channel']} — {best_roas['roas']:.2f}x")
print(f"Worst ROAS (paid): {worst_roas['Channel']} — {worst_roas['roas']:.2f}x")

# ---------- private json (real numbers, for Loan's own reference — NOT for GitHub) ----------
private_out = {
    "period": "2026-06-01 to 2026-08-17 (78 days)",
    "by_channel_install": by_channel_install.round(4).to_dict(orient="records"),
    "by_os": by_os.round(2).to_dict(orient="records"),
    "by_channel_revenue_REAL_VND": by_channel_rev.round(2).to_dict(orient="records"),
    "fraud": fraud_sorted.round(2).to_dict(orient="records"),
    "funnel": funnel,
    "totals": {
        "total_cost_vnd": float(total_cost),
        "total_revenue_vnd": float(total_revenue),
        "blended_roas": float(total_revenue / total_cost),
    },
}
with open(f"{OUT}/real_summary_private.json", "w", encoding="utf-8") as f:
    json.dump(private_out, f, ensure_ascii=False, indent=2)

# ---------- public json (ANONYMIZED — revenue/cost as % share + index, no raw VND) ----------
pub_channel_rev = paid_rev.copy()
pub_channel_rev["cost_share_pct"] = pub_channel_rev["cost_vnd"] / pub_channel_rev["cost_vnd"].sum() * 100
pub_channel_rev["revenue_share_pct"] = pub_channel_rev["revenue_vnd"] / pub_channel_rev["revenue_vnd"].sum() * 100
# CAC index: blended average paid CAC = 100
blended_cac = pub_channel_rev["cost_vnd"].sum() / pub_channel_rev["order_users"].sum()
pub_channel_rev["cac_index"] = pub_channel_rev["cac_vnd"] / blended_cac * 100
pub_channel_rev = pub_channel_rev[["Channel", "orders", "order_users", "roas", "cac_index", "cost_share_pct", "revenue_share_pct"]]

pub_install = by_channel_install[["Channel", "clicks", "installs", "install_rate"]].copy()
pub_install["install_share_pct"] = pub_install["installs"] / pub_install["installs"].sum() * 100

public_out = {
    "period": "2026-06-01 to 2026-08-17 (78 ngày)",
    "note": "Dữ liệu THẬT từ MMP Airbridge (BUTL) — chỉ số tài chính (revenue/cost/CAC) đã được ẨN DANH HÓA thành % / index để bảo mật số liệu kinh doanh; ROAS là tỷ lệ (revenue/cost) nên giữ nguyên vì không lộ giá trị tuyệt đối.",
    "by_channel_install": json.loads(pub_install.round(4).to_json(orient="records")),
    "by_os": by_os.round(2).to_dict(orient="records"),
    "by_channel_economics_anonymized": json.loads(pub_channel_rev.round(2).to_json(orient="records")),
    "fraud": fraud_sorted[["Channel", "Installs (App)", "reinstall_rate_pct"]].round(2).to_dict(orient="records"),
    "funnel": funnel,
    "voucher": {
        "voucher_viewed": voucher_viewed,
        "voucher_applied": voucher_applied,
        "apply_rate_pct": round(voucher_applied / voucher_viewed * 100, 1),
    },
    "ops": {
        "no_driver_found": no_driver_found,
        "order_cancel": order_cancel,
        "order_complete": order_complete,
        "cancel_rate_pct": round(order_cancel / (order_complete + order_cancel) * 100, 1),
    },
    "blended_roas_all_channels": float(total_revenue / total_cost),
    "paid_only_roas": float(paid_revenue / paid_cost),
    "paid_installs_share_pct": float(by_channel_install[by_channel_install["Channel"].isin(paid_rev["Channel"])]["installs"].sum() / by_channel_install["installs"].sum() * 100),
}
with open(f"{OUT}/real_summary_public.json", "w", encoding="utf-8") as f:
    json.dump(public_out, f, ensure_ascii=False, indent=2)

print("\nSaved output/real_summary_private.json (real VND, keep private)")
print("Saved output/real_summary_public.json (anonymized, safe for GitHub/dashboard)")
