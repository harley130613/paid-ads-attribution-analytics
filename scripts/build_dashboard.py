import json

with open("/home/claude/marketing_attribution_project/output/summary.json", encoding="utf-8") as f:
    DATA = json.load(f)

data_json = json.dumps(DATA, ensure_ascii=False)

HTML = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paid Ads & Customer Journey Attribution — BI Dashboard</title>
<style>
  :root {
    --surface-1:  #fcfcfb;
    --page:       #f9f9f7;
    --text-1:     #0b0b0b;
    --text-2:     #52514e;
    --muted:      #898781;
    --grid:       #e1e0d9;
    --baseline:   #c3c2b7;
    --border:     rgba(11,11,11,0.10);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--page); color: var(--text-1);
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 28px 32px 60px;
  }
  h1 { font-size: 21px; margin: 0 0 4px; }
  .subtitle { color: var(--text-2); font-size: 13px; margin: 0 0 24px; }
  .subtitle b { color: var(--text-1); }
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }
  .kpi-card {
    background: var(--surface-1); border: 1px solid var(--border); border-radius: 10px;
    padding: 16px 18px;
  }
  .kpi-label { font-size: 12px; color: var(--muted); margin-bottom: 6px; }
  .kpi-value { font-size: 24px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .kpi-sub { font-size: 12px; color: var(--text-2); margin-top: 4px; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
  .panel {
    background: var(--surface-1); border: 1px solid var(--border); border-radius: 10px;
    padding: 18px 20px;
  }
  .panel h2 { font-size: 14px; margin: 0 0 2px; }
  .panel .desc { font-size: 12px; color: var(--text-2); margin: 0 0 14px; }
  .chart-wrap svg { display: block; width: 100%; height: auto; overflow: visible; }
  .bar-label { font-size: 11px; fill: var(--text-2); font-variant-numeric: tabular-nums; }
  .axis-label { font-size: 10.5px; fill: var(--muted); }
  .cat-label { font-size: 11.5px; fill: var(--text-1); }
  table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
  th, td { text-align: right; padding: 7px 8px; border-bottom: 1px solid var(--grid); }
  th:first-child, td:first-child { text-align: left; }
  th { color: var(--muted); font-weight: 600; font-size: 11.5px; text-transform: uppercase; letter-spacing: .02em; }
  .legend-row { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-2); margin: 12px 0 0; }
  .legend-dot { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: 5px; vertical-align: -1px; }
  .insight {
    background: var(--surface-1); border: 1px solid var(--border); border-radius: 10px;
    padding: 16px 20px; margin-bottom: 16px; font-size: 13px; line-height: 1.65; color: var(--text-2);
  }
  .insight b { color: var(--text-1); }
  footer { color: var(--muted); font-size: 11.5px; margin-top: 20px; }
</style>
</head>
<body>
  <h1>Paid Ads &amp; Customer Journey Attribution — BI Dashboard</h1>
  <p class="subtitle">Dữ liệu <b>mô phỏng cá nhân</b> (không phải số liệu doanh nghiệp thật) &middot; 4 thị trường &middot; 4 kênh paid ads &middot; 01/03 &ndash; 30/04/2026</p>

  <div class="kpi-row" id="kpiRow"></div>

  <div class="grid-2">
    <div class="panel">
      <h2>Spend theo thị trường</h2>
      <p class="desc">Tổng ngân sách chi tiêu theo từng thị trường</p>
      <div class="chart-wrap" id="marketSpendChart"></div>
    </div>
    <div class="panel">
      <h2>Bookings theo thị trường</h2>
      <p class="desc">Số booking thu được theo từng thị trường</p>
      <div class="chart-wrap" id="marketBookingChart"></div>
    </div>
  </div>

  <div class="grid-2">
    <div class="panel">
      <h2>CPA theo kênh (last-click / platform view)</h2>
      <p class="desc">Chi phí trên mỗi booking theo báo cáo mặc định của từng nền tảng quảng cáo</p>
      <div class="chart-wrap" id="channelCpaChart"></div>
    </div>
    <div class="panel">
      <h2>Customer journey funnel</h2>
      <p class="desc">Impression &rarr; Click &rarr; Install &rarr; Booking (toàn bộ 4 kênh, 4 thị trường)</p>
      <div class="chart-wrap" id="funnelChart"></div>
    </div>
  </div>

  <div class="panel" style="margin-bottom:16px;">
    <h2>So sánh mô hình attribution theo kênh</h2>
    <p class="desc">Số booking được ghi nhận cho mỗi kênh theo 3 mô hình: First-touch, Last-touch, Linear (đa chạm)</p>
    <div class="chart-wrap" id="attributionChart"></div>
    <div class="legend-row">
      <span><span class="legend-dot" style="background:#c3c2b7"></span>First-touch</span>
      <span><span class="legend-dot" style="background:#898781"></span>Last-touch</span>
      <span><span class="legend-dot" style="background:#2a78d6"></span>Linear (đa chạm)</span>
    </div>
  </div>

  <div class="insight" id="insightBox"></div>

  <div class="panel">
    <h2>Chi tiết CPA theo thị trường</h2>
    <p class="desc">Sắp xếp theo tổng ngân sách chi tiêu</p>
    <table id="marketTable"></table>
  </div>

  <footer>BI Dashboard tương tác (HTML + SVG thuần, không phụ thuộc thư viện ngoài) &middot; Dự án cá nhân, dữ liệu mô phỏng &middot; github.com/harley130613</footer>

<script>
const DATA = __DATA_JSON__;
const PALETTE = { blue: '#2a78d6', orange: '#eb6834', aqua: '#1baf7a', yellow: '#eda100' };
const CHANNEL_COLOR = {
  'Google Ads': PALETTE.blue,
  'Facebook Ads': PALETTE.orange,
  'TikTok Ads': PALETTE.aqua,
  'Zalo Ads': PALETTE.yellow,
};
const MARKET_COLOR = {
  'TP.HCM': PALETTE.blue,
  'Hà Nội': PALETTE.orange,
  'Đà Nẵng': PALETTE.aqua,
  'Cần Thơ': PALETTE.yellow,
};
const fmtVND = n => new Intl.NumberFormat('vi-VN').format(Math.round(n)) + 'đ';
const fmtN = n => new Intl.NumberFormat('vi-VN').format(Math.round(n));
const fmtCompact = n => n >= 1e9 ? (n/1e9).toFixed(2)+' tỷ' : n >= 1e6 ? (n/1e6).toFixed(0)+' tr' : fmtN(n);

const NS = 'http://www.w3.org/2000/svg';
function el(tag, attrs) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  return e;
}

