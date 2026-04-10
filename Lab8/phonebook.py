from connect import connect

def create_table():
    """Create the phonebook table if it doesn't exist."""
    conn = connect()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    phone VARCHAR(20) NOT NULL
                );
            """)
            conn.commit()
        print("Table 'phonebook' is ready.")
    except Exception as error:
        print(error)
    finally:
        conn.close()


def ups():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()
    conn = connect()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_u(%s, %s)", (username, phone))
            conn.commit()
        print(f"User '{username}' upserted successfully.")
    except Exception as error:
        print(error)
    finally:
        conn.close()


def hz():
    print("Enter list of usernames and list of phones")
    print("Usernames: ", end="")
    u = input().split()
    print("Phones: ", end="")
    p = input().split()
    if len(u) != len(p):
        print("Error: number of usernames and phones must match.")
        return

    conn = connect()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL loophz(%s, %s)", (u, p))
        conn.commit()
        for notice in conn.notices:
            print(notice.strip())
        print("Lists inserted successfully.")
    except Exception as error:
        print(error)
    finally:
        conn.close()


def delete_contact():
    print("Delete by (1) username or (2) phone?")
    choice = input().strip()

    if choice == "1":
        param = input("Enter username: ").strip()
    elif choice == "2":
        param = input("Enter phone: ").strip()
    else:
        print("Invalid choice.")
        return

    conn = connect()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("CALL del_user(%s)", (param,))
            conn.commit()
        print("User deleted successfully.")
    except Exception as error:
        print(error)
    finally:
        conn.close()


def match_return():
    print("Write the username or phone part that you want to match.")
    a = input().strip()
    conn = connect()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM records(%s)", (a,))
            rows = cur.fetchall()
        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
        else:
            print("No matching contacts.")
    except Exception as error:
        print(error)
    finally:
        conn.close()


def pages():
    print("Enter limit: ", end="")
    lim = int(input().strip())
    print("Enter offset: ", end="")
    offs = int(input().strip())
    conn = connect()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM pagination(%s, %s)", (lim, offs))
            rows = cur.fetchall()
        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
        else:
            print("No results.")
    except Exception as error:
        print(error)
    finally:
        conn.close()


def main():
    while True:
        print("\n1. Create table")
        print("2. Upsert user")
        print("3. Insert list of users and phones")
        print("4. Delete contact")
        print("5. Return matching records")
        print("6. Paginated data")
        print("7. Exit")

        try:
            a = int(input("\nChoice: ").strip())
            if   a == 1: create_table()
            elif a == 2: ups()
            elif a == 3: hz()
            elif a == 4: delete_contact()
            elif a == 5: match_return()
            elif a == 6: pages()
            elif a == 7:
                print("Bye!")
                return
            else:
                print("Try again!")
                continue
        except ValueError:
            print("Please enter a number.")
            continue

        print("\nWould you like to continue? y/n")
        while True:
            a = input().strip()
            if a == "y":
                break
            elif a == "n":
                print("Bye!")
                return
            else:
                print("Try again!")


main()
