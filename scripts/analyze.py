"""
Analysis: market x channel performance + multi-touch attribution comparison.
Reads data/daily_performance.csv and data/touchpoints.csv, writes output/summary.json
(consumed by dashboard.html) and prints the headline numbers used in the CV project bullet.
"""
import json
import pandas as pd
import numpy as np

perf = pd.read_csv("/home/claude/marketing_attribution_project/data/daily_performance.csv")
touch = pd.read_csv("/home/claude/marketing_attribution_project/data/touchpoints.csv")

# ---------- 1. Market performance ----------
by_market = perf.groupby("market", as_index=False).agg(
    impressions=("impressions", "sum"),
    clicks=("clicks", "sum"),
    spend_vnd=("spend_vnd", "sum"),
    installs=("installs", "sum"),
    bookings=("bookings", "sum"),
)
by_market["ctr"] = by_market["clicks"] / by_market["impressions"]
by_market["cpc_vnd"] = by_market["spend_vnd"] / by_market["clicks"]
by_market["cpa_vnd"] = by_market["spend_vnd"] / by_market["bookings"]
by_market["install_to_booking"] = by_market["bookings"] / by_market["installs"]
by_market = by_market.sort_values("spend_vnd", ascending=False)

# ---------- 2. Channel performance (last-click / platform-reported) ----------
by_channel = perf.groupby("channel", as_index=False).agg(
    impressions=("impressions", "sum"),
    clicks=("clicks", "sum"),
    spend_vnd=("spend_vnd", "sum"),
    installs=("installs", "sum"),
    bookings=("bookings", "sum"),
)
by_channel["ctr"] = by_channel["clicks"] / by_channel["impressions"]
by_channel["cpc_vnd"] = by_channel["spend_vnd"] / by_channel["clicks"]
by_channel["cpa_platform_vnd"] = by_channel["spend_vnd"] / by_channel["bookings"]
by_channel = by_channel.sort_values("spend_vnd", ascending=False)

# ---------- 3. Market x Channel matrix (for heatmap) ----------
mx = perf.groupby(["market", "channel"], as_index=False).agg(
    spend_vnd=("spend_vnd", "sum"), bookings=("bookings", "sum")
)
mx["cpa_vnd"] = mx["spend_vnd"] / mx["bookings"].replace(0, np.nan)

# ---------- 4. Attribution models ----------
total_bookings = touch["user_id"].nunique()
spend_by_channel = by_channel.set_index("channel")["spend_vnd"].to_dict()

first_touch = touch[touch["is_first"]].groupby("channel")["user_id"].nunique()
last_touch = touch[touch["is_last"]].groupby("channel")["user_id"].nunique()
# linear: each touchpoint in a journey gets equal credit (1/touch_count)
touch["credit"] = 1.0 / touch["touch_count"]
linear = touch.groupby("channel")["credit"].sum()

attribution = pd.DataFrame({
    "first_touch_bookings": first_touch,
    "last_touch_bookings": last_touch,
    "linear_bookings": linear,
}).fillna(0)
attribution = attribution.reindex(CHANNELS := list(by_channel["channel"])).fillna(0)
attribution["spend_vnd"] = attribution.index.map(spend_by_channel)
for col in ["first_touch", "last_touch", "linear"]:
    attribution[f"{col}_cpa_vnd"] = attribution["spend_vnd"] / attribution[f"{col}_bookings"]
attribution = attribution.reset_index().rename(columns={"index": "channel"})

# ---------- 5. Headline diagnostics ----------
# Channels most under-valued by last-click (platform) view vs linear (fuller-funnel) view
attribution["linear_vs_last_gap_pct"] = (
    (attribution["linear_bookings"] - attribution["last_touch_bookings"])
    / attribution["last_touch_bookings"].replace(0, np.nan) * 100
)

top_market = by_market.iloc[by_market["cpa_vnd"].argmin()]
worst_market = by_market.iloc[by_market["cpa_vnd"].argmax()]
cheapest_channel_linear = attribution.iloc[attribution["linear_cpa_vnd"].argmin()]
most_undervalued = attribution.iloc[attribution["linear_vs_last_gap_pct"].argmax()]

total_spend = int(perf["spend_vnd"].sum())
total_bookings_n = int(perf["bookings"].sum())
blended_cpa = total_spend / total_bookings_n

print("=" * 70)
print(f"TOTAL SPEND: {total_spend:,.0f} VND | TOTAL BOOKINGS: {total_bookings_n:,} | BLENDED CPA: {blended_cpa:,.0f} VND")
print("=" * 70)
print("\n--- By market (sorted by spend) ---")
print(by_market[["market", "spend_vnd", "bookings", "cpa_vnd"]].to_string(index=False))
print("\n--- By channel (platform / last-click view) ---")
print(by_channel[["channel", "spend_vnd", "bookings", "cpa_platform_vnd"]].to_string(index=False))
print("\n--- Attribution model comparison ---")
print(attribution[["channel", "first_touch_bookings", "last_touch_bookings", "linear_bookings",
                    "last_touch_cpa_vnd", "linear_cpa_vnd", "linear_vs_last_gap_pct"]].to_string(index=False))

print(f"\nRẻ nhất theo CPA (thị trường): {top_market['market']} — {top_market['cpa_vnd']:,.0f}đ/booking")
print(f"Đắt nhất theo CPA (thị trường): {worst_market['market']} — {worst_market['cpa_vnd']:,.0f}đ/booking")
print(f"Kênh bị đánh giá thấp nhất theo last-click vs linear: {most_undervalued['channel']} "
      f"(+{most_undervalued['linear_vs_last_gap_pct']:.1f}% booking được ghi nhận thêm khi tính full-funnel)")
print(f"CPA chênh lệch thị trường tốt nhất vs kém nhất: "
      f"{(worst_market['cpa_vnd'] / top_market['cpa_vnd'] - 1) * 100:.1f}%")

# ---------- 6. Save for dashboard ----------
out = {
    "kpi": {
        "total_spend_vnd": total_spend,
        "total_bookings": total_bookings_n,
        "blended_cpa_vnd": round(blended_cpa),
        "total_installs": int(perf["installs"].sum()),
        "total_clicks": int(perf["clicks"].sum()),
        "total_impressions": int(perf["impressions"].sum()),
    },
    "by_market": by_market.round(4).to_dict(orient="records"),
    "by_channel": by_channel.round(4).to_dict(orient="records"),
    "market_channel_matrix": mx.round(2).to_dict(orient="records"),
    "attribution": attribution.round(2).to_dict(orient="records"),
    "funnel": {
        "impressions": int(perf["impressions"].sum()),
        "clicks": int(perf["clicks"].sum()),
        "installs": int(perf["installs"].sum()),
        "bookings": int(perf["bookings"].sum()),
    },
}
with open("/home/claude/marketing_attribution_project/output/summary.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\nSaved output/summary.json")
