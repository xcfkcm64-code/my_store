import streamlit as st
import pandas as pd
import os
import pickle
import datetime
import base64
import random
import plotly.express as px

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="نظام الوارد والصادر المخزني - العتبة الكاظمية", layout="wide", page_icon="📦")

# --- 2. إعدادات مسار وحفظ البيانات (Database & Backup) ---
DB_FILE = "store_database_backup.pkl"

def save_data_to_disk():
    try:
        data_to_save = {}
        for key, value in st.session_state.items():
            if key.startswith("_") or key == "authenticated":
                continue
            try:
                pickle.dumps(value)
                data_to_save[key] = value
            except Exception:
                pass

        with open(DB_FILE, "wb") as f:
            pickle.dump(data_to_save, f)
        return True
    except Exception as e:
        st.error(f"خطأ أثناء الحفظ: {e}")
        return False

# استرجاع البيانات المحفوظة (مع إبقاء حالة المصادقة منفصلة تماماً للأمان)
if "data_loaded_from_disk" not in st.session_state:
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "rb") as f:
                saved_data = pickle.load(f)
                for key, value in saved_data.items():
                    if key != "authenticated":
                        st.session_state[key] = value
        except Exception:
            pass
    st.session_state.data_loaded_from_disk = True

# --- 3. نظام تسجيل الدخول (إجباري في البداية) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    img_path = "ali.jpg"
    img_base64 = ""
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    bg_css = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .stTextInput label {{
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #fff; background-color: rgba(27,77,62,0.85); padding: 12px; border-radius: 10px; border: 2px solid #b8860b;'>🔐 تسجيل دخول إلى نظام الوارد والصادر المخزني</h2>", unsafe_allow_html=True)
    
    qaul_list = [
        "✨ قال الإمام موسى الكاظم (عليه السلام): (إياك والمزاح فإنه يذهب نور إيمانك)",
        "✨ قال الإمام موسى الكاظم (عليه السلام): (من عقل عن الله أمن مقت الله عز وجل)",
        "✨ قال الإمام محمد الجواد (عليه السلام): (التقرب إلى الله عز وجل بالثقة به، والتوكل عليه)",
        "✨ قال الإمام محمد الجواد (عليه السلام): (الثقة بالله حصن حصن, لا يسكنه إلا مؤمن)",
        "✨ قال الإمام موسى الكاظم (عليه السلام): (ليس من لم يُحاسب نفسه في كل يوم؛ فإن عمل حسناً استزاد، وإن عمل سيئاً استغفر الله منه)",
        "✨ قال الإمام محمد الجواد (عليه السلام): (عز المؤمن غناه عن الناس)"
    ]
    random_quote = random.choice(qaul_list)
    
    st.markdown(f"<p style='text-align: center; font-weight: bold; color: #ffeb3b; background-color: rgba(0,0,0,0.7); padding: 12px; border-radius: 8px; font-size: 19px;'>{random_quote}</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        with st.form("login_secure_form"):
            username_input = st.text_input("اسم المستخدم")
            password_input = st.text_input("كلمة المرور", type="password")
            login_submit_btn = st.form_submit_button("تسجيل الدخول")
            
            if login_submit_btn:
                if username_input == "علي مازن" and password_input == "20052005":
                    st.session_state.authenticated = True
                    st.success("✅ تم تسجيل الدخول بنجاح! جاري فتح النظام...")
                    st.rerun()
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
                    
    current_time_str = datetime.datetime.now().strftime("%Y-%m-%d | %I:%M:%S %p")
    st.markdown(f"<br><p style='text-align: center; color: #ffffff; font-size: 14px; background-color: rgba(0,0,0,0.5); padding: 6px; border-radius: 5px;'>📅 التاريخ والوقت الحالي: {current_time_str}</p>", unsafe_allow_html=True)
    
    st.stop()


# --- 4. الشريط الجانبي والنسخ الاحتياطي (Sidebar & Backup) ---
DB_FILE = "store_database_backup.pkl"
st.sidebar.title("🛠️ إعدادات الحفظ والنظام")
st.sidebar.markdown("---")

if st.sidebar.button("💾 حفظ التغييرات الحالية"):
    if save_data_to_disk():
        st.sidebar.success("✅ تم حفظ كافة البيانات بنجاح في النظام!")
    else:
        st.sidebar.error("❌ حدث خطأ أثناء محاولة الحفظ.")

if os.path.exists(DB_FILE):
    with open(DB_FILE, "rb") as f:
        bytes_data = f.read()
    st.sidebar.download_button(
        label="📥 تحميل نسخة احتياطية (Backup)",
        data=bytes_data,
        file_name=f"store_backup_{datetime.date.today()}.pkl",
        mime="application/octet-stream"
    )

st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.authenticated = False
    st.rerun()


# --- 5. الشاشة الرئيسية للبرنامج بعد الدخول ---
st.title("📦 نظام الوارد والصادر المخزني المركزي")
st.success("مرحباً بك يا أستاذ علي مازن! تم تأمين النظام، وتفعيل الحفظ التلقائي والنسخ الاحتياطي بنجاح.")

if "inbound_data" not in st.session_state:
    st.session_state.inbound_data = pd.DataFrame(columns=[
        "اسم المادة", "وحدة القياس", "الكمية", "رقم القائمة", 
        "رقم المستند", "تاريخ المستند", "تاريخ التسجيل", 
        "الجهة المستفيدة", "نوع المستند", "المرفقات"
    ])

if "inventory_stock" not in st.session_state:
    st.session_state.inventory_stock = pd.DataFrame(columns=[
        "اسم المادة", "صورة المادة", "الكمية", "وحدة القياس"
    ])

if "outbound_data" not in st.session_state:
    st.session_state.outbound_data = pd.DataFrame(columns=[
        "اسم المستند", "رقم المستند", "ملف كتابه", "الكميه كتابة", 
        "الكمية", "الشعبة", "الوحدة", "القسم", "المستند"
    ])

st.markdown("<h1 style='text-align: center; color: #1E3A8A; font-family: Tahoma;'>العتبة الكاظمية المقدسة</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #374151; font-family: Tahoma;'>قسم الشؤون الخدمية - وحدة إدارة المخازن</h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #059669; font-family: Tahoma;'>نظام الوارد والصادر المخزني</h4>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.title("القائمة الرئيسية")
menu_option = st.sidebar.radio(
    "الانتقال السريع للأقسام",
    [
        "📊 الواجهة الرئيسية واللوحة التفاعلية", 
        "📥 قسم إدخال البيانات (الوارد)", 
        "سجل البيانات والبحث", 
        "📤 قسم الصادر المخزني", 
        "📋 قسم الرصيد المخزني", 
        "رصيد المخزن", 
        "📤 قسم الصرف المخزني", 
        "🏷️ قسم الباركودات", 
        "🧼 رصيد الأقداح والصابون السائل", 
        "رصيد المواد الاستهلاكية", 
        "📈 التقارير والمخططات البيانية"
    ]
)

if menu_option == "📊 الواجهة الرئيسية واللوحة التفاعلية":
    st.markdown("### 🔔 لوحة التنبيهات والإشعارات الفورية")
    col_notif1, col_notif2, col_notif3 = st.columns(3)
    
    with col_notif1:
        if not st.session_state.inventory_stock.empty:
            low_stock = st.session_state.inventory_stock[st.session_state.inventory_stock["الكمية"] < 5]
            if not low_stock.empty:
                for idx, row in low_stock.iterrows():
                    st.warning(f"⚠️ **تنبيه حد أدنى:** المادة (**{row['اسم المادة']}**) رصيدها منخفض ({row['الكمية']}!")
            else:
                st.success("✅ **حالة المخزن:** جميع الأرصدة في المستويات الآمنة ولا توجد مواد أوشكت على النفاد.")
        else:
            st.info("ℹ️ النظام جاهز. لم يتم تسجيل رصيد مواد في المخزن بعد.")
            
    with col_notif2:
        st.info("📅 **تذكير إداري:** يرجى مراجعة وتدقيق إعداد التقارير المخزنية اليومية والشهرية بانتظام لضمان تطابق السجلات.")

    with col_notif3:
        st.info("🔄 **إشعار الجرد:** تنبيه بضرورة إجراء المطابقة الدورية وجرد رصيد المخزن لتحديث الذمم والكميات الفعليّة.")

    st.markdown("---")
    st.markdown("### 📊 المؤشرات الإحصائية العامة")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        inbound_total_count = len(st.session_state.inbound_data) if "inbound_data" in st.session_state else 0
        st.metric("📦 إجمالي حركات الوارد", inbound_total_count)
    with m2:
        outbound_total_count = len(st.session_state.outbound_data) if "outbound_data" in st.session_state else 0
        st.metric("📤 إجمالي حركات الصادر", outbound_total_count)
    with m3:
        inventory_items_count = len(st.session_state.inventory_stock) if "inventory_stock" in st.session_state else 0
        st.metric("📋 أصناف المخزن الحالية", inventory_items_count)
    with m4:
        active_alerts = 0
        if "inventory_stock" in st.session_state and not st.session_state.inventory_stock.empty:
            active_alerts = len(st.session_state.inventory_stock[st.session_state.inventory_stock["الكمية"] < 5])
        st.metric("⚠️ التنبيهات النشطة", active_alerts)

    st.markdown("---")
    st.markdown("### 📈 تحليلات حركة المواد والملخصات التفاعلية")
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        st.markdown("#### 📥 ملخص الوارد حسب نوع المستند")
        if "inbound_data" in st.session_state and not st.session_state.inbound_data.empty:
            doc_counts = st.session_state.inbound_data["نوع المستند"].value_counts().reset_index()
            doc_counts.columns = ["نوع المستند", "العدد"]
            fig_doc = px.bar(doc_counts, x="نوع المستند", y="العدد", color="نوع المستند", text_auto=True)
            st.plotly_chart(fig_doc, use_container_width=True)
        else:
            st.info("لا توجد بيانات واردة كافية لعرض الرسم البياني.")
            
    with c_chart2:
        st.markdown("#### 📤 تحليل حركة الصادر والأقسام المستفيدة")
        if "outbound_data" in st.session_state and not st.session_state.outbound_data.empty:
            dept_counts = st.session_state.outbound_data["القسم"].value_counts().reset_index()
            dept_counts.columns = ["القسم", "العدد"]
            fig_dept = px.pie(dept_counts, names="القسم", values="العدد", hole=0.4)
            st.plotly_chart(fig_dept, use_container_width=True)
        else:
            st.info("لا توجد بيانات صادرة كافية لعرض التوزيع البياني.")

    st.markdown("---")
    st.markdown("### 🔍 ملخصات حركة وسحب المواد والشعب")
    col_ana1, col_ana2 = st.columns(2)
    
    with col_ana1:
        st.markdown("##### 🔥 أكثر 5 مواد صرفاً")
        if "outbound_data" in st.session_state and not st.session_state.outbound_data.empty and "اسم المادة" in st.session_state.outbound_data.columns:
            top_materials = st.session_state.outbound_data["اسم المادة"].value_counts().reset_index().head(5)
            top_materials.columns = ["اسم المادة", "عدد مرات الصرف"]
            st.dataframe(top_materials, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بيانات كافية لعرض أكثر المواد صرفاً.")

        st.markdown("##### 🧊 مواد ليس لها أي حركة صرف (راكدة)")
        if "inventory_stock" in st.session_state and not st.session_state.inventory_stock.empty:
            inv_df = st.session_state.inventory_stock
            if "outbound_data" in st.session_state and not st.session_state.outbound_data.empty and "اسم المادة" in st.session_state.outbound_data.columns:
                active_items = st.session_state.outbound_data["اسم المادة"].unique()
                stagnant_items = inv_df[~inv_df["اسم المادة"].isin(active_items)]
            else:
                stagnant_items = inv_df
            
            if not stagnant_items.empty:
                st.dataframe(stagnant_items[["اسم المادة", "الكمية"]], use_container_width=True, hide_index=True)
            else:
                st.success("جميع مواد المخزن شهدت حركات صرف ولا توجد مواد راكدة حالياً.")
        else:
            st.info("قائمة المخزن فارغة.")

    with col_ana2:
        st.markdown("##### 🏢 أكثر الشعب المستفيدة صرفاً")
        if "outbound_data" in st.session_state and not st.session_state.outbound_data.empty and "القسم" in st.session_state.outbound_data.columns:
            top_depts = st.session_state.outbound_data["القسم"].value_counts().reset_index().head(5)
            top_depts.columns = ["القسم / الشعبة", "عدد الطلبات"]
            st.dataframe(top_depts, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بيانات كافية لتحليل الشعب الأكثر صرفاً.")

        st.markdown("##### 📉 أقل الشعب المستفيدة صرفاً")
        if "outbound_data" in st.session_state and not st.session_state.outbound_data.empty and "القسم" in st.session_state.outbound_data.columns:
            bottom_depts = st.session_state.outbound_data["القسم"].value_counts().reset_index().tail(5)
            bottom_depts.columns = ["القسم / الشعبة", "عدد الطلبات"]
            st.dataframe(bottom_depts, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد بيانات كافية لتحليل الشعب الأقل صرفاً.")
import os
import datetime
import pandas as pd
import streamlit as st

# --- 1. قسم إدخال البيانات (الوارد) مع القوائم الذكية والتحديث التلقائي للرصيد المخزني ---
if menu_option == "📥 قسم إدخال البيانات (الوارد)":
    st.subheader("📥 إدخال بيانات الوارد المخزني (لمادة واحدة)")
    
    # 1. تهيئة قوائم الخيارات الأساسية في session_state إذا لم تكن موجودة
    if "material_list" not in st.session_state:
        st.session_state.material_list = [
            "صابون سائل", "اكياس نفايات اسود", "معطر جو", "كرمل", "ملمع زجاج", "زاهي تصنيع", 
            "مطهر ومنظف خاص بالعجلات", "ماسحات", "ربد خشب", "شناطة", "عملاق تصنيع", "فلاش", 
            "منظف دهون", "وصل مسح", "النكي", "ريشة دريل", "سبانة راجز", "لاصق عريض", "كف مطاط", 
            "قفل كبير", "فوم", "اقلام جاف", "لوح كتابة", "فرشاة ( مكناسة)", "قماش بازة", "كف طبي", 
            "لوكر خشب تصنيع", "كشوانية المنيوم تصنيع", "نايلون زراعي", "اطار صغير قفل", "تعلاكة ستيل ثلاثية", 
            "سبري تاشير الوان", "فيتة 5 متر", "رول بولد حديد 10 ملم", "رول بولد حديد 12 ملم", "ورق ابيض A4",
            "كلينكس", "بطل براد ماء فارغ", "ملمع دشبول", "اسفنج", "فرشاة تنظيف", "كابسة وسط", "تربة صلاة تصنيع"
        ]
        
    if "unit_list" not in st.session_state:
        st.session_state.unit_list = [
            "كارتون", "عدد", "دبة *20 لتر", "سطل", "كيس", "بالة", "درزن", "باكيت", "سيت", 
            "لفة", "طول", "قطعة", "صندوق", "كيلو غرام", "بند", "لتر", "متر مربع", "رولة", 
            "متر", "كيلو", "روطة", "علبة", "دبة 3.6 لتر", "شريط", "طبقة", "غالون", "زوج", "متر مكعب"
        ]

    if "dept_list" not in st.session_state:
        st.session_state.dept_list = [
            "وحدة إدارة المخازن", "شعبة رعاية الصحون الخارجية", "صحن الرسول الأعظم (ص) وصحن الإمام الصادق (ع)",
            "صحن أمير المؤمنين وسيدة نساء العالمين وصحن الحسنين وصحن الإمام الرضا (عليهما السلام)",
            "صحن العسكريين وصحن صاحب الزمان (عليهما السلام)", "الصحن الشريف (الصحن القديم)", "التعطير",
            "المكتبة القرآنية", "شعبة التنظيف الآلي", "العجلات الخدمية", "الصيانة", "غسل السجاد والمفروشات",
            "عجلات التنظيف", "شعبة الخدمات الخارجية", "الطرق والمقتربات", "المجاميع الصحية (رجال)",
            "شعبة الشؤون الخدمية", "الحرم المطهر للنساء", "وحدة المجاميع الصحية للنساء", "وحدة الإدارة", "قسم الشؤون الخدمية"
        ]

    # تهيئة جداول البيانات في الجلسة إذا لم تكن موجودة
    if "inbound_data" not in st.session_state:
        st.session_state.inbound_data = pd.DataFrame(columns=[
            "اسم المادة", "وحدة القياس", "الكمية", "رقم القائمة", "رقم المستند", 
            "تاريخ المستند", "تاريخ التسجيل", "الجهة المستفيدة", "نوع المستند", "المرفقات"
        ])
        
    if "inventory_stock" not in st.session_state:
        st.session_state.inventory_stock = pd.DataFrame(columns=[
            "اسم المادة", "القياس", "الكمية"
        ])

    with st.form("inbound_single_form"):
        st.markdown("### 📄 معلومات المستند والمادة")
        
        c1, c2 = st.columns(2)
        with c1:
            # قائمة منسدلة لاختيار اسم المادة مع خيار لإضافة مادة جديدة
            selected_item = st.selectbox("اختر اسم المادة", ["-- اختر المادة --"] + st.session_state.material_list)
            new_item_input = st.text_input("أو اكتب اسم مادة جديدة (إذا لم تكن موجودة بالقائمة):")
            
            # تحديد اسم المادة النهائي
            item_name = new_item_input.strip() if new_item_input else (selected_item if selected_item != "-- اختر المادة --" else "")

            # قائمة منسدلة لوحدة القياس مع إمكانية الإضافة
            selected_unit = st.selectbox("وحدة القياس", ["-- اختر وحدة القياس --"] + st.session_state.unit_list)
            new_unit_input = st.text_input("أو اكتب وحدة قياس جديدة (إذا لم تكن موجودة):")
            item_unit = new_unit_input.strip() if new_unit_input else (selected_unit if selected_unit != "-- اختر وحدة القياس --" else "")

            quantity = st.number_input("الكمية الاستلامية", min_value=1, step=1, value=1)
            list_no = st.text_input("رقم القائمة")
            
        with c2:
            doc_no = st.text_input("رقم المستند")
            doc_date = st.date_input("تاريخ المستند", datetime.date.today())
            
            # قائمة منسدلة للجهة المستفيدة مع إمكانية الإضافة
            selected_dept = st.selectbox("الجهة المستفيدة", ["-- اختر الجهة المستفيدة --"] + st.session_state.dept_list)
            new_dept_input = st.text_input("أو اكتب جهة مستفيدة جديدة (إذا لم تكن موجودة):")
            beneficiary = new_dept_input.strip() if new_dept_input else (selected_dept if selected_dept != "-- اختر الجهة المستفيدة --" else "")

            doc_type = st.selectbox("نوع المستند", ["مذكرة داخلية", "طلب شراء", "استرجاع مادة", "شطب مادة", "طلب مواد"])
        
        attachment = st.file_uploader("ملف الأوليات والمرفقات", type=["pdf", "png", "jpg"])
        
        submitted = st.form_submit_button("💾 حفظ البيانات وتحديث الرصيد المخزني")
        
        if submitted:
            if not item_name:
                st.error("⚠️ يرجى اختيار أو إدخال اسم المادة.")
            elif not item_unit or item_unit == "-- اختر وحدة القياس --":
                st.error("⚠️ يرجى اختيار أو إدخال وحدة القياس.")
            elif not beneficiary or beneficiary == "-- اختر الجهة المستفيدة --":
                st.error("⚠️ يرجى اختيار أو إدخال الجهة المستفيدة.")
            elif not list_no:
                st.error("⚠️ يرجى إدخال رقم القائمة.")
            else:
                # تحديث القوائم العامة فورياً إذا تم إدخال عناصر جديدة
                if item_name not in st.session_state.material_list:
                    st.session_state.material_list.append(item_name)
                if item_unit not in st.session_state.unit_list:
                    st.session_state.unit_list.append(item_unit)
                if beneficiary not in st.session_state.dept_list:
                    st.session_state.dept_list.append(beneficiary)

                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "طلب مواد عام 2026")
                
                att_path = "بدون مرفق"
                if attachment is not None:
                    sub_folder = os.path.join(desktop_path, doc_type)
                    if not os.path.exists(sub_folder):
                        os.makedirs(sub_folder)
                    att_path = os.path.join(sub_folder, attachment.name)
                    with open(att_path, "wb") as f:
                        f.write(attachment.getbuffer())
                
                clean_item_name = item_name.strip()
                new_inbound_row = {
                    "اسم المادة": clean_item_name,
                    "وحدة القياس": item_unit,
                    "الكمية": int(quantity),
                    "رقم القائمة": list_no,
                    "رقم المستند": doc_no,
                    "تاريخ المستند": str(doc_date),
                    "تاريخ التسجيل": str(datetime.date.today()),
                    "الجهة المستفيدة": beneficiary,
                    "نوع المستند": doc_type,
                    "المرفقات": att_path
                }
                
                # إضافة السجل لسجل الوارد
                st.session_state.inbound_data = pd.concat(
                    [st.session_state.inbound_data, pd.DataFrame([new_inbound_row])], 
                    ignore_index=True
                )
                
                # تحديث أو إضافة الرصيد المخزني بدون تكرار السطر (جمع الكميات للمادة والقياس نفسه)
                if not st.session_state.inventory_stock.empty:
                    existing_match = (
                        (st.session_state.inventory_stock["اسم المادة"] == clean_item_name) & 
                        (st.session_state.inventory_stock["القياس"] == item_unit)
                    )
                    if existing_match.any():
                        st.session_state.inventory_stock.loc[existing_match, "الكمية"] += int(quantity)
                    else:
                        new_stock_row = {
                            "اسم المادة": clean_item_name,
                            "القياس": item_unit,
                            "الكمية": int(quantity)
                        }
                        st.session_state.inventory_stock = pd.concat(
                            [st.session_state.inventory_stock, pd.DataFrame([new_stock_row])], 
                            ignore_index=True
                        )
                else:
                    new_stock_row = {
                        "اسم المادة": clean_item_name,
                        "القياس": item_unit,
                        "الكمية": int(quantity)
                    }
                    st.session_state.inventory_stock = pd.DataFrame([new_stock_row])
                
                # مزامنة stock_data أيضاً لضمان تكامل الأقسام
                st.session_state.stock_data = st.session_state.inventory_stock.copy()
                
                st.success("✅ تم حفظ البيانات، وتحديث الرصيد المخزني وإضافة العناصر الجديدة للقوائم بنجاح!")


# --- 2. قسم الرصيد المخزني (مع خاصية البحث التلقائي) ---
elif menu_option == "📋 قسم الرصيد المخزني":
    st.subheader("📦 قسم الرصيد المخزني العام")
    
    # التأكد من وجود جدول الرصيد المخزني أو تحديثه من الوارد مباشرة
    if "inventory_stock" not in st.session_state:
        st.session_state.inventory_stock = pd.DataFrame(columns=["اسم المادة", "القياس", "الكمية"])
        
    # خاصية البحث عن اسم مادة لمعرفة كميتها بدقة
    search_query = st.text_input("🔍 البحث السريع عن اسم مادة في الرصيد المخزني:")
    
    current_stock_df = st.session_state.inventory_stock.copy()
    
    if search_query:
        current_stock_df = current_stock_df[
            current_stock_df["اسم المادة"].astype(str).str.contains(search_query, case=False, na=False)
        ]
        
    if not current_stock_df.empty:
        # إعادة ترتيب وتسلسل الجدول بشكل أنيق وعرضه
        display_df = current_stock_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        display_df.index.name = "التسلسل"
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("ℹ️ لا توجد مواد مطابقة في الرصيد المخزني حالياً أو لم يتم إدخال بيانات واردة بعد.")
# 3. قسم سجل البيانات والبحث (مع تقرير A4 العرضي الرسمي والزخارف والترويسة)
if menu_option == "سجل البيانات والبحث":
    st.subheader("📋 قسم سجل بيانات وعرض الوارد المخزني")
    
    if not st.session_state.inbound_data.empty:
        st.markdown("### 🔍 خيارات البحث والتصفية المستقلة المتقدمة")
        
        # التأكد من وجود قائمة المواد في الـ session_state (التي تم إرسالها سابقاً)
        if "items_list" not in st.session_state:
            st.session_state.items_list = []

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            # قائمة منسدلة لأسماء المواد المعتمدة مع خيار الكل
            item_options = ["(بحث الكل / بدون تحديد)"] + st.session_state.items_list
            selected_search_item = st.selectbox("🔍 تصفية حسب اسم المادة", item_options)
            
            # خيار لإضافة مادة جديدة مباشرة في قسم البحث والتصفية
            add_new_search_item_check = st.checkbox("➕ إضافة مادة جديدة للتصفية؟")
            search_item_custom = ""
            if add_new_search_item_check:
                search_item_custom = st.text_input("أدخل اسم المادة الجديدة")
                if search_item_custom and search_item_custom not in st.session_state.items_list:
                    st.session_state.items_list.append(search_item_custom)

        with col_b2:
            search_list_no = st.text_input("🔍 بحث حسب رقم القائمة")
            search_doc_no = st.text_input("🔍 بحث حسب رقم المستند")
            
        with col_b3:
            doc_type_filter = st.selectbox(
                "📁 تصفية حسب نوع المستند", 
                ["الكل", "مذكرة داخلية", "طلب شراء", "استرجاع مادة", "شطب مادة", "طلب مواد"]
            )
            date_mode = st.radio("نوع البحث التاريخي", ["فترة مفتوحة", "تحديد فترة زمنية"], horizontal=True)
        
        filtered_df = st.session_state.inbound_data.copy()
        
        if doc_type_filter != "الكل":
            filtered_df = filtered_df[filtered_df["نوع المستند"] == doc_type_filter]
            
        # منطق التصفية حسب المادة المختارة من القائمة أو المضافة حديثاً
        active_item_filter = search_item_custom if (add_new_search_item_check and search_item_custom) else selected_search_item
        if active_item_filter and active_item_filter != "(بحث الكل / بدون تحديد)":
            filtered_df = filtered_df[filtered_df["اسم المادة"].astype(str).str.contains(active_item_filter, case=False, na=False)]
            
        if search_list_no:
            filtered_df = filtered_df[filtered_df["رقم القائمة"].astype(str).str.contains(search_list_no, case=False, na=False)]
        if search_doc_no:
            filtered_df = filtered_df[filtered_df["رقم المستند"].astype(str).str.contains(search_doc_no, case=False, na=False)]
            
        if date_mode == "تحديد فترة زمنية":
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                start_date = st.date_input("تاريخ البداية", datetime.date.today() - datetime.timedelta(days=30))
            with col_d2:
                end_date = st.date_input("تاريخ النهاية", datetime.date.today())
            
            filtered_df["تاريخ المستند"] = pd.to_datetime(filtered_df["تاريخ المستند"]).dt.date
            filtered_df = filtered_df[
                (filtered_df["تاريخ المستند"] >= start_date) & (filtered_df["تاريخ المستند"] <= end_date)
            ]

        # تنظيف مسار المرفقات لعرض اسم الملف فقط داخل الجدول العادي
        display_df = filtered_df.copy()
        display_df["المرفقات"] = display_df["المرفقات"].apply(
            lambda x: os.path.basename(str(x)) if x != "بدون مرفق" and pd.notna(x) else "بدون مرفق"
        )

        desired_columns = [
            "اسم المادة", "وحدة القياس", "الكمية", "رقم القائمة", 
            "رقم المستند", "تاريخ المستند", "تاريخ التسجيل", 
            "الجهة المستفيدة", "نوع المستند", "المرفقات"
        ]
        existing_cols = [col for col in desired_columns if col in display_df.columns]
        display_df = display_df[existing_cols]

        display_df = display_df.reset_index(drop=True)
        display_df.index = display_df.index + 1
        display_df.index.name = "التسلسل"

        st.markdown("---")
        st.markdown("### 📊 جدول سجل الوارد")
        
        st.markdown(
            """
            <style>
            div.stDataFrame { direction: ltr; text-align: left; }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        st.dataframe(display_df, use_container_width=True)
        
        # إجمالي الكميات وعرض الملفات
        if not filtered_df.empty:
            st.markdown("### 📈 إجمالي الكميات الواردة لكل مادة (نتيجة البحث الحالي)")
            summary_df = filtered_df.groupby("اسم المادة")["الكمية"].sum().reset_index()
            summary_df.columns = ["اسم المادة", "إجمالي الكمية الواردة"]
            st.dataframe(summary_df, use_container_width=True)
            
            st.markdown("---")
            with st.expander("📂 لوحة عرض وطباعة المرفقات للسجلات الظاهرة"):
                st.info("💡 اختر المستند المطلوب أدناه لعرض المرفق الخاص به وطباعته مباشرة دون الحاجة للتحميل.")
                
                attachment_options = []
                row_mapping = {}
                for idx, row in filtered_df.iterrows():
                    att_name = os.path.basename(str(row["المرفقات"])) if row["المرفقات"] != "بدون مرفق" and pd.notna(row["المرفقات"]) else "بدون مرفق"
                    label_text = f"المادة: {row['اسم المادة']} | المستند: {row['رقم المستند']} | الملف: {att_name}"
                    attachment_options.append(label_text)
                    row_mapping[label_text] = row
                
                selected_option_label = st.selectbox("اختر المستند/المرفق للعرض والطباعة:", attachment_options)
                
                if selected_option_label:
                    selected_row = row_mapping[selected_option_label]
                    att_file_path = selected_row["المرفقات"]
                    file_name_only = os.path.basename(str(att_file_path)) if att_file_path != "بدون مرفق" else "بدون مرفق"
                    
                    st.write(f"**الملف المحدد:** {file_name_only}")
                    
                    if att_file_path != "بدون مرفق" and os.path.exists(str(att_file_path)):
                        file_ext = os.path.splitext(att_file_path)[1].lower()
                        
                        try:
                            with open(att_file_path, "rb") as f_att:
                                bytes_data = f_att.read()
                                b64_encoded_file = base64.b64encode(bytes_data).decode("utf-8")
                            
                            if file_ext == ".pdf":
                                pdf_display = f'<iframe src="data:application/pdf;base64,{b64_encoded_file}" width="100%" height="600px" type="application/pdf"></iframe>'
                                st.markdown(pdf_display, unsafe_allow_html=True)
                            elif file_ext in [".png", ".jpg", ".jpeg"]:
                                img_display = f'<div style="text-align:center;"><img src="data:image/{file_ext[1:]};base64,{b64_encoded_file}" style="max-width:100%; height:auto; border-radius:8px;"></div>'
                                st.markdown(img_display, unsafe_allow_html=True)
                            else:
                                st.warning("⚠️ نوع الملف المرفق لا يدعم العرض المباشر.")
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء عرض الملف: {e}")
                    else:
                        st.warning("⚠️ لا يوجد ملف مرفق لهذا السجل أو أن الملف غير موجود محلياً.")
            
            # --- قسم إعداد وتصدير التقرير الرسمي A4 العرضي ---
            st.markdown("---")
            st.subheader("🖨️ إعداد التقرير الرسمي للطباعة (A4 عرضي)")
            
            report_title_input = st.text_input("أدخل عنوان التقرير (مثال: تقرير الوارد المخزني لشهر تموز)", value="تقرير حركة الوارد المخزني")
            
            if st.button("📄 توليد معاينة التقرير الرسمي"):
                def number_to_words(n):
                    try:
                        n = int(n)
                    except:
                        return str(n)
                    if n == 0:
                        return "صفر"
                    ones = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]
                    tens = ["", "عشرة", "عشرون", "ثلاثون", "أربعون", "خمسون", "ستون", "سبعون", "ثمانون", "تسعون"]
                    teens = ["عشرة", "أحد عشر", "اثنا عشر", "ثلاثة عشر", "أربعة عشر", "خمسة عشر", "ستة عشر", "سبعة عشر", "ثمانية عشر", "تسعة عشر"]
                    
                    if n < 10:
                        return ones[n]
                    elif 10 <= n < 20:
                        return teens[n - 10]
                    elif 20 <= n < 100:
                        t = n // 10
                        o = n % 10
                        return ones[o] + (" و " + tens[t] if o != 0 else tens[t])
                    elif 100 <= n < 1000:
                        h = n // 100
                        rem = n % 100
                        h_str = "مائة" if h == 1 else ("مائتان" if h == 2 else ones[h] + "مائة")
                        return h_str + (" و " + number_to_words(rem) if rem != 0 else "")
                    elif 1000 <= n < 1000000:
                        th = n // 1000
                        rem = n % 1000
                        th_str = "ألف" if th == 1 else ("ألفان" if th == 2 else number_to_words(th) + " آلاف")
                        return th_str + (" و " + number_to_words(rem) if rem != 0 else "")
                    return str(n)

                aggregated_data = []
                grouped = filtered_df.groupby(["اسم المادة", "وحدة القياس"])
                
                seq = 1
                for (item_name, unit), group in grouped:
                    total_qty = group["الكمية"].sum() if "الكمية" in group.columns else 0
                    
                    lists = ", ".join(group["رقم القائمة"].dropna().astype(str).unique())
                    docs = ", ".join(group["رقم المستند"].dropna().astype(str).unique())
                    dates = ", ".join(pd.to_datetime(group["تاريخ المستند"]).dt.strftime('%Y-%m-%d').dropna().unique())
                    
                    aggregated_data.append({
                        "التسلسل": seq,
                        "اسم المادة": item_name,
                        "وحدة القياس": unit,
                        "الكمية رقما": total_qty,
                        "الكمية كتابة": number_to_words(total_qty),
                        "رقم القائمة": lists,
                        "رقم المستند": docs,
                        "تاريخ المستند": dates
                    })
                    seq += 1
                
                report_df = pd.DataFrame(aggregated_data)
                
                logo_path = os.path.join(os.path.expanduser("~"), "Desktop", "logo.jpg")
                logo_base64 = ""
                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as img_file:
                        logo_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                
                # الكود المحسّن للـ HTML والـ CSS (الإطار يحيط بكل الصفحة، والخط الفاصل تحت الترويسة)
                html_content = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <style>
                        @page {{
                            size: A4 landscape;
                            margin: 6mm;
                        }}
                        * {{
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                            box-sizing: border-box;
                        }}
                        body {{
                            font-family: 'Cairo', 'Tahoma', sans-serif;
                            background-color: #ffffff;
                            color: #000000;
                            margin: 0;
                            padding: 0;
                            direction: rtl;
                        }}
                        .a4-container {{
                            width: 100%;
                            min-height: 195mm;
                            margin: 0 auto;
                            padding: 15px;
                            border: 6px double #1b4d3e; /* إطار يحيط بكامل الورقة */
                            background: #fcfcfc;
                        }}
                        .header-table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 10px;
                        }}
                        .header-table td {{
                            vertical-align: middle;
                        }}
                        .right-header {{
                            text-align: right;
                            font-weight: bold;
                            font-size: 15px;
                            line-height: 1.6;
                            color: #1b4d3e;
                        }}
                        .center-header {{
                            text-align: center;
                            font-size: 20px;
                            font-weight: bold;
                            color: #b8860b;
                            text-decoration: underline;
                        }}
                        .left-header {{
                            text-align: left;
                        }}
                        .left-header img {{
                            width: 75px;
                            height: auto;
                        }}
                        .divider {{
                            border: none;
                            height: 3px;
                            background: linear-gradient(to left, #1b4d3e, #b8860b, #1b4d3e);
                            margin-top: 5px;
                            margin-bottom: 15px;
                        }}
                        .report-table {{
                            width: 100%;
                            border-collapse: collapse;
                            text-align: center;
                            margin-top: 10px;
                        }}
                        .report-table th, .report-table td {{
                            border: 1.5px solid #333333;
                            padding: 8px 6px;
                            font-size: 13px;
                            font-weight: bold;
                        }}
                        .report-table th {{
                            background-color: #1b4d3e !important;
                            color: #ffffff !important;
                        }}
                        .report-table tr:nth-child(even) {{
                            background-color: #f2f2f2 !important;
                        }}
                    </style>
                </head>
                <body>
                    <div class="a4-container">
                        <table class="header-table">
                            <tr>
                                <td class="right-header" style="width: 35%;">
                                    العتبة الكاظمية المقدسة<br>
                                    قسم الشؤون الخدمية<br>
                                    وحدة إدارة المخازن
                                </td>
                                <td class="center-header" style="width: 30%;">
                                    {report_title_input}
                                </td>
                                <td class="left-header" style="width: 35%; text-align: left;">
                                    {"<img src='data:image/png;base64," + logo_base64 + "'>" if logo_base64 else "<b>[شعار العتبة]</b>"}
                                </td>
                            </tr>
                        </table>
                        
                        <!-- الخط الفاصل تم وضعه هنا تحت الترويسة مباشرة وفوق الجدول -->
                        <hr class="divider">
                        
                        <table class="report-table">
                            <thead>
                                <tr>
                                    <th>التسلسل</th>
                                    <th>اسم المادة</th>
                                    <th>وحدة القياس</th>
                                    <th>الكمية رقماً</th>
                                    <th>الكمية كتابةً</th>
                                    <th>رقم القائمة</th>
                                    <th>رقم المستند</th>
                                    <th>تاريخ المستند</th>
                                </tr>
                            </thead>
                            <tbody>
                """
                
                for idx, row in report_df.iterrows():
                    html_content += f"""
                                <tr>
                                    <td>{row['التسلسل']}</td>
                                    <td>{row['اسم المادة']}</td>
                                    <td>{row['وحدة القياس']}</td>
                                    <td>{row['الكمية رقما']}</td>
                                    <td>{row['الكمية كتابة']}</td>
                                    <td>{row['رقم القائمة']}</td>
                                    <td>{row['رقم المستند']}</td>
                                    <td>{row['تاريخ المستند']}</td>
                                </tr>
                    """
                
                html_content += """
                            </tbody>
                        </table>
                    </div>
                </body>
                </html>
                """
                
                st.markdown("### 🖨️ معاينة التقرير الجاهز للطباعة:")
                st.components.v1.html(html_content, height=650, scrolling=True)
                
                st.download_button(
                    label="📥 تحميل التقرير كملف HTML (اضغط عليه ثم اطبع عبر المتصفح بوضع Landscape)",
                    data=html_content,
                    file_name="التقرير_المخزني_الرسمي.html",
                    mime="text/html"
                )
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لخيارات البحث المحددة.")
    else:
        st.info("ℹ️ لا توجد بيانات واردة مسجلة حتى الآن.")

import os
import base64
import pandas as pd
import streamlit as st
import streamlit as st
import pandas as pd

# تهيئة الجلسة العامة للبرنامج
if "barcodes_data" not in st.session_state:
    st.session_state.barcodes_data = pd.DataFrame(columns=[
        "رقم الباركود", "اسم المادة", "بذمة من", "رقم الباج", "القسم", "الشعبة", "الوحدة", "الموقع", "ملاحظات"
    ])
# 8. قسم الباركودات مع إضافة استمارة الذمة الرسمية (A4 طولي)
if menu_option == "🏷️ قسم الباركودات":
    st.subheader("🏷️ قسم إدارة الباركودات والذمم المخزنية")
    
    # اختيار وضع العمل (تسجيل جديد أو تعديل باركود حالي)
    action_mode = st.radio("اختر العملية:", ["تسجيل باركود جديد", "تعديل باركود موجود"], horizontal=True)
    
    if action_mode == "تسجيل باركود جديد":
        with st.form("barcode_form"):
            bc_col1, bc_col2, bc_col3 = st.columns(3)
            with bc_col1:
                bc_number = st.text_input("رقم الباركود")
                bc_item_name = st.text_input("اسم المادة")
                bc_holder = st.text_input("بذمة من (اسم الشخص)")
            with bc_col2:
                bc_badge = st.text_input("رقم الباج")
                bc_department = st.text_input("القسم")
                bc_branch = st.text_input("الشعبة")
            with bc_col3:
                bc_unit = st.text_input("الوحدة")
                bc_location = st.text_input("الموقع")
                bc_notes = st.text_area("ملاحظات")
                
            bc_submitted = st.form_submit_button("حفظ الباركود الجديد")
            
            if bc_submitted:
                if bc_number and bc_item_name:
                    new_bc_row = {
                        "رقم الباركود": bc_number,
                        "اسم المادة": bc_item_name,
                        "بذمة من": bc_holder,
                        "رقم الباج": bc_badge,
                        "القسم": bc_department,
                        "الشعبة": bc_branch,
                        "الوحدة": bc_unit,
                        "الموقع": bc_location,
                        "ملاحظات": bc_notes
                    }
                    st.session_state.barcodes_data = pd.concat(
                        [st.session_state.barcodes_data, pd.DataFrame([new_bc_row])], 
                        ignore_index=True
                    )
                    st.success("✅ تمت إضافة الباركود وتسجيل البيانات بنجاح!")
                else:
                    st.error("⚠️ يرجى إدخال 'رقم الباركود' و'اسم المادة' على الأقل.")
                    
    else:  # وضع تعديل باركود موجود
        if not st.session_state.barcodes_data.empty:
            selected_barcode = st.selectbox(
                "اختر رقم الباركود المراد تعديله:", 
                st.session_state.barcodes_data["رقم الباركود"].tolist()
            )
            
            if selected_barcode:
                row_to_edit = st.session_state.barcodes_data[
                    st.session_state.barcodes_data["رقم الباركود"] == selected_barcode
                ].iloc[0]
                
                with st.form("edit_barcode_form"):
                    e_col1, e_col2, e_col3 = st.columns(3)
                    with e_col1:
                        new_bc_number = st.text_input("رقم الباركود", value=str(row_to_edit["رقم الباركود"]))
                        new_item_name = st.text_input("اسم المادة", value=str(row_to_edit["اسم المادة"]))
                        new_holder = st.text_input("بذمة من (اسم الشخص)", value=str(row_to_edit.get("بذمة من", "")))
                    with e_col2:
                        new_badge = st.text_input("رقم الباج", value=str(row_to_edit.get("رقم الباج", "")))
                        new_department = st.text_input("القسم", value=str(row_to_edit["القسم"]))
                        new_branch = st.text_input("الشعبة", value=str(row_to_edit["الشعبة"]))
                    with e_col3:
                        new_unit = st.text_input("الوحدة", value=str(row_to_edit["الوحدة"]))
                        new_location = st.text_input("الموقع", value=str(row_to_edit["الموقع"]))
                        new_notes = st.text_area("ملاحظات", value=str(row_to_edit["ملاحظات"]))
                        
                    update_submitted = st.form_submit_button("تحديث بيانات الباركود")
                    
                    if update_submitted:
                        st.session_state.barcodes_data.loc[
                            st.session_state.barcodes_data["رقم الباركود"] == selected_barcode,
                            ["رقم الباركود", "اسم المادة", "بذمة من", "رقم الباج", "القسم", "الشعبة", "الوحدة", "الموقع", "ملاحظات"]
                        ] = [new_bc_number, new_item_name, new_holder, new_badge, new_department, new_branch, new_unit, new_location, new_notes]
                        
                        st.success("✅ تم تحديث بيانات الباركود بنجاح!")
        else:
            st.info("لا توجد باركودات مسجلة لتعديلها.")

    st.markdown("---")
    
    # قسم البحث المخصص والمستقل لكل فئة
    st.subheader("🔍 البحث المخصص لكل فئة")
    
    if not st.session_state.barcodes_data.empty:
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            s_barcode = st.text_input("بحث برقم الباركود")
            s_item = st.text_input("بحث باسم المادة")
        with f_col2:
            s_holder = st.text_input("بحث بذمة من (الشخص)")
            s_dept = st.text_input("بحث بالقسم")
        with f_col3:
            s_branch = st.text_input("بحث بالشعبة")
            s_unit = st.text_input("بحث بالوحدة أو الموقع")
            
        filtered_bc_df = st.session_state.barcodes_data.copy()
        
        # التأكد من وجود أعمدة الحقول الجديدة إن لم تكن موجودة في البيانات القديمة
        for col_name in ["بذمة من", "رقم الباج"]:
            if col_name not in filtered_bc_df.columns:
                filtered_bc_df[col_name] = ""

        # تطبيق الفلاتر المخصصة بشكل مستقل
        if s_barcode:
            filtered_bc_df = filtered_bc_df[filtered_bc_df["رقم الباركود"].astype(str).str.contains(s_barcode, case=False)]
        if s_item:
            filtered_bc_df = filtered_bc_df[filtered_bc_df["اسم المادة"].astype(str).str.contains(s_item, case=False)]
        if s_holder:
            filtered_bc_df = filtered_bc_df[filtered_bc_df["بذمة من"].astype(str).str.contains(s_holder, case=False)]
        if s_dept:
            filtered_bc_df = filtered_bc_df[filtered_bc_df["القسم"].astype(str).str.contains(s_dept, case=False)]
        if s_branch:
            filtered_bc_df = filtered_bc_df[filtered_bc_df["الشعبة"].astype(str).str.contains(s_branch, case=False)]
        if s_unit:
            filtered_bc_df = filtered_bc_df[
                filtered_bc_df["الوحدة"].astype(str).str.contains(s_unit, case=False) | 
                filtered_bc_df["الموقع"].astype(str).str.contains(s_unit, case=False)
            ]
            
        # تسلسل تلقائي
        display_bc_df = filtered_bc_df.reset_index(drop=True)
        display_bc_df.index = display_bc_df.index + 1
        display_bc_df.index.name = "التسلسل"
        
        # تنسيق الجدول من اليسار لليمين
        st.markdown(
            """
            <style>
            div.stDataFrame { direction: ltr; text-align: left; }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("### 📊 جدول النتائج")
        st.dataframe(display_bc_df, use_container_width=True)
        st.info(f"عدد النتائج المطابقة: {len(filtered_bc_df)}")
        
        # --- قسم استمارة الذمة الرسمية (A4 طولي) ---
        if not filtered_bc_df.empty:
            st.markdown("---")
            st.subheader("🖨️ إعداد وتوليد استمارة الذمة الرسمية (A4 طولي)")
            
            if st.button("📄 توليد معاينة استمارة الذمة"):
                holders = ", ".join(filtered_bc_df["بذمة من"].dropna().astype(str).unique())
                badges = ", ".join(filtered_bc_df["رقم الباج"].dropna().astype(str).unique())
                depts = ", ".join(filtered_bc_df["القسم"].dropna().astype(str).unique())
                branches = ", ".join(filtered_bc_df["الشعبة"].dropna().astype(str).unique())
                units = ", ".join(filtered_bc_df["الوحدة"].dropna().astype(str).unique())
                locations = ", ".join(filtered_bc_df["الموقع"].dropna().astype(str).unique())
                
                logo_path = os.path.join(os.path.expanduser("~"), "Desktop", "logo.jpg")
                logo_base64 = ""
                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as img_file:
                        logo_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                
                html_debt_content = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <style>
                        @page {{ size: A4 portrait; margin: 5mm; }}
                        * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
                        body {{ font-family: 'Cairo', 'Tahoma', sans-serif; background-color: #fff; color: #000; margin: 0; padding: 0; }}
                        .a4-portrait-container {{ width: 100%; max-width: 200mm; min-height: 283mm; margin: 0 auto; padding: 10px; box-sizing: border-box; border: 5px double #1b4d3e; background: #fcfcfc; position: relative; }}
                        .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; }}
                        .header-table td {{ vertical-align: middle; }}
                        .right-header {{ text-align: right; font-weight: bold; font-size: 14px; line-height: 1.5; color: #1b4d3e; }}
                        .center-header {{ text-align: center; font-size: 18px; font-weight: bold; color: #b8860b; text-decoration: underline; }}
                        .left-header {{ text-align: left; }}
                        .left-header img {{ width: 70px; height: auto; }}
                        .divider {{ border: none; height: 3px; background-color: #1b4d3e; background-image: linear-gradient(to left, #1b4d3e, #b8860b, #1b4d3e); margin-top: 5px; margin-bottom: 15px; }}
                        .info-box {{ background-color: #f2f4f3 !important; border: 1px solid #1b4d3e; padding: 10px 15px; margin-bottom: 15px; border-radius: 5px; font-size: 13px; font-weight: bold; line-height: 1.8; }}
                        .report-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-top: 10px; }}
                        .report-table th, .report-table td {{ border: 1.5px solid #333; padding: 10px; font-size: 14px; font-weight: bold; }}
                        .report-table th {{ background-color: #1b4d3e !important; color: #fff !important; }}
                        .report-table tr:nth-child(even) {{ background-color: #f2f2f2 !important; }}
                    </style>
                </head>
                <body>
                    <div class="a4-portrait-container">
                        <table class="header-table">
                            <tr>
                                <td class="right-header" style="width: 35%;">
                                    العتبة الكاظمية المقدسة<br>
                                    قسم الشؤون الخدمية<br>
                                    وحدة إدارة المخازن
                                </td>
                                <td class="center-header" style="width: 30%;">
                                    استمارة الذمة
                                </td>
                                <td class="left-header" style="width: 35%; text-align: left;">
                                    {"<img src='data:image/jpeg;base64," + logo_base64 + "'>" if logo_base64 else "<b>[شعار العتبة]</b>"}
                                </td>
                            </tr>
                        </table>
                        
                        <div class="divider"></div>
                        
                        <div class="info-box">
                            اسم صاحب الذمة: {holders if holders else "---"} &nbsp;|&nbsp; رقم الباج: {badges if badges else "---"}<br>
                            القسم: {depts if depts else "---"} &nbsp;|&nbsp; الشعبة: {branches if branches else "---"} &nbsp;|&nbsp; الوحدة: {units if units else "---"} &nbsp;|&nbsp; الموقع: {locations if locations else "---"}
                        </div>
                        
                        <table class="report-table">
                            <thead>
                                <tr>
                                    <th>التسلسل</th>
                                    <th>اسم المادة</th>
                                    <th>رقم الباركود</th>
                                </tr>
                            </thead>
                            <tbody>
                """
                
                for idx, row in display_bc_df.iterrows():
                    html_debt_content += f"""
                                <tr>
                                    <td>{idx}</td>
                                    <td>{row['اسم المادة']}</td>
                                    <td>{row['رقم الباركود']}</td>
                                </tr>
                    """
                
                html_debt_content += """
                            </tbody>
                        </table>
                    </div>
                </body>
                </html>
                """
                
                st.markdown("### 🖨️ معاينة استمارة الذمة للطباعة:")
                st.components.v1.html(html_debt_content, height=750, scrolling=True)
                
                st.download_button(
                    label="📥 تحميل استمارة الذمة كملف HTML (اضغط عليه ثم اطبع بوضع Portrait)",
                    data=html_debt_content,
                    file_name="استمارة_الذمة_الرسمية.html",
                    mime="text/html"
                )
    else:
        st.info("ℹ️ لا توجد باركودات مسجلة للبحث عنها حتى الآن.")# 9. قسم رصيد الأقداح البلاستيكية والصابون السائل
elif menu_option == "🧼 رصيد الأقداح والصابون السائل":
    st.subheader("🥤 قسم إدارة رصيد الأقداح البلاستيكية والصابون السائل")
    
    # تهيئة جدول الأقداح والصابون في الـ session_state إذا لم يكن موجوداً
    if "cups_soap_data" not in st.session_state:
        st.session_state.cups_soap_data = pd.DataFrame(columns=[
            "التاريخ", "اسم المادة", "الموقع / المخزن", "رصيد البداية", "الوارد", 
            "الصادر", "الرصيد النهائي", "اسم المستلم", "طريقة الوارد", "ملاحظات"
        ])
        
    sub_action = st.radio("اختر العملية:", ["تسجيل حركة يومية جديدة (وارد/صادر)", "بحث وتقارير خلال فترة زمنية"], horizontal=True)
    
    if sub_action == "تسجيل حركة يومية جديدة (وارد/صادر)":
        with st.form("cups_soap_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                t_date = st.date_input("التاريخ")
                item_choice = st.selectbox("اسم المادة", ["أقداح بلاستيكية", "صابون سائل"])
            with col2:
                warehouse_choice = st.selectbox("الموقع / المخزن", ["المخزن الرئيسي (1)", "المخزن الفرعي (2)"])
                # حساب رصيد البداية تلقائياً بناءً على آخر رصيد نهائي مسجل لنفس المادة ونفس المخزن
                previous_balance = 0.0
                if not st.session_state.cups_soap_data.empty:
                    last_match = st.session_state.cups_soap_data[
                        (st.session_state.cups_soap_data["اسم المادة"] == item_choice) & 
                        (st.session_state.cups_soap_data["الموقع / المخزن"] == warehouse_choice)
                    ]
                    if not last_match.empty:
                        previous_balance = float(last_match.iloc[-1]["الرصيد النهائي"])
                
                start_balance = st.number_input("رصيد البداية", value=previous_balance, step=1.0)
            with col3:
                incoming_qty = st.number_input("الكمية الواردة", min_value=0.0, value=0.0, step=1.0)
                outgoing_qty = st.number_input("الكمية الصادرة", min_value=0.0, value=0.0, step=1.0)
                
            col4, col5 = st.columns(2)
            with col4:
                receiver_name = st.text_input("اسم المستلم (عند وجود وارد)")
                incoming_type = st.selectbox("طريقة الوارد", ["حسب مذكرة", "بدون مذكرة", "لا يوجد وارد"])
            with col5:
                notes_text = st.text_area("ملاحظات إضافية")
                
            submit_cs = st.form_submit_button("حفظ وترحيل الحركة اليومية")
            
            if submit_cs:
                # حساب الرصيد النهائي تلقائياً: (رصيد البداية + الوارد - الصادر)
                final_balance = start_balance + incoming_qty - outgoing_qty
                
                new_row = {
                    "التاريخ": str(t_date),
                    "اسم المادة": item_choice,
                    "الموقع / المخزن": warehouse_choice,
                    "رصيد البداية": start_balance,
                    "الوارد": incoming_qty,
                    "الصادر": outgoing_qty,
                    "الرصيد النهائي": final_balance,
                    "اسم المستلم": receiver_name if incoming_qty > 0 else "---",
                    "طريقة الوارد": incoming_type if incoming_qty > 0 else "---",
                    "ملاحظات": notes_text
                }
                
                st.session_state.cups_soap_data = pd.concat(
                    [st.session_state.cups_soap_data, pd.DataFrame([new_row])], 
                    ignore_index=True
                )
                st.success(f"✅ تم تسجيل حركة اليوم بنجاح! الرصيد النهائي الحالي هو: {final_balance} (وسيُرحل تلقائياً كرصيد بداية لليوم القادم).")
                
    else:  # وضع البحث والتقارير الزمنية
        st.subheader("📊 البحث والتقارير التفصيلية خلال فترة زمنية")
        
        if not st.session_state.cups_soap_data.empty:
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                filter_item = st.selectbox("تصفية حسب المادة:", ["الكل", "أقداح بلاستيكية", "صابون سائل"])
            with r_col2:
                filter_warehouse = st.selectbox("تصفية حسب المخزن:", ["الكل", "المخزن الرئيسي (1)", "المخزن الفرعي (2)"])
            with r_col3:
                start_f_date = st.date_input("من تاريخ")
                end_f_date = st.date_input("إلى تاريخ")
                
            df_report = st.session_state.cups_soap_data.copy()
            
            # تطبيق الفلاتر
            if filter_item != "الكل":
                df_report = df_report[df_report["اسم المادة"] == filter_item]
            if filter_warehouse != "الكل":
                df_report = df_report[df_report["الموقع / المخزن"] == filter_warehouse]
                
            # الفلترة حسب التاريخ
            df_report["التاريخ_dt"] = pd.to_datetime(df_report["التاريخ"])
            df_report = df_report[
                (df_report["التاريخ_dt"] >= pd.to_datetime(start_f_date)) & 
                (df_report["التاريخ_dt"] <= pd.to_datetime(end_f_date))
            ]
            df_report = df_report.drop(columns=["التاريخ_dt"])
            
            # عرض الملخص والإحصائيات
            if not df_report.empty:
                total_in = df_report["الوارد"].sum()
                losses_out = df_report["الصادر"].sum()
                
                m1, m2 = st.columns(2)
                m1.metric("إجمالي الوارد خلال الفترة", f"{total_in}")
                m2.metric("إجمالي الصادر خلال الفترة", f"{losses_out}")
                
                st.markdown("### 📋 جدول الحركات التفصيلية")
                display_report_df = df_report.reset_index(drop=True)
                display_report_df.index = display_report_df.index + 1
                display_report_df.index.name = "التسلسل"
                
                st.dataframe(display_report_df, use_container_width=True)
            else:
                st.warning("⚠️ لا توجد بيانات مطابقة لهذه الفترة أو الفلاتر المحددة.")
        else:
            st.info("ℹ️ لا توجد سجلات مخزنية مسجلة حتى الآن.")
import os
import base64
import pandas as pd
import streamlit as st

# دالة مساعدة لتحويل الأرقام إلى كلمات عربية للكميات (كتابة)
def number_to_arabic_words(num):
    try:
        num = float(num)
        if num == int(num):
            num = int(num)
        return f"فقط ({num}) لا غير"
    except:
        return str(num)
import os
import base64
import pandas as pd
import streamlit as st

# دالة لتحويل الأرقام إلى كلمات عربية صحيحة (تفصيلية)
def number_to_arabic_words_full(num):
    try:
        num = float(num)
        if num.is_integer():
            num = int(num)
            ones_words = {
                0: "صفر", 1: "واحد", 2: "اثنان", 3: "ثلاثة", 4: "أربعة", 
                5: "خمسة", 6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة",
                10: "عشرة", 11: "أحد عشر", 12: "اثنا عشر", 13: "ثلاثة عشر",
                14: "أربعة عشر", 15: "خمسة عشر", 16: "ستة عشر", 17: "سبعة عشر",
                18: "ثمانية عشر", 19: "تسعة عشر", 20: "عشرون", 30: "ثلاثون",
                40: "أربعون", 50: "خمسون", 60: "ستون", 70: "سبعون", 80: "ثمانون", 90: "تسعون",
                100: "مائة", 200: "مئتان"
            }
            if num in ones_words:
                word = ones_words[num]
            else:
                word = str(num)
            return f"فقط ({word}) لا غير"
        else:
            return f"فقط ({num}) لا غير"
    except:
        return str(num)
# --- قسم الصرف المخزني ومستند الصرف الرسمي (A4 بالعرض Landscape) ---
if menu_option == "📤 قسم الصرف المخزني":    
    st.subheader("📤 قسم الصرف المخزني وإنشاء مستند الصرف الرسمي")
    
    if "issued_data" not in st.session_state:
        st.session_state.issued_data = pd.DataFrame(columns=[
            "رقم المستند", "تاريخ المستند", "نوع المستند", "نوع المخزن", 
            "رقم القائمة", "تاريخ القائمة", "القسم", "الشعبة", "الوحدة", 
            "اسم المادة", "القياس", "الكمية", "ملاحظات", "حالة الصادر"
        ])
        
    if "export_records" not in st.session_state:
        st.session_state.export_records = pd.DataFrame(columns=[
            "رقم المستند", "تاريخ المستند", "نوع المستند", "نوع المخزن", 
            "رقم القائمة", "القسم", "الشعبة", "الوحدة", "المواد المصروفة", "ملف المستند"
        ])

    with st.form("issue_doc_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            doc_type = st.text_input("نوع المستند", value="صرف مخزني")
            warehouse_type = st.text_input("نوع المخزن", value="المخزن الرئيسي")
            doc_number = st.text_input("رقم المستند")
            doc_date = st.date_input("تاريخ المستند")
        with col2:
            list_number = st.text_input("بموجب القائمة (رقم الموافقة)")
            list_date = st.date_input("تاريخ القائمة")
            # تثبيت القسم على اسم واحد فقط
            department = st.text_input("القسم (جهزت المواد الى القسم)", value="قسم الشؤون الخدمية", disabled=True)
        with col3:
            # تحديث قائمة الشعب بالخيارات المطلوبة
            branch_options = [
                "شعبة رعاية الصحون الخارجية",
                "شعبة الخدمات الخارجية",
                "شعبة التنظيف الالي",
                "شعبة الشؤون الخدمية نساء"
            ]
            branch = st.selectbox("الشعبة", branch_options)
            
            # تحديث قائمة الوحدات بالخيارات المطلوبة
            unit_options = [
                "وحدة إدارة المخازن",
                "صحن الرسول الاعظم (ص) وصحن الامام الصادق (ع)",
                "صحن امير المومنين وسيدة نساء العالمين وصحن الحسنين وصحن الامام الرضا (عليهما السلام)",
                "صحن العسكريين وصحن صاحب الزمان (عليهما السلام)",
                "الصحن الشريف (الصحن القديم)",
                "التعطير",
                "المكتبة القرانية",
                "العجلات الخدمية",
                "الصيانة",
                "غسل السجاد والمفروشات",
                "عجلات التنظيف",
                "الطرق والمقتربات",
                "المجاميع الصحية (رجال)",
                "الحرم المطهر للنساء",
                "وحدة المجاميع الصحية للنساء",
                "وحدة الادارة"
            ]
            unit = st.selectbox("الوحدة", unit_options)
            notes = st.text_area("ملاحظات عامة")
            
        st.markdown("---")
        st.markdown("#### 📦 إضافة المواد المراد صرفها")
        
        if "inventory_stock" in st.session_state and not st.session_state.inventory_stock.empty:
            item_options = st.session_state.inventory_stock["اسم المادة"].tolist()
            selected_item_to_issue = st.selectbox("اختر المادة للصرف", item_options)
            
            matching_rows = st.session_state.inventory_stock[st.session_state.inventory_stock["اسم المادة"] == selected_item_to_issue]
            available_sizes = matching_rows["القياس"].tolist() if "القياس" in matching_rows.columns else ["قطعة"]
            selected_size = st.selectbox("القياس", available_sizes)
            
            available_qty = float(matching_rows[matching_rows["القياس"] == selected_size]["الكمية"].values[0]) if not matching_rows.empty and "الكمية" in matching_rows.columns else 0.0
            st.info(f"الكمية المتاحة حالياً في المخزن لهذه المادة والقياس: **{available_qty}**")
            
            issue_qty = st.number_input("الكمية المراد صرفها", min_value=0.0, max_value=max(available_qty, 0.0), step=1.0)
        else:
            st.warning("⚠️ لا توجد مواد في الرصيد المخزني حالياً للصرف منها.")
            selected_item_to_issue, selected_size, issue_qty = "", "", 0.0
            
        submit_issue = st.form_submit_button("💾 حفظ مستند الصرف وخصم الكمية وارفاقه للصادر")
        
        if submit_issue:
            if doc_number and list_number and issue_qty > 0:
                existing_match = (
                    (st.session_state.inventory_stock["اسم المادة"] == selected_item_to_issue) & 
                    (st.session_state.inventory_stock["القياس"] == selected_size)
                )
                if existing_match.any():
                    current_stock_val = float(st.session_state.inventory_stock.loc[existing_match, "الكمية"].values[0])
                    if issue_qty <= current_stock_val:
                        st.session_state.inventory_stock.loc[existing_match, "الكمية"] = current_stock_val - issue_qty
                        st.session_state.stock_data = st.session_state.inventory_stock.copy()
                        
                        new_issue_row = {
                            "رقم المستند": doc_number,
                            "تاريخ المستند": str(doc_date),
                            "نوع المستند": doc_type,
                            "نوع المخزن": warehouse_type,
                            "رقم القائمة": list_number,
                            "تاريخ القائمة": str(list_date),
                            "القسم": department,
                            "الشعبة": branch,
                            "الوحدة": unit,
                            "اسم المادة": selected_item_to_issue,
                            "القياس": selected_size,
                            "الكمية": issue_qty,
                            "ملاحظات": notes,
                            "حالة الصادر": "تم الصرف والترحيل"
                        }
                        st.session_state.issued_data = pd.concat(
                            [st.session_state.issued_data, pd.DataFrame([new_issue_row])], 
                            ignore_index=True
                        )
                        
                        st.success("✅ تم حفظ مستند الصرف، خصم الكمية من الرصيد، وترحيل البيانات بنجاح!")
                    else:
                        st.error("⚠️ الكمية المراد صرفها أكبر من الرصيد المتاح في المخزن!")
                else:
                    st.error("⚠️ المادة المحددة غير موجودة في الرصيد المخزني!")
            else:
                st.error("⚠️ يرجى ملء حقول رقم المستند، رقم القائمة، وكمية صرف صحيحة.")

    # معاينة وتوليد مستند الصرف الرسمي (A4 بالعرض Landscape)
    if not st.session_state.issued_data.empty:
        st.markdown("---")
        st.subheader("🖨️ معاينة وتوليد مستند الصرف المخزني (A4 عرضي)")
        
        unique_docs = st.session_state.issued_data["رقم المستند"].unique().tolist()
        selected_doc_to_print = st.selectbox("اختر رقم المستند للطباعة وعرض أولياته:", unique_docs, key="print_doc_select")
        
        if selected_doc_to_print:
            doc_df = st.session_state.issued_data[st.session_state.issued_data["رقم المستند"] == selected_doc_to_print]
            first_row = doc_df.iloc[0]
            
            logo2_path = os.path.join(os.path.expanduser("~"), "Desktop", "logo.jpg")
            logo2_base64 = ""
            if os.path.exists(logo2_path):
                with open(logo2_path, "rb") as img_file:
                    logo2_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                    
            html_issue_content = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4 landscape;
                        margin: 5mm;
                    }}
                    * {{
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }}
                    body {{
                        font-family: 'Cairo', 'Tahoma', sans-serif;
                        background-color: #fff;
                        color: #000;
                        margin: 0;
                        padding: 0;
                    }}
                    .a4-landscape-container {{
                        width: 287mm;
                        height: 200mm;
                        margin: 0 auto;
                        padding: 12px 15px;
                        box-sizing: border-box;
                        border: 5px double #1b4d3e;
                        background: #fcfcfc !important;
                        position: relative;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }}
                    .content-wrapper {{ width: 100%; }}
                    .header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 2px; }}
                    .header-table td {{ vertical-align: top; }}
                    .right-header {{ text-align: right; font-weight: bold; font-size: 13px; line-height: 1.6; color: #1b4d3e; width: 33%; }}
                    .center-header {{ text-align: center; width: 34%; }}
                    .center-header img {{ width: 65px; height: auto; }}
                    .left-header {{ text-align: left; font-family: 'Tahoma', sans-serif; font-size: 11px; font-weight: bold; line-height: 1.4; color: #1b4d3e; width: 33%; }}
                    .divider {{ border: none; height: 3px; background: linear-gradient(to left, #1b4d3e, #b8860b, #1b4d3e) !important; margin: 5px 0 8px 0; }}
                    .sub-header-table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; font-size: 13px; font-weight: bold; }}
                    .sub-header-table td {{ vertical-align: top; padding: 3px; }}
                    .report-table {{ width: 100%; border-collapse: collapse; text-align: center; margin-top: 5px; }}
                    .report-table th, .report-table td {{ border: 1.5px solid #333; padding: 6px; font-size: 13px; font-weight: bold; }}
                    .report-table th {{ background-color: #1b4d3e !important; color: #fff !important; }}
                    .signatures-table {{ width: 100%; border-collapse: collapse; text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 5px; }}
                    .signature-line {{ margin-top: 25px; border-top: 1.5px dashed #000; width: 75%; margin-left: auto; margin-right: auto; }}
                </style>
            </head>
            <body>
                <div class="a4-landscape-container">
                    <div class="content-wrapper">
                        <table class="header-table">
                            <tr>
                                <td class="right-header">
                                    العتبة الكاظمية المقدسة<br>
                                    قسم الشؤون الخدمية<br>
                                    وحدة إدارة المخازن
                                </td>
                                <td class="center-header">
                                    {"<img src='data:image/jpeg;base64," + logo2_base64 + "'>" if logo2_base64 else "<b>[شعار Logo 2]</b>"}
                                </td>
                                <td class="left-header">
                                    Secretariat General<br>
                                    AL-Kadhmia Holly Shrine<br>
                                    Warehouses Department
                                </td>
                            </tr>
                        </table>
                        
                        <div class="divider"></div>
                        
                        <table class="sub-header-table">
                            <tr>
                                <td style="width: 35%; text-align: right;">
                                    نوع المخزن : {first_row.get('نوع المخزن', '---')}<br>
                                    بموجب القائمة : {first_row.get('رقم القائمة', '---')}<br>
                                    جهزت المواد الى القسم : {first_row.get('القسم', '---')}
                                </td>
                                <td style="width: 30%; text-align: center;">
                                    <div style="font-size: 15px; color: #b8860b; text-decoration: underline; margin-bottom: 4px;">{first_row.get('نوع المستند', 'صرف مخزني')}</div>
                                    المؤرخ في : {first_row.get('تاريخ القائمة', '---')}<br>
                                    الشعبة : {first_row.get('الشعبة', '---')}
                                </td>
                                <td style="width: 35%; text-align: left;">
                                    رقم المستند : {first_row.get('رقم المستند', '---')}<br>
                                    التاريخ : {first_row.get('تاريخ المستند', '---')}<br>
                                    رقم الموافقة : {first_row.get('رقم القائمة', '---')}<br>
                                    الوحدة : {first_row.get('الوحدة', '---')}
                                </td>
                            </tr>
                        </table>
                        
                        <table class="report-table">
                            <thead>
                                <tr>
                                    <th>التسلسل</th>
                                    <th>اسم المادة</th>
                                    <th>القياس</th>
                                    <th>الكمية</th>
                                    <th>الكمية كتابة</th>
                                    <th>الملاحظات</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            
            for idx, r in doc_df.reset_index(drop=True).iterrows():
                qty_val = r['الكمية']
                qty_words = number_to_arabic_words_full(qty_val)
                html_issue_content += f"""
                                <tr>
                                    <td>{idx + 1}</td>
                                    <td>{r['اسم المادة']}</td>
                                    <td>{r['القياس']}</td>
                                    <td>{qty_val}</td>
                                    <td>{qty_words}</td>
                                    <td>{r.get('ملاحظات', '---')}</td>
                                </tr>
                """
                
            html_issue_content += f"""
                            </tbody>
                        </table>
                    </div>
                    
                    <table class="signatures-table">
                        <tr>
                            <td style="width: 33%; text-align: right; padding-right: 20px;">
                                لجنة الاستلام
                                <div class="signature-line" style="margin-right: 0;"></div>
                            </td>
                            <td style="width: 34%; text-align: center;">
                                لجنة التدقيق
                                <div class="signature-line"></div>
                            </td>
                            <td style="width: 33%; text-align: left; padding-left: 20px;">
                                إدارة وحدة المخازن
                                <div class="signature-line" style="margin-left: 0; margin-right: auto;"></div>
                            </td>
                        </tr>
                    </table>
                </div>
            </body>
            </html>
            """
            
            st.components.v1.html(html_issue_content, height=650, scrolling=True)
            
            st.download_button(
                label="📥 تحميل مستند الصرف كملف HTML وطباعته بوضع Landscape",
                data=html_issue_content,
                file_name=f"مستند_صرف_{selected_doc_to_print}.html",
                mime="text/html"
            )
            
            if st.button("📁 اعتماد وترحيل المستند إلى قسم الصادر المخزني كأوليات"):
                if "out_df" not in st.session_state:
                    st.session_state.out_df = pd.DataFrame(columns=[
                        "اسم المادة", "وحدة القياس", "الكمية", "رقم القائمة", 
                        "رقم المستند", "تاريخ المستند", "تاريخ التسجيل", 
                        "القسم", "نوع المستند", "المرفقات"
                    ])
                
                already_exists = False
                if not st.session_state.out_df.empty:
                    already_exists = (st.session_state.out_df["رقم المستند"].astype(str) == str(selected_doc_to_print)).any()
                
                if not already_exists:
                    new_rows_to_add = []
                    for _, row in doc_df.iterrows():
                        new_out_row = {
                            "اسم المادة": row['اسم المادة'],
                            "وحدة القياس": row['القياس'],
                            "الكمية": row['الكمية'],
                            "رقم القائمة": first_row.get("رقم القائمة"),
                            "رقم المستند": selected_doc_to_print,
                            "تاريخ المستند": first_row.get("تاريخ المستند"),
                            "تاريخ التسجيل": str(datetime.date.today()),
                            "القسم": first_row.get("القسم"),
                            "نوع المستند": first_row.get(" نوع المستند"),
                            "المرفقات": html_issue_content
                        }
                        new_rows_to_add.append(new_out_row)
                    
                    st.session_state.out_df = pd.concat(
                        [st.session_state.out_df, pd.DataFrame(new_rows_to_add)], 
                        ignore_index=True
                    )
                    st.success("✅ تم ترحيل مستند الصرف وأولياته بنجاح إلى قسم الصادر المخزني!")
                else:
                    st.warning("⚠️ هذا المستند مرحل مسبقاً إلى قسم الصادر المخزني.")# --- قسم الصادر المخزني والبحث وتقرير A4 العرضي الرسمي ---
if menu_option == "📤 قسم الصادر المخزني":
    st.subheader("📤 قسم الصادر المخزني")
    
    # التأكد من تهيئة متغير الصادر في الـ session_state لضمان جلب البيانات المترحلة
    if "out_df" not in st.session_state:
        st.session_state.out_df = pd.DataFrame(columns=[
            "اسم المادة", "وحدة القياس", "الكمية", "رقم القائمة", 
            "رقم المستند", "تاريخ المستند", "تاريخ التسجيل", 
            "القسم", "نوع المستند", "المرفقات"
        ])
    
    out_df = st.session_state.out_df

    if not out_df.empty:
        st.markdown("### 🔍 خيارات البحث والتصفية المستقلة المتقدمة")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            search_item_out = st.text_input("🔍 بحث حسب اسم المادة", key="search_item_out")
            search_list_no_out = st.text_input("🔍 بحث حسب رقم القائمة", key="search_list_no_out")
        with col_b2:
            search_doc_no_out = st.text_input("🔍 بحث حسب رقم المستند", key="search_doc_no_out")
            search_dept_out = st.text_input("🔍 بحث حسب الجهة أو القسم المستفيد", key="search_dept_out")
        with col_b3:
            doc_type_filter_out = st.selectbox(
                "📁 تصفية حسب نوع المستند", 
                ["الكل", "صرف مخزني", "مذكرة صرف", "سند صادر", "تحويل مخزني", "استرجاع"],
                key="doc_type_filter_out"
            )
            date_mode_out = st.radio("نوع البحث التاريخي", ["فترة مفتوحة", "تحديد فترة زمنية"], horizontal=True, key="date_mode_out")
        
        filtered_out_df = out_df.copy()
        
        # تطبيق الفلاتر
        if doc_type_filter_out != "الكل" and "نوع المستند" in filtered_out_df.columns:
            filtered_out_df = filtered_out_df[filtered_out_df["نوع المستند"] == doc_type_filter_out]
        if search_item_out and "اسم المادة" in filtered_out_df.columns:
            filtered_out_df = filtered_out_df[filtered_out_df["اسم المادة"].astype(str).str.contains(search_item_out, case=False, na=False)]
        if search_list_no_out and "رقم القائمة" in filtered_out_df.columns:
            filtered_out_df = filtered_out_df[filtered_out_df["رقم القائمة"].astype(str).str.contains(search_list_no_out, case=False, na=False)]
        if search_doc_no_out and "رقم المستند" in filtered_out_df.columns:
            filtered_out_df = filtered_out_df[filtered_out_df["رقم المستند"].astype(str).str.contains(search_doc_no_out, case=False, na=False)]
        if search_dept_out and "القسم" in filtered_out_df.columns:
            filtered_out_df = filtered_out_df[filtered_out_df["القسم"].astype(str).str.contains(search_dept_out, case=False, na=False)]
            
        if date_mode_out == "تحديد فترة زمنية" and "تاريخ المستند" in filtered_out_df.columns:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                start_date_out = st.date_input("تاريخ البداية", datetime.date.today() - datetime.timedelta(days=30), key="start_date_out")
            with col_d2:
                end_date_out = st.date_input("تاريخ النهاية", datetime.date.today(), key="end_date_out")
            
            filtered_out_df["تاريخ المستند"] = pd.to_datetime(filtered_out_df["تاريخ المستند"]).dt.date
            filtered_out_df = filtered_out_df[
                (filtered_out_df["تاريخ المستند"] >= start_date_out) & (filtered_out_df["تاريخ المستند"] <= end_date_out)
            ]

        # تنظيف مسار المرفقات لعرض اسم أو حالة الملف فقط داخل الجدول العادي
        display_out_df = filtered_out_df.copy()
        if "المرفقات" in display_out_df.columns:
            display_out_df["المرفقات"] = display_out_df["المرفقات"].apply(
                lambda x: "ملف مستند HTML متاح" if (x != "بدون مرفق" and pd.notna(x) and len(str(x)) > 50) else "بدون مرفق"
            )

        desired_cols_out = [
            "اسم المادة", "وحدة القياس", "الكمية", "رقم القائمة", 
            "رقم المستند", "تاريخ المستند", "تاريخ التسجيل", 
            "القسم", "نوع المستند", "المرفقات"
        ]
        existing_cols_out = [col for col in desired_cols_out if col in display_out_df.columns]
        display_out_df = display_out_df[existing_cols_out]

        display_out_df = display_out_df.reset_index(drop=True)
        display_out_df.index = display_out_df.index + 1
        display_out_df.index.name = "التسلسل"
        
        st.markdown("---")
        st.markdown("### 📊 جدول سجل الصادر")
        
        st.markdown(
            """
            <style>
            div.stDataFrame { direction: ltr; text-align: left; }
            </style>
            """, 
            unsafe_allow_html=True
        )
        
        st.dataframe(display_out_df, use_container_width=True)
        
        # إجمالي الكميات وعرض الملفات المرفقة
        if not filtered_out_df.empty:
            st.markdown("### 📈 إجمالي الكميات الصادرة لكل مادة (نتيجة البحث الحالي)")
            if "اسم المادة" in filtered_out_df.columns and "الكمية" in filtered_out_df.columns:
                summary_out_df = filtered_out_df.groupby("اسم المادة")["الكمية"].sum().reset_index()
                summary_out_df.columns = ["اسم المادة", "إجمالي الكمية الصادرة"]
                st.dataframe(summary_out_df, use_container_width=True)
            
            st.markdown("---")
            
            with st.expander("📂 لوحة فتح أو تحميل المستندات والأوليات للسجلات الظاهرة"):
                filtered_out_df_reset = filtered_out_df.reset_index(drop=True)
                filtered_out_df_reset.index = filtered_out_df_reset.index + 1
                
                selectbox_options = []
                for idx, r in filtered_out_df_reset.iterrows():
                    opt_label = f"تسلسل ({idx}) - مادة: {r.get('اسم المادة', '')} - مستند: {r.get('رقم المستند', '')} - كمية: {r.get('الكمية', '')}"
                    selectbox_options.append((idx, opt_label))
                
                if selectbox_options:
                    selected_opt = st.selectbox(
                        "اختر السجل المطلوب للاطلاع على أولياته:",
                        options=selectbox_options,
                        format_func=lambda x: x[1],
                        key="select_row_out_adv"
                    )
                    
                    if selected_opt:
                        row_idx_o = selected_opt[0]
                        selected_row_o = filtered_out_df_reset.loc[row_idx_o]
                        att_content_o = selected_row_o.get("المرفقات", "بدون مرفق")
                        doc_num_val = selected_row_o.get("رقم المستند", "مستند")
                        
                        st.markdown(f"**معلومات المستند المحدد:** المادة: `{selected_row_o.get('اسم المادة', '')}` | رقم المستند: `{doc_num_val}` | الكمية: `{selected_row_o.get('الكمية', '')}`")
                        
                        if att_content_o != "بدون مرفق" and pd.notna(att_content_o) and len(str(att_content_o)) > 50:
                            st.components.v1.html(str(att_content_o), height=400, scrolling=True)
                            st.download_button(
                                label="📥 تحميل ملف مستند الصرف الرسمي (HTML)",
                                data=str(att_content_o),
                                file_name=f"مستند_صرف_{doc_num_val}.html",
                                mime="text/html",
                                key=f"download_adv_out_{row_idx_o}"
                            )
                        else:
                            st.warning("⚠️ لا توجد أوليات أو ملف مرفق بهذا السجل.")
                else:
                    st.info("لا توجد سجلات متاحة في نطاق البحث الحالي.")
            
            # --- قسم إعداد وتصدير التقرير الرسمي A4 العرضي ---
            st.markdown("---")
            st.subheader("🖨 إعداد التقرير الرسمي للطباعة (A4 عرضي)")
            
            report_title_input_out = st.text_input("أدخل عنوان التقرير", value="تقرير حركة الصادر المخزني", key="report_title_input_out")
            
            if st.button("📄 توليد معاينة التقرير الرسمي", key="btn_gen_out_report_official"):
                def number_to_words(n):
                    try:
                        n = int(n)
                    except:
                        return str(n)
                    if n == 0:
                        return "صفر"
                    ones = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]
                    tens = ["", "عشرة", "عشرون", "ثلاثون", "أربعون", "خمسون", "ستون", "سبعون", "ثمانون", "تسعون"]
                    teens = ["عشرة", "أحد عشر", "اثنا عشر", "ثلاثة عشر", "أربعة عشر", "خمسة عشر", "ستة عشر", "سبعة عشر", "ثمانية عشر", "تسعة عشر"]
                    
                    if n < 10:
                        return ones[n]
                    elif 10 <= n < 20:
                        return teens[n - 10]
                    elif 20 <= n < 100:
                        t = n // 10
                        o = n % 10
                        return ones[o] + (" و " + tens[t] if o != 0 else tens[t])
                    elif 100 <= n < 1000:
                        h = n // 100
                        rem = n % 100
                        h_str = "مائة" if h == 1 else ("مائتان" if h == 2 else ones[h] + "مائة")
                        return h_str + (" و " + number_to_words(rem) if rem != 0 else "")
                    elif 1000 <= n < 1000000:
                        th = n // 1000
                        rem = n % 1000
                        th_str = "ألف" if th == 1 else ("ألفان" if th == 2 else number_to_words(th) + " آلاف")
                        return th_str + (" و " + number_to_words(rem) if rem != 0 else "")
                    return str(n)

                aggregated_data_out = []
                grouped_out = filtered_out_df.groupby(["اسم المادة", "وحدة القياس"])
                
                seq_o = 1
                for (item_name_o, unit_o), group_o in grouped_out:
                    total_qty_o = group_o["الكمية"].sum() if "الكمية" in group_o.columns else 0
                    
                    lists_o = ", ".join(group_o["رقم القائمة"].dropna().astype(str).unique()) if "رقم القائمة" in group_o.columns else ""
                    docs_o = ", ".join(group_o["رقم المستند"].dropna().astype(str).unique()) if "رقم المستند" in group_o.columns else ""
                    dates_o = ", ".join(pd.to_datetime(group_o["تاريخ المستند"]).dt.strftime('%Y-%m-%d').dropna().unique()) if "تاريخ المستند" in group_o.columns else ""
                    depts_o = ", ".join(group_o["القسم"].dropna().astype(str).unique()) if "القسم" in group_o.columns else ""
                    
                    aggregated_data_out.append({
                        "التسلسل": seq_o,
                        "اسم المادة": item_name_o,
                        "وحدة القياس": unit_o,
                        "الكمية رقما": total_qty_o,
                        "الكمية كتابة": number_to_words(total_qty_o),
                        "رقم القائمة": lists_o,
                        "رقم المستند": docs_o,
                        "تاريخ المستند": dates_o,
                        "القسم المستفيد": depts_o
                    })
                    seq_o += 1
                
                report_df_out = pd.DataFrame(aggregated_data_out)
                
                logo_path = os.path.join(os.path.expanduser("~"), "Desktop", "logo.jpg")
                logo_base64 = ""
                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as img_file:
                        logo_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                
                html_content_out = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <style>
                        @page {{
                            size: A4 landscape;
                            margin: 5mm;
                        }}
                        * {{
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                        }}
                        body {{
                            font-family: 'Cairo', 'Tahoma', sans-serif;
                            background-color: #fff;
                            color: #000;
                            margin: 0;
                            padding: 0;
                        }}
                        .a4-container {{
                            width: 287mm;
                            height: 200mm;
                            margin: 0 auto;
                            padding: 12px 15px;
                            box-sizing: border-box;
                            border: 5px double #1b4d3e;
                            background: #fcfcfc !important;
                            position: relative;
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                        }}
                        .content-wrapper {{ width: 100%; }}
                        .header-table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin-bottom: 2px;
                        }}
                        .header-table td {{
                            vertical-align: middle;
                        }}
                        .right-header {{
                            text-align: right;
                            font-weight: bold;
                            font-size: 13px;
                            line-height: 1.6;
                            color: #1b4d3e;
                            width: 33%;
                        }}
                        .center-header {{
                            text-align: center;
                            font-size: 16px;
                            font-weight: bold;
                            color: #b8860b;
                            text-decoration: underline;
                            width: 34%;
                        }}
                        .left-header {{
                            text-align: left;
                            width: 33%;
                        }}
                        .left-header img {{
                            width: 65px;
                            height: auto;
                        }}
                        .divider {{
                            border: none;
                            height: 3px;
                            background: linear-gradient(to left, #1b4d3e, #b8860b, #1b4d3e) !important;
                            margin: 5px 0 12px 0;
                        }}
                        .report-table {{
                            width: 100%;
                            border-collapse: collapse;
                            text-align: center;
                            margin-top: 5px;
                        }}
                        .report-table th, .report-table td {{
                            border: 1.5px solid #333;
                            padding: 6px;
                            font-size: 13px;
                            font-weight: bold;
                        }}
                        .report-table th {{
                            background-color: #1b4d3e !important;
                            color: #fff !important;
                        }}
                        .report-table tr:nth-child(even) {{
                            background-color: #f2f2f2 !important;
                        }}
                    </style>
                </head>
                <body>
                    <div class="a4-container">
                        <div class="content-wrapper">
                            <table class="header-table">
                                <tr>
                                    <td class="right-header">
                                        العتبة الكاظمية المقدسة<br>
                                        قسم الشؤون الخدمية<br>
                                        وحدة إدارة المخازن
                                    </td>
                                    <td class="center-header">
                                        {report_title_input_out}
                                    </td>
                                    <td class="left-header">
                                        {"<img src='data:image/jpeg;base64," + logo_base64 + "'>" if logo_base64 else "<b>[شعار العتبة]</b>"}
                                    </td>
                                </tr>
                            </table>
                            
                            <div class="divider"></div>
                            
                            <table class="report-table">
                                <thead>
                                    <tr>
                                        <th>التسلسل</th>
                                        <th>اسم المادة</th>
                                        <th>وحدة القياس</th>
                                        <th>الكمية رقماً</th>
                                        <th>الكمية كتابةً</th>
                                        <th>رقم القائمة</th>
                                        <th>رقم المستند</th>
                                        <th>تاريخ المستند</th>
                                        <th>القسم المستفيد</th>
                                    </tr>
                                </thead>
                                <tbody>
                """
                
                for idx, row in report_df_out.iterrows():
                    html_content_out += f"""
                                    <tr>
                                        <td>{row['التسلسل']}</td>
                                        <td>{row['اسم المادة']}</td>
                                        <td>{row['وحدة القياس']}</td>
                                        <td>{row['الكمية رقما']}</td>
                                        <td>{row['الكمية كتابة']}</td>
                                        <td>{row['رقم القائمة']}</td>
                                        <td>{row['رقم المستند']}</td>
                                        <td>{row['تاريخ المستند']}</td>
                                        <td>{row['القسم المستفيد']}</td>
                                    </tr>
                    """
                
                html_content_out += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                st.markdown("### 🖨 معاينة التقرير الجاهز للطباعة:")
                st.components.v1.html(html_content_out, height=700, scrolling=True)
                
                st.download_button(
                    label="📥 تحميل تقرير الصادر كملف HTML (اضغط عليه ثم اطبع عبر المتصفح بوضع Landscape)",
                    data=html_content_out,
                    file_name="تقرير_الصادر_الرسمي.html",
                    mime="text/html",
                    key="download_btn_out_html"
                )
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لخيارات البحث المحددة في الصادر.")
    else:
        st.info("ℹ️ لا توجد بيانات صادر مسجلة حتى الآن. قم بإنشاء واعتماد مستند صادر جديد من قسم الصرف المخزني لتظهر البيانات والخيارات هنا تلقائياً.")# --- قسم رصيد المخزن         st.info("ℹ️ لا توجد بيانات صادر مسجلة حتى الآن. قم بإنشاء واعتماد مستند صادر جديد من قسم الصرف المخزني لتظهر البيانات والخيارات هنا تلقائياً.")# --- قسم وسجل توزيع الشعب والقواطع والتقارير الرسمية كاملاً ---
if menu_option == "رصيد المخزن":
    st.subheader("📦 إدارة رصيد المخزن العام وسجل القواطع اليومي")
    
    # 1. تهيئة الأقسام والمتغيرات في session_state مع دعم الوارد والقطع والكراتين
    if "store_balance_df" not in st.session_state:
        st.session_state.store_balance_df = pd.DataFrame(columns=[
            "اسم المادة", "الرصيد الافتتاحي كرتون", "رصيد الافتتاحي قطع", 
            "سعة الكرتون", "إجمالي الوارد كرتون", "إجمالي الوارد قطع", "إجمالي الصادر", 
            "الرصيد المتبقي قطع", "الرصيد التفصيلي", "تاريخ التحديث"
        ])

    if "sections_sectors_df" not in st.session_state:
        st.session_state.sections_sectors_df = pd.DataFrame(columns=["الشعبة", "القاطع"])

    if "store_archive" not in st.session_state:
        st.session_state.store_archive = pd.DataFrame(columns=[
            "التاريخ", "الشعبة", "القاطع", "اسم المادة", "الكمية المصروفة"
        ])

    if "store_grid_register" not in st.session_state:
        st.session_state.store_grid_register = pd.DataFrame(columns=["الشعبة", "القاطع"])

    # دالة مساعدة لتوزيع الإجمالي قطع إلى (كراتين + قطع مفردة)
    def calculate_cartons_and_pcs(total_pcs, carton_cap):
        try:
            total_pcs = int(total_pcs)
            carton_cap = int(carton_cap)
            if carton_cap <= 0:
                carton_cap = 1
        except:
            total_pcs = 0
            carton_cap = 1
            
        cartons = total_pcs // carton_cap
        pcs = total_pcs % carton_cap
        return cartons, pcs, f"{cartons} كرتون و {pcs} قطعة"

    # --- نموذج الإدارة (إضافة مادة جديدة + إضافة وارد كرتون + إضافة قاطع وشعبة) ---
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        with st.form("add_new_mat_form_clean"):
            st.markdown("#### ➕ إضافة مادة جديدة أو تسجيل وارد جديد")
            
            action_type = st.radio("اختر العملية:", ["إضافة مادة جديدة", "إضافة وارد جديد لمادة موجودة"], horizontal=True)
            
            existing_mats = st.session_state.store_balance_df["اسم المادة"].tolist() if not st.session_state.store_balance_df.empty else []
            
            if action_type == "إضافة مادة جديدة":
                new_mat_name = st.text_input("اسم المادة الجديدة")
                c1, c2, c3 = st.columns(3)
                with c1:
                    new_open_carton = st.number_input("افتتاحي كرتون", min_value=0, value=0)
                with c2:
                    new_open_pcs = st.number_input("افتتاحي قطع", min_value=0, value=0)
                with c3:
                    new_carton_cap = st.number_input("سعة الكرتون", min_value=1, value=24)
                
                # إضافة وارد أولي كرتون عند إنشاء المادة بناءً على طلبك
                incoming_carton_init = st.number_input("الوارد الجديد (بالكرتون)", min_value=0, value=0, help="الوارد دائماً يتم إدخاله بالكرتون ليُضاف لرصيد الكراتين")
            else:
                new_mat_name = st.selectbox("اختر المادة", existing_mats if existing_mats else ["لا توجد مواد"])
                incoming_carton_init = st.number_input("الوارد الجديد (بالكرتون)", min_value=0, value=0, help="الوارد دائماً يتم إدخاله بالكرتون ليُضاف لرصيد الكراتين")
                new_open_carton, new_open_pcs, new_carton_cap = 0, 0, 24
                
            submitted_new_mat = st.form_submit_button("حفظ وتحديث")
            
            if submitted_new_mat and new_mat_name and new_mat_name != "لا توجد مواد":
                df_store = st.session_state.store_balance_df
                
                if action_type == "إضافة مادة جديدة":
                    if new_mat_name not in df_store["اسم المادة"].values:
                        carton_cap = int(new_carton_cap)
                        total_init_pcs = (int(new_open_carton) * carton_cap) + int(new_open_pcs)
                        total_incoming_pcs = int(incoming_carton_init) * carton_cap
                        total_net_pcs = total_init_pcs + total_incoming_pcs
                        
                        c_res, p_res, desc_res = calculate_cartons_and_pcs(total_net_pcs, carton_cap)
                        
                        new_row = {
                            "اسم المادة": new_mat_name,
                            "الرصيد الافتتاحي كرتون": int(new_open_carton),
                            "رصيد الافتتاحي قطع": int(new_open_pcs),
                            "سعة الكرتون": carton_cap,
                            "إجمالي الوارد كرتون": int(incoming_carton_init),
                            "إجمالي الوارد قطع": 0,
                            "إجمالي الصادر": 0.0,
                            "الرصيد المتبقي قطع": total_net_pcs,
                            "الرصيد التفصيلي": desc_res,
                            "تاريخ التحديث": str(datetime.date.today())
                        }
                        st.session_state.store_balance_df = pd.concat(
                            [df_store, pd.DataFrame([new_row])], 
                            ignore_index=True
                        )
                        
                        if new_mat_name not in st.session_state.store_grid_register.columns:
                            st.session_state.store_grid_register[new_mat_name] = 0.0
                            
                        st.success(f"✅ تمت إضافة المادة ({new_mat_name}) بنجاح!")
                        st.rerun()
                    else:
                        st.warning("⚠️ المادة موجودة مسبقاً. استخدم خيار 'إضافة وارد جديد للمادة موجودة'.")
                else:
                    # تحديث الوارد للمادة الموجودة
                    idx_match = df_store[df_store["اسم المادة"] == new_mat_name].index
                    if not idx_match.empty:
                        i = idx_match[0]
                        current_inc_carton = int(df_store.loc[i, "إجمالي الوارد كرتون"])
                        new_inc_carton = current_inc_carton + int(incoming_carton_init)
                        
                        carton_cap = int(df_store.loc[i, "سعة الكرتون"])
                        init_c = int(df_store.loc[i, "الرصيد الافتتاحي كرتون"])
                        init_p = int(df_store.loc[i, "رصيد الافتتاحي قطع"])
                        total_init_pcs = (init_c * carton_cap) + init_p
                        
                        total_incoming_pcs = new_inc_carton * carton_cap
                        total_issued = float(df_store.loc[i, "إجمالي الصادر"])
                        
                        net_pcs = max(0.0, (total_init_pcs + total_incoming_pcs) - total_issued)
                        c_res, p_res, desc_res = calculate_cartons_and_pcs(net_pcs, carton_cap)
                        
                        st.session_state.store_balance_df.loc[i, "إجمالي الوارد كرتون"] = new_inc_carton
                        st.session_state.store_balance_df.loc[i, "الرصيد المتبقي قطع"] = net_pcs
                        st.session_state.store_balance_df.loc[i, "الرصيد التفصيلي"] = desc_res
                        st.session_state.store_balance_df.loc[i, "تاريخ التحديث"] = str(datetime.date.today())
                        
                        st.success(f"✅ تمت إضافة الوارد ({incoming_carton_init} كرتون) للمادة ({new_mat_name}) بنجاح!")
                        st.rerun()

    with col_form2:
        with st.form("add_new_sector_form"):
            st.markdown("#### ➕ إضافة قاطع جديد وشعبته")
            new_section_name = st.text_input("اسم الشعبة (مثال: الشؤون الخدمية)")
            new_sector_name = st.text_input("اسم القاطع (مثال: مغسل السويدة)")
            
            submitted_new_sector = st.form_submit_button("حفظ القاطع والشعبة")
            if submitted_new_sector and new_section_name and new_sector_name:
                exists = False
                if not st.session_state.sections_sectors_df.empty:
                    exists = (
                        (st.session_state.sections_sectors_df["الشعبة"] == new_section_name) & 
                        (st.session_state.sections_sectors_df["القاطع"] == new_sector_name)
                    ).any()
                
                if not exists:
                    new_sec_row = {"الشعبة": new_section_name, "القاطع": new_sector_name}
                    st.session_state.sections_sectors_df = pd.concat(
                        [st.session_state.sections_sectors_df, pd.DataFrame([new_sec_row])], 
                        ignore_index=True
                    )
                    
                    grid_rows = []
                    for _, r_sec in st.session_state.sections_sectors_df.iterrows():
                        r_dict = {"الشعبة": r_sec["الشعبة"], "القاطع": r_sec["القاطع"]}
                        for m_col in st.session_state.store_balance_df["اسم المادة"].tolist():
                            r_dict[m_col] = 0.0
                        grid_rows.append(r_dict)
                    st.session_state.store_grid_register = pd.DataFrame(grid_rows)
                    
                    st.success(f"✅ تمت إضافة القاطع ({new_sector_name}) تحت شعبة ({new_section_name}) بنجاح!")
                    st.rerun()
                else:
                    st.warning("⚠️ هذا القاطع مرتبط بهذه الشعبة مسبقاً.")

    st.markdown("---")
    st.markdown("### 📊 جدول رصيد المخزن العام الحالي (يوضح الرصيد بالكرتون والقطع مفصلاً)")
    st.dataframe(st.session_state.store_balance_df, use_container_width=True)

    # --- خاصية الجرد الآلي والترحيل التلقائي قبل إنهاء وتصفية اليوم ---
    st.markdown("---")
    st.markdown("### 🔍 خاصية الجرد اليومي للمخزن وتصفية الحسابات")
    st.info("💡 خاصية الجرد: يمكنك إدخال الكميات الفعلية الموجودة فعلياً في المخزن أو القواطع. سيقوم النظام بمقارنتها واحتساب الصرف أو الفروقات وترحيلها تلقائياً للسجل والقواطع لضبط المادة.")

    if not st.session_state.store_balance_df.empty:
        with st.form("inventory_audit_form"):
            st.markdown("#### 📋 جدول جرد المواد الفعلي")
            audit_rows = []
            for idx, r in st.session_state.store_balance_df.iterrows():
                m_name = r["اسم المادة"]
                current_net_pcs = float(r["الرصيد المتبقي قطع"])
                cap = int(r["سعة الكرتون"])
                c_def, p_def, _ = calculate_cartons_and_pcs(current_net_pcs, cap)
                
                col_a1, col_a2, col_a3 = st.columns(3)
                with col_a1:
                    st.text(f"المادة: {m_name}")
                with col_a2:
                    audited_cartons = st.number_input(f"المجرد كرتون ({m_name})", min_value=0, value=c_def, key=f"aud_c_{idx}")
                with col_a3:
                    audited_pcs = st.number_input(f"المجرد قطع ({m_name})", min_value=0, value=p_def, key=f"aud_p_{idx}")
                
                audit_rows.append({"اسم المادة": m_name, "مجرد كرتون": audited_cartons, "مجرد قطع": audited_pcs, "سعة الكرتون": cap, "الرصيد الحالي قطع": current_net_pcs})
            
            submitted_audit = st.form_submit_button("🔄 اعتماد الجرد وضبط المخزن تلقائياً")
            if submitted_audit:
                today_str = str(datetime.date.today())
                archive_audit_rows = []
                
                for item in audit_rows:
                    m_name = item["اسم المادة"]
                    total_audited_pcs = (item["مجرد كرتون"] * item["سعة الكرتون"]) + item["مجرد قطع"]
                    old_pcs = item["الرصيد الحالي قطع"]
                    
                    # الفارق يعتبر صرفاً أو تسوية لضبط المخزن
                    diff_pcs = old_pcs - total_audited_pcs
                    if diff_pcs > 0:
                        # حدث استهلاك/صرف لتغطية العجز بين النظام والجرد الفعلي
                        archive_audit_rows.append({
                            "التاريخ": today_str,
                            "الشعبة": "تسوية جرد عامة",
                            "القاطع": "المخزن الرئيسي",
                            "اسم المادة": m_name,
                            "الكمية المصروفة": diff_pcs
                        })
                        
                        # تحديث إجمالي الصادر والرصيد
                        idx_m = st.session_state.store_balance_df[st.session_state.store_balance_df["اسم المادة"] == m_name].index[0]
                        curr_issued = float(st.session_state.store_balance_df.loc[idx_m, "إجمالي الصادر"]) + diff_pcs
                        st.session_state.store_balance_df.loc[idx_m, "إجمالي الصادر"] = curr_issued
                        st.session_state.store_balance_df.loc[idx_m, "الرصيد المتبقي قطع"] = total_audited_pcs
                        
                        _, _, desc_res = calculate_cartons_and_pcs(total_audited_pcs, item["سعة الكرتون"])
                        st.session_state.store_balance_df.loc[idx_m, "الرصيد التفصيلي"] = desc_res
                
                if archive_audit_rows:
                    st.session_state.store_archive = pd.concat(
                        [st.session_state.store_archive, pd.DataFrame(archive_audit_rows)], 
                        ignore_index=True
                    )
                
                st.success("✅ تم إجراء الجرد بنجاح، وتدوير الفروقات وتسويتها وترحيل الصرف التلقائي للمخزن!")
                st.rerun()

    st.markdown("---")
    st.markdown("### 📋 سجل توزيع الشعب والقواطع اليومي (أدخل الكميات المصروفة)")
    
    if not st.session_state.store_grid_register.empty and not st.session_state.store_balance_df.empty:
        edited_grid_df = st.data_editor(
            st.session_state.store_grid_register,
            use_container_width=True,
            key="grid_daily_editor"
        )
        
        if st.button("🔄 اعتماد وتحديث الخصم التلقائي وتصفير السجل لليوم الجديد"):
            today_str = str(datetime.date.today())
            archive_rows = []
            
            mat_columns = st.session_state.store_balance_df["اسم المادة"].tolist()
            for _, row in edited_grid_df.iterrows():
                sec_val = row["الشعبة"]
                sect_val = row["القاطع"]
                for mat in mat_columns:
                    if mat in row and float(row[mat]) > 0:
                        qty_val = float(row[mat])
                        archive_rows.append({
                            "التاريخ": today_str,
                            "الشعبة": sec_val,
                            "القاطع": sect_val,
                            "اسم المادة": mat,
                            "الكمية المصروفة": qty_val
                        })
            
            if archive_rows:
                st.session_state.store_archive = pd.concat(
                    [st.session_state.store_archive, pd.DataFrame(archive_rows)], 
                    ignore_index=True
                )
            
            for idx, row in st.session_state.store_balance_df.iterrows():
                mat_name = row["اسم المادة"]
                if mat_name in edited_grid_df.columns:
                    total_issued_today = edited_grid_df[mat_name].astype(float).sum()
                    
                    current_total_issued = float(row["إجمالي الصادر"]) + total_issued_today
                    carton_cap = float(row["سعة الكرتون"])
                    init_carton = float(row["الرصيد الافتتاحي كرتون"])
                    init_pcs = float(row["رصيد الافتتاحي قطع"])
                    inc_carton = float(row["إجمالي الوارد كرتون"])
                    
                    total_initial_pcs = (init_carton * carton_cap) + init_pcs + (inc_carton * carton_cap)
                    net_remaining = max(0.0, total_initial_pcs - current_total_issued)
                    _, _, detail_desc = calculate_cartons_and_pcs(net_remaining, carton_cap)
                    
                    st.session_state.store_balance_df.loc[idx, "إجمالي الصادر"] = current_total_issued
                    st.session_state.store_balance_df.loc[idx, "الرصيد المتبقي قطع"] = net_remaining
                    st.session_state.store_balance_df.loc[idx, "الرصيد التفصيلي"] = detail_desc
            
            st.session_state.store_grid_register[mat_columns] = 0.0
            
            st.success("✅ تم اعتماد الصرف، خصم الكميات من الرصيد، حفظ أرشيف اليوم، وتصفير السجل بنجاح!")
            st.rerun()
    else:
        st.info("ℹ️ يرجى إضافة مواد إلى المخزن وأقسام/قواطع لكي يظهر جدول السجل وتتمكن من إدخال الصرف.")

    # --- قسم البحث المتقدم في الأرشيف والتقارير اليومية والفترات ---
    st.markdown("---")
    st.markdown("### 🔍 البحث المتقدم في الصادر وتقارير الفترات الزمنية")
    
    if not st.session_state.store_archive.empty:
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            search_mat_arc = st.text_input("بحث حسب اسم المادة (اختياري)", key="search_mat_arc")
            search_sec_arc = st.text_input("بحث حسب الشعبة (اختياري)", key="search_sec_arc")
        with col_s2:
            search_sect_arc = st.text_input("بحث حسب القاطع (اختياري)", key="search_sect_arc")
            date_filter_mode = st.radio("نوع البحث الزمني", ["بدون فترة (كل الأرشيف)", "تحديد فترة زمنية"], horizontal=True, key="date_filter_mode")
        with col_s3:
            if date_filter_mode == "تحديد فترة زمنية":
                start_f_date = st.date_input("من تاريخ", datetime.date.today() - datetime.timedelta(days=7), key="start_f_date")
                end_f_date = st.date_input("إلى تاريخ", datetime.date.today(), key="end_f_date")

        filtered_arc = st.session_state.store_archive.copy()
        
        if search_mat_arc:
            filtered_arc = filtered_arc[filtered_arc["اسم المادة"].astype(str).str.contains(search_mat_arc, case=False, na=False)]
        if search_sec_arc:
            filtered_arc = filtered_arc[filtered_arc["الشعبة"].astype(str).str.contains(search_sec_arc, case=False, na=False)]
        if search_sect_arc:
            filtered_arc = filtered_arc[filtered_arc["القاطع"].astype(str).str.contains(search_sect_arc, case=False, na=False)]
            
        if date_filter_mode == "تحديد فترة زمنية":
            filtered_arc["التاريخ_dt"] = pd.to_datetime(filtered_arc["التاريخ"]).dt.date
            filtered_arc = filtered_arc[
                (filtered_arc["التاريخ_dt"] >= start_f_date) & (filtered_arc["التاريخ_dt"] <= end_f_date)
            ]

        st.markdown("#### 📄 نتائج حركات الصادر المطابقة للبحث:")
        st.dataframe(filtered_arc.drop(columns=["التاريخ_dt"], errors="ignore"), use_container_width=True)

        st.markdown("---")
        st.markdown("### 📊 التقارير الإجمالية للفترة المحددة")
        
        col_rep1, col_rep2, col_rep3 = st.columns(3)
        with col_rep1:
            st.markdown("##### 📌 إجمالي الصادر حسب المادة")
            if not filtered_arc.empty:
                rep_mat = filtered_arc.groupby("اسم المادة")["الكمية المصروفة"].sum().reset_index()
                st.dataframe(rep_mat, use_container_width=True)
            else:
                st.write("لا توجد بيانات.")
                
        with col_rep2:
            st.markdown("##### 📌 إجمالي الصادر حسب الشعبة")
            if not filtered_arc.empty:
                rep_sec = filtered_arc.groupby("الشعبة")["الكمية المصروفة"].sum().reset_index()
                st.dataframe(rep_sec, use_container_width=True)
            else:
                st.write("لا توجد بيانات.")
                
        with col_rep3:
            st.markdown("##### 📌 إجمالي الصادر حسب القاطع")
            if not filtered_arc.empty:
                rep_sect = filtered_arc.groupby("القاطع")["الكمية المصروفة"].sum().reset_index()
                st.dataframe(rep_sect, use_container_width=True)
            else:
                st.write("لا توجد بيانات.")

        # --- قسم توليد التقارير الرسمية (A4 عمودي Portrait) المطلوبة ---
        st.markdown("---")
        st.subheader("🖨️ توليد المستندات والتقارير الرسمية (A4 عمودي)")

        report_type_choice = st.selectbox(
            "اختر نوع التقرير الرسمي للطباعة:",
            [
                "تقرير حركة شعبة معينة خلال فترة", 
                "تقرير حركة قاطع معين خلال فترة", 
                "تقرير صرف مادة واحدة خلال فترة", 
                "تقرير الصادر الإجمالي الشامل خلال فترة"
            ],
            key="store_rep_choice"
        )
        
        col_rc1, col_rc2, col_rc3 = st.columns(3)
        with col_rc1:
            rep_start_date = st.date_input("من تاريخ", datetime.date.today() - datetime.timedelta(days=30), key="rep_start_date")
        with col_rc2:
            rep_end_date = st.date_input("إلى تاريخ", datetime.date.today(), key="rep_end_date")
        with col_rc3:
            selected_target_value = ""
            if report_type_choice == "تقرير حركة شعبة معينة خلال فترة":
                available_sections = st.session_state.store_archive["الشعبة"].dropna().unique().tolist()
                selected_target_value = st.selectbox("اختر الشعبة", available_sections, key="rep_sec_select")
            elif report_type_choice == "تقرير حركة قاطع معين خلال فترة":
                available_sectors = st.session_state.store_archive["القاطع"].dropna().unique().tolist()
                selected_target_value = st.selectbox("اختر القاطع", available_sectors, key="rep_sect_select")
            elif report_type_choice == "تقرير صرف مادة واحدة خلال فترة":
                available_materials = st.session_state.store_archive["اسم المادة"].dropna().unique().tolist()
                selected_target_value = st.selectbox("اختر المادة", available_materials, key="rep_mat_select")

        if st.button("📄 توليد معاينة التقرير الرسمي (A4 عمودي)", key="btn_generate_store_portrait_report"):
            temp_arc = st.session_state.store_archive.copy()
            temp_arc["التاريخ_dt"] = pd.to_datetime(temp_arc["التاريخ"]).dt.date
            
            filtered_rep_df = temp_arc[
                (temp_arc["التاريخ_dt"] >= rep_start_date) & (temp_arc["التاريخ_dt"] <= rep_end_date)
            ]
            
            report_title_text = "تقرير مخزني"
            if report_type_choice == "تقرير حركة شعبة معينة خلال فترة":
                filtered_rep_df = filtered_rep_df[filtered_rep_df["الشعبة"] == selected_target_value]
                report_title_text = f"تقرير حركة الصادر للشعبة: {selected_target_value}"
            elif report_type_choice == "تقرير حركة قاطع معين خلال فترة":
                filtered_rep_df = filtered_rep_df[filtered_rep_df["القاطع"] == selected_target_value]
                report_title_text = f"تقرير حركة الصادر للقاطع: {selected_target_value}"
            elif report_type_choice == "تقرير صرف مادة واحدة خلال فترة":
                filtered_rep_df = filtered_rep_df[filtered_rep_df["اسم المادة"] == selected_target_value]
                report_title_text = f"تقرير صرف المادة: {selected_target_value}"
            else:
                report_title_text = "تقرير الصادر الإجمالي الشامل للمخزن"

            # قراءة شعار logo من سطح المكتب
            logo1_path = os.path.join(os.path.expanduser("~"), "Desktop", "Logo.jpg")
            if not os.path.exists(logo1_path):
                logo1_path = os.path.join(os.path.expanduser("~"), "Desktop", "Logo.png")
            if not os.path.exists(logo1_path):
                logo1_path = os.path.join(os.path.expanduser("~"), "Desktop", "logo 1.jpg")
            if not os.path.exists(logo1_path):
                logo1_path = os.path.join(os.path.expanduser("~"), "Desktop", "logo 1.png")
                
            logo1_base64 = ""
            if os.path.exists(logo1_path):
                with open(logo1_path, "rb") as img_file:
                    logo1_base64 = base64.b64encode(img_file.read()).decode("utf-8")

            html_portrait_content = f"""
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4 portrait;
                        margin: 5mm;
                    }}
                    body {{
                        font-family: 'Cairo', 'Tahoma', sans-serif;
                        background-color: #fff;
                        color: #000;
                        margin: 0;
                        padding: 0;
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }}
                    .a4-portrait-container {{
                        width: 200mm;
                        height: 287mm;
                        margin: 0 auto;
                        padding: 12mm 10mm;
                        box-sizing: border-box;
                        border: 4px double #1b4d3e;
                        background: #fcfcfc;
                        position: relative;
                    }}
                    .header-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 10px;
                    }}
                    .header-table td {{
                        vertical-align: middle;
                    }}
                    .right-header {{
                        text-align: right;
                        font-weight: bold;
                        font-size: 13px;
                        line-height: 1.6;
                        color: #1b4d3e;
                        width: 35%;
                    }}
                    .center-header {{
                        text-align: center;
                        font-size: 15px;
                        font-weight: bold;
                        color: #b8860b;
                        text-decoration: underline;
                        width: 30%;
                    }}
                    .left-header {{
                        text-align: left;
                        width: 35%;
                    }}
                    .left-header img {{
                        width: 65px;
                        height: auto;
                    }}
                    .divider {{
                        border: none;
                        height: 2.5px;
                        background: linear-gradient(to left, #1b4d3e, #b8860b, #1b4d3e);
                        margin-bottom: 15px;
                    }}
                    .info-bar {{
                        font-size: 12px;
                        font-weight: bold;
                        margin-bottom: 15px;
                        text-align: center;
                        color: #333;
                    }}
                    .report-table {{
                        width: 100%;
                        border-collapse: collapse;
                        text-align: center;
                        margin-top: 10px;
                        margin-bottom: 20px;
                    }}
                    .report-table th, .report-table td {{
                        border: 1.2px solid #333;
                        padding: 8px 5px;
                        font-size: 12px;
                        font-weight: bold;
                    }}
                    .report-table th {{
                        background-color: #1b4d3e !important;
                        color: #fff !important;
                    }}
                    .report-table tr:nth-child(even) {{
                        background-color: #f9f9f9 !important;
                    }}
                </style>
            </head>
            <body>
                <div class="a4-portrait-container">
                    <table class="header-table">
                        <tr>
                            <td class="right-header">
                                العتبة الكاظمية المقدسة<br>
                                قسم الشؤون الخدمية<br>
                                وحدة إدارة المخازن
                            </td>
                            <td class="center-header">
                                {report_title_text}
                            </td>
                            <td class="left-header">
                                {"<img src='data:image/jpeg;base64," + logo1_base64 + "'>" if logo1_base64 else "<b>[شعار Logo]</b>"}
                            </td>
                        </tr>
                    </table>
                    
                    <hr class="divider">
                    
                    <div class="info-bar">
                        الفترة من : {rep_start_date} إلى : {rep_end_date}
                    </div>
                    
                    <table class="report-table">
                        <thead>
                            <tr>
                                <th>التسلسل</th>
                                <th>التاريخ</th>
                                <th>الشعبة</th>
                                <th>القاطع</th>
                                <th>اسم المادة</th>
                                <th>الكمية المصروفة</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            if not filtered_rep_df.empty:
                for idx, row in filtered_rep_df.reset_index(drop=True).iterrows():
                    html_portrait_content += f"""
                                <tr>
                                    <td>{idx + 1}</td>
                                    <td>{row['التاريخ']}</td>
                                    <td>{row.get('الشعبة', '---')}</td>
                                    <td>{row.get('القاطع', '---')}</td>
                                    <td>{row['اسم المادة']}</td>
                                    <td>{row['الكمية المصروفة']}</td>
                                </tr>
                    """
            else:
                html_portrait_content += """
                                <tr>
                                    <td colspan="6" style="padding: 20px; color: #777;">لا توجد بيانات مطابقة لهذه الفترة أو الاختيار.</td>
                                </tr>
                """
                
            html_portrait_content += f"""
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """
            
            st.markdown("### 🖨️ معاينة التقرير الرسمي (وضع عمودي Portrait):")
            st.components.v1.html(html_portrait_content, height=750, scrolling=True)
            
            st.download_button(
                label="📥 تحميل التقرير الرسمي كملف HTML (اطبعه بوضع Portrait عمودي من المتصفح)",
                data=html_portrait_content,
                file_name=f"تقرير_المخزن_{report_type_choice}.html",
                mime="text/html",
                key="download_portrait_report_btn"
            )
    else:
        st.info("ℹ️ لا يوجد أرشيف حركات صادر مسجل حتى الآن. قم بملء السجل والاعتماد لتتمكن من البحث واستخراج التقارير.")

# --- قسم رصيد المواد الاستهلاكية والجرد اليومي ---
if menu_option == "رصيد المواد الاستهلاكية":
    st.subheader("🛠️ إدارة رصيد المواد الاستهلاكية والجرد اليومي")
    
    # 1. تهيئة جداول المواد الاستهلاكية والأرشيف اليومي في session_state
    if "consumable_stock_df" not in st.session_state:
        st.session_state.consumable_stock_df = pd.DataFrame(columns=[
            "اسم المادة", "حالة المادة", "الرصيد الافتتاحي", 
            "إجمالي الوارد", "إجمالي الصادر", "إجمالي الراجع", 
            "الرصيد المتبقي", "تاريخ آخر تحديث"
        ])

    if "consumable_daily_grid" not in st.session_state:
        st.session_state.consumable_daily_grid = pd.DataFrame(columns=[
            "اسم المادة", "حالة المادة", "الوارد اليومي", 
            "الصادر اليومي", "الراجع اليومي", "ملاحظات"
        ])

    # 2. نموذج إضافة مادة استهلاكية جديدة
    with st.expander("➕ إضافة مادة استهلاكية جديدة للمخزن"):
        with st.form("add_consumable_mat_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                cons_mat_name = st.text_input("اسم المادة الاستهلاكية")
            with c2:
                cons_mat_status = st.selectbox("حالة المادة", ["جديد", "مستخدم", "تالف"])
            with c3:
                cons_open_qty = st.number_input("الرصيد الافتتاحي / الكمية", min_value=0, value=0)
                
            submitted_cons_mat = st.form_submit_button("حفظ وإضافة المادة الاستهلاكية")
            if submitted_cons_mat and cons_mat_name:
                # التحقق إذا كانت المادة بنفس الاسم والحالة موجودة مسبقاً
                exists = False
                if not st.session_state.consumable_stock_df.empty:
                    exists = (
                        (st.session_state.consumable_stock_df["اسم المادة"] == cons_mat_name) & 
                        (st.session_state.consumable_stock_df["حالة المادة"] == cons_mat_status)
                    ).any()

                if not exists:
                    new_cons_row = {
                        "اسم المادة": cons_mat_name,
                        "حالة المادة": cons_mat_status,
                        "الرصيد الافتتاحي": cons_open_qty,
                        "إجمالي الوارد": 0,
                        "إجمالي الصادر": 0,
                        "إجمالي الراجع": 0,
                        "الرصيد المتبقي": cons_open_qty,
                        "تاريخ آخر تحديث": str(datetime.date.today())
                    }
                    st.session_state.consumable_stock_df = pd.concat(
                        [st.session_state.consumable_stock_df, pd.DataFrame([new_cons_row])], 
                        ignore_index=True
                    )
                    
                    # تحديث جدول الجرد اليومي ليضم المادة الجديدة
                    grid_rows = []
                    for _, r_item in st.session_state.consumable_stock_df.iterrows():
                        grid_rows.append({
                            "اسم المادة": r_item["اسم المادة"],
                            "حالة المادة": r_item["حالة المادة"],
                            "الوارد اليومي": 0,
                            "الصادر اليومي": 0,
                            "الراجع اليومي": 0,
                            "ملاحظات": ""
                        })
                    st.session_state.consumable_daily_grid = pd.DataFrame(grid_rows)
                    
                    st.success(f"✅ تمت إضافة المادة الاستهلاكية ({cons_mat_name} - {cons_mat_status}) بنجاح!")
                    st.rerun()
                else:
                    st.warning("⚠️ هذه المادة بنفس الحالة موجودة مسبقاً في رصيد المواد الاستهلاكية.")

    st.markdown("---")
    st.markdown("### 📊 جدول رصيد المواد الاستهلاكية العام الحالي")
    if not st.session_state.consumable_stock_df.empty:
        st.dataframe(st.session_state.consumable_stock_df, use_container_width=True)
    else:
        st.info("ℹ️ لا توجد مواد استهلاكية مضافة حتى الآن. استخدم نموذج الإضافة في الأعلى.")

    st.markdown("---")
    st.markdown("### 📋 جدول الجرد والحركات اليومية (استهلاكية)")
    st.info("💡 أدخل الحركات اليومية (الوارد، الصادر، الراجع) مباشرة في الجدول أدناه، ثم اضغط على زر الاعتماد والتحديث لخصم وتحديث الأرصدة تلقائياً وتصفير الحقول ليوم جديد.")

    if not st.session_state.consumable_daily_grid.empty:
        # محرر البيانات للجرد اليومي
        edited_cons_grid = st.data_editor(
            st.session_state.consumable_daily_grid,
            use_container_width=True,
            key="cons_daily_editor_table"
        )

        if st.button("🔄 اعتماد وتحديث حركات المواد الاستهلاكية وتصفير الجرد اليومي"):
            today_date = str(datetime.date.today())
            
            # تحديث الأرصدة في جدول رصيد المواد الاستهلاكية بناءً على المدخلات اليومية
            for idx, row in st.session_state.consumable_stock_df.iterrows():
                m_name = row["اسم المادة"]
                m_status = row["حالة المادة"]
                
                # البحث عن الصف المطابق في الجدول المعدل
                match_row = edited_cons_grid[
                    (edited_cons_grid["اسم المادة"] == m_name) & 
                    (edited_cons_grid["حالة المادة"] == m_status)
                ]
                
                if not match_row.empty:
                    daily_in = float(match_row["الوارد اليومي"].values[0])
                    daily_out = float(match_row["الصادر اليومي"].values[0])
                    daily_back = float(match_row["الراجع اليومي"].values[0])
                    
                    # التجميع التراكمي
                    old_total_in = float(row["إجمالي الوارد"])
                    old_total_out = float(row["إجمالي الصادر"])
                    old_total_back = float(row["إجمالي الراجع"])
                    open_qty = float(row["الرصيد الافتتاحي"])
                    
                    new_total_in = old_total_in + daily_in
                    new_total_out = old_total_out + daily_out
                    new_total_back = old_total_back + daily_back
                    
                    # المعادلة الحسابية للرصيد المتبقي: (الافتتاحي + الوارد + الراجع) - الصادر
                    new_remaining = (open_qty + new_total_in + new_total_back) - new_total_out
                    
                    # تحديث القيم في DataFrame الأساسي
                    st.session_state.consumable_stock_df.loc[idx, "إجمالي الوارد"] = new_total_in
                    st.session_state.consumable_stock_df.loc[idx, "إجمالي الصادر"] = new_total_out
                    st.session_state.consumable_stock_df.loc[idx, "إجمالي الراجع"] = new_total_back
                    st.session_state.consumable_stock_df.loc[idx, "الرصيد المتبقي"] = max(0.0, new_remaining)
                    st.session_state.consumable_stock_df.loc[idx, "تاريخ آخر تحديث"] = today_date

            # تصفير حقول الحركات اليومية ليصبح جاهزاً لليوم التالي
            st.session_state.consumable_daily_grid["الوارد اليومي"] = 0.0
            st.session_state.consumable_daily_grid["الصادر اليومي"] = 0.0
            st.session_state.consumable_daily_grid["الراجع اليومي"] = 0.0
            st.session_state.consumable_daily_grid["ملاحظات"] = ""
            
            st.success("✅ تم اعتماد حركات المواد الاستهلاكية، وتحديث الأرصدة (وارد، صادر، راجع)، وتصفير الجرد اليومي بنجاح!")
            st.rerun()
    else:
        st.info("ℹ️ يرجى إضافة مواد استهلاكية أولاً ليظهر جدول الجرد اليومي.")
	 