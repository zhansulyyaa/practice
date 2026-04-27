import csv
import json
from connect import connect


def print_contacts(rows):
    if not rows:
        print("  (no results)")
        return
    for r in rows:
        print(f"  [{r[0]}] {r[1]}  email={r[2]}  bday={r[3]}  group={r[4]}")

def get_groups(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM groups ORDER BY name")
    return [row[0] for row in cur.fetchall()]

def get_or_create_group(cur, group_name):
    cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (group_name,))
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def create_tables():
    conn = connect()
    cur = conn.cursor()
    sql = open("schema.sql").read()
    cur.execute(sql)
    conn.commit()
    conn.close()
    print("Tables are ready.")

def run_procedures():
    conn = connect()
    cur = conn.cursor()
    sql = open("procedures.sql").read()
    cur.execute(sql)
    conn.commit()
    conn.close()
    print("Procedures loaded.")


def add_contact():
    username = input("Username: ").strip()
    email    = input("Email (leave blank to skip): ").strip() or None
    birthday = input("Birthday YYYY-MM-DD (leave blank to skip): ").strip() or None

    conn = connect()
    cur = conn.cursor()

    groups = get_groups(conn)
    print("Groups:", ", ".join(groups))
    group_name = input("Group (leave blank for 'Other'): ").strip() or "Other"
    group_id = get_or_create_group(cur, group_name)

    cur.execute("""
        INSERT INTO contacts (username, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO UPDATE
            SET email    = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
        RETURNING id
    """, (username, email, birthday, group_id))
    contact_id = cur.fetchone()[0]

    while True:
        phone = input("Phone number (leave blank to stop): ").strip()
        if not phone:
            break
        ptype = input("Type (home/work/mobile): ").strip() or "mobile"
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, ptype)
        )

    conn.commit()
    conn.close()
    print(f"Contact '{username}' saved.")


def add_phone():
    name  = input("Contact username: ").strip()
    phone = input("Phone number: ").strip()
    ptype = input("Type (home/work/mobile): ").strip() or "mobile"

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()
    conn.close()
    print("Phone added.")


def move_to_group():
    name  = input("Contact username: ").strip()
    group = input("New group name: ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    conn.close()
    print(f"Moved '{name}' to '{group}'.")


def delete_contact():
    name = input("Username to delete: ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE username = %s", (name,))
    conn.commit()
    conn.close()
    print(f"Deleted '{name}'.")


def search():
    query = input("Search (name / email / phone): ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    conn.close()
    print_contacts(rows)


def filter_by_group():
    conn = connect()
    groups = get_groups(conn)
    print("Available groups:", ", ".join(groups))
    group = input("Group name: ").strip()

    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.username
    """, (group,))
    rows = cur.fetchall()
    conn.close()
    print_contacts(rows)


def search_by_email():
    fragment = input("Email fragment: ").strip()

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
    """, (f"%{fragment}%",))
    rows = cur.fetchall()
    conn.close()
    print_contacts(rows)


def list_sorted():
    print("Sort by: (1) name  (2) birthday  (3) date added")
    choice = input("Choice: ").strip()
    order = {"1": "c.username", "2": "c.birthday", "3": "c.created_at"}.get(choice, "c.username")

    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.username, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order}
    """)
    rows = cur.fetchall()
    conn.close()
    print_contacts(rows)


def paginated_view():
    limit = 5
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        cur.execute("SELECT * FROM paginate_contacts(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print(f"\n--- Page (offset={offset}) ---")
        print_contacts(rows)

        options = []
        if offset > 0:
            options.append("prev")
        if len(rows) == limit:
            options.append("next")
        options.append("quit")

        cmd = input(f"[{'/'.join(options)}]: ").strip().lower()
        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

    conn.close()


def import_csv():
    path = input("CSV file path (default: contacts.csv): ").strip() or "contacts.csv"

    conn = connect()
    cur = conn.cursor()
    inserted = 0

    for row in csv.DictReader(open(path, newline="")):
        name     = row.get("name", "").strip()
        phone    = row.get("phone", "").strip()
        ptype    = row.get("phone_type", "mobile").strip() or "mobile"
        email    = row.get("email", "").strip() or None
        birthday = row.get("birthday", "").strip() or None
        group    = row.get("group", "Other").strip() or "Other"

        if not name or not phone:
            continue

        group_id = get_or_create_group(cur, group)

        cur.execute("""
            INSERT INTO contacts (username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO UPDATE
                SET email    = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
            RETURNING id
        """, (name, email, birthday, group_id))
        contact_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones (contact_id, phone, type)
            SELECT %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM phones WHERE contact_id = %s AND phone = %s
            )
        """, (contact_id, phone, ptype, contact_id, phone))
        inserted += 1

    conn.commit()
    conn.close()
    print(f"Imported {inserted} rows from '{path}'.")


def export_json():
    path = input("Output file (default: contacts.json): ").strip() or "contacts.json"

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday::TEXT, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.username
    """)
    contacts = cur.fetchall()

    result = []
    for cid, username, email, birthday, grp in contacts:
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
        phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
        result.append({"username": username, "email": email, "birthday": birthday, "group": grp, "phones": phones})

    conn.close()
    json.dump(result, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Exported {len(result)} contacts to '{path}'.")


def import_json():
    path = input("JSON file path (default: contacts.json): ").strip() or "contacts.json"
    data = json.load(open(path, encoding="utf-8"))

    conn = connect()
    cur = conn.cursor()

    for entry in data:
        username = entry.get("username", "").strip()
        if not username:
            continue

        cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
        existing = cur.fetchone()

        if existing:
            ans = input(f"'{username}' already exists. Overwrite? (y/n): ").strip().lower()
            if ans != "y":
                print(f"  Skipped '{username}'.")
                continue
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (existing[0],))

        group_id = get_or_create_group(cur, entry.get("group") or "Other")

        cur.execute("""
            INSERT INTO contacts (username, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO UPDATE
                SET email    = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
            RETURNING id
        """, (username, entry.get("email"), entry.get("birthday"), group_id))
        contact_id = cur.fetchone()[0]

        for p in entry.get("phones", []):
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, p.get("phone"), p.get("type", "mobile"))
            )
        print(f"  Imported '{username}'.")

    conn.commit()
    conn.close()
    print("JSON import complete.")

def main():
    while True:
        print("""
===== PhoneBook =====
 1. Setup (create tables + load procedures)
 2. Add / update contact
 3. Add phone to existing contact
 4. Move contact to group
 5. Delete contact
 6. Search (name / email / phone)
 7. Filter by group
 8. Search by email
 9. List contacts (sorted)
10. Browse pages
11. Import from CSV
12. Export to JSON
13. Import from JSON
 0. Exit
""")
        choice = input("Choice: ").strip()

        if   choice == "1":  create_tables(); run_procedures()
        elif choice == "2":  add_contact()
        elif choice == "3":  add_phone()
        elif choice == "4":  move_to_group()
        elif choice == "5":  delete_contact()
        elif choice == "6":  search()
        elif choice == "7":  filter_by_group()
        elif choice == "8":  search_by_email()
        elif choice == "9":  list_sorted()
        elif choice == "10": paginated_view()
        elif choice == "11": import_csv()
        elif choice == "12": export_json()
        elif choice == "13": import_json()
        elif choice == "0":
            print("Closed")
            break
        else:
            print("Invalid choice, try again.")

main()