# Sistem Mimarisi ve Veri Modeli

## 1. Mimari Yapı
- **Backend:** Python 3.11 & Flask Web Framework
- **Veritabanı:** SQLite (gym.db)
- **Konteynerleştirme:** Docker
- **CI/CD:** GitHub Actions (Otomatik Pytest)
- **Cloud Platform:** Render (PaaS)

## 2. Veri Modeli (members Tablosu)
| Alan Adı | Veri Tipi | Açıklama |
| :--- | :--- | :--- |
| id | INTEGER (PK) | Otomatik artan benzersiz üye numarası |
| 
ame | TEXT | Üyenin adı ve soyadı |
| plan | TEXT | Üyelik paketi (1 Aylık, 3 Aylık, 12 Aylık) |
| end_date | TEXT | Üyelik bitiş tarihi (YYYY-MM-DD) |
