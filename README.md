# 📒 NoteApp – Flask Notes Management System

NoteApp là ứng dụng quản lý ghi chú (Notes) viết bằng **Flask**, hỗ trợ người dùng đăng ký – đăng nhập – tạo ghi chú – phân loại theo Tag. Ứng dụng cũng có **Admin Dashboard** cho phép quản trị người dùng, quản lý ghi chú và tag.

---

## 🚀 Chức năng chính

### 👤 Người dùng

* Đăng ký tài khoản
* Đăng nhập / đăng xuất
* Tạo ghi chú
* Chỉnh sửa ghi chú
* Xoá ghi chú
* Gán tag cho ghi chú
* Xem chi tiết ghi chú

### 🛠️ Admin

* Quản lý tất cả người dùng
* Thêm / xoá người dùng
* Quản lý tất cả note của mọi user
* Quản lý tag
* Xem ngày tạo & cập nhật của ghi chú

---

## 🗂️ Cấu trúc thư mục dự án

```
NOTEAPP/
├─ app/
│   ├─ routes/
│   │   ├─ auth.py          # Đăng ký / đăng nhập
│   │   ├─ notes.py         # CRUD Notes
│   │   └─ tags.py          # CRUD Tags
│   ├─ static/              # File CSS/JS (nếu có)
│   ├─ templates/
│   │   ├─ base.html
│   │   ├─ dashboard.html
│   │   ├─ edit_note.html
│   │   ├─ home.html
│   │   ├─ login.html
│   │   ├─ new_note.html
│   │   ├─ note_form.html
│   │   ├─ register.html
│   │   ├─ tag_form.html
│   │   ├─ tag_list.html
│   │   └─ view_note.html
│   ├─ admin.py             # Blueprint Admin
│   ├─ models.py            # Models SQLAlchemy
│   └─ __init__.py          # Khởi tạo Flask app
│
├─ migrations/              # Alembic migrations
├─ static/                  # (tuỳ chọn)
├─ .env                     # Cấu hình biến môi trường
├─ config.py                # Cấu hình Flask
├─ requirements.txt         # Danh sách thư viện Python
└─ run.py                   # File chạy chính
```

---

## ⚙️ Cài đặt

### 1️⃣ Clone dự án

```sh
git clone <URL>
cd NOTEAPP
```

### 2️⃣ Tạo môi trường ảo

```sh
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Cài đặt thư viện

```sh
pip install -r requirements.txt
```

### 4️⃣ Tạo file `.env`

```sh
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///noteapp.db
```

### 5️⃣ Khởi tạo database

```sh
flask db init
flask db migrate
flask db upgrade
```

---

## ▶️ Chạy ứng dụng

```sh
python run.py
```

Ứng dụng chạy tại:
👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🔐 Tạo tài khoản Admin

```sh
flask shell
```

```python
from app import db
from app.models import User

admin = User(username='admin', email='admin@example.com', role='admin')
admin.set_password('123456')
db.session.add(admin)
db.session.commit()
```

---

## 💾 Database Models

### User

* id
* username
* email
* password_hash
* role (user/admin)
* notes (relationship)

### Note

* id
* title
* content
* user_id
* created_at
* updated_at
* tags (many-to-many)

### Tag

* id
* name

---

## 🧩 Công nghệ sử dụng

* Flask
* Flask-Login
* Flask-Migrate
* SQLAlchemy
* Bootstrap 5

---