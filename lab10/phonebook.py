import psycopg2 # для работы бд
import csv
import re

#подключение к бд
conn = psycopg2.connect(
    dbname="phonebook",
    user="rrovi1",
    password="15Rodionmagic",
    host="38.244.137.21",
    port="5432"
)
cur = conn.cursor() #создаем курсор


#----------------------------------------------------------------Insert----------------------------------------------------------------------------------
#вставка
def insert(): 
    name = input("Enter name: ") #вводим имя
    phone = input("Enter phone: ") #вводим телефон
    cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone)) #вставляем в таблицу
    conn.commit() #коммитим изменения
    print("Data inserted") #выводим сообщение 

#вставить с файла
def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile: #открываем файл
        reader = csv.reader(csvfile) #читаем файл
        for row in reader: #проходим по строкам
            name, phone = row #разделяем строку на имя и телефон
            cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone)) #вставляем в таблицу
            conn.commit() #коммитим изменения

    print("CSV upload complete.")

#-------------------------------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------Update---------------------------------------------------------------------------------
# обновление данных
def update_data(): 
    field = input("What do you want to update? (name/phone): ").strip().lower() #поле для обновления (автоматически приводим к нижнему регистру)
    if field == "name": #если имя
        phone = input("Enter existing phone number: ") #вводим телефон
        new_name = input("Enter new name: ") #вводим новое имя
        cur.execute("UPDATE phonebook SET first_name = %s WHERE phone_number = %s", (new_name, phone)) #обновляем имя по телефону
    elif field == "phone": #если телефон
        name = input("Enter existing name: ") #вводим имя
        new_phone = input("Enter new phone: ") #вводим новый телефон
        cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, name)) #обновляем телефон по имени
    print("Data updated")


#-----------------------------------------------------------------------------------------------------------------------------------------------------






#---------------------------------------------------------------Query---------------------------------------------------------------------------------
def query_data(): # запрос данных
    option = input("Choose filter: all/by-name/by-phone ").strip().lower() #выбираем фильтр (автоматически приводим к нижнему регистру)
    if option == "all": #если все
        cur.execute("SELECT * FROM phonebook") #выбираем все данные
        rows = cur.fetchall() # получаем все строки

        if not rows: # если нет строк
            print("Phonebook is empty!") #выводим сообщение
            return 

        print("\nAll Contacts") #рисуем текст
        print("=" * 40) #разделитель
        print(f"{'ID':<5} {'Name':<20} {'Phone':<15}") #выводим заголовки
        print("-" * 40) #разделитель

        for row in rows: #проходим по строкам
            name = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9 ]', '', row[1])  # убираем спец символы
            phone = re.sub(r'\D', '', row[2])  # только цифры
            print(f"{row[0]:<5} {name:<20} {phone:<15}") 


    elif option == "by-name":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", ('%' + name + '%',))
        rows = cur.fetchall() # получаем все строки

        if not rows:
            print("Phonebook is empty!")
            return

        print("\nAll Contacts")
        print("=" * 40)
        print(f"{'ID':<5} {'Name':<20} {'Phone':<15}")
        print("-" * 40)

        for row in rows:
            name = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9 ]', '', row[1])  # убираем спец символы
            phone = re.sub(r'\D', '', row[2])  # только цифры
            print(f"{row[0]:<5} {name:<20} {phone:<15}") 
    elif option == "by-phone":
        phone = input("Enter phone part: ")
        cur.execute("SELECT * FROM phonebook WHERE phone_number LIKE %s", ('%' + phone + '%',))
        rows = cur.fetchall() # получаем все строки

        if not rows:
            print("Phonebook is empty!")
            return

        print("\nAll Contacts")
        print("=" * 40)
        print(f"{'ID':<5} {'Name':<20} {'Phone':<15}")
        print("-" * 40)

        for row in rows:
            name = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9 ]', '', row[1])  # убираем спец символы
            phone = re.sub(r'\D', '', row[2])  # только цифры
            print(f"{row[0]:<5} {name:<20} {phone:<15}") 
#---------------------------------------------------------------Query---------------------------------------------------------------------------------







#---------------------------------------------------------------Delete---------------------------------------------------------------------------------

def delete_data():
    data = input("Delete by (name/phone): ").strip().lower()
    if data == "name":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif data == "phone":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone,))
    conn.commit()
    print("Data deleted!")



#---------------------------------------------------------------------------------------------------------------------------------------------------------

# меню
def menu():
    while True:
        print("\n📞 PHONEBOOK MENU")
        print("1 - Insert from console")
        print("2 - Insert from CSV")
        print("3 - Update data")
        print("4 - Query data")
        print("5 - Delete data")
        print("0 - Exit")
        choice = input("Choose option: ")

        if choice == "1":
            insert()
        elif choice == "2":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "3":
            update_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "0":
            break
        else:
            print("Invalid option")

    cur.close()
    conn.close()

if __name__ == "__main__":
    menu()
#------------------------------------------------------------------------------------------------------------------------------------------------------