# Paid Ads & Customer Journey Attribution Analytics

Phân tích hiệu quả phân bổ ngân sách paid ads đa kênh và mô hình hóa customer journey —
trả lời câu hỏi **"khách hàng thực sự đến từ đâu, và ngân sách ads có đang được chi đúng chỗ?"**

Repo gồm **2 phần**:

- **Phần 1 — Attribution modeling (dữ liệu mô phỏng):** so sánh 3 mô hình attribution
  (first-touch/last-touch/linear) trên dữ liệu paid ads + customer journey **tự mô phỏng**,
  luyện tập kỹ năng multi-touch attribution ở cấp touchpoint.
- **Phần 2 — Paid channel performance (dữ liệu thật, đã ẩn danh hóa):** phân tích dữ liệu
  **thật** từ MMP Airbridge của BUTL (01/06 – 17/08/2026), đo ROAS/CAC theo kênh và chất lượng
  traffic — các chỉ số tài chính tuyệt đối đã được **ẩn danh hóa thành % / index** trước khi
  đưa vào repo công khai để bảo mật số liệu kinh doanh của doanh nghiệp.

> **Về nguồn dữ liệu:** Phần 1 dùng dữ liệu mô phỏng (simulated), không phải số liệu doanh
> nghiệp thật — được nêu rõ trong mục tương ứng bên dưới. Phần 2 dùng dữ liệu xuất thật từ hệ
> thống MMP (Airbridge) nơi tác giả đang làm việc; các file CSV gốc **không** được đưa vào repo
> (chỉ số liệu tổng hợp đã ẩn danh hóa mới được công khai — xem mục "Bảo mật dữ liệu" bên dưới).

## Phần 1 — Attribution modeling (dữ liệu mô phỏng)

### Bài toán

Các nền tảng quảng cáo (Facebook, Google, TikTok, Zalo) đều báo cáo hiệu quả theo **last-click**
— chỉ tính công cho điểm chạm cuối cùng trước khi khách đặt chuyến. Cách nhìn này thường đánh
giá thấp các kênh đóng vai trò "mở phễu" (tạo nhận biết ban đầu) và đánh giá cao các kênh
"chốt đơn". Dự án mô phỏng dữ liệu ở cấp **touchpoint** (không chỉ cấp campaign) để so sánh
3 mô hình attribution và xem ngân sách nên được phân bổ lại như thế nào nếu nhìn toàn bộ hành trình
khách hàng thay vì chỉ điểm chạm cuối.

### Dữ liệu mô phỏng

- **Phạm vi:** 4 thị trường (TP.HCM, Hà Nội, Đà Nẵng, Cần Thơ) × 4 kênh paid ads (Facebook Ads,
  Google Ads, TikTok Ads, Zalo Ads) × 61 ngày (01/03 – 30/04/2026).
- **`data/daily_performance.csv`** — hiệu quả theo ngày/thị trường/kênh: impressions, clicks,
  spend (VND), installs, bookings. Sinh bằng phân phối Poisson/Binomial có tham số hóa theo
  đặc điểm từng kênh (CTR, CPC, install rate, booking rate) và từng thị trường (demand weight,
  cost multiplier), cộng thêm seasonality theo ngày trong tuần và ramp ngân sách dần theo thời gian.
- **`data/touchpoints.csv`** — hành trình cấp user dẫn đến từng booking (1–4 touchpoint/hành trình),
  với xác suất mỗi kênh xuất hiện ở vị trí "first / mid / last touch" được tham số hóa theo vai trò
  kênh trong phễu (Facebook & TikTok thiên về first-touch, Google Ads thiên về last-touch, Zalo Ads
  ở giữa) — mô phỏng đúng đặc điểm hành vi thường thấy trong ngành.

### Phương pháp phân tích

1. **Performance theo thị trường & kênh** — tổng hợp spend, CTR, CPC, CPA từ `daily_performance.csv`.
2. **So sánh 3 mô hình attribution** từ `touchpoints.csv`:
   - *First-touch*: 100% công cho điểm chạm đầu tiên.
   - *Last-touch*: 100% công cho điểm chạm cuối cùng (mặc định của các nền tảng ads).
   - *Linear*: chia đều công cho mọi điểm chạm trong hành trình.
3. **So sánh CPA theo mô hình** để phát hiện kênh nào bị định giá sai nếu chỉ nhìn theo last-click.
4. **Đề xuất tái phân bổ ngân sách** dựa trên chênh lệch CPA giữa thị trường và giữa các mô hình attribution.

### Kết quả chính (trên bộ dữ liệu mô phỏng)

| Chỉ số | Giá trị |
|---|---|
| Tổng ngân sách | 1.624.592.340đ |
| Tổng booking | 23.853 |
| Blended CPA | 68.109đ |
| CTR trung bình | 2,17% |

- Theo **last-click**, TikTok Ads có vẻ là kênh kém hiệu quả nhất (CPA ~123.000đ). Nhưng theo mô
  hình **linear/đa chạm**, TikTok Ads được ghi nhận thêm **+74% booking** — cho thấy vai trò thật
  của kênh này là **top-of-funnel**, không phải kênh chốt đơn. Nếu tối ưu ngân sách chỉ theo
  last-click, ngân sách TikTok Ads rất dễ bị cắt nhầm.
- CPA giữa thị trường rẻ nhất (Đà Nẵng, ~56.181đ) và đắt nhất (TP.HCM, ~74.066đ) chênh lệch
  **~32%**, gợi ý dư địa tái phân bổ ngân sách sang các thị trường nhỏ hơn nhưng hiệu quả hơn.

### BI Dashboard (Phần 1)

`output/dashboard.html` — dashboard tương tác dựng bằng **HTML + SVG thuần** (không phụ thuộc
thư viện biểu đồ ngoài, mở trực tiếp bằng trình duyệt, không cần server): KPI tổng quan, spend
& booking theo thị trường, CPA theo kênh, customer journey funnel, so sánh 3 mô hình attribution,
và bảng chi tiết theo thị trường.

## Phần 2 — Paid channel performance (dữ liệu thật, đã ẩn danh hóa)

### Bài toán

Doanh nghiệp chạy paid ads trên 4 kênh (Google Ads, Apple Search Ads, TikTok Ads, Facebook Ads)
song song với tăng trưởng Organic/Unattributed. Câu hỏi đặt ra: ngân sách ads có đang chi hiệu
quả không, kênh nào đáng đầu tư thêm/cắt giảm, và traffic từ mỗi kênh có "sạch" hay không
(re-install/fraud)?

### Nguồn dữ liệu

4 báo cáo xuất trực tiếp từ **MMP Airbridge**, 01/06/2026 – 17/08/2026 (78 ngày):

- Daily App Install by OS & Channel — click, install theo ngày/kênh/hệ điều hành.
- Daily App Revenue — order, doanh thu, chi phí theo ngày/kênh.
- Fraud Touchpoint Conversion — install, first-install, re-install theo kênh.
- Total Event Traffic — tổng số sự kiện trong app (install, sign-up, product view, checkout, order...).

**Bảo mật dữ liệu:** đây là số liệu kinh doanh thật của doanh nghiệp nơi tác giả đang làm việc.
File CSV gốc **chỉ lưu cục bộ, không đưa vào repo**. Trước khi công khai, các chỉ số tài chính
tuyệt đối (doanh thu, chi phí, CAC) được chuyển thành **% thị phần / chỉ số (index, trung bình
paid = 100)** — chỉ ROAS (revenue/cost, một tỷ lệ thuần) được giữ nguyên vì bản thân nó không
làm lộ quy mô doanh thu thật. `output/real_summary_public.json` là dữ liệu **đã ẩn danh hóa**,
an toàn để công khai; `real_summary_private.json` (số VND thật) không được đưa vào bản public.

### Phương pháp phân tích

1. **Channel install performance** — click → install theo kênh & hệ điều hành.
2. **Channel economics** — ROAS và CAC index theo kênh trả phí (loại Unattributed vì cost = 0).
3. **Traffic quality** — tỷ lệ re-install theo kênh (chỉ số nghi ngờ fraud/traffic kém chất lượng).
4. **Product activity** — khối lượng sự kiện trong app (Install → Sign-up → Product View → Checkout
   → Order Complete), trình bày như hoạt động theo kỳ (không phải phễu 1 cohort, vì Sign-up chỉ
   tính user mới còn Order Complete tính cả user cũ — hai tập hợp không lồng nhau).

### Kết quả chính (đã ẩn danh hóa)

- Paid ads chỉ đóng góp **33,3%** tổng install — phần lớn tăng trưởng (**66,7%**) đến từ
  **Unattributed/Organic**.
- **Paid-only ROAS: 4,51x** (ROAS tính trên toàn kênh kể cả Organic bị lệch lên 33,5x vì Organic
  cost = 0 — không phản ánh đúng hiệu quả ads nên cần tách riêng).
- **Apple Search Ads** hiệu quả nhất: ROAS **8,42x**, CAC index thấp nhất (54, tức ~46% rẻ hơn
  trung bình paid).
- **Facebook Ads** có ROAS chỉ **0,69x** (dưới 1 — chi tiêu ads cao hơn doanh thu ghi nhận được)
  và CAC index **829** (~8 lần trung bình paid) — ứng viên hàng đầu để cắt giảm/tối ưu ngân sách.
- Kênh **Referral** có tỷ lệ re-install cao nhất (5,26%), đáng theo dõi thêm về chất lượng traffic.

### BI Dashboard (Phần 2)

`output/dashboard_real.html` — dashboard tương tác từ dữ liệu thật đã ẩn danh hóa: thị phần
install theo kênh/OS, ROAS & CAC index theo kênh, hoạt động sản phẩm trong kỳ, tỷ lệ re-install,
và bảng chi tiết theo kênh.

## Công nghệ sử dụng

Python (Pandas, NumPy) cho xử lý & phân tích dữ liệu · HTML/CSS/SVG/JavaScript thuần cho BI
Dashboard (không phụ thuộc thư viện ngoài) · Phương pháp: funnel/activity analysis, multi-touch
attribution modeling (first-touch/last-touch/linear), channel economics (ROAS, CAC), data
anonymization cho số liệu kinh doanh nhạy cảm.

## Cấu trúc thư mục

```
marketing_attribution_project/
├── data/                          # Phần 1 — dữ liệu mô phỏng
│   ├── daily_performance.csv      # hiệu quả theo ngày x thị trường x kênh
│   └── touchpoints.csv            # hành trình touchpoint cấp user → booking
├── scripts/
│   ├── generate_data.py           # (P1) sinh dữ liệu mô phỏng
│   ├── analyze.py                 # (P1) tổng hợp performance + so sánh mô hình attribution
│   ├── build_dashboard.py         # (P1) dựng dashboard.html từ output/summary.json
│   ├── analyze_real.py            # (P2) phân tích dữ liệu MMP Airbridge thật + ẩn danh hóa
│   └── build_dashboard_real.py    # (P2) dựng dashboard_real.html từ real_summary_public.json
├── output/
│   ├── summary.json               # (P1) số liệu tổng hợp mô phỏng
│   ├── dashboard.html             # (P1) BI Dashboard — attribution modeling
│   ├── real_summary_public.json   # (P2) số liệu thật ĐÃ ẨN DANH HÓA — an toàn để public
│   └── dashboard_real.html        # (P2) BI Dashboard — paid channel performance (thật)
└── README.md
```

> `real_data/` (CSV gốc từ MMP Airbridge) và `real_summary_private.json` (số VND thật) chỉ tồn
> tại ở bản làm việc cục bộ, **không** có trong repo public.

## Cách chạy lại

```bash
pip install pandas numpy

# Phần 1 — dữ liệu mô phỏng
python scripts/generate_data.py     # sinh data/daily_performance.csv, data/touchpoints.csv
python scripts/analyze.py           # in kết quả phân tích + ghi output/summary.json
python scripts/build_dashboard.py   # dựng output/dashboard.html

# Phần 2 — dữ liệu thật (cần đặt 4 file CSV MMP Airbridge vào real_data/, xem analyze_real.py)
python scripts/analyze_real.py         # phân tích + ghi output/real_summary_{private,public}.json
python scripts/build_dashboard_real.py # dựng output/dashboard_real.html
```

---
*Trần Thị Cẩm Loan — Marketing Data Analyst*
