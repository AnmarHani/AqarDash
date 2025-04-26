import sqlite3
from datetime import datetime

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Marketer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        marketer_type TEXT NOT NULL CHECK (marketer_type IN ('وسيط', 'بائع')),
        email TEXT,
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (admin_id) REFERENCES Admin(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RealEstate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        announcement_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        property_type TEXT NOT NULL CHECK (property_type IN ('تجاري', 'صناعي', 'زراعي', 'سكني')),
        property_scale TEXT NOT NULL CHECK (property_scale IN ('فيلا', 'عمارة', 'شقة', 'قصر')),
        area REAL NOT NULL,
        category TEXT NOT NULL CHECK (category IN ('عوائل', 'افراد')),
        floors INTEGER,
        bedrooms INTEGER,
        bathrooms INTEGER,
        living_rooms INTEGER,
        price REAL NOT NULL,
        region TEXT NOT NULL,
        district TEXT NOT NULL,
        city TEXT NOT NULL,
        location_link TEXT,
        source_link TEXT,
        location_details TEXT,
        description TEXT,
        status TEXT NOT NULL CHECK (status IN ('متاح', 'محجوز', 'مباع')),
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (admin_id) REFERENCES Admin(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Buyer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        budget REAL NOT NULL,
        interests TEXT,
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (admin_id) REFERENCES Admin(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MarketerRealEstate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marketer_id INTEGER NOT NULL,
        real_estate_id INTEGER NOT NULL,
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (marketer_id) REFERENCES Marketer(id),
        FOREIGN KEY (real_estate_id) REFERENCES RealEstate(id),
        FOREIGN KEY (admin_id) REFERENCES Admin(id),
        UNIQUE(marketer_id, real_estate_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BuyerRealEstate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER NOT NULL,
        real_estate_id INTEGER NOT NULL,
        admin_id INTEGER NOT NULL,
        FOREIGN KEY (buyer_id) REFERENCES Buyer(id),
        FOREIGN KEY (real_estate_id) REFERENCES RealEstate(id),
        FOREIGN KEY (admin_id) REFERENCES Admin(id),
        UNIQUE(buyer_id, real_estate_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('aqardash.db')

def recreate_db():
    """Drop all tables and recreate them with the updated schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop all tables
    cursor.execute("DROP TABLE IF EXISTS BuyerRealEstate")
    cursor.execute("DROP TABLE IF EXISTS MarketerRealEstate")
    cursor.execute("DROP TABLE IF EXISTS Buyer")
    cursor.execute("DROP TABLE IF EXISTS RealEstate")
    cursor.execute("DROP TABLE IF EXISTS Marketer")
    cursor.execute("DROP TABLE IF EXISTS Admin")
    
    # Recreate tables
    init_db()
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database has been initialized with the new schema.") 