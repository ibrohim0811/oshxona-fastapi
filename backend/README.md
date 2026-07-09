# 🍽 Restaurant Menu & Order API — Amaliy Vazifa

**Mavzu:** FastAPI | Faqat CRUD · Qo'lda SQL Query (ORM yo'q)
**Daraja:** O'rta
**Tavsiya etilgan vaqt:** 1-2 kun

---

## 🎯 Vazifa maqsadi

Restoran uchun menu va buyurtmalarni boshqaradigan REST API yarating. API faqat quyidagini qo'llab-quvvatlashi kerak:

- Modellar (jadvallar) bilan to'liq **CRUD** (Create, Read, Update, Delete)
- Ma'lumotlar bazasi bilan ishlash **faqat qo'lda yozilgan SQL query'lar** orqali

> ⚠️ **Muhim cheklovlar:**
> - **Hech qanday ORM ishlatilmaydi** — SQLAlchemy ORM, Tortoise, Django ORM va shu kabilar **taqiqlanadi**. Barcha so'rovlar qo'lda yoziladigan SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) orqali bajariladi.
> - Filter, search, ordering **kerak emas**.
> - Autentifikatsiya (JWT/Basic), permissions, user role'lar **kerak emas**.

---

## 🧱 1. Ma'lumotlar bazasi jadvallari (Tables)

Quyidagi jadvallarni `CREATE TABLE` SQL orqali qo'lda yarating.

### `categories`
| Ustun | Type | Izoh |
|-------|------|------|
| `id` | INTEGER / SERIAL | Primary key, auto increment |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL |
| `created_at` | TIMESTAMP | default — hozirgi vaqt |

### `menu_items`
| Ustun | Type | Izoh |
|-------|------|------|
| `id` | INTEGER / SERIAL | Primary key |
| `name` | VARCHAR(200) | NOT NULL |
| `description` | TEXT | NULL bo'lishi mumkin |
| `price` | NUMERIC(8, 2) | NOT NULL |
| `category_id` | INTEGER | FOREIGN KEY → `categories(id)` |
| `is_available` | BOOLEAN | default TRUE |
| `created_at` | TIMESTAMP | default — hozirgi vaqt |

### `orders`
| Ustun | Type | Izoh |
|-------|------|------|
| `id` | INTEGER / SERIAL | Primary key |
| `customer_name` | VARCHAR(150) | Buyurtma bergan mijoz ismi |
| `status` | VARCHAR(20) | qiymatlar: `pending`, `preparing`, `delivered`, `cancelled` (default `pending`) |
| `created_at` | TIMESTAMP | default — hozirgi vaqt |

### `order_items`
| Ustun | Type | Izoh |
|-------|------|------|
| `id` | INTEGER / SERIAL | Primary key |
| `order_id` | INTEGER | FOREIGN KEY → `orders(id)` |
| `menu_item_id` | INTEGER | FOREIGN KEY → `menu_items(id)` |
| `quantity` | INTEGER | default 1, > 0 |

> 💡 **Bonus:** `Order` ni o'qiyotganda `total_price` ni qo'shimcha SQL query orqali hisoblang
> (har bir `order_item` uchun `menu_items.price × order_items.quantity` yig'indisi —
> masalan `SUM(mi.price * oi.quantity)` ko'rinishida `JOIN` bilan).

---

## 🔌 2. Endpointlar — faqat CRUD

### Categories
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/categories/` | Barcha kategoriyalar |
| GET | `/categories/{id}/` | Bitta kategoriya |
| POST | `/categories/` | Yangi kategoriya |
| PUT/PATCH | `/categories/{id}/` | Kategoriyani o'zgartirish |
| DELETE | `/categories/{id}/` | Kategoriyani o'chirish |

### Menu Items
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/menu-items/` | Barcha taomlar |
| GET | `/menu-items/{id}/` | Bitta taom |
| POST | `/menu-items/` | Yangi taom |
| PUT/PATCH | `/menu-items/{id}/` | Taomni o'zgartirish |
| DELETE | `/menu-items/{id}/` | Taomni o'chirish |

### Orders
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/orders/` | Barcha buyurtmalar |
| GET | `/orders/{id}/` | Bitta buyurtma (ichidagi item'lari bilan) |
| POST | `/orders/` | Yangi buyurtma |
| PUT/PATCH | `/orders/{id}/` | Buyurtmani o'zgartirish (masalan status) |
| DELETE | `/orders/{id}/` | Buyurtmani o'chirish |

> Buyurtma yaratishda bir nechta `order_item` qabul qilishingiz mumkin (nested body),
> har birini alohida `INSERT` query bilan bazaga yozasiz.

---

## 🛠 3. Texnik talablar

### Framework va kutubxonalar
```bash
pip install fastapi uvicorn
# SQLite uchun — qo'shimcha kutubxona shart emas (standart `sqlite3`)
# PostgreSQL uchun:
pip install psycopg2-binary
```

### Ma'lumotlar bazasi
- **SQLite** (`sqlite3`) yoki **PostgreSQL** (`psycopg2`) dan birini tanlang.
- Ulanish va kursor (cursor) ni o'zingiz boshqarasiz.
- Har bir query qo'lda yoziladi. Misol:
```python
# SELECT misoli
cursor.execute("SELECT id, name, price FROM menu_items WHERE id = ?", (item_id,))
row = cursor.fetchone()

# INSERT misoli
cursor.execute(
    "INSERT INTO categories (name) VALUES (?)",
    (category.name,)
)
conn.commit()

# UPDATE misoli
cursor.execute(
    "UPDATE menu_items SET name = ?, price = ? WHERE id = ?",
    (data.name, data.price, item_id)
)
conn.commit()

# DELETE misoli
cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
conn.commit()
```

> ⚠️ **SQL injection'dan himoyalaning:** har doim parametrlangan query (`?` yoki `%s`)
> dan foydalaning, qiymatlarni stringga `f"...{value}..."` orqali yopishtirmang.

### Pydantic schema'lar
So'rov (request) va javob (response) uchun Pydantic modellarini ishlating:
- `CategoryCreate`, `CategoryOut`
- `MenuItemCreate`, `MenuItemOut`
- `OrderCreate` (ichida `order_items` ro'yxati), `OrderOut`

### Xatoliklar
- Topilmagan resurs uchun `404 Not Found` (`HTTPException`) qaytaring.
- Noto'g'ri ma'lumot uchun `400 Bad Request` qaytaring.

---

## ✅ 4. Topshirish talablari

1. Loyiha GitHub repositoriyada bo'lsin.
2. `requirements.txt` mavjud bo'lsin.
3. Jadvallarni yaratuvchi SQL (yoki init script) loyihada bo'lsin.
4. Loyiha `uvicorn main:app --reload` bilan ishga tushsin.
5. FastAPI avtomatik hujjatlari (`/docs` — Swagger UI) ishlasin.

---

## 🏆 Baholash mezonlari (100 ball)

| Bo'lim | Ball |
|--------|------|
| Jadvallar to'g'ri tuzilgan (SQL bilan) | 20 |
| Categories CRUD ishlaydi | 20 |
| Menu Items CRUD ishlaydi | 25 |
| Orders CRUD ishlaydi (item'lari bilan) | 25 |
| README + kod tozaligi | 10 |
| **Bonus:** `total_price` hisoblash, nested order yaratish | +10 |

---

## 💡 Bonus topshiriqlar (ixtiyoriy)

- `Order` yaratishda bitta so'rovda bir nechta `order_item` qo'shish (nested body + bir nechta `INSERT`).
- `GET /orders/{id}/` da `total_price` ni `JOIN` + `SUM` query orqali hisoblab qaytarish.
- Pagination (`LIMIT` / `OFFSET` SQL orqali).
- Buyurtmani o'chirganda unga tegishli order_items larni ham o'chirish (yoki `ON DELETE CASCADE`).

---

Omad! 🚀