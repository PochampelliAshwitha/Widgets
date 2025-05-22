import psycopg2

# Your Aiven PostgreSQL connection string
DB_URI = 'postgres://avnadmin:AVNS_2_65ikq6jVV8ip2LWI0@pg-c11a32f-uniqueanonymous2516-46a0.k.aivencloud.com:17972/Users?sslmode=require'

def setup_database():
    try:
        # Connect to the database
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')

        # Insert default admin user (only if not exists)
        cur.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            ON CONFLICT (username) DO NOTHING;
        ''', ('admin', 'admin'))

        conn.commit()
        print("✅ Table created and admin user inserted.")
    
    except Exception as e:
        print("❌ Error:", e)
    
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()


# import psycopg2

# # Connect to your Aiven PostgreSQL instance (to any existing DB like defaultdb)
# DB_URI = 'postgres://avnadmin:AVNS_2_65ikq6jVV8ip2LWI0@pg-c11a32f-uniqueanonymous2516-46a0.k.aivencloud.com:17972/defaultdb?sslmode=require'

# def list_databases():
#     try:
#         conn = psycopg2.connect(DB_URI)
#         cur = conn.cursor()
#         cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
#         databases = cur.fetchall()
#         print("📂 Databases:")
#         for db in databases:
#             print(" -", db[0])
#     except Exception as e:
#         print("❌ Error listing databases:", e)
#     finally:
#         if 'cur' in locals():
#             cur.close()
#         if 'conn' in locals():
#             conn.close()

# if __name__ == "__main__":
#     list_databases()

# import psycopg2

# DB_URI = 'postgres://avnadmin:AVNS_2_65ikq6jVV8ip2LWI0@pg-c11a32f-uniqueanonymous2516-46a0.k.aivencloud.com:17972/defaultdb?sslmode=require'

# def truncate_all_tables():
#     try:
#         # Connect to your database
#         conn = psycopg2.connect(DB_URI)
#         conn.autocommit = True  # We need autocommit for DDL commands
#         cursor = conn.cursor()

#         # Get all the table names in the public schema
#         cursor.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
#         """)
#         tables = cursor.fetchall()

#         # Loop through the tables and truncate each one
#         for table in tables:
#             table_name = table[0]
#             print(f"Truncating table: {table_name}")
#             try:
#                 cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
#                 print(f"✅ Truncated table: {table_name}")
#             except Exception as e:
#                 print(f"❌ Could not truncate {table_name}: {e}")

#     except Exception as e:
#         print("❌ Error:", e)
#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()

# if __name__ == "__main__":
#     truncate_all_tables()
