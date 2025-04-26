import streamlit as st
import pandas as pd
from database_utils import (
    search_properties, add_property, update_property, delete_property,
    get_all_real_estates
)

def real_estate_page():
    st.title("إدارة العقارات")
    
    # Check if user is logged in
    if not st.session_state.authenticated:
        st.warning("الرجاء تسجيل الدخول أولاً")
        return
    
    # Initialize session state for editing
    if 'edit_property_id' not in st.session_state:
        st.session_state.edit_property_id = None
    if 'edit_property_data' not in st.session_state:
        st.session_state.edit_property_data = None
    
    # Add/Edit property section
    with st.expander("إضافة/تعديل عقار", expanded=st.session_state.edit_property_id is not None):
        with st.form("property_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("عنوان العقار", value=st.session_state.edit_property_data['title'] if st.session_state.edit_property_data else "")
                property_types = ["شقة", "فيلا", "أرض", "عمارة", "محل تجاري", "مستودع", "صناعي"]
                property_type = st.selectbox(
                    "نوع العقار",
                    property_types,
                    index=property_types.index(st.session_state.edit_property_data['property_type']) if st.session_state.edit_property_data and st.session_state.edit_property_data['property_type'] in property_types else 0
                )
                property_scale = st.selectbox(
                    "نطاق العقار",
                    ["فيلا", "عمارة", "شقة", "قصر"],
                    index=["فيلا", "عمارة", "شقة", "قصر"].index(st.session_state.edit_property_data['property_scale']) if st.session_state.edit_property_data and st.session_state.edit_property_data['property_scale'] in ["فيلا", "عمارة", "شقة", "قصر"] else 0
                )
                area = st.number_input("المساحة (م²)", min_value=0.0, value=float(st.session_state.edit_property_data['area']) if st.session_state.edit_property_data else 0.0)
                category = st.selectbox(
                    "الفئة",
                    ["عوائل", "افراد"],
                    index=["عوائل", "افراد"].index(st.session_state.edit_property_data['category']) if st.session_state.edit_property_data and st.session_state.edit_property_data['category'] in ["عوائل", "افراد"] else 0
                )
                floors = st.number_input("عدد الطوابق", min_value=0, value=int(st.session_state.edit_property_data['floors']) if st.session_state.edit_property_data else 0)
            
            with col2:
                bedrooms = st.number_input("عدد غرف النوم", min_value=0, value=int(st.session_state.edit_property_data['bedrooms']) if st.session_state.edit_property_data else 0)
                bathrooms = st.number_input("عدد الحمامات", min_value=0, value=int(st.session_state.edit_property_data['bathrooms']) if st.session_state.edit_property_data else 0)
                living_rooms = st.number_input("عدد الصالات", min_value=0, value=int(st.session_state.edit_property_data['living_rooms']) if st.session_state.edit_property_data else 0)
                price = st.number_input("السعر (ريال)", min_value=0.0, value=float(st.session_state.edit_property_data['price']) if st.session_state.edit_property_data else 0.0)
                region = st.text_input("المنطقة", value=st.session_state.edit_property_data['region'] if st.session_state.edit_property_data else "")
                district = st.text_input("الحي", value=st.session_state.edit_property_data['district'] if st.session_state.edit_property_data else "")
                city = st.text_input("المدينة", value=st.session_state.edit_property_data['city'] if st.session_state.edit_property_data else "")
                location_link = st.text_input("رابط الموقع", value=st.session_state.edit_property_data['location_link'] if st.session_state.edit_property_data else "")
                source_link = st.text_input("رابط المصدر", value=st.session_state.edit_property_data['source_link'] if st.session_state.edit_property_data else "")
                location_details = st.text_area("تفاصيل الموقع", value=st.session_state.edit_property_data['location_details'] if st.session_state.edit_property_data else "")
                description = st.text_area("الوصف", value=st.session_state.edit_property_data['description'] if st.session_state.edit_property_data else "")
                status = st.selectbox(
                    "الحالة",
                    ["متاح", "محجوز", "مباع"],
                    index=["متاح", "محجوز", "مباع"].index(st.session_state.edit_property_data['status']) if st.session_state.edit_property_data and st.session_state.edit_property_data['status'] in ["متاح", "محجوز", "مباع"] else 0
                )
            
            if st.form_submit_button("حفظ"):
                property_data = {
                    'title': title,
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
                    'location_link': location_link,
                    'source_link': source_link,
                    'location_details': location_details,
                    'description': description,
                    'status': status,
                    'admin_id': st.session_state.admin_id
                }
                
                try:
                    if st.session_state.edit_property_id:
                        property_data['id'] = st.session_state.edit_property_id
                        update_property(property_data)
                        st.success("تم تحديث بيانات العقار بنجاح")
                    else:
                        add_property(property_data)
                        st.success("تم إضافة العقار بنجاح")
                    st.session_state.edit_property_id = None
                    st.session_state.edit_property_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
    
    # Search and filter section
    st.header("البحث والتصفية")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("بحث", key="search_term")
        property_type = st.selectbox(
            "نوع العقار",
            ["الكل", "شقة", "فيلا", "أرض", "عمارة", "محل تجاري", "مستودع", "صناعي"],
            key="filter_property_type"
        )
    
    with col2:
        min_price = st.number_input("الحد الأدنى للسعر (ريال)", min_value=0, value=0)
        max_price = st.number_input("الحد الأقصى للسعر (ريال)", min_value=0, value=10000000)
        city = st.text_input("المدينة", key="filter_city")
    
    with col3:
        min_area = st.number_input("الحد الأدنى للمساحة (م²)", min_value=0, value=0)
        max_area = st.number_input("الحد الأقصى للمساحة (م²)", min_value=0, value=10000)
        district = st.text_input("الحي", key="filter_district")
    
    # Get filtered properties
    properties = search_properties(
        admin_id=st.session_state.admin_id,
        search_term=search_term if search_term else None,
        property_type=property_type if property_type != "الكل" else None,
        min_price=min_price,
        max_price=max_price,
        min_area=min_area,
        max_area=max_area,
        city=city if city else None,
        district=district if district else None
    )
    
    # Display properties
    if properties:
        st.header("قائمة العقارات")
        properties_df = pd.DataFrame(properties, columns=[
            'id', 'title', 'announcement_date', 'property_type', 'property_scale', 
            'area', 'category', 'floors', 'bedrooms', 'bathrooms', 'living_rooms', 
            'price', 'region', 'district', 'city', 'location_link', 'source_link', 
            'location_details', 'description', 'status', 'admin_id'
        ])
        
        # Display properties with edit/delete options
        for _, property in properties_df.iterrows():
            title = property['title'] if property['title'] else f"{property['property_type']} في {property['region']} - {property['city']}, {property['district']}"
            with st.expander(title):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**النوع:** {property['property_type']}")
                    st.write(f"**المساحة:** {property['area']} م²")
                    st.write(f"**المدينة:** {property['city']}")
                    st.write(f"**الحي:** {property['district']}")
                    st.write(f"**عدد الطوابق:** {property['floors']}")
                    st.write(f"**غرف النوم:** {property['bedrooms']}")
                    st.write(f"**الحمامات:** {property['bathrooms']}")
                    st.write(f"**الصالات:** {property['living_rooms']}")
                
                with col2:
                    st.write(f"**نطاق العقار:** {property['property_scale']}")
                    st.write(f"**الفئة:** {property['category']}")
                    st.write(f"**السعر:** {property['price']} ريال")
                    st.write(f"**الحالة:** {property['status']}")
                    if property['location_link']:
                        st.write(f"**رابط الموقع:** [{property['location_link']}]({property['location_link']})")
                    if property['source_link']:
                        st.write(f"**رابط المصدر:** [{property['source_link']}]({property['source_link']})")
                    if property['location_details']:
                        st.write(f"**تفاصيل الموقع:** {property['location_details']}")
                    if property['description']:
                        st.write(f"**الوصف:** {property['description']}")
                
                # Edit/Delete buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("تعديل", key=f"edit_{property['id']}"):
                        st.session_state.edit_property_id = property['id']
                        st.session_state.edit_property_data = property.to_dict()
                        st.rerun()
                
                with col2:
                    if st.button("حذف", key=f"delete_{property['id']}"):
                        confirm = st.checkbox(f"هل أنت متأكد من حذف {title}؟", key=f"confirm_delete_{property['id']}")
                        if confirm:
                            try:
                                delete_property(property['id'])
                                st.success("تم حذف العقار بنجاح")
                                st.rerun()
                            except Exception as e:
                                st.error(f"حدث خطأ أثناء حذف العقار: {str(e)}")
    else:
        st.info("لا توجد عقارات مطابقة للبحث") 