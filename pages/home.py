import streamlit as st
import pandas as pd
import plotly.express as px
from database_utils import search_properties, search_buyers, search_marketers

def create_price_ranges(price):
    if price < 100000:
        return "0-100K"
    elif price < 200000:
        return "100K-200K"
    elif price < 300000:
        return "200K-300K"
    elif price < 400000:
        return "300K-400K"
    else:
        return "400K+"

def create_area_ranges(area):
    if area < 100:
        return "0-100"
    elif area < 200:
        return "100-200"
    elif area < 300:
        return "200-300"
    elif area < 400:
        return "300-400"
    else:
        return "400+"

def home_page():
    # Check if user is logged in
    if 'admin_id' not in st.session_state:
        st.warning("الرجاء تسجيل الدخول أولاً")
        return
    
    st.title("لوحة التحكم")
    
    # Get all data for analytics
    properties = search_properties(admin_id=st.session_state.admin_id)
    buyers = search_buyers(admin_id=st.session_state.admin_id)
    marketers = search_marketers(admin_id=st.session_state.admin_id)
    
    # Convert to DataFrames with proper column names
    properties_df = pd.DataFrame(properties, columns=[
        'id', 'title', 'announcement_date', 'property_type', 'property_scale', 
        'area', 'category', 'floors', 'bedrooms', 'bathrooms', 'living_rooms', 
        'price', 'region', 'district', 'city', 'location_link', 'source_link', 
        'location_details', 'description', 'status', 'admin_id'
    ])
    
    buyers_df = pd.DataFrame(buyers, columns=[
        'id', 'name', 'phone', 'email', 'budget', 'interests', 'status'
    ])
    
    marketers_df = pd.DataFrame(marketers, columns=[
        'id', 'name', 'phone', 'marketer_type', 'email', 'admin_id'
    ])
    
    # Section 1: Key Metrics
    st.header("المؤشرات الرئيسية")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("إجمالي العقارات", len(properties))
    
    with col2:
        st.metric("إجمالي المشترين", len(buyers))
    
    with col3:
        st.metric("إجمالي المعلنين", len(marketers))
    
    # Section 2: Real Estate Analytics
    if not properties_df.empty:
        st.header("تحليلات العقارات")
        
        # Create tabs for different real estate analytics
        tab1, tab2, tab3, tab4 = st.tabs(["حسب الحالة", "حسب نطاق السعر", "حسب المدينة", "حسب المساحة"])
        
        with tab1:
            status_counts = properties_df['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, title="توزيع العقارات حسب الحالة")
            st.plotly_chart(fig)
        
        with tab2:
            properties_df['price_range'] = properties_df['price'].apply(create_price_ranges)
            price_counts = properties_df['price_range'].value_counts()
            fig = px.pie(values=price_counts.values, names=price_counts.index, title="توزيع العقارات حسب نطاق السعر")
            st.plotly_chart(fig)
        
        with tab3:
            city_counts = properties_df['city'].value_counts()
            city_df = pd.DataFrame({
                'city': city_counts.index,
                'count': city_counts.values
            })
            fig = px.bar(city_df, x='city', y='count', title="توزيع العقارات حسب المدينة")
            st.plotly_chart(fig)
        
        with tab4:
            properties_df['area_range'] = properties_df['area'].apply(create_area_ranges)
            area_counts = properties_df['area_range'].value_counts()
            fig = px.pie(values=area_counts.values, names=area_counts.index, title="توزيع العقارات حسب المساحة")
            st.plotly_chart(fig)
    
    # Section 3: Buyers Analytics
    if not buyers_df.empty:
        st.header("تحليلات المشترين")
        top_buyers = buyers_df.sort_values('budget', ascending=False).head(10)
        fig = px.bar(top_buyers, x='name', y='budget', title="أعلى 10 مشترين حسب الميزانية")
        st.plotly_chart(fig)
    
    # Section 4: Marketers Analytics
    if not marketers_df.empty:
        st.header("تحليلات المعلنين")
        marketer_type_counts = marketers_df['marketer_type'].value_counts()
        marketer_df = pd.DataFrame({
            'type': marketer_type_counts.index,
            'count': marketer_type_counts.values
        })
        fig = px.bar(marketer_df, x='type', y='count', title="توزيع المعلنين حسب النوع")
        st.plotly_chart(fig) 