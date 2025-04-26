import streamlit as st
import pandas as pd
from database_utils import (
    search_buyers, add_buyer, update_buyer, delete_buyer,
    get_all_real_estates, add_buyer_real_estate, delete_buyer_real_estate,
    get_buyer_real_estates
)

def buyers_page():
    st.title("إدارة المشترين")
    
    # Check if user is logged in
    if not st.session_state.authenticated:
        st.warning("الرجاء تسجيل الدخول أولاً")
        return
    
    # Initialize session state for editing
    if 'edit_buyer_id' not in st.session_state:
        st.session_state.edit_buyer_id = None
    if 'edit_buyer_data' not in st.session_state:
        st.session_state.edit_buyer_data = None
    
    # Add/Edit buyer section
    with st.expander("إضافة/تعديل مشتر", expanded=st.session_state.edit_buyer_id is not None):
        with st.form("buyer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("اسم المشتري", value=st.session_state.edit_buyer_data['name'] if st.session_state.edit_buyer_data else "")
                phone = st.text_input("رقم الهاتف", value=st.session_state.edit_buyer_data['phone'] if st.session_state.edit_buyer_data else "")
                email = st.text_input("البريد الإلكتروني", value=st.session_state.edit_buyer_data['email'] if st.session_state.edit_buyer_data else "")
                budget = st.number_input("الميزانية (ريال)", min_value=0.0, value=float(st.session_state.edit_buyer_data['budget']) if st.session_state.edit_buyer_data else 0.0)
            
            with col2:
                interests = st.text_area("الاهتمامات", value=st.session_state.edit_buyer_data.get('interests', '') if st.session_state.edit_buyer_data else "")
            
            submit_button = st.form_submit_button("حفظ")
            
            if submit_button:
                buyer_data = {
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'budget': budget,
                    'interests': interests,
                    'admin_id': st.session_state.admin_id
                }
                
                try:
                    if st.session_state.edit_buyer_id:
                        buyer_data['id'] = st.session_state.edit_buyer_id
                        update_buyer(buyer_data)
                        st.success("تم تحديث بيانات المشتري بنجاح")
                    else:
                        add_buyer(buyer_data)
                        st.success("تم إضافة المشتري بنجاح")
                    st.session_state.edit_buyer_id = None
                    st.session_state.edit_buyer_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
    
    # Search and filter section
    st.header("البحث والتصفية")
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("بحث", key="search_term")
        min_budget = st.number_input("الحد الأدنى للميزانية (ريال)", min_value=0, value=0)
        max_budget = st.number_input("الحد الأقصى للميزانية (ريال)", min_value=0, value=10000000)
    
    # Get filtered buyers
    buyers = search_buyers(
        admin_id=st.session_state.admin_id,
        search_term=search_term if search_term else None,
        min_budget=min_budget,
        max_budget=max_budget
    )
    
    # Display buyers
    if buyers:
        st.header("قائمة المشترين")
        buyers_df = pd.DataFrame(buyers, columns=[
            'id', 'name', 'phone', 'email', 'budget',
            'interests', 'admin_id'
        ])
        
        # Display buyers with edit/delete options
        for _, buyer in buyers_df.iterrows():
            with st.expander(buyer['name']):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**رقم الهاتف:** {buyer['phone']}")
                    st.write(f"**البريد الإلكتروني:** {buyer['email']}")
                    st.write(f"**الميزانية:** {buyer['budget']} ريال")
                
                with col2:
                    st.write(f"**الاهتمامات:** {buyer['interests']}")
                
                # Edit/Delete buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("تعديل", key=f"edit_{buyer['id']}"):
                        st.session_state.edit_buyer_id = buyer['id']
                        st.session_state.edit_buyer_data = buyer.to_dict()
                        st.rerun()
                
                with col2:
                    if st.button("حذف", key=f"delete_{buyer['id']}"):
                        if st.checkbox(f"هل أنت متأكد من حذف {buyer['name']}؟", key=f"confirm_delete_{buyer['id']}"):
                            try:
                                delete_buyer(buyer['id'])
                                st.success("تم حذف المشتري بنجاح")
                                st.rerun()
                            except Exception as e:
                                st.error(f"حدث خطأ أثناء حذف المشتري: {str(e)}")
                
                # Real estate associations
                st.subheader("العقارات المرتبطة")
                real_estates = get_buyer_real_estates(buyer['id'])
                if real_estates:
                    for real_estate in real_estates:
                        st.write(f"- {real_estate['title']} ({real_estate['price']} ريال)")
                        if st.button("إزالة", key=f"remove_{buyer['id']}_{real_estate['id']}"):
                            try:
                                delete_buyer_real_estate(buyer['id'], real_estate['id'])
                                st.success("تم إزالة العقار بنجاح")
                                st.rerun()
                            except Exception as e:
                                st.error(f"حدث خطأ أثناء إزالة العقار: {str(e)}")
                else:
                    st.info("لا توجد عقارات مرتبطة")
                
                # Add real estate association
                st.subheader("إضافة عقار")
                all_real_estates = get_all_real_estates(st.session_state.admin_id)
                if all_real_estates:
                    real_estate_options = {f"{re['title']} ({re['price']} ريال)": re['id'] for re in all_real_estates}
                    selected_real_estate = st.selectbox(
                        "اختر عقار",
                        options=list(real_estate_options.keys()),
                        key=f"select_real_estate_{buyer['id']}"
                    )
                    if st.button("إضافة", key=f"add_real_estate_{buyer['id']}"):
                        try:
                            add_buyer_real_estate(buyer['id'], real_estate_options[selected_real_estate])
                            st.success("تم إضافة العقار بنجاح")
                            st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء إضافة العقار: {str(e)}")
                else:
                    st.info("لا توجد عقارات متاحة")
    else:
        st.info("لا توجد مشترين مطابقين للبحث") 