# AqarDash - Real Estate Dashboard

A Streamlit-based dashboard for managing real estate properties with Arabic interface.

## Features

- Add new properties with detailed information
- View all registered properties
- Manage marketers and their associated properties
- Arabic language interface
- SQLite database for data storage

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Database Structure

The application uses SQLite with the following tables:
- Admin: For dashboard administrators
- Marketer: For property marketers/sellers
- RealEstate: For property listings
- Buyer: For potential buyers (to be implemented)

## Usage

1. Navigate to the application in your web browser (default: http://localhost:8501)
2. Use the sidebar to switch between pages:
   - "اضافة عقار" (Add Property): Add new property listings
   - "عرض العقارات" (View Properties): Browse existing properties

## Future Enhancements

- Buyer management system
- Property search and filtering
- Image gallery for properties
- User authentication
- Data analysis and reporting 