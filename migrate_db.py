import sqlite3
print("--- Running Database Migration Script ---")

try:
    conn = sqlite3.connect('discussion.db')
    cursor = conn.cursor()

    # Check for is_pinned column
    cursor.execute("PRAGMA table_info(posts)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'is_pinned' not in columns:
        print("Column 'is_pinned' not found. Adding it now...")
        cursor.execute('ALTER TABLE posts ADD COLUMN is_pinned INTEGER DEFAULT 0 NOT NULL')
        print("'is_pinned' column added successfully.")
    else:
        print("'is_pinned' column already exists.")

    # Check for is_resolved column
    cursor.execute("PRAGMA table_info(posts)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'is_resolved' not in columns:
        print("Column 'is_resolved' not found. Adding it now...")
        cursor.execute('ALTER TABLE posts ADD COLUMN is_resolved INTEGER DEFAULT 0 NOT NULL')
        print("'is_resolved' column added successfully.")
    else:
        print("'is_resolved' column already exists.")

    conn.commit()
    conn.close()
    print("--- Migration script finished successfully! ---")

except sqlite3.Error as e:
    print(f"A database error occurred: {e}")