// Simple horizontal bar chart: one value per category, direct labels (small N is fine to label every bar)
function hBarChart(containerId, { labels, values, colors, valueFmt, title }) {
  const container = document.getElementById(containerId);
  const W = container.clientWidth || 460, rowH = 36, gap = 10;
  const H = labels.length * (rowH + gap) + 10;
  const leftPad = 92, rightPad = 64;
  const maxV = Math.max(...values) * 1.15;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H });

  // gridlines
  for (let i = 0; i <= 4; i++) {
    const x = leftPad + (i / 4) * (W - leftPad - rightPad);
    svg.appendChild(el('line', { x1: x, x2: x, y1: 4, y2: H - 4, stroke: '#e1e0d9', 'stroke-width': 1 }));
  }

  labels.forEach((label, i) => {
    const y = i * (rowH + gap) + 6;
    const barW = (values[i] / maxV) * (W - leftPad - rightPad);
    const barColor = colors[i];

    const catText = el('text', { x: leftPad - 10, y: y + rowH / 2 + 4, 'text-anchor': 'end', class: 'cat-label' });
    catText.textContent = label;
    svg.appendChild(catText);

    svg.appendChild(el('rect', { x: leftPad, y, width: Math.max(barW, 2), height: rowH, rx: 4, fill: barColor }));

    const valText = el('text', { x: leftPad + barW + 8, y: y + rowH / 2 + 4, class: 'bar-label' });
    valText.textContent = valueFmt(values[i]);
    svg.appendChild(valText);
  });

  container.innerHTML = '';
  container.appendChild(svg);
}

