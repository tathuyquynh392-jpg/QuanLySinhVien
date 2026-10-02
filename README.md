# Hệ thống quản lý sinh viên

Hệ thống quản lý sinh viên được xây dựng phục vụ học phần **Triển khai và Quản trị Hệ thống**.

Hệ thống hỗ trợ quản lý sinh viên, lớp học và điểm số, đồng thời triển khai cơ sở dữ liệu, reverse proxy, monitoring, logging và các biện pháp hardening bằng Docker Compose.

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

Hệ thống gồm các thành phần chính:

```text
                    Client
                       |
                       v
                +-------------+
                |    Nginx    |
                | HTTPS :8443 |
                +------+------+
                       |
                       v
                +-------------+
                |    Django   |
                | student_web |
                +------+------+
                       |
                       v
                +-------------+
                |    MySQL    |
                | student_mysql|
                +-------------+

Monitoring:
Prometheus -> cAdvisor
Prometheus -> MySQL Exporter
Grafana    -> Prometheus

Logging:
Docker -> Promtail -> Loki -> Grafana
