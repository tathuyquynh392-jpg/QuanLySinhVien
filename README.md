# HỆ THỐNG QUẢN LÝ SINH VIÊN

Hệ thống quản lý sinh viên được xây dựng phục vụ học phần **Triển khai và Quản trị Hệ thống**.

Hệ thống hỗ trợ quản lý sinh viên, lớp học và điểm số, đồng thời triển khai cơ sở dữ liệu, reverse proxy, HTTPS, monitoring, logging và các biện pháp hardening bằng Docker Compose.

---

## 1. Công nghệ sử dụng

- Django
- MySQL
- phpMyAdmin
- Docker / Docker Compose
- Nginx
- HTTPS
- Prometheus
- Grafana
- cAdvisor
- MySQL Exporter
- Loki
- Promtail
- LogQL

---

## 2. Kiến trúc hệ thống

```text
                         CLIENT
                            |
                            | HTTPS :8443
                            v
                    +---------------+
                    |     Nginx     |
                    | Reverse Proxy |
                    +-------+-------+
                            |
                            | HTTP :8000
                            v
                    +---------------+
                    |     Django    |
                    | student_web   |
                    +-------+-------+
                            |
                            | :3306
                            v
                    +---------------+
                    |     MySQL     |
                    | student_mysql |
                    +---------------+

              MONITORING
                    |
       +------------+-------------+
       |                          |
       v                          v
   cAdvisor                MySQL Exporter
       |                          |
       +------------+-------------+
                    |
                    v
                Prometheus
                    |
                    v
                 Grafana

                LOGGING
                    |
                  Docker
                    |
                    v
                Promtail
                    |
                    v
                  Loki
                    |
                    v
             Grafana Explore
```

Hệ thống sử dụng hai network chính:

- `frontend`: network dành cho các thành phần cần giao tiếp với Nginx.
- `backend`: network nội bộ dành cho ứng dụng và cơ sở dữ liệu.

Backend network được cấu hình `internal: true` nhằm hạn chế truy cập từ bên ngoài.

---

## 3. Chức năng chính

### Quản lý sinh viên

- Xem danh sách sinh viên
- Thêm sinh viên
- Chỉnh sửa sinh viên
- Xóa sinh viên
- Tìm kiếm và quản lý thông tin sinh viên

### Quản lý lớp

- Quản lý thông tin lớp
- Liên kết sinh viên với lớp

### Quản lý điểm

- Quản lý điểm sinh viên
- Thêm và cập nhật điểm

---

## 4. Cấu trúc project

```text
QuanLySinhVien/
├── app/
│   ├── students/
│   ├── manage.py
│   └── requirements.txt
├── monitoring/
│   ├── prometheus.yml
│   ├── promtail-config.yml
│   └── .my.cnf
├── nginx/
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

> Lưu ý: `.env` và `monitoring/.my.cnf` chứa thông tin nhạy cảm và không được commit lên GitHub.

---

## 5. Yêu cầu môi trường

Cần cài đặt:

- Git
- Docker
- Docker Compose

Kiểm tra:

```powershell
docker --version
docker compose version
```

---

## 6. Clone project

Clone repository:

```powershell
git clone https://github.com/tathuyquynh392-jpg/QuanLySinhVien.git
```

Di chuyển vào thư mục:

```powershell
cd QuanLySinhVien
```

---

## 7. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc của project.

Ví dụ:

```env
DB_NAME=student_db
DB_USER=student_user
DB_PASSWORD=CHANGE_ME
DB_HOST=mysql
DB_PORT=3306

MYSQL_DATABASE=student_db
MYSQL_USER=student_user
MYSQL_PASSWORD=CHANGE_ME
MYSQL_ROOT_PASSWORD=CHANGE_ME

DJANGO_SECRET_KEY=CHANGE_ME

MYSQL_EXPORTER_USER=exporter
MYSQL_EXPORTER_PASSWORD=CHANGE_ME
```

Không đưa mật khẩu thật lên GitHub.

File `.env` được khai báo trong `.gitignore`.

---

## 8. Khởi động hệ thống

Build và khởi động các container:

```powershell
docker compose up -d --build
```

Kiểm tra trạng thái:

```powershell
docker compose ps
```

Xem log:

```powershell
docker compose logs -f
```

---

## 9. Các địa chỉ truy cập

| Thành phần | Địa chỉ |
|---|---|
| Website | https://localhost:8443 |
| phpMyAdmin | http://localhost:8081 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| cAdvisor | http://localhost:8082 |
| Loki | http://localhost:3100 |

HTTPS sử dụng chứng chỉ phục vụ môi trường triển khai/demo.

---

## 10. Monitoring

### Prometheus

Prometheus được sử dụng để thu thập metrics từ các thành phần trong hệ thống.

Các target chính:

- Prometheus
- cAdvisor
- MySQL Exporter

Một số PromQL:

```promql
up{job="cadvisor"}
```

```promql
mysql_up
```

```promql
mysql_global_status_threads_connected
```

```promql
mysql_global_status_queries
```

### Grafana

Grafana được sử dụng để trực quan hóa metrics.

Dashboard theo dõi:

- RAM container
- Trạng thái MySQL
- Số lượng kết nối MySQL
- MySQL queries
- Metrics của container

Truy cập:

```text
http://localhost:3000
```

### MySQL Exporter

MySQL Exporter cung cấp metrics của MySQL cho Prometheus.

Kiểm tra:

```promql
mysql_up
```

Giá trị `1` cho biết Prometheus có thể thu thập metrics từ MySQL Exporter.

---

## 11. Logging

Hệ thống sử dụng:

```text
Docker
   |
   v
Promtail
   |
   v
Loki
   |
   v
Grafana Explore
```

Promtail thu thập Docker logs và gửi đến Loki.

Một số truy vấn LogQL:

```logql
{container=~".+"}
```

```logql
{container="student_web"}
```

```logql
{container="student_nginx"}
```

```logql
{container="student_mysql"}
```

Có thể sử dụng Grafana Explore để xem và phân tích logs.

---

## 12. Reverse Proxy và HTTPS

Nginx được sử dụng làm reverse proxy cho ứng dụng Django.

Luồng truy cập:

```text
Client
   |
   | HTTPS :8443
   v
Nginx
   |
   | HTTP :8000
   v
Django
```

Nginx cấu hình các security headers:

```text
X-Frame-Options
X-Content-Type-Options
Referrer-Policy
Cross-Origin-Opener-Policy
```

Kiểm tra HTTPS:

```powershell
curl.exe -k -I https://localhost:8443
```

---

## 13. Hardening

Các biện pháp bảo mật được triển khai:

### 13.1. Chạy container non-root

Django container chạy bằng user ứng dụng thay vì `root`.

### 13.2. Cô lập backend network

Backend network được cấu hình:

```yaml
internal: true
```

### 13.3. Không expose MySQL ra host

MySQL không publish port `3306` ra máy host.

### 13.4. Quản lý secrets bằng biến môi trường

Thông tin nhạy cảm được lưu trong `.env`.

### 13.5. Không commit secrets

Các file chứa secrets được thêm vào `.gitignore`:

```text
.env
monitoring/.my.cnf
```

### 13.6. HTTPS và Security Headers

Nginx sử dụng HTTPS và các security headers để tăng cường bảo vệ ứng dụng.

---

## 14. Kiểm tra hệ thống

Kiểm tra container:

```powershell
docker compose ps
```

Kiểm tra logs:

```powershell
docker compose logs --tail 50
```

Kiểm tra MySQL:

```powershell
docker exec student_mysql mysql -u student_user -p
```

Kiểm tra MySQL Exporter:

```powershell
docker exec student_mysql_exporter wget -qO- http://localhost:9104/metrics
```

Kiểm tra HTTPS:

```powershell
curl.exe -k -I https://localhost:8443
```

---

## 15. Git Workflow

Kiểm tra trạng thái:

```powershell
git status
```

Thêm thay đổi:

```powershell
git add .
```

Commit:

```powershell
git commit -m "message"
```

Push lên GitHub:

```powershell
git push origin master
```

Xem lịch sử commit:

```powershell
git log --oneline
```

---

## 16. Repository

GitHub Repository:

https://github.com/tathuyquynh392-jpg/QuanLySinhVien

---

## 17. Thông tin sinh viên

- Họ và tên: Tạ Thị Thúy Quỳnh
- MSSV: DTC245280022
- Lớp: CNTT K23A
- Học phần: Triển khai và Quản trị Hệ thống
- Năm học: 2026
