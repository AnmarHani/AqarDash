import streamlit as st
import pandas as pd
from database_utils import (
    search_marketers, add_marketer, update_marketer, delete_marketer,
    get_all_real_estates, add_marketer_real_estate, delete_marketer_real_estate,
    get_marketer_real_estates
)

def marketers_page():
    st.title("إدارة المسوقين")
    
    # Check if user is logged in
    if not st.session_state.authenticated:
        st.warning("الرجاء تسجيل الدخول أولاً")
        return
    
    # Initialize session state for editing
    if 'edit_marketer_id' not in st.session_state:
        st.session_state.edit_marketer_id = None
    if 'edit_marketer_data' not in st.session_state:
        st.session_state.edit_marketer_data = None
    
    # Add/Edit marketer section
    with st.expander("إضافة/تعديل مسوق", expanded=st.session_state.edit_marketer_id is not None):
        with st.form("marketer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("اسم المسوق", value=st.session_state.edit_marketer_data['name'] if st.session_state.edit_marketer_data else "")
                phone = st.text_input("رقم الهاتف", value=st.session_state.edit_marketer_data['phone'] if st.session_state.edit_marketer_data else "")
                email = st.text_input("البريد الإلكتروني", value=st.session_state.edit_marketer_data['email'] if st.session_state.edit_marketer_data else "")
            
            with col2:
                marketer_type = st.selectbox(
                    "نوع المسوق",
                    ["وسيط", "بائع"],
                    index=["وسيط", "بائع"].index(st.session_state.edit_marketer_data['marketer_type']) if st.session_state.edit_marketer_data and st.session_state.edit_marketer_data['marketer_type'] in ["وسيط", "بائع"] else 0
                )
            
            submit_button = st.form_submit_button("حفظ")
            
            if submit_button:
                marketer_data = {
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'marketer_type': marketer_type,
                    'admin_id': st.session_state.admin_id
                }
                
                try:
                    if st.session_state.edit_marketer_id:
                        marketer_data['id'] = st.session_state.edit_marketer_id
                        update_marketer(marketer_data)
                        st.success("تم تحديث بيانات المسوق بنجاح")
                    else:
                        add_marketer(marketer_data)
                        st.success("تم إضافة المسوق بنجاح")
                    st.session_state.edit_marketer_id = None
                    st.session_state.edit_marketer_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
    
    # Search and filter section
    st.header("البحث والتصفية")
    search_term = st.text_input("بحث", key="search_term")
    
    # Get filtered marketers
    marketers = search_marketers(
        admin_id=st.session_state.admin_id,
        search_term=search_term if search_term else None
    )
    
    # Display marketers
    if marketers:
        st.header("قائمة المسوقين")
        marketers_df = pd.DataFrame(marketers, columns=[
            'id', 'name', 'phone', 'marketer_type', 'email', 'admin_id'
        ])
        
        # Display marketers with edit/delete options
        for _, marketer in marketers_df.iterrows():
            with st.expander(marketer['name']):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**رقم الهاتف:** {marketer['phone']}")
                    st.write(f"**البريد الإلكتروني:** {marketer['email']}")
                
                with col2:
                    st.write(f"**نوع المسوق:** {marketer['marketer_type']}")
                
                # Edit/Delete buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("تعديل", key=f"edit_{marketer['id']}"):
                        st.session_state.edit_marketer_id = marketer['id']
                        st.session_state.edit_marketer_data = marketer.to_dict()
                        st.rerun()
                
                with col2:
                    if st.button("حذف", key=f"delete_{marketer['id']}"):
                        if st.checkbox(f"هل أنت متأكد من حذف {marketer['name']}؟", key=f"confirm_delete_{marketer['id']}"):
                            try:
                                delete_marketer(marketer['id'])
                                st.success("تم حذف المسوق بنجاح")
                                st.rerun()
                            except Exception as e:
                                st.error(f"حدث خطأ أثناء حذف المسوق: {str(e)}")
                
                # Real estate associations
                st.subheader("العقارات المرتبطة")
                real_estates = get_marketer_real_estates(marketer['id'])
                if real_estates:
                    for real_estate in real_estates:
                        st.write(f"- {real_estate['title']} ({real_estate['price']} ريال)")
                        if st.button("إزالة", key=f"remove_{marketer['id']}_{real_estate['id']}"):
                            try:
                                delete_marketer_real_estate(marketer['id'], real_estate['id'])
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
                        key=f"select_real_estate_{marketer['id']}"
                    )
                    if st.button("إضافة", key=f"add_real_estate_{marketer['id']}"):
                        try:
                            add_marketer_real_estate(marketer['id'], real_estate_options[selected_real_estate])
                            st.success("تم إضافة العقار بنجاح")
                            st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء إضافة العقار: {str(e)}")
                else:
                    st.info("لا توجد عقارات متاحة")
    else:
        st.info("لا توجد مسوقين مطابقين للبحث")
