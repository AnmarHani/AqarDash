import random
from datetime import datetime, timedelta
from database_utils import execute_query, execute_update, register_admin, add_property, add_marketer, add_buyer

# Constants for property types and scales
PROPERTY_TYPES = ['تجاري', 'صناعي', 'زراعي', 'سكني']
PROPERTY_SCALES = ['فيلا', 'عمارة', 'شقة', 'قصر']
CATEGORIES = ['عوائل', 'افراد']
STATUSES = ['متاح', 'محجوز', 'مباع']
MARKETER_TYPES = ['وسيط', 'بائع']

# Saudi cities and regions
REGIONS = {
    'الرياض': 'الرياض',
    'مكة المكرمة': 'مكة المكرمة',
    'المدينة المنورة': 'المدينة المنورة',
    'المنطقة الشرقية': 'المنطقة الشرقية',
    'عسير': 'عسير'
}

CITIES = {
    'الرياض': ['الرياض', 'الخرج', 'المجمعة', 'الدوادمي', 'الزلفي'],
    'مكة المكرمة': ['مكة المكرمة', 'جدة', 'الطائف', 'خميس مشيط', 'رابغ', 'خليص'],
    'المدينة المنورة': ['المدينة المنورة', 'ينبع', 'خيبر'],
    'المنطقة الشرقية': ['الدمام', 'الخبر', 'القطيف', 'الجبيل', 'الأحساء'],
    'عسير': ['أبها', 'خميس مشيط', 'النماص', 'رجال ألمع']
}

DISTRICTS = {
    'الرياض': ['اليرموك', 'الربوة', 'الخالدية', 'الملز', 'الروضة'],
    'مكة المكرمة': ['الزاهر', 'العزيزية', 'الشوقية', 'المنصور', 'الخالدية'],
    'المدينة المنورة': ['العزيزية', 'الخالدية', 'المناخ', 'الربوة', 'الروضة'],
    'المنطقة الشرقية': ['الخبر', 'الروضة', 'الخالدية', 'الربوة', 'اليرموك'],
    'عسير': ['الخالدية', 'الربوة', 'اليرموك', 'الروضة', 'المناخ']
}

def generate_real_estate_data(admin_id):
    """Generate realistic real estate data"""
    # Select random location
    region = random.choice(list(CITIES.keys()))
    city = random.choice(CITIES[region])
    district = random.choice(DISTRICTS.get(city, ["غير محدد"]))
    
    # Generate property details
    property_type = random.choice(PROPERTY_TYPES)
    property_scale = random.choice(PROPERTY_SCALES)
    area = random.randint(50, 500)  # Realistic area in m²
    category = random.choice(CATEGORIES)
    floors = random.randint(1, 5)
    bedrooms = random.randint(1, 6)
    bathrooms = random.randint(1, 4)
    living_rooms = random.randint(1, 3)
    
    # Generate realistic price based on property type and area
    base_price = area * random.randint(1000, 5000)  # Price per m²
    if property_type == "تجاري":
        base_price *= 1.5
    elif property_type == "صناعي":
        base_price *= 0.8
    price = round(base_price, 2)
    
    # Generate title if not provided
    title = f"{property_type} في {region} - {city}, {district}"
    
    return {
        'title': title,
        'announcement_date': datetime.now().strftime('%Y-%m-%d'),
        'property_type': property_type,
        'property_scale': property_scale,
        'area': area,
        'category': category,
        'floors': floors,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'living_rooms': living_rooms,
        'price': price,
        'region': region,
        'district': district,
        'city': city,
        'location_link': f"https://maps.google.com/?q={city},{district}",
        'source_link': "https://example.com",
        'location_details': f"عقار {property_type} في {district}، {city}، {region}",
        'description': f"عقار {property_type} {property_scale} في {district}، {city}. المساحة {area} م²، {bedrooms} غرف نوم، {bathrooms} حمامات، {living_rooms} صالات.",
        'status': random.choice(STATUSES),
        'admin_id': admin_id
    }

def generate_marketer_data(count: int) -> list:
    marketers = []
    first_names = ['أحمد', 'محمد', 'عبدالله', 'عبدالرحمن', 'خالد', 'سعود', 'ناصر', 'علي', 'حسن', 'سعد']
    middle_names = ['محمد', 'عبدالله', 'سعود', 'ناصر', 'علي', 'حسن', 'سعد', 'خالد', 'عبدالرحمن', 'أحمد']
    last_names = ['السديري', 'الغامدي', 'الحربي', 'الشهري', 'القرشي', 'الزهراني', 'العتيبي', 'العسيري', 'القحطاني']
    
    for _ in range(count):
        name = f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"
        phone = f"05{random.randint(0, 9)}{random.randint(10000000, 99999999)}"
        email = f"{name.replace(' ', '.')}@example.com"
        
        marketer_data = {
            'name': name,
            'phone': phone,
            'marketer_type': random.choice(MARKETER_TYPES),
            'email': email
        }
        marketers.append(marketer_data)
    return marketers

def generate_buyer_data(count: int) -> list:
    buyers = []
    first_names = ['أحمد', 'محمد', 'عبدالله', 'عبدالرحمن', 'خالد', 'سعود', 'ناصر', 'علي', 'حسن', 'سعد', 'نورة', 'لطيفة', 'سارة', 'فاطمة']
    middle_names = ['محمد', 'عبدالله', 'سعود', 'ناصر', 'علي', 'حسن', 'سعد', 'خالد', 'عبدالرحمن', 'أحمد']
    last_names = ['السديري', 'الغامدي', 'الحربي', 'الشهري', 'القرشي', 'الزهراني', 'العتيبي', 'العسيري', 'القحطاني']
    
    for _ in range(count):
        name = f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"
        phone = f"05{random.randint(0, 9)}{random.randint(10000000, 99999999)}"
        email = f"{name.replace(' ', '.')}@example.com"
        
        # Generate interests
        interests = [
            "مكيفات سبليت",
            "مدفأة",
            "مسبح",
            "حديقة",
            "موقف سيارات",
            "نظام أمن",
            "مطبخ مجهز",
            "غرفة خادمة",
            "مستودع"
        ]
        selected_interests = random.sample(interests, random.randint(2, 5))
        
        buyer_data = {
            'name': name,
            'phone': phone,
            'email': email,
            'budget': round(random.uniform(500000, 5000000), 2),
            'interests': "، ".join(selected_interests)
        }
        buyers.append(buyer_data)
    return buyers

def get_admin_id(username):
    """Get admin ID by username"""
    result = execute_query(
        "SELECT id FROM Admin WHERE username = ?",
        [username]
    )
    return result[0][0] if result else None

def insert_dummy_data():
    # Add default admin users
    admin_users = [
        ("admin123", "admin123"),
        ("manager", "manager123"),
        ("user", "user123")
    ]
    
    admin_ids = []
    for username, password in admin_users:
        success, message = register_admin(username, password)
        if success:
            admin_id = get_admin_id(username)
            admin_ids.append(admin_id)
            print(f"Successfully registered admin user: {username} with ID: {admin_id}")
        else:
            print(f"Failed to register admin user {username}: {message}")
    
    if not admin_ids:
        print("No admin users available. Cannot proceed with data generation.")
        return
    
    # Generate and insert real estate data - evenly distributed among admins
    properties_per_admin = 12  # Each admin gets 12 properties
    for admin_id in admin_ids:
        real_estates = [generate_real_estate_data(admin_id) for _ in range(properties_per_admin)]
        for real_estate in real_estates:
            try:
                property_id = add_property(real_estate)
                print(f"Successfully added property: {real_estate['title']} for admin {admin_id}")
            except Exception as e:
                print(f"Failed to add property: {str(e)}")
    
    # Generate and insert marketer data - evenly distributed among admins
    marketers_per_admin = 5  # Each admin gets 5 marketers
    for admin_id in admin_ids:
        marketers = generate_marketer_data(marketers_per_admin)
        for marketer in marketers:
            try:
                marketer['admin_id'] = admin_id
                marketer_id = add_marketer(marketer)
                print(f"Successfully added marketer: {marketer['name']} for admin {admin_id}")
            except Exception as e:
                print(f"Failed to add marketer: {str(e)}")
    
    # Generate and insert buyer data - evenly distributed among admins
    buyers_per_admin = 8
    for admin_id in admin_ids:
        buyers = generate_buyer_data(buyers_per_admin)
        for buyer in buyers:
            try:
                buyer['admin_id'] = admin_id
                buyer_id = add_buyer(buyer)
                print(f"Successfully added buyer: {buyer['name']} for admin {admin_id}")
            except Exception as e:
                print(f"Failed to add buyer: {str(e)}")
    
    print("Dummy data has been generated and inserted into the database.")

if __name__ == "__main__":
    insert_dummy_data() 