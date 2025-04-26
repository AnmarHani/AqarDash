import sqlite3
import os

def init_db():
    # Remove existing database if it exists
    if os.path.exists('aqardash.db'):
        os.remove('aqardash.db')
    
    # Create new database
    conn = sqlite3.connect('aqardash.db')
    cursor = conn.cursor()
    
    # Create Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create Marketer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Marketer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            marketer_type TEXT NOT NULL,
            email TEXT
        )
    ''')
    
    # Create RealEstate table with status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RealEstate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            announcement_date DATE NOT NULL,
            property_type TEXT NOT NULL,
            area REAL NOT NULL,
            category TEXT NOT NULL,
            floors INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            living_rooms INTEGER NOT NULL,
            price REAL NOT NULL,
            region TEXT NOT NULL,
            district TEXT NOT NULL,
            city TEXT NOT NULL,
            location_link TEXT,
            source_link TEXT,
            location_details TEXT,
            description TEXT,
            status TEXT NOT NULL CHECK (status IN ('متاح', 'تم البيع')),
            marketer_id INTEGER,
            FOREIGN KEY (marketer_id) REFERENCES Marketer(id)
        )
    ''')
    
    # Create Buyer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Buyer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            budget REAL NOT NULL,
            interests TEXT
        )
    ''')
    
    # Create BuyerRealEstate junction table for many-to-many relationship
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BuyerRealEstate (
            buyer_id INTEGER,
            real_estate_id INTEGER,
            PRIMARY KEY (buyer_id, real_estate_id),
            FOREIGN KEY (buyer_id) REFERENCES Buyer(id),
            FOREIGN KEY (real_estate_id) REFERENCES RealEstate(id)
        )
    ''')

    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 