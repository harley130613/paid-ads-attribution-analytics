# Paid Ads & Customer Journey Attribution Analytics

Dự án phân tích hiệu quả phân bổ ngân sách quảng cáo đa kênh và mô hình hóa hành trình khách hàng, nhằm trả lời hai câu hỏi:

> **Khách hàng thực sự đến từ đâu? Ngân sách quảng cáo có đang được phân bổ đúng kênh?**

## Mục lục

- [Tổng quan dự án](#tổng-quan-dự-án)
- [Phần 1 - Attribution Modeling](#phần-1---attribution-modeling-dữ-liệu-mô-phỏng)
- [Phần 2 - Paid Channel Performance](#phần-2---paid-channel-performance-dữ-liệu-thực-tế-đã-ẩn-danh)
- [Công nghệ và phương pháp](#công-nghệ-và-phương-pháp)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cách chạy dự án](#cách-chạy-dự-án)
- [Bảo mật dữ liệu](#bảo-mật-dữ-liệu)

## Tổng quan dự án

Dự án gồm hai phần:

### Phần 1 - Attribution Modeling

Sử dụng dữ liệu Paid Ads và Customer Journey tự mô phỏng để so sánh ba mô hình phân bổ chuyển đổi:

- First-touch Attribution
- Last-touch Attribution
- Linear Attribution

Mục tiêu là thực hành Multi-touch Attribution ở cấp độ điểm chạm và đánh giá vai trò của từng kênh trong toàn bộ hành trình khách hàng.

### Phần 2 - Paid Channel Performance

Phân tích dữ liệu thực tế được trích xuất từ MMP Airbridge trong giai đoạn **01/06 - 17/08/2026**, bao gồm:

- Hiệu quả Click → Install theo từng kênh.
- ROAS và CAC của các kênh trả phí.
- Chất lượng traffic và tỷ lệ Re-install.
- Hoạt động của người dùng trong ứng dụng.

Các chỉ số tài chính tuyệt đối đã được chuyển đổi thành tỷ trọng hoặc chỉ số Index trước khi đưa vào repository công khai nhằm bảo mật dữ liệu kinh doanh.

> **Lưu ý về nguồn dữ liệu**
>
> - Phần 1 sử dụng dữ liệu mô phỏng, không phải dữ liệu thực tế của doanh nghiệp.
> - Phần 2 sử dụng dữ liệu xuất trực tiếp từ MMP Airbridge.
> - Các tệp CSV gốc và số liệu tài chính tuyệt đối không được đưa vào repository.
> - Chỉ dữ liệu tổng hợp đã ẩn danh được sử dụng trong phiên bản công khai.

---

## Phần 1 - Attribution Modeling (dữ liệu mô phỏng)

### Bài toán

Các nền tảng quảng cáo như Facebook, Google, TikTok và Zalo thường báo cáo hiệu quả theo mô hình **Last-click Attribution**, trong đó toàn bộ giá trị chuyển đổi được ghi nhận cho điểm chạm cuối cùng trước khi khách hàng đặt chuyến.

Cách tiếp cận này có thể:

- Đánh giá thấp các kênh tạo nhận biết và mở phễu.
- Đánh giá cao các kênh chốt chuyển đổi.
- Dẫn đến quyết định cắt giảm hoặc phân bổ ngân sách chưa chính xác.

Dự án mô phỏng dữ liệu ở cấp độ **touchpoint**, thay vì chỉ phân tích ở cấp độ campaign, nhằm:

1. So sánh kết quả giữa ba mô hình Attribution.
2. Đánh giá vai trò của từng kênh trong hành trình khách hàng.
3. Xác định những kênh có nguy cơ bị đánh giá sai nếu chỉ sử dụng Last-click.
4. Đề xuất phương án tái phân bổ ngân sách phù hợp hơn.

### Phạm vi dữ liệu

- **Thị trường:** TP.HCM, Hà Nội, Đà Nẵng và Cần Thơ.
- **Kênh Paid Ads:** Facebook Ads, Google Ads, TikTok Ads và Zalo Ads.
- **Thời gian:** 61 ngày, từ 01/03 - 30/04/2026.
- **Cấp độ dữ liệu:** Ngày, thị trường, kênh và điểm chạm người dùng.

### Bộ dữ liệu

#### `data/daily_performance.csv`

Dữ liệu hiệu quả quảng cáo theo ngày, thị trường và kênh, bao gồm:

- Impressions
- Clicks
- Spend
- Installs
- Bookings

Dữ liệu được tạo bằng phân phối Poisson và Binomial, với tham số riêng theo đặc điểm từng kênh như CTR, CPC, Install Rate và Booking Rate.

Mô hình đồng thời bổ sung:

- Trọng số nhu cầu theo từng thị trường.
- Hệ số chi phí theo thị trường.
- Seasonality theo ngày trong tuần.
- Mức tăng ngân sách theo thời gian.

#### `data/touchpoints.csv`

Dữ liệu hành trình người dùng dẫn đến từng booking, gồm từ **1 - 4 touchpoint** cho mỗi hành trình.

Xác suất xuất hiện của từng kênh tại vị trí First-touch, Mid-touch và Last-touch được thiết lập theo vai trò trong phễu:

- Facebook Ads và TikTok Ads thiên về mở phễu.
- Google Ads thiên về chốt chuyển đổi.
- Zalo Ads đảm nhiệm vai trò trung gian.

### Phương pháp phân tích

#### 1. Channel and Market Performance

Tổng hợp và đánh giá các chỉ số theo thị trường và kênh:

- Spend
- CTR
- CPC
- CPA
- Installs
- Bookings

#### 2. Attribution Modeling

So sánh ba mô hình phân bổ chuyển đổi:

| Mô hình | Cách ghi nhận chuyển đổi |
| --- | --- |
| First-touch | Ghi nhận 100% giá trị chuyển đổi cho điểm chạm đầu tiên |
| Last-touch | Ghi nhận 100% giá trị chuyển đổi cho điểm chạm cuối cùng |
| Linear | Phân bổ đồng đều giá trị chuyển đổi cho tất cả điểm chạm |

#### 3. Attribution-based CPA

So sánh CPA giữa các mô hình để xác định những kênh có nguy cơ bị đánh giá sai nếu chỉ sử dụng Last-click Attribution.

#### 4. Budget Reallocation

Đề xuất tái phân bổ ngân sách dựa trên:

- Chênh lệch CPA giữa các thị trường.
- Vai trò của từng kênh trong hành trình khách hàng.
- Kết quả chuyển đổi theo từng mô hình Attribution.

### Kết quả chính

| Chỉ số | Giá trị |
| --- | ---: |
| Tổng ngân sách | 1.624.592.340 đồng |
| Tổng booking | 23.853 |
| Blended CPA | 68.109 đồng |
| CTR trung bình | 2,17% |

#### TikTok Ads bị đánh giá thấp khi sử dụng Last-click

Theo mô hình Last-click, TikTok Ads có CPA khoảng **123.000 đồng**, khiến kênh này có vẻ là kênh kém hiệu quả nhất.

Tuy nhiên, theo Linear Attribution, số booking được ghi nhận cho TikTok Ads tăng thêm **74%**.

Kết quả cho thấy TikTok Ads chủ yếu đóng vai trò tạo nhận biết và mở phễu, thay vì trực tiếp chốt chuyển đổi. Nếu chỉ tối ưu ngân sách theo Last-click, doanh nghiệp có thể cắt giảm nhầm một kênh đang đóng góp quan trọng ở đầu hành trình khách hàng.

#### Hiệu quả khác biệt giữa các thị trường

CPA của Đà Nẵng đạt khoảng **56.181 đồng**, trong khi TP.HCM đạt khoảng **74.066 đồng**, chênh lệch gần **32%**.

Kết quả cho thấy tiềm năng tái phân bổ một phần ngân sách sang các thị trường nhỏ nhưng có hiệu quả tốt hơn.

### BI Dashboard - Phần 1

File: [`output/dashboard.html`](output/dashboard.html)

Dashboard được xây dựng bằng HTML, CSS, SVG và JavaScript thuần, không phụ thuộc thư viện biểu đồ bên ngoài và có thể mở trực tiếp trên trình duyệt.

Dashboard bao gồm:

- KPI tổng quan.
- Spend và Booking theo thị trường.
- CPA theo kênh.
- Customer Journey Funnel.
- So sánh ba mô hình Attribution.
- Bảng hiệu quả chi tiết theo thị trường.

---

## Phần 2 - Paid Channel Performance (dữ liệu thực tế đã ẩn danh)

### Bài toán

Doanh nghiệp triển khai Paid Ads trên bốn kênh:

- Google Ads
- Apple Search Ads
- TikTok Ads
- Facebook Ads

Hoạt động Paid Ads diễn ra song song với lượng người dùng đến từ Organic hoặc Unattributed.

Phần phân tích này tập trung trả lời các câu hỏi:

1. Ngân sách quảng cáo có đang được sử dụng hiệu quả không?
2. Kênh nào nên được tăng, cắt giảm hoặc tối ưu ngân sách?
3. Traffic từ mỗi kênh có bảo đảm chất lượng không?
4. Kênh nào có tỷ lệ Re-install cao hoặc tiềm ẩn Fraud?

### Nguồn dữ liệu

Dữ liệu gồm bốn báo cáo được xuất trực tiếp từ **MMP Airbridge** trong giai đoạn **01/06 - 17/08/2026**, tương ứng 78 ngày:

| Báo cáo | Nội dung |
| --- | --- |
| Daily App Install by OS & Channel | Click và Install theo ngày, kênh và hệ điều hành |
| Daily App Revenue | Order, doanh thu và chi phí theo ngày và kênh |
| Fraud Touchpoint Conversion | Install, First-install và Re-install theo kênh |
| Total Event Traffic | Các sự kiện trong ứng dụng như Install, Sign-up, Product View, Checkout và Order Complete |

### Phương pháp phân tích

#### 1. Channel Install Performance

Phân tích hành trình Click → Install theo từng kênh và hệ điều hành.

#### 2. Channel Economics

Đánh giá hiệu quả tài chính của các kênh trả phí thông qua:

- ROAS
- CAC Index
- Install Share
- Cost Share

Unattributed được loại khỏi phép tính Paid-only ROAS và CAC do không phát sinh chi phí quảng cáo.

#### 3. Traffic Quality

Phân tích tỷ lệ Re-install theo từng kênh nhằm phát hiện:
