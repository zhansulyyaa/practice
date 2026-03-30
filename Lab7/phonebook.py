import psycopg2
import csv

# --- Подключение к базе ---
conn = psycopg2.connect(
    host="localhost",
    database="phonebook",
    user="postgres",
    password="12345678"  
)
cur = conn.cursor()

#Функции
def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Contact added!")

def upload_csv():
    filename = input("Enter CSV filename (example: contacts.csv): ")
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row[0], row[1]))
        conn.commit()
        print("CSV uploaded!")
    except FileNotFoundError:
        print("File not found!")

def update_contact():
    name = input("Enter username to update: ")
    new_phone = input("Enter new phone: ")
    cur.execute("UPDATE phonebook SET phone=%s WHERE username=%s", (new_phone, name))
    conn.commit()
    print("Updated!")

def search_contact():
    name = input("Enter username to search: ")
    cur.execute("SELECT * FROM phonebook WHERE username=%s", (name,))
    results = cur.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("No contact found.")

def delete_contact():
    name = input("Enter username to delete: ")
    cur.execute("DELETE FROM phonebook WHERE username=%s", (name,))
    conn.commit()
    print("Deleted!")
    
def show_all():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("PhoneBook is empty.")

def menu():
    print("\n--- PhoneBook Menu ---")
    print("1. Add contact from console")
    print("2. Upload contacts from CSV")
    print("3. Update contact")
    print("4. Search contact")
    print("5. Delete contact")
    print("6. Show all contacts")
    print("0. Exit")

#Основной цикл
while True:
    menu()
    choice = input("Choose option: ")
    if choice == "1":
        add_contact()
    elif choice == "2":
        upload_csv()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        search_contact()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        show_all()
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")

#Закрыть соединение
cur.close()
conn.close()