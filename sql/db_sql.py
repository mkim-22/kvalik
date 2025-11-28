import pymysql.cursors


def get_db():
    return pymysql.connect(
        host='localhost',
        database='tich',
        user='root',
        password='root',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_reg(login, password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE login = %s", (login,))
            if cursor.fetchone():
                return False, 'Логин уже существует'
            cursor.execute("INSERT INTO users (login, password, role) VALUES(%s, %s,'client')", (login, password))
            db.commit()
            return True, "Успешно"
    except Exception as e:
        return False, f'Ошибка{e}'
    finally:
        db.close()


def get_login(login, password):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT role FROM users WHERE login = %s AND password = %s", (login, password))
            suc = cursor.fetchone()
            if suc:
                return True, suc['role']
            return False, None
    except Exception as e:
        return False, None

    finally:
        db.close()


# ===============================================================
# Получение всех броней (для QTableView)
# ===============================================================
def get_all_bookings():
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM bookings")
            return cursor.fetchall()
    finally:
        db.close()


# ===============================================================
# Фильтрация по датам
# ===============================================================
def get_bookings_by_date_range(date_from, date_to):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM bookings
                WHERE check_in >= %s AND check_out <= %s
            """, (date_from, date_to))
            return cursor.fetchall()
    finally:
        db.close()



# ===============================================================
# Добавление брони
# ===============================================================
def add_booking(guest_id, room_id, check_in, check_out, price, created_by="user"):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO bookings (guest_id, room_id, check_in, check_out, price, created_by, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Забронировано')
            """, (guest_id, room_id, check_in, check_out, price, created_by))
            db.commit()
            return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        db.close()


# ===============================================================
# Удаление брони
# ===============================================================
def delete_booking(booking_id):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
            db.commit()
            return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        db.close()


# ===============================================================
# Изменение статуса
# ===============================================================
def update_booking(booking_id, room_id, price):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE bookings
                SET room_id = %s, price = %s
                WHERE id = %s
            """, (room_id, price, booking_id))
            db.commit()
            return True
    except:
        return False
    finally:
        db.close()


# ===============================================================
# Получить одну бронь
# ===============================================================
def get_booking_by_id(booking_id):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
            return cursor.fetchone()
    finally:
        db.close()
