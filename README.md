# SelfCareBalance - סיכום התקדמות הפיתוח

אפליקציה למעקב מצב רוח וטיפול עצמי בגישה מבוססת CBT, מבוססת על **FastAPI**, מסד נתונים **MongoDB** עם Beanie, ותהליך עבודה מבוסס GIT מקצועי.

---

## ✅ פיצ'רים שבוצעו

### 🔐 התחברות והרשמה (`/auth`)

- `POST /auth/register`: הרשמה עם אימייל, שם משתמש וסיסמה (בהצפנה)
- `POST /auth/login`: התחברות באמצעות JWT
- `GET /auth/me`: נקודת קצה מוגנת שמחזירה את המשתמש המחובר
- הצפנת סיסמאות עם `passlib`
- ניהול JWT עם `python-jose`

### 🧠 מעקב מצב רוח (`/mood`)

- `POST /mood/add`: הוספת רשומת מצב רוח חדשה (למשתמש מחובר)
- `GET /mood/my`: שליפת כל רשומות המשתמש המחובר
- `GET /mood/emotions`: רשימה קבועה של רגשות חיוביים ושליליים (בעברית)
- `PUT /mood/{id}`: עריכת רשומת מצב רוח (רק על ידי הבעלים)

---

## 📁 מודלים במסד הנתונים

### `User` (מסמך Beanie)

- `username`, `email`, `hashed_password`, `created_at`

### `MoodEntry` (מסמך Beanie)

- `user` (קישור ל־User)
- `mood_score` (ציון בין 1 ל־10)
- `emotions` (רשימת רגשות)
- `reasons`, `note`
- `created_at`

---

## 🔒 אבטחה ובקרת גישה

- כל הנתיבים הרגישים מוגנים עם JWT (`Depends(get_current_user)`)
- בדיקת בעלות על רשומות באמצעות `fetch_link()` לפני עריכה

---

## 📚 סכמות (Schemas)

- `RegisterRequest`, `LoginRequest`, `TokenResponse`, `UserResponse`
- `MoodEntryCreate`, `MoodEntryUpdate`, `MoodEntryResponse`

---

## 🛠️ תהליך עבודה עם GIT

- עבודה לפי ענפים לכל פיצ'ר
- כל פיצ'ר מוזג ל־`develop` דרך Pull Request מתועד
- `main` נשאר יציב ונקי

---

## 🔄 פיצ'רים בהמשך

- `DELETE /mood/{id}`: מחיקת רשומות מצב רוח
- ניהול רגשות דינמי דרך ממשק ניהול (בעתיד)
- גרפים ותובנות מתוך היסטוריית מצבי רוח

---

## 🧠 הערות

- רשימת הרגשות סטטית בשלב זה — תעבור למסד נתונים עם ניהול בהמשך
- כל הפיצ'רים נבדקו דרך Swagger UI ו־Postman
- שימוש בקובץ `.env` עבור URI של MongoDB ו־JWT SECRET

---

## הרצה

- .venv\Scripts\activate
- uvicorn app.main:app --reload

_עודכן לאחרונה: 29 באפריל 2025_
