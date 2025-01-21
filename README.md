## **1. Giới Thiệu**

Trong bối cảnh thị trường bất động sản ngày càng phát triển, việc thu thập và phân tích dữ liệu giúp người dùng có thể đưa ra các quyết định sáng suốt hơn. Đồ án này được thực hiện với mục tiêu xây dựng một hệ thống tự động thu thập dữ liệu bất động sản về chung ở Thành phố Hồ Chí Minh từ website [BatDongSan.com.vn](https://batdongsan.com.vn), lưu trữ vào cơ sở dữ liệu PostgreSQL và tiến hành phân tích dữ liệu nhằm đưa ra các thông tin hữu ích như giá trung bình, xu hướng giá theo khu vực, hoặc diện tích phổ biến.

### **Mục tiêu của dự án:**
- Tự động hóa việc thu thập dữ liệu bất động sản từ trang web.
- Lưu trữ dữ liệu vào cơ sở dữ liệu để dễ dàng quản lý và truy vấn.
- Tiến hành phân tích dữ liệu để tìm hiểu xu hướng thị trường.

---

## **2. Các Bước Setup**

### **Yêu cầu môi trường**
- Python >= 3.8 (nên là 3.11)
- PostgreSQL >= 13
- Trình duyệt Chrome và ChromeDriver
- Các thư viện Python: `selenium`, `psycopg2`, `pandas`, `concurrent.futures`, `webdriver-manager`, `numpy`, `matplotlib`, `seaborn`, `psycopg2`, `scikit-learn`, `tensorflow`

### **1. Tạo môi trường ảo**
```bash
python3.11 -m venv venv
source venv/bin/activate    # Trên Linux/macOS
venv\Scripts\activate       # Trên Windows
```

### **2. Cài đặt các thư viện cần thiết**
Cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

### **3. Cài đặt PostgreSQL**
1. Tải và cài đặt PostgreSQL 
- Download từ [trang chính thức](https://www.postgresql.org/download/).
- Sử dụng Docker:
```bash
docker pull postgres
```
2. Khởi tạo cơ sở dữ liệu:
   - Username: `your_username` (Username mặc định: postgres)
   - Password: `your_password` (Password mặc định: postgres)

---

## **3. Sơ Lược Về Code**

### **1. Chức năng chính**
- **Thu thập dữ liệu**: Sử dụng Selenium để trích xuất thông tin bất động sản từ từng trang web.
- **Xử lý dữ liệu**: Chuẩn hóa thông tin giá, diện tích, và địa chỉ.
- **Lưu trữ dữ liệu**: Kết nối PostgreSQL để tạo bảng, kiểm tra dữ liệu trùng lặp và lưu thông tin.
- **Phân tích dữ liệu**: Xuất dữ liệu ra tệp CSV và sử dụng các công cụ phân tích.

### **2. Các tệp chính**
- **`main.py`**: File chính điều khiển luồng hoạt động.
- **`transform.py`**: Chứa các hàm xử lý và chuẩn hóa dữ liệu.
- **`database.py`**: Cung cấp các hàm kết nối và thao tác với PostgreSQL.

### **3. Luồng hoạt động của chương trình**
1. **Xác định số trang cuối**: Dùng Selenium để lấy số trang cần quét.
2. **Thu thập dữ liệu**:
   - Tạo các luồng song song để giảm thời gian xử lý.
   - Cuộn trang và trích xuất thông tin từ các phần tử HTML.
3. **Lưu trữ dữ liệu**:
   - Tạo cơ sở dữ liệu và bảng nếu chưa tồn tại.
   - Thêm dữ liệu mới vào bảng.
4. **Xuất tệp CSV**: Lưu dữ liệu vào file `chung_cu.csv` để dễ dàng phân tích.

---

## **4. Các Bước Phân Tích Dữ Liệu**

1. **Phân tích ảnh hưởng địa điểm:**
- Mã hóa “Địa chỉ” thành dạng số.
- Tiến hành hồi quy tuyến tính và kiểm định ANOVA để xem ảnh hưởng tới giá.
2. **Phân tích phân khúc bất động sản:** Phân khúc theo giá (Bình dân, Trung cấp, Cao cấp) và thực hiện mô hình phân loại Random Forest.
3. **Dự đoán giá:**
- Xây dựng mô hình Deep Learning (TensorFlow) để dự đoán giá dựa trên diện tích, số phòng, địa chỉ.
- Huấn luyện, đánh giá mô hình, so sánh kết quả dự đoán và giá trị thực tế.

## **5. Kết Luận**

Đồ án này không chỉ cung cấp một hệ thống thu thập dữ liệu tự động mà còn tạo cơ sở để phân tích dữ liệu bất động sản một cách khoa học và hiệu quả. Qua đó, dự án đã thể hiện khả năng ứng dụng Python và PostgreSQL trong việc giải quyết các vấn đề thực tiễn. 
