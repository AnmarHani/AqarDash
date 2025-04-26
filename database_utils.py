from database import get_db_connection
from typing import List, Dict, Any, Optional, Union, Tuple
import sqlite3
import os

def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect('aqardash.db')

def execute_query(query: str, params: List[Any] = None) -> List[tuple]:
    """Execute a query and return results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()

def execute_update(query: str, params: List[Any]) -> int:
    """Execute an update query and return the last row ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def execute_delete(query: str, params: List[Any]) -> None:
    """Execute a delete query."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    finally:
        conn.close()

def register_admin(username: str, password: str) -> Tuple[bool, str]:
    """Register a new admin user."""
    try:
        # Check if user already exists
        existing_user = execute_query(
            "SELECT id FROM Admin WHERE username = ?",
            [username]
        )
        
        if existing_user:
            print(f"Registration failed: Username '{username}' already exists")
            return False, "اسم المستخدم موجود بالفعل"
        
        # Register new user
        execute_update(
            "INSERT INTO Admin (username, password) VALUES (?, ?)",
            [username, password]
        )
        print(f"Successfully registered user: {username}")
        return True, "تم تسجيل المستخدم بنجاح"
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("Registration failed: Admin table does not exist")
            return False, "الجدول غير موجود. يرجى تهيئة قاعدة البيانات أولاً"
        print(f"Registration failed with error: {str(e)}")
        return False, f"حدث خطأ: {str(e)}"
    except Exception as e:
        print(f"Registration failed with unexpected error: {str(e)}")
        return False, f"حدث خطأ غير متوقع: {str(e)}"

def verify_admin(username: str, password: str) -> Tuple[bool, Optional[int]]:
    """Verify admin credentials and return (success, admin_id)."""
    try:
        result = execute_query(
            "SELECT id FROM Admin WHERE username = ? AND password = ?",
            [username, password]
        )
        if len(result) > 0:
            admin_id = result[0][0]
            print(f"Login successful for user: {username} with ID: {admin_id}")
            return True, admin_id
        else:
            print(f"Login failed for user: {username} - Invalid credentials")
            return False, None
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("Login failed: Admin table does not exist")
            return False, None
        print(f"Login failed with error: {str(e)}")
        raise e

# Real Estate functions
def search_properties(admin_id, search_term=None, property_type=None, min_price=None, max_price=None, min_area=None, max_area=None, city=None, district=None):
    """Search for properties with various filters"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM RealEstate 
            WHERE admin_id = ?
        """
        params = [admin_id]
        
        if search_term:
            query += " AND (title LIKE ? OR description LIKE ? OR location_details LIKE ?)"
            params.extend([f"%{search_term}%"] * 3)
        
        if property_type:
            query += " AND property_type = ?"
            params.append(property_type)
        
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        
        if min_area is not None:
            query += " AND area >= ?"
            params.append(min_area)
        
        if max_area is not None:
            query += " AND area <= ?"
            params.append(max_area)
        
        if city:
            query += " AND city = ?"
            params.append(city)
        
        if district:
            query += " AND district = ?"
            params.append(district)
        
        cursor.execute(query, params)
        properties = cursor.fetchall()
        
        return properties
    except Exception as e:
        print(f"Error searching properties: {str(e)}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def add_property(property_data: dict) -> int:
    """Add a new property"""
    query = """
    INSERT INTO RealEstate (
        title, property_type, property_scale, area, category,
        floors, bedrooms, bathrooms, living_rooms, price,
        region, district, city, location_link, source_link,
        location_details, description, status, admin_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = [
        property_data['title'],
        property_data['property_type'],
        property_data['property_scale'],
        property_data['area'],
        property_data['category'],
        property_data['floors'],
        property_data['bedrooms'],
        property_data['bathrooms'],
        property_data['living_rooms'],
        property_data['price'],
        property_data['region'],
        property_data['district'],
        property_data['city'],
        property_data['location_link'],
        property_data['source_link'],
        property_data['location_details'],
        property_data['description'],
        property_data['status'],
        property_data['admin_id']
    ]
    return execute_update(query, params)

def update_property(property_data):
    """Update an existing property"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE RealEstate
            SET title = ?, property_type = ?, property_scale = ?, area = ?,
                category = ?, floors = ?, bedrooms = ?, bathrooms = ?,
                living_rooms = ?, price = ?, region = ?, district = ?,
                city = ?, location_link = ?, source_link = ?,
                location_details = ?, description = ?, status = ?
            WHERE id = ? AND admin_id = ?
        """, (
            property_data['title'],
            property_data['property_type'],
            property_data['property_scale'],
            property_data['area'],
            property_data['category'],
            property_data['floors'],
            property_data['bedrooms'],
            property_data['bathrooms'],
            property_data['living_rooms'],
            property_data['price'],
            property_data['region'],
            property_data['district'],
            property_data['city'],
            property_data['location_link'],
            property_data['source_link'],
            property_data['location_details'],
            property_data['description'],
            property_data['status'],
            property_data['id'],
            property_data['admin_id']
        ))
        conn.commit()
    except Exception as e:
        print(f"Error updating property: {str(e)}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()

def delete_property(property_id, admin_id=1):
    """Delete a property"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First delete associated records
        cursor.execute("DELETE FROM MarketerRealEstate WHERE real_estate_id = ? AND admin_id = ?", (property_id, admin_id))
        cursor.execute("DELETE FROM BuyerRealEstate WHERE real_estate_id = ? AND admin_id = ?", (property_id, admin_id))
        # Then delete the property
        cursor.execute("DELETE FROM RealEstate WHERE id = ? AND admin_id = ?", (property_id, admin_id))
        conn.commit()
    except Exception as e:
        print(f"Error deleting property: {str(e)}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()

# Buyer functions
def search_buyers(admin_id, search_term=None, min_budget=None, max_budget=None, preferred_city=None):
    """Search for buyers with various filters"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM Buyer 
            WHERE admin_id = ?
        """
        params = [admin_id]
        
        if search_term:
            query += " AND (name LIKE ? OR phone LIKE ? OR email LIKE ? OR interests LIKE ?)"
            params.extend([f"%{search_term}%"] * 4)
        
        if min_budget is not None:
            query += " AND budget >= ?"
            params.append(min_budget)
        
        if max_budget is not None:
            query += " AND budget <= ?"
            params.append(max_budget)
        
        if preferred_city:
            query += " AND preferred_city = ?"
            params.append(preferred_city)
        
        cursor.execute(query, params)
        buyers = cursor.fetchall()
        
        return buyers
    except Exception as e:
        print(f"Error searching buyers: {str(e)}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def add_buyer(buyer_data: dict) -> int:
    """Add a new buyer"""
    query = """
    INSERT INTO Buyer (
        name, phone, email, budget, interests, admin_id
    ) VALUES (?, ?, ?, ?, ?, ?)
    """
    params = [
        buyer_data['name'],
        buyer_data['phone'],
        buyer_data['email'],
        buyer_data['budget'],
        buyer_data['interests'],
        buyer_data['admin_id']
    ]
    return execute_update(query, params)

def update_buyer(buyer_data):
    """Update an existing buyer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Buyer
            SET name = ?, phone = ?, email = ?, budget = ?,
                preferred_region = ?, preferred_district = ?,
                preferred_city = ?, interests = ?
            WHERE id = ? AND admin_id = ?
        """, (
            buyer_data['name'],
            buyer_data['phone'],
            buyer_data['email'],
            buyer_data['budget'],
            buyer_data['preferred_region'],
            buyer_data['preferred_district'],
            buyer_data['preferred_city'],
            buyer_data['interests'],
            buyer_data['id'],
            buyer_data['admin_id']
        ))
        conn.commit()
    finally:
        conn.close()

def delete_buyer(buyer_id, admin_id=1):
    """Delete a buyer"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First delete associated records
        cursor.execute("DELETE FROM BuyerRealEstate WHERE buyer_id = ? AND admin_id = ?", (buyer_id, admin_id))
        # Then delete the buyer
        cursor.execute("DELETE FROM Buyer WHERE id = ? AND admin_id = ?", (buyer_id, admin_id))
        conn.commit()
    except Exception as e:
        print(f"Error deleting buyer: {str(e)}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()

# Marketer functions
def search_marketers(admin_id, search_term=None, city=None):
    """Search for marketers with various filters"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT id, name, phone, email, marketer_type, admin_id 
            FROM Marketer 
            WHERE admin_id = ?
        """
        params = [admin_id]
        
        if search_term:
            query += " AND (name LIKE ? OR phone LIKE ? OR email LIKE ? OR marketer_type LIKE ?)"
            params.extend([f"%{search_term}%"] * 4)
        
        cursor.execute(query, params)
        marketers = cursor.fetchall()
        
        return marketers
    except Exception as e:
        print(f"Error searching marketers: {str(e)}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def add_marketer(marketer_data: dict) -> int:
    """Add a new marketer"""
    query = """
    INSERT INTO Marketer (
        name, phone, marketer_type, email, admin_id
    ) VALUES (?, ?, ?, ?, ?)
    """
    params = [
        marketer_data['name'],
        marketer_data['phone'],
        marketer_data['marketer_type'],
        marketer_data['email'],
        marketer_data['admin_id']
    ]
    return execute_update(query, params)

def update_marketer(marketer_data):
    """Update an existing marketer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Marketer
            SET name = ?, phone = ?, email = ?, marketer_type = ?
            WHERE id = ? AND admin_id = ?
        """, (
            marketer_data['name'],
            marketer_data['phone'],
            marketer_data['email'],
            marketer_data['marketer_type'],
            marketer_data['id'],
            marketer_data['admin_id']
        ))
        conn.commit()
    finally:
        conn.close()

def delete_marketer(marketer_id, admin_id=1):
    """Delete a marketer"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First delete associated records
        cursor.execute("DELETE FROM MarketerRealEstate WHERE marketer_id = ? AND admin_id = ?", (marketer_id, admin_id))
        # Then delete the marketer
        cursor.execute("DELETE FROM Marketer WHERE id = ? AND admin_id = ?", (marketer_id, admin_id))
        conn.commit()
    except Exception as e:
        print(f"Error deleting marketer: {str(e)}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()

def get_marketer_real_estates(marketer_id, admin_id=1):
    """Get all real estates associated with a marketer"""
    query = """
    SELECT r.* 
    FROM RealEstate r
    JOIN MarketerRealEstate mr ON r.id = mr.real_estate_id
    WHERE mr.marketer_id = ? AND mr.admin_id = ?
    ORDER BY r.announcement_date DESC
    """
    return execute_query(query, [marketer_id, admin_id])

def get_marketer_buyers(marketer_id: int) -> List[tuple]:
    """Get all buyers associated with a marketer's real estates"""
    query = """
    SELECT DISTINCT b.*, 
           GROUP_CONCAT(r.region) as regions,
           GROUP_CONCAT(r.district) as districts,
           GROUP_CONCAT(r.city) as cities
    FROM Buyer b
    JOIN BuyerRealEstate br ON b.id = br.buyer_id
    JOIN RealEstate r ON br.real_estate_id = r.id
    JOIN MarketerRealEstate mr ON r.id = mr.real_estate_id
    WHERE mr.marketer_id = ?
    GROUP BY b.id
    ORDER BY b.name
    """
    return execute_query(query, [marketer_id])

def get_buyer_real_estates(buyer_id: int, admin_id=1) -> List[tuple]:
    """Get all real estates associated with a buyer that he is intrested in buying"""
    # query = """
    # SELECT r.*, 
    #        GROUP_CONCAT(m.name) as marketer_names,
    #        GROUP_CONCAT(m.phone) as marketer_phones,
    #        br.status as buyer_status
    # FROM RealEstate r
    # JOIN BuyerRealEstate br ON r.id = br.real_estate_id
    # JOIN MarketerRealEstate mr ON r.id = mr.real_estate_id
    # JOIN Marketer m ON mr.marketer_id = m.id
    # WHERE br.buyer_id = ?
    # GROUP BY r.id
    # ORDER BY r.announcement_date DESC
    # """
    query = """
    SELECT r.*
    FROM RealEstate r
    JOIN BuyerRealEstate br ON r.id = br.real_estate_id
    WHERE br.buyer_id = ? AND r.admin_id = ?
    ORDER BY r.announcement_date DESC
    """
    return execute_query(query, [buyer_id, admin_id])

def add_buyer_real_estate(buyer_id, real_estate_id, admin_id=1):
    """Add a relationship between a buyer and a real estate"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO BuyerRealEstate (buyer_id, real_estate_id, admin_id)
            VALUES (?, ?, ?)
        """, (buyer_id, real_estate_id, admin_id))
        conn.commit()
    except Exception as e:
        print(f"Error adding buyer real estate: {str(e)}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()


def delete_buyer_real_estate(buyer_id: int, real_estate_id: int, admin_id=1) -> None:
    """Delete a relationship between a buyer and a real estate"""
    query = """
    DELETE FROM BuyerRealEstate
    WHERE buyer_id = ? AND real_estate_id = ? AND admin_id = ?
    """
    execute_delete(query, [buyer_id, real_estate_id, admin_id])

def add_marketer_real_estate(marketer_id: int, real_estate_id: int, admin_id=1) -> None:
    """Add a relationship between a marketer and a real estate"""
    query = """
    INSERT INTO MarketerRealEstate (marketer_id, real_estate_id, admin_id)
    VALUES (?, ?, ?)
    """
    execute_update(query, [marketer_id, real_estate_id, admin_id])


def delete_marketer_real_estate(marketer_id: int, real_estate_id: int, admin_id=1) -> None:
    """Delete a relationship between a marketer and a real estate"""
    query = """
    DELETE FROM MarketerRealEstate
    WHERE marketer_id = ? AND real_estate_id = ? AND admin_id = ?
    """
    execute_delete(query, [marketer_id, real_estate_id, admin_id])

def get_all_real_estates(admin_id):
    """Get all real estates for a dropdown"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, property_type, region, city, district, price
            FROM RealEstate
            WHERE admin_id = ?
            ORDER BY title
        """, (admin_id,))
        
        real_estates = cursor.fetchall()
        return [{
            'id': re[0],
            'title': re[1],
            'property_type': re[2],
            'region': re[3],
            'city': re[4],
            'district': re[5],
            'price': re[6]
        } for re in real_estates]
    except Exception as e:
        print(f"Error getting real estates: {str(e)}")
        return []
    finally:
        if 'conn' in locals():
            conn.close() 