import streamlit as st
import pandas as pd

# 1. Page Configuration & Design Setup
st.set_page_config(page_title="College Master Registry", layout="wide")
st.title("🛡️ Centralized College Reality & Cutoff Registry")
st.subheader("No Predictions. Only Absolute Transparency for Millions of Students!")
st.write("---")

# 2. Comprehensive Hardcoded Database (No External File Required)
@st.cache_data
def get_clean_college_database():
    return [
        {
            "college_name": "Veermata Jijabai Technological Institute (VJTI), Mumbai",
            "established": 1887,
            "accepted_exams": "MHT-CET, JEE Main",
            "overall_placement_rate": "92.4%",
            "highest_package": "62.0 LPA",
            "average_package": "11.8 LPA",
            "median_package": "9.5 LPA",
            "top_companies": "Google, Amazon, Morgan Stanley, TCS, Infosys",
            "scholarships_offered": [
                "Rajarshi Chhatrapati Shahu Maharaj Scheme (EBC) - 50% Fee Waiver",
                "TFWS (Tuition Fee Waiver Scheme) - 100% Tuition Fee Off",
                "Dr. Panjabrao Deshmukh Hostel Allowance Scheme"
            ],
            "cutoff_matrix": [
                {"Branch": "Computer Engineering", "Quota / Seat Type": "Open (Home State)", "Closing Percentile": 99.91},
                {"Branch": "Computer Engineering", "Quota / Seat Type": "TFWS (Fee Waiver)", "Closing Percentile": 99.97},
                {"Branch": "Computer Engineering", "Quota / Seat Type": "OBC (Home State)", "Closing Percentile": 99.75},
                {"Branch": "Information Technology", "Quota / Seat Type": "Open (Home State)", "Closing Percentile": 99.82},
                {"Branch": "Information Technology", "Quota / Seat Type": "Linguistic Minority (Gujarati)", "Closing Percentile": 94.20},
                {"Branch": "Electronics Engineering", "Quota / Seat Type": "Open (General)", "Closing Percentile": 98.90},
                {"Branch": "Mechanical Engineering", "Quota / Seat Type": "Open (General)", "Closing Percentile": 97.40},
                {"Branch": "Civil Engineering", "Quota / Seat Type": "Open (General)", "Closing Percentile": 92.10},
                {"Branch": "Civil Engineering", "Quota / Seat Type": "SC (Home State)", "Closing Percentile": 84.50}
            ]
        },
        {
            "college_name": "Thadomal Shahani Engineering College (TSEC), Mumbai",
            "established": 1977,
            "accepted_exams": "MHT-CET, JEE Main",
            "overall_placement_rate": "84.0%",
            "highest_package": "40.0 LPA",
            "average_package": "8.1 LPA",
            "median_package": "6.5 LPA",
            "top_companies": "Deutsche Bank, JP Morgan, Wipro, LTI, Cognizant",
            "scholarships_offered": [
                "MOMA Post-Matric Minority Scholarship - Up to ₹30,000/year",
                "TFWS Scheme - 100% Tuition Fee Waiver",
                "EBC Concession for Open Category Students"
            ],
            "cutoff_matrix": [
                {"Branch": "Computer Engineering", "Quota / Seat Type": "Open (General)", "Closing Percentile": 97.80},
                {"Branch": "Computer Engineering", "Quota / Seat Type": "Sindhi Linguistic Minority", "Closing Percentile": 81.20},
                {"Branch": "Artificial Intelligence & Data Science", "Quota / Seat Type": "Open (General)", "Closing Percentile": 95.40},
                {"Branch": "Artificial Intelligence & Data Science", "Quota / Seat Type": "Sindhi Linguistic Minority", "Closing Percentile": 74.50},
                {"Branch": "Information Technology", "Quota / Seat Type": "Open (General)", "Closing Percentile": 96.10},
                {"Branch": "Information Technology", "Quota / Seat Type": "Sindhi Linguistic Minority", "Closing Percentile": 78.00}
            ]
        }
    ]

db = get_clean_college_database()

# 3. Sidebar Panel for Student Inputs
st.sidebar.header("👤 Student Score Card")
user_exam = st.sidebar.selectbox("Aapne kaun sa exam diya?", ["MHT-CET", "JEE Main"])
student_score = st.sidebar.number_input("Apna Exact Percentile Daalein:", min_value=0.0, max_value=100.0, value=85.0, step=0.1)

# 4. Main Search Interface
college_names = [c["college_name"] for c in db]
selected_college = st.selectbox("🔍 Kis College Ki A to Z Report Card Dekhni Hai?", ["-- Select College --"] + college_names)

if selected_college != "-- Select College --":
    # College ka specific data extract karna
    college_data = None
    for c in db:
        if c["college_name"] == selected_college:
            college_data = c
            break
            
    if college_data:
        # TABS Create karna info clean dikhane ke liye
        tab1, tab2, tab3 = st.tabs(["📈 Placement & Profile", "📊 Branch Cutoff Matrix", "💰 Scholarships Available"])
        
        with tab1:
            st.markdown(f"## 🏢 {college_data['college_name']}")
            st.caption(f"📅 **Established Year:** {college_data['established']} | 📝 **Exam Accepted:** {college_data['accepted_exams']}")
            st.write("---")
            
            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Placement Rate", college_data["overall_placement_rate"])
            m2.metric("Highest Package", college_data["highest_package"])
            m3.metric("Average Package", college_data["average_package"])
            m4.metric("Median Package", college_data["median_package"])
            
            st.info(f"💼 **Top Recruiting Companies:** {college_data['top_companies']}")
            
        with tab2:
            st.markdown("### 🗂️ Complete Branch Closing List & Eligibility Check")
            st.write("Neeche diye gaye system data se match karein ki aapke marks par kaun si branch safe hai:")
            
            # DataFrame create karna cutoff list ke liye
            df_cutoffs = pd.DataFrame(college_data["cutoff_matrix"])
            
            # Filter Logic: Student ko kaun sa branch mil sakta hai
            eligible_options = df_cutoffs[df_cutoffs["Closing Percentile"] <= student_score]
            
            st.markdown(f"#### 🎯 Options Open for Your **{student_score}%tile**:")
            if not eligible_options.empty:
                st.success("Pichle saal ke official closing records ke mutabik aapko in combinations par seat mil sakti hai:")
                st.dataframe(eligible_options, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ Is college ki sabhi general/minority seats aapke percentile se upar band hui thi. Kripya doosra college check karein.")
                
            st.write("---")
            st.markdown("#### 📋 Full Institutional Closing Cutoff Matrix (All Quotas)")
            st.dataframe(df_cutoffs, use_container_width=True, hide_index=True)
            
        with tab3:
            st.markdown("### 💰 Financial Aid & Welfare Schemes")
            st.write("Is college mein padhte waqt aap in government ya institutional scholarships ka fayda utha sakte hain:")
            for s in college_data["scholarships_offered"]:
                st.markdown(f"- ✅ **{s}**")
else:
    st.info("💡 Shuru karne ke liye upar diye gaye drop-down se kisi ek college ka naam select karein, uski poori details samne aa jayengi.")