// Vertical bar chart (for funnel-like or category comparisons)
function vBarChart(containerId, { labels, values, colors, valueFmt }) {
  const container = document.getElementById(containerId);
  const W = container.clientWidth || 460, H = 240;
  const topPad = 20, bottomPad = 30, barGap = 22;
  const n = labels.length;
  const barW = (W - barGap * (n + 1)) / n;
  const maxV = Math.max(...values) * 1.2;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H });

  for (let i = 0; i <= 3; i++) {
    const y = topPad + (i / 3) * (H - topPad - bottomPad);
    svg.appendChild(el('line', { x1: 0, x2: W, y1: y, y2: y, stroke: '#e1e0d9', 'stroke-width': 1 }));
  }

  labels.forEach((label, i) => {
    const x = barGap + i * (barW + barGap);
    const h = (values[i] / maxV) * (H - topPad - bottomPad);
    const y = H - bottomPad - h;
    svg.appendChild(el('rect', { x, y, width: barW, height: h, rx: 4, fill: colors[i] }));
    const valText = el('text', { x: x + barW / 2, y: y - 6, 'text-anchor': 'middle', class: 'bar-label' });
    valText.textContent = valueFmt(values[i]);
    svg.appendChild(valText);
    const labText = el('text', { x: x + barW / 2, y: H - 10, 'text-anchor': 'middle', class: 'axis-label' });
    labText.textContent = label;
    svg.appendChild(labText);
  });

  container.innerHTML = '';
  container.appendChild(svg);
}

// Grouped horizontal bar chart: categories x N series, single shared axis
function groupedHBarChart(containerId, { categories, series, colors, valueFmt }) {
  // series: [{name, values:[...]}]
  const container = document.getElementById(containerId);
  const W = container.clientWidth || 900;
  const rowH = 16, rowGap = 3, groupGap = 16;
  const nSeries = series.length;
  const groupH = nSeries * (rowH + rowGap) + groupGap;
  const H = categories.length * groupH + 10;
  const leftPad = 100, rightPad = 60;
  let maxV = 0;
  series.forEach(s => s.values.forEach(v => { if (v > maxV) maxV = v; }));
  maxV *= 1.15;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H });

  for (let i = 0; i <= 4; i++) {
    const x = leftPad + (i / 4) * (W - leftPad - rightPad);
    svg.appendChild(el('line', { x1: x, x2: x, y1: 4, y2: H - 4, stroke: '#e1e0d9', 'stroke-width': 1 }));
  }

  categories.forEach((cat, ci) => {
    const groupTop = ci * groupH + groupGap / 2;
    const catText = el('text', { x: leftPad - 10, y: groupTop + (groupH - groupGap) / 2 + 4, 'text-anchor': 'end', class: 'cat-label' });
    catText.textContent = cat;
    svg.appendChild(catText);

    series.forEach((s, si) => {
      const y = groupTop + si * (rowH + rowGap);
      const v = s.values[ci];
      const barW = (v / maxV) * (W - leftPad - rightPad);
      svg.appendChild(el('rect', { x: leftPad, y, width: Math.max(barW, 1), height: rowH, rx: 3, fill: colors[si] }));
      const valText = el('text', { x: leftPad + barW + 6, y: y + rowH / 2 + 3.5, class: 'bar-label', style: 'font-size:10px' });
      valText.textContent = valueFmt(v);
      svg.appendChild(valText);
    });
  });

  container.innerHTML = '';
  container.appendChild(svg);
}

// ---------- KPI cards ----------
const kpiRow = document.getElementById('kpiRow');
const kpis = [
  { label: 'Tổng ngân sách', value: fmtVND(DATA.kpi.total_spend_vnd), sub: `${fmtN(DATA.kpi.total_impressions)} impressions` },
  { label: 'Tổng booking', value: fmtN(DATA.kpi.total_bookings), sub: `${fmtN(DATA.kpi.total_installs)} installs` },
  { label: 'Blended CPA', value: fmtVND(DATA.kpi.blended_cpa_vnd), sub: 'Toàn bộ 4 kênh & 4 thị trường' },
  { label: 'CTR trung bình', value: ((DATA.kpi.total_clicks / DATA.kpi.total_impressions) * 100).toFixed(2) + '%', sub: `${fmtN(DATA.kpi.total_clicks)} clicks` },
];
kpiRow.innerHTML = kpis.map(k => `
  <div class="kpi-card">
    <div class="kpi-label">${k.label}</div>
    <div class="kpi-value">${k.value}</div>
    <div class="kpi-sub">${k.sub}</div>
  </div>`).join('');

// ---------- Market: spend & bookings (two single-axis charts, no dual-axis) ----------
const byMarket = [...DATA.by_market].sort((a, b) => b.spend_vnd - a.spend_vnd);
hBarChart('marketSpendChart', {
  labels: byMarket.map(m => m.market),
  values: byMarket.map(m => m.spend_vnd),
  colors: byMarket.map(m => MARKET_COLOR[m.market]),
  valueFmt: fmtCompact,
});
hBarChart('marketBookingChart', {
  labels: byMarket.map(m => m.market),
  values: byMarket.map(m => m.bookings),
  colors: byMarket.map(m => MARKET_COLOR[m.market]),
  valueFmt: fmtN,
});

// ---------- Channel CPA (platform view) ----------
const byChannel = [...DATA.by_channel].sort((a, b) => a.cpa_platform_vnd - b.cpa_platform_vnd);
hBarChart('channelCpaChart', {
  labels: byChannel.map(c => c.channel),
  values: byChannel.map(c => c.cpa_platform_vnd),
  colors: byChannel.map(c => CHANNEL_COLOR[c.channel]),
  valueFmt: fmtVND,
});

// ---------- Funnel ----------
const funnel = DATA.funnel;
vBarChart('funnelChart', {
  labels: ['Impressions', 'Clicks', 'Installs', 'Bookings'],
  values: [funnel.impressions, funnel.clicks, funnel.installs, funnel.bookings],
  colors: ['#cde2fb', '#86b6ef', '#3987e5', '#184f95'],
  valueFmt: fmtCompact,
});

// ---------- Attribution comparison ----------
const attr = [...DATA.attribution].sort((a, b) => b.spend_vnd - a.spend_vnd);
groupedHBarChart('attributionChart', {
  categories: attr.map(a => a.channel),
  series: [
    { name: 'First-touch', values: attr.map(a => a.first_touch_bookings) },
    { name: 'Last-touch', values: attr.map(a => a.last_touch_bookings) },
    { name: 'Linear', values: attr.map(a => a.linear_bookings) },
  ],
  colors: ['#c3c2b7', '#898781', '#2a78d6'],
  valueFmt: fmtN,
});

// ---------- Insight box ----------
const gapSorted = [...attr].sort((a, b) => b.linear_vs_last_gap_pct - a.linear_vs_last_gap_pct);
const mostUndervalued = gapSorted[0];
const marketSorted = [...DATA.by_market].sort((a, b) => a.cpa_vnd - b.cpa_vnd);
const cheapest = marketSorted[0], priciest = marketSorted[marketSorted.length - 1];
document.getElementById('insightBox').innerHTML = `
  <b>Insight chính:</b> Theo mô hình last-click (mặc định của các nền tảng ads), <b>${mostUndervalued.channel}</b>
  trông kém hiệu quả nhất — nhưng khi đổi sang mô hình <b>linear / đa chạm</b> (tính công cho mọi touchpoint trong hành trình khách hàng,
  không chỉ cú click cuối), kênh này được ghi nhận thêm <b>${mostUndervalued.linear_vs_last_gap_pct.toFixed(0)}%</b> booking —
  cho thấy vai trò thật của nó là kênh <b>top-of-funnel</b> (tạo nhận biết ban đầu) chứ không phải kênh chốt đơn.
  Nếu chỉ tối ưu ngân sách theo last-click, ngân sách cho ${mostUndervalued.channel} rất dễ bị cắt nhầm.<br><br>
  Theo thị trường: <b>${cheapest.market}</b> có CPA thấp nhất (${fmtVND(cheapest.cpa_vnd)}), trong khi
  <b>${priciest.market}</b> có CPA cao nhất (${fmtVND(priciest.cpa_vnd)}) — chênh lệch
  <b>${((priciest.cpa_vnd / cheapest.cpa_vnd - 1) * 100).toFixed(0)}%</b>, gợi ý nên tái phân bổ một phần ngân sách
  từ thị trường CPA cao sang thị trường CPA thấp còn dư địa tăng trưởng.
`;

// ---------- Market table ----------
const tbl = document.getElementById('marketTable');
const byMarketForTable = [...DATA.by_market].sort((a, b) => b.spend_vnd - a.spend_vnd);
tbl.innerHTML = `
  <thead><tr><th>Thị trường</th><th>Spend</th><th>Bookings</th><th>CTR</th><th>CPA</th></tr></thead>
  <tbody>
    ${byMarketForTable.map(m => `
      <tr>
        <td><span class="legend-dot" style="background:${MARKET_COLOR[m.market]}"></span>${m.market}</td>
        <td>${fmtVND(m.spend_vnd)}</td>
        <td>${fmtN(m.bookings)}</td>
        <td>${(m.ctr * 100).toFixed(2)}%</td>
        <td>${fmtVND(m.cpa_vnd)}</td>
      </tr>`).join('')}
  </tbody>
`;
</script>
</body>
</html>
"""

HTML = HTML.replace("__DATA_JSON__", data_json)

out_path = "/home/claude/marketing_attribution_project/output/dashboard.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML)
print("written", out_path, len(HTML), "bytes")
