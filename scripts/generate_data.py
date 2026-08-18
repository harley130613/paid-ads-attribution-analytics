"""
Simulated dataset generator — Paid Ads & Customer Journey Attribution project.
This is a PERSONAL / SIMULATED dataset (not real company data), built to practice
multi-channel marketing analytics and attribution modeling.

Produces:
  data/daily_performance.csv   -- market x channel x day performance (impressions, clicks, spend, installs, bookings)
  data/touchpoints.csv         -- user-level touchpoint journeys leading to a booking (for attribution modeling)
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta

rng = np.random.default_rng(42)

# ---------- config ----------
MARKETS = {
    # market: (relative demand weight, cost multiplier - bigger city = pricier ads)
    "TP.HCM":   {"weight": 1.00, "cost_mult": 1.15},
    "Hà Nội":   {"weight": 0.78, "cost_mult": 1.10},
    "Đà Nẵng":  {"weight": 0.28, "cost_mult": 0.90},
    "Cần Thơ":  {"weight": 0.19, "cost_mult": 0.85},
}

CHANNELS = {
    # channel: (impressions weight, base CTR, base CPC (VND), install rate from click, booking rate from install)
    "Facebook Ads": {"imp_w": 1.00, "ctr": 0.0135, "cpc": 3800, "install_rate": 0.145, "booking_rate": 0.320},
    "TikTok Ads":   {"imp_w": 0.85, "ctr": 0.0190, "cpc": 3200, "install_rate": 0.110, "booking_rate": 0.250},
    "Google Ads":   {"imp_w": 0.55, "ctr": 0.0410, "cpc": 5600, "install_rate": 0.230, "booking_rate": 0.460},
    "Zalo Ads":     {"imp_w": 0.40, "ctr": 0.0220, "cpc": 2600, "install_rate": 0.160, "booking_rate": 0.360},
}

START = date(2026, 3, 1)
DAYS = 61  # 01/03 - 30/04/2026

BASE_DAILY_IMPRESSIONS = 42000  # base impressions/day for a weight=1.0 market x channel=1.0

rows = []
for d in range(DAYS):
    day = START + timedelta(days=d)
    # mild weekly seasonality (weekends slightly lower for B2C ride-hailing ads) + slow overall ramp
    dow_factor = 0.90 if day.weekday() >= 5 else 1.0
    ramp = 1.0 + 0.15 * (d / DAYS)  # budget scaled up slightly over the period

    for market, mcfg in MARKETS.items():
        for channel, ccfg in CHANNELS.items():
            impressions = rng.poisson(
                BASE_DAILY_IMPRESSIONS * mcfg["weight"] * ccfg["imp_w"] * dow_factor * ramp
            )
            ctr = max(0.001, rng.normal(ccfg["ctr"], ccfg["ctr"] * 0.12))
            clicks = rng.binomial(impressions, ctr) if impressions > 0 else 0

            cpc = max(300, rng.normal(ccfg["cpc"] * mcfg["cost_mult"], ccfg["cpc"] * 0.08))
            spend = round(clicks * cpc)

            install_rate = max(0.01, rng.normal(ccfg["install_rate"], ccfg["install_rate"] * 0.15))
            installs = rng.binomial(clicks, min(install_rate, 0.9)) if clicks > 0 else 0

            booking_rate = max(0.01, rng.normal(ccfg["booking_rate"], ccfg["booking_rate"] * 0.15))
            bookings = rng.binomial(installs, min(booking_rate, 0.9)) if installs > 0 else 0

            rows.append({
                "date": day.isoformat(),
                "market": market,
                "channel": channel,
                "impressions": int(impressions),
                "clicks": int(clicks),
                "spend_vnd": int(spend),
                "installs": int(installs),
                "bookings": int(bookings),
            })

perf = pd.DataFrame(rows)
perf.to_csv("/home/claude/marketing_attribution_project/data/daily_performance.csv", index=False)
print("daily_performance.csv:", perf.shape)
print(perf[["impressions", "clicks", "spend_vnd", "installs", "bookings"]].sum())

# ---------- touchpoint-level journeys (for attribution modeling) ----------
# Build one journey per booking: 1-4 touchpoints across channels, weighted by each
# channel's funnel role (Facebook/TikTok skew top-of-funnel/first-touch,
# Google Ads skews bottom-of-funnel/last-touch, Zalo Ads mid-funnel).
FUNNEL_ROLE = {
    "Facebook Ads": {"first_w": 0.42, "mid_w": 0.28, "last_w": 0.18},
    "TikTok Ads":   {"first_w": 0.38, "mid_w": 0.22, "last_w": 0.12},
    "Google Ads":   {"first_w": 0.10, "mid_w": 0.24, "last_w": 0.48},
    "Zalo Ads":     {"first_w": 0.10, "mid_w": 0.26, "last_w": 0.22},
}
channels_list = list(CHANNELS.keys())
total_bookings = int(perf["bookings"].sum())

journeys = []
first_w = np.array([FUNNEL_ROLE[c]["first_w"] for c in channels_list]); first_w /= first_w.sum()
mid_w   = np.array([FUNNEL_ROLE[c]["mid_w"] for c in channels_list]);   mid_w /= mid_w.sum()
last_w  = np.array([FUNNEL_ROLE[c]["last_w"] for c in channels_list]);  last_w /= last_w.sum()

for uid in range(total_bookings):
    n_touch = rng.choice([1, 2, 3, 4], p=[0.28, 0.34, 0.24, 0.14])
    seq = []
    if n_touch == 1:
        seq = [rng.choice(channels_list, p=last_w)]
    else:
        seq.append(rng.choice(channels_list, p=first_w))
        for _ in range(n_touch - 2):
            seq.append(rng.choice(channels_list, p=mid_w))
        seq.append(rng.choice(channels_list, p=last_w))
    conv_day = START + timedelta(days=int(rng.integers(0, DAYS)))
    for pos, ch in enumerate(seq):
        journeys.append({
            "user_id": f"U{uid:06d}",
            "touch_position": pos + 1,
            "touch_count": n_touch,
            "channel": ch,
            "is_first": pos == 0,
            "is_last": pos == n_touch - 1,
            "conversion_date": conv_day.isoformat(),
        })

touch_df = pd.DataFrame(journeys)
touch_df.to_csv("/home/claude/marketing_attribution_project/data/touchpoints.csv", index=False)
print("\ntouchpoints.csv:", touch_df.shape, "| unique users:", touch_df["user_id"].nunique())
