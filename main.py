import sqlite3

con = sqlite3.connect('DB.db')
cursor = con.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Equipments (
        ID_com INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        total_number INTEGER NOT NULL,
        not_used_number INTEGER NOT NULL
    )
''')
con.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        ID_us INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        foun_numb TEXTNOT NULL,
        ID_equip_thet_he_used INTEGER,
        FOREIGN KEY (ID_equip_thet_he_used) REFERENCES Equipments (ID_com)
    )
''')
con.commit()

# Додавання даних до таблиці Equipments
def insert_equipment(name, description, total_number, not_used_number):
    cursor.execute('''
        INSERT INTO Equipments (name, description, total_number, not_used_number)
        VALUES (?, ?, ?, ?) ''', (name, description, total_number, not_used_number))
    con.commit()

# Додавання користувача
def insert_user(name, foun_numb, ID_equip_thet_he_used):
    cursor.execute('''
        INSERT INTO Users (name, foun_numb, ID_equip_thet_he_used)
        VALUES (?, ?, ?)''', (name, foun_numb, ID_equip_thet_he_used))
    con.commit()
    cursor.execute('''
         UPDATE Equipments
         SET not_used_number = not_used_number - 1
         WHERE ID_com = ?''', (ID_equip_thet_he_used,))
    con.commit()

# заміна поточного обладнання
def edit_user_equipment(user_id, new_equipment_id):
    cursor.execute('''
         SELECT ID_equip_thet_he_used FROM Users
         WHERE ID_us = ?
     ''', (user_id,))
    current_equipment_id = cursor.fetchone()[0]
    cursor.execute('''
           UPDATE Users
           SET ID_equip_thet_he_used = ?
           WHERE ID_us = ?
       ''', (new_equipment_id, user_id))
    cursor.execute('''
            UPDATE Equipments
            SET not_used_number = not_used_number + 1
            WHERE ID_com = ?
        ''', (current_equipment_id,))
    cursor.execute('''
            UPDATE Equipments
            SET not_used_number = not_used_number - 1
            WHERE ID_com = ?
        ''', (new_equipment_id,))
    conn.commit()

def delete_user(user_id):
    cursor.execute('''
        SELECT ID_equip_thet_he_used FROM Users
        WHERE ID_us = ?
    ''', (user_id,))
    equipment_id = cursor.fetchone()[0]
    cursor.execute('''
        DELETE FROM Users
        WHERE ID_us = ?
    ''', (user_id,))
    cursor.execute('''
        UPDATE Equipments
        SET not_used_number = not_used_number + 1
        WHERE ID_com = ?
    ''', (equipment_id,))

def display_data_equipments():
    print("Data from Equipments table:")
    cursor.execute(f'SELECT * FROM Equipments')
    data = cursor.fetchall()
    for row in data:
        print(row)

def display_data_usrs():
    print("Data from Users table:")
    cursor.execute(f'SELECT * FROM Users')
    data = cursor.fetchall()
    for row in data:
        print(row)

# Додати обладнання до таблиці equipments (назва, опис, загальна кількість, кількість на складі)
#insert_equipment('Нетбук', 'Компактний', 10, 10)

# Додати користувача до таблиці users(імя, номер телефону, ід обладнання)
#insert_user('Петро', '021548', 1)

# Змінити пристрій для користувача(ід користувача, ід нового обладнання) старе обладнання повертається на склад
#edit_user_equipment(1, 2)

# Видалити користувача з таблиці
#delete_user(1)

# Показати таблицю Equipments
#display_data_equipments()

# Показати таблицю usrs
#display_data_usrs()


con.commit()
con.close()