# Paid Ads & Customer Journey Attribution Analytics

Dự án phân tích hiệu quả phân bổ ngân sách quảng cáo đa kênh và mô hình hóa hành trình khách hàng, nhằm trả lời hai câu hỏi:

> **Khách hàng thực sự đến từ đâu? Ngân sách quảng cáo có đang được phân bổ đúng kênh?**

## Mục lục

- [Tổng quan dự án](#tổng-quan-dự-án)
- [Phần 1 - Attribution Modeling](#phần-1---attribution-modeling)
  - [Bài toán](#bài-toán)
  - [Dữ liệu mô phỏng](#dữ-liệu-mô-phỏng)
  - [Phương pháp phân tích](#phương-pháp-phân-tích)
  - [Kết quả chính](#kết-quả-chính-trên-dữ-liệu-mô-phỏng)
  - [BI Dashboard](#bi-dashboard---phần-1)
- [Phần 2 - Paid Channel Performance](#phần-2---paid-channel-performance)
  - [Bài toán](#bài-toán-1)
  - [Nguồn dữ liệu](#nguồn-dữ-liệu)
  - [Bảo mật dữ liệu](#bảo-mật-dữ-liệu)
  - [Phương pháp phân tích](#phương-pháp-phân-tích-1)
  - [Kết quả chính](#kết-quả-chính-đã-ẩn-danh)
  - [BI Dashboard](#bi-dashboard---phần-2)
- [Công nghệ sử dụng](#công-nghệ-và-phương-pháp-sử-dụng)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cách chạy dự án](#cách-chạy-dự-án)
- [Tác giả](#tác-giả)

## Tổng quan dự án

Dự án gồm hai phần:

### Phần 1 - Attribution Modeling

Sử dụng dữ liệu Paid Ads và Customer Journey tự mô phỏng để so sánh ba mô hình Attribution:

- First-touch Attribution
- Last-touch Attribution
- Linear Attribution

Mục tiêu là thực hành Multi-touch Attribution ở cấp độ điểm chạm và đánh giá vai trò của từng kênh trong toàn bộ hành trình khách hàng.

### Phần 2 - Paid Channel Performance

Phân tích dữ liệu thực tế được trích xuất từ MMP Airbridge trong giai đoạn **01/06 - 17/08/2026**, tập trung vào:

- Hiệu quả Paid Ads theo từng kênh
- ROAS và CAC
- Tỷ trọng Install
- Chất lượng Traffic
- Tỷ lệ Re-install
- Dấu hiệu Fraud

Các chỉ số tài chính tuyệt đối đã được chuyển đổi thành tỷ trọng hoặc chỉ số Index trước khi đưa vào repository công khai nhằm bảo mật dữ liệu kinh doanh.

> **Lưu ý về nguồn dữ liệu**
>
> - Phần 1 sử dụng dữ liệu mô phỏng, không phải dữ liệu thực tế của doanh nghiệp.
> - Phần 2 sử dụng dữ liệu được xuất trực tiếp từ hệ thống MMP Airbridge.
> - Các tệp CSV gốc không được đưa vào repository.
> - Chỉ dữ liệu tổng hợp đã được ẩn danh mới được công khai.

---

## Phần 1 - Attribution Modeling

### Bài toán

Các nền tảng quảng cáo như Facebook, Google, TikTok và Zalo thường báo cáo hiệu quả theo mô hình **Last-click Attribution**. Theo đó, toàn bộ giá trị chuyển đổi được ghi nhận cho điểm chạm cuối cùng trước khi khách hàng đặt chuyến.

Cách tiếp cận này có thể:

- Đánh giá thấp các kênh đóng vai trò tạo nhận biết và mở phễu.
- Đánh giá cao các kênh đảm nhiệm vai trò chốt chuyển đổi.
- Dẫn đến quyết định cắt giảm hoặc tăng ngân sách chưa phù hợp.
- Không phản ánh đầy đủ hành trình đa điểm chạm của khách hàng.

Dự án mô phỏng dữ liệu ở cấp độ **touchpoint**, thay vì chỉ dừng ở cấp chiến dịch, nhằm:

1. So sánh kết quả giữa ba mô hình Attribution.
2. Đánh giá vai trò của từng kênh trong hành trình khách hàng.
3. Xác định những kênh có nguy cơ bị định giá sai nếu chỉ sử dụng Last-click.
4. Đề xuất phương án tái phân bổ ngân sách phù hợp hơn.

### Dữ liệu mô phỏng

#### Phạm vi dữ liệu

- **Thị trường:** TP.HCM, Hà Nội, Đà Nẵng và Cần Thơ
- **Kênh quảng cáo:** Facebook Ads, Google Ads, TikTok Ads và Zalo Ads
- **Thời gian:** 61 ngày, từ 01/03 đến 30/04/2026

#### `data/daily_performance.csv`

Dữ liệu hiệu quả quảng cáo theo ngày, thị trường và kênh, bao gồm:

- Impressions
- Clicks
- Spend
- Installs
- Bookings

Dữ liệu được tạo bằng phân phối Poisson và Binomial, với tham số riêng theo:

- CTR
- CPC
- Install Rate
- Booking Rate
- Trọng số nhu cầu theo thị trường
- Hệ số chi phí theo thị trường
- Tính mùa vụ theo ngày trong tuần
- Mức tăng ngân sách theo thời gian

#### `data/touchpoints.csv`

Dữ liệu hành trình người dùng dẫn đến từng booking, gồm từ **1 đến 4 điểm chạm** cho mỗi hành trình.

Xác suất xuất hiện của từng kênh tại vị trí First-touch, Mid-touch và Last-touch được thiết lập theo vai trò trong phễu:

| Kênh | Vai trò chính trong hành trình |
| --- | --- |
| Facebook Ads | Tạo nhận biết và mở phễu |
| TikTok Ads | Tạo nhận biết và mở phễu |
| Google Ads | Chốt nhu cầu và chuyển đổi |
| Zalo Ads | Điểm chạm trung gian |

### Phương pháp phân tích

#### 1. Phân tích hiệu quả theo thị trường và kênh

Tổng hợp các chỉ số từ `daily_performance.csv`:

- Spend
- Impressions
- Clicks
- CTR
- CPC
- Installs
- Bookings
- CPA

#### 2. So sánh ba mô hình Attribution

| Mô hình | Cách phân bổ giá trị chuyển đổi |
| --- | --- |
| First-touch | Ghi nhận 100% giá trị cho điểm chạm đầu tiên |
| Last-touch | Ghi nhận 100% giá trị cho điểm chạm cuối cùng |
| Linear | Phân bổ đồng đều cho tất cả điểm chạm |

#### 3. So sánh CPA giữa các mô hình

Đánh giá sự thay đổi về số booking và CPA của từng kênh khi chuyển từ Last-touch sang First-touch hoặc Linear Attribution.

#### 4. Đề xuất tái phân bổ ngân sách

Đề xuất được xây dựng dựa trên:

- Chênh lệch CPA giữa các thị trường
- Chênh lệch CPA giữa các mô hình Attribution
- Vai trò của từng kênh trong hành trình khách hàng
- Mức đóng góp của từng kênh tại đầu, giữa và cuối phễu

### Kết quả chính trên dữ liệu mô phỏng

| Chỉ số | Giá trị |
| --- | ---: |
| Tổng ngân sách | 1.624.592.340 đồng |
| Tổng booking | 23.853 |
| Blended CPA | 68.109 đồng |
| CTR trung bình | 2,17% |

#### TikTok Ads bị đánh giá thấp theo Last-click

Theo mô hình **Last-click**, TikTok Ads có CPA khoảng **123.000 đồng**, khiến đây dường như là kênh kém hiệu quả nhất.

Tuy nhiên, khi sử dụng **Linear Attribution**, số booking được ghi nhận cho TikTok Ads tăng thêm **74%**.

Kết quả cho thấy TikTok Ads chủ yếu đảm nhiệm vai trò:

- Tạo nhận biết
- Tiếp cận khách hàng mới
- Mở đầu hành trình chuyển đổi

Nếu chỉ tối ưu ngân sách theo Last-click, doanh nghiệp có thể cắt giảm nhầm một kênh đang đóng góp quan trọng ở đầu phễu.

#### Chênh lệch CPA giữa các thị trường

| Thị trường | CPA |
| --- | ---: |
| Đà Nẵng | Khoảng 56.181 đồng |
| TP.HCM | Khoảng 74.066 đồng |

CPA giữa thị trường có chi phí thấp nhất và cao nhất chênh lệch gần **32%**.

Kết quả cho thấy doanh nghiệp có thể cân nhắc tái phân bổ một phần ngân sách sang các thị trường nhỏ nhưng có hiệu quả chi phí tốt hơn.

### BI Dashboard - Phần 1

File dashboard:

```text
output/dashboard.html
```

Dashboard được xây dựng bằng **HTML, CSS, SVG và JavaScript thuần**, không phụ thuộc thư viện biểu đồ bên ngoài và không yêu cầu server.

Dashboard bao gồm:

- KPI tổng quan
- Spend và Booking theo thị trường
- CPA theo kênh
- Customer Journey Funnel
- So sánh ba mô hình Attribution
- Bảng hiệu quả chi tiết theo thị trường

---

## Phần 2 - Paid Channel Performance

### Bài toán

Doanh nghiệp triển khai Paid Ads trên bốn kênh:

- Google Ads
- Apple Search Ads
- TikTok Ads
- Facebook Ads

Song song đó, ứng dụng còn ghi nhận tăng trưởng từ nhóm **Organic hoặc Unattributed**.

Phần phân tích tập trung trả lời các câu hỏi:

1. Ngân sách quảng cáo có đang được sử dụng hiệu quả không?
2. Kênh nào nên được tăng, duy trì hoặc cắt giảm ngân sách?
3. Traffic từ mỗi kênh có bảo đảm chất lượng không?
4. Kênh nào có tỷ lệ Re-install cao?
5. Kênh nào có dấu hiệu Traffic kém chất lượng hoặc tiềm ẩn Fraud?

### Nguồn dữ liệu

Dữ liệu gồm bốn báo cáo được xuất trực tiếp từ **MMP Airbridge** trong giai đoạn **01/06 - 17/08/2026**, tương ứng 78 ngày.

| Báo cáo | Nội dung |
| --- | --- |
| Daily App Install by OS & Channel | Click và Install theo ngày, kênh và hệ điều hành |
| Daily App Revenue | Order, doanh thu và chi phí theo ngày và kênh |
| Fraud Touchpoint Conversion | Install, First-install và Re-install theo kênh |
| Total Event Traffic | Install, Sign-up, Product View, Checkout và Order Complete |

### Bảo mật dữ liệu

Đây là dữ liệu kinh doanh thực tế của doanh nghiệp nơi tác giả đang làm việc.

Các tệp CSV gốc chỉ được lưu trong môi trường làm việc cục bộ và không được đưa vào repository công khai.

Trước khi công khai dữ liệu:

- Doanh thu tuyệt đối được chuyển đổi thành tỷ trọng.
- Chi phí tuyệt đối được chuyển đổi thành tỷ trọng.
- CAC được chuyển đổi thành **CAC Index**.
- Mức CAC trung bình của nhóm Paid được quy ước bằng 100.
- ROAS được giữ nguyên vì đây là tỷ lệ và không trực tiếp làm lộ quy mô doanh thu.
- Chỉ dữ liệu tổng hợp đã ẩn danh mới được đưa vào repository.

| File | Trạng thái |
| --- | --- |
| `output/real_summary_public.json` | Dữ liệu đã ẩn danh, được phép công khai |
| `real_summary_private.json` | Dữ liệu tài chính tuyệt đối, không công khai |
| `real_data/` | Dữ liệu CSV gốc, chỉ lưu cục bộ |

### Phương pháp phân tích

#### 1. Channel Install Performance

Phân tích hành trình từ Click đến Install theo:

- Kênh quảng cáo
- Hệ điều hành
- Ngày
- Tỷ trọng Install
- Click-to-install Rate

#### 2. Channel Economics

Đánh giá hiệu quả tài chính của từng kênh thông qua:

- ROAS
- CAC Index
- Cost Share
- Revenue Share
- Order Share

Nhóm Unattributed được loại khỏi phép tính Paid-only ROAS và CAC do không phát sinh chi phí quảng cáo.

#### 3. Traffic Quality

Phân tích tỷ lệ Re-install theo từng kênh nhằm phát hiện:

- Traffic kém chất lượng
- Người dùng cài đặt lại nhiều lần
- Sai lệch Attribution
- Dấu hiệu nghi ngờ Fraud

#### 4. Product Activity

Phân tích khối lượng sự kiện trong ứng dụng:

```text
Install -> Sign-up -> Product View -> Checkout -> Order Complete
```

> **Lưu ý:** Các sự kiện trên được trình bày như mức độ hoạt động trong kỳ, không phải Funnel của cùng một Cohort.
>
> Sign-up chỉ bao gồm người dùng mới, trong khi Order Complete có thể bao gồm cả người dùng mới và người dùng hiện hữu. Vì vậy, hai tập dữ liệu không hoàn toàn lồng nhau.

### Kết quả chính đã ẩn danh

#### Cơ cấu Install

- Paid Ads đóng góp **33,3% tổng Install**.
- Organic hoặc Unattributed đóng góp **66,7% tổng Install**.

Kết quả cho thấy phần lớn lượt cài đặt chưa được ghi nhận trực tiếp cho các kênh Paid.

#### Paid-only ROAS

**Paid-only ROAS đạt 4,51x.**

Nếu tính cả Organic hoặc Unattributed, ROAS tăng lên 33,5x do nhóm này không phát sinh chi phí quảng cáo.

Vì vậy, ROAS tính trên toàn bộ kênh không phản ánh chính xác hiệu quả Paid Ads và cần được tách riêng khi đánh giá.

#### Apple Search Ads

Apple Search Ads là kênh hiệu quả nhất:

- **ROAS:** 8,42x
- **CAC Index:** 54
- CAC thấp hơn khoảng **46% so với trung bình Paid**

Đây là kênh có thể được cân nhắc tăng ngân sách, nhưng cần tiếp tục theo dõi khả năng mở rộng quy mô và hiệu suất biên.

#### Facebook Ads

Facebook Ads ghi nhận:

- **ROAS:** 0,69x
- **CAC Index:** 829
- CAC cao hơn khoảng tám lần so với trung bình Paid

Chi phí quảng cáo của kênh đang cao hơn doanh thu được hệ thống ghi nhận. Đây là kênh cần được ưu tiên:

- Rà soát Tracking
- Kiểm tra Targeting
- Tối ưu Creative
- Đánh giá lại Landing Flow
- Cắt giảm ngân sách nếu hiệu quả không được cải thiện

#### Referral

Referral có tỷ lệ Re-install cao nhất, đạt **5,26%**.

Kênh này cần được theo dõi thêm để đánh giá:

- Chất lượng Traffic
- Hành vi cài đặt lại
- Sai lệch Tracking
- Nguy cơ Fraud

### BI Dashboard - Phần 2

File dashboard:

```text
output/dashboard_real.html
```

Dashboard được xây dựng từ dữ liệu thực tế đã ẩn danh, bao gồm:

- Thị phần Install theo kênh
- Install theo hệ điều hành
- ROAS theo kênh
- CAC Index theo kênh
- Mức độ hoạt động của người dùng trong kỳ
- Tỷ lệ Re-install
- Bảng hiệu quả chi tiết theo kênh

---

## Công nghệ và phương pháp sử dụng

### Công nghệ

| Nhóm | Công nghệ |
| --- | --- |
| Xử lý dữ liệu | Python, Pandas, NumPy |
| Dashboard | HTML, CSS, SVG, JavaScript |
| Nguồn dữ liệu | MMP Airbridge |
| Định dạng dữ liệu | CSV, JSON |

### Phương pháp phân tích

- Funnel Analysis
- Activity Analysis
- Multi-touch Attribution Modeling
- First-touch Attribution
- Last-touch Attribution
- Linear Attribution
- Channel Economics
- Traffic Quality Analysis
- Data Anonymization

### Chỉ số đánh giá

- CTR
- CPC
- CPA
- CAC
- CAC Index
- ROAS
- Install Share
- Click-to-install Rate
- Re-install Rate
- Cost Share
- Revenue Share

---

## Cấu trúc thư mục

```text
marketing_attribution_project/
├── data/
│   ├── daily_performance.csv
│   └── touchpoints.csv
├── scripts/
│   ├── generate_data.py
│   ├── analyze.py
│   ├── build_dashboard.py
│   ├── analyze_real.py
│   └── build_dashboard_real.py
├── output/
│   ├── summary.json
│   ├── dashboard.html
│   ├── real_summary_public.json
│   └── dashboard_real.html
└── README.md
```

### Mô tả các file chính

| File | Mô tả |
| --- | --- |
| `data/daily_performance.csv` | Dữ liệu hiệu quả quảng cáo mô phỏng theo ngày, thị trường và kênh |
| `data/touchpoints.csv` | Dữ liệu hành trình điểm chạm ở cấp độ người dùng |
| `scripts/generate_data.py` | Sinh dữ liệu mô phỏng |
| `scripts/analyze.py` | Phân tích Performance và Attribution |
| `scripts/build_dashboard.py` | Xây dựng dashboard cho Phần 1 |
| `scripts/analyze_real.py` | Phân tích dữ liệu Airbridge và ẩn danh hóa |
| `scripts/build_dashboard_real.py` | Xây dựng dashboard cho Phần 2 |
| `output/summary.json` | Dữ liệu tổng hợp của Phần 1 |
| `output/dashboard.html` | Attribution Dashboard |
| `output/real_summary_public.json` | Dữ liệu thực tế đã ẩn danh |
| `output/dashboard_real.html` | Paid Channel Dashboard |

> Thư mục `real_data/` và file `real_summary_private.json` chỉ tồn tại trong môi trường làm việc cục bộ, không được đưa vào repository công khai.

---

## Cách chạy dự án

### 1. Cài đặt thư viện

```bash
pip install pandas numpy
```

### 2. Chạy Phần 1 - Dữ liệu mô phỏng

```bash
python scripts/generate_data.py
python scripts/analyze.py
python scripts/build_dashboard.py
```

Kết quả được lưu tại:

```text
output/summary.json
output/dashboard.html
```

### 3. Chạy Phần 2 - Dữ liệu thực tế

Đặt bốn tệp CSV được xuất từ MMP Airbridge vào thư mục:

```text
real_data/
```

Sau đó chạy:

```bash
python scripts/analyze_real.py
python scripts/build_dashboard_real.py
```

Kết quả được lưu tại:

```text
output/real_summary_public.json
output/dashboard_real.html
```

---
