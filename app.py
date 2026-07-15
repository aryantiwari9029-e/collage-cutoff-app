import streamlit as st
import pandas as pd

st.set_page_config(page_title="Maharashtra College Master Registry", layout="wide")
st.title("🛡️ Centralized College Reality & Cutoff Registry")
st.subheader("Live Master Data Portal — Maharashtra Top 20 Engineering Institutes")
st.write("---")

@st.cache_data
def load_dynamic_db():
    try:
        df = pd.read_csv("colleges.csv")
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return pd.DataFrame()

df_master = load_dynamic_db()

if not df_master.empty:
    st.sidebar.header("👤 Student Score Card")
    user_exam = st.sidebar.selectbox("Aapne kaun sa exam diya?", ["MHT-CET", "JEE Main"])
    student_score = st.sidebar.number_input("Apna Exact Percentile Daalein:", min_value=0.0, max_value=100.0, value=85.0, step=0.1)

    college_names = df_master["college_name"].tolist()
    selected_college = st.selectbox("🔍 Kis College Ki A to Z Report Card Dekhni Hai?", ["-- Select College --"] + college_names)

    if selected_college != "-- Select College --":
        row = df_master[df_master["college_name"] == selected_college].iloc[0]
        
        tab1, tab2, tab3 = st.tabs(["📈 Placement & Profile", "📊 Branch Cutoff Matrix", "💰 Scholarships Available"])
        
        with tab1:
            st.markdown(f"## 🏢 {row['college_name']}")
            st.caption(f"📅 **Established Year:** {row['established']} | 📝 **Exam Accepted:** {row['accepted_exams']}")
            st.write("---")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Placement Rate", str(row["placement_rate"]))
            m2.metric("Highest Package", str(row["highest_package"]))
            m3.metric("Average Package", str(row["average_package"]))
            m4.metric("Median Package", str(row["median_package"]))
            st.info(f"💼 **Top Recruiting Companies:** {row['top_companies']}")
            
        with tab2:
            st.markdown("### 🗂️ Complete Branch Closing List")
            
            raw_cutoffs = str(row["cutoff_matrix"]).split("|")
            cutoff_list = []
            for item in raw_cutoffs:
                parts = item.split(":")
                if len(parts) == 3:
                    cutoff_list.append({"Branch": parts[0], "Quota / Seat Type": parts[1], "Closing Percentile": float(parts[2])})
            
            df_cutoffs = pd.DataFrame(cutoff_list)
            eligible_options = df_cutoffs[df_cutoffs["Closing Percentile"] <= student_score]
            
            st.markdown(f"#### 🎯 Options Open for Your **{student_score}%tile**:")
            if not eligible_options.empty:
                st.success("Pichle saal ke official records ke mutabik aapko in seats par admission mil sakta hai:")
                st.dataframe(eligible_options, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ Is college ki sabhi seats pichle saal aapke percentile se upar band hui thi. Niche poori list check karein.")
                
            st.write("---")
            st.markdown("#### 📋 Full Institutional Closing Cutoff Matrix")
            st.dataframe(df_cutoffs, use_container_width=True, hide_index=True)
            
        with tab3:
            st.markdown("### 💰 Financial Aid & Welfare Schemes")
            for s in str(row["scholarships_offered"]).split(","):
                st.markdown(f"- ✅ **{s.strip()}**")
else:
    st.warning("Kripya check karein ki aapne GitHub par 'colleges.csv' file sahi se upload ki hai.")
# --- 30 NAYE COLLEGES KA COMPREHENSIVE DATA (A-to-Z DETAILS) ---
# Yeh sabhi colleges aapki purani list se bilkul alag hain aur ek hi code block mein hain.

more_colleges_data = [
    {
        "College Name": "IIT Bombay (IITB), Mumbai",
        "Established": 1958,
        "Entrance Exam": "JEE Advanced",
        "Cutoff (General - CSE)": "Opening-Closing Rank: 1 - 66",
        "Cutoff (Minority/EWS)": "EWS Rank: 1 - 15 | SC/ST Seats Reserved",
        "Highest Package": "3.67 Crore (International) / 1.00 Crore (Domestic)",
        "Average Package": "21.82 LPA",
        "Mean Package": "19.61 LPA",
        "Placement Rate": "93.5%",
        "State": "Maharashtra"
    },
    {
        "College Name": "ICT Mumbai (Institute of Chemical Technology)",
        "Established": 1933,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "99.10+ Percentile (Chemical Branches)",
        "Cutoff (Minority/EWS)": "OBC: 98.40% | EWS: 98.70% | SC/ST: 90%",
        "Highest Package": "25.00 LPA",
        "Average Package": "8.50 LPA",
        "Mean Package": "7.90 LPA",
        "Placement Rate": "87.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "VNIT Nagpur (Visvesvaraya National Institute of Tech)",
        "Established": 1960,
        "Entrance Exam": "JEE Main",
        "Cutoff (General - CSE)": "Home State Rank: 6000 - 8500",
        "Cutoff (Minority/EWS)": "OBC: 2800 Rank | SC/ST: 1200 Rank",
        "Highest Package": "64.00 LPA",
        "Average Package": "11.50 LPA",
        "Mean Package": "10.20 LPA",
        "Placement Rate": "89.2%",
        "State": "Maharashtra"
    },
    {
        "College Name": "IIIT Nagpur (Indian Institute of Information Tech)",
        "Established": 2016,
        "Entrance Exam": "JEE Main",
        "Cutoff (General - CSE)": "All India Rank: 22,000 - 25,000",
        "Cutoff (Minority/EWS)": "EWS: 4200 Rank | OBC: 8500 Rank",
        "Highest Package": "90.00 LPA",
        "Average Package": "14.03 LPA",
        "Mean Package": "13.10 LPA",
        "Placement Rate": "84.5%",
        "State": "Maharashtra"
    },
    {
        "College Name": "IIIT Pune (Indian Institute of Information Tech)",
        "Established": 2016,
        "Entrance Exam": "JEE Main",
        "Cutoff (General - CSE)": "All India Rank: 15,000 - 18,000",
        "Cutoff (Minority/EWS)": "EWS: 2800 Rank | OBC: 6200 Rank",
        "Highest Package": "53.00 LPA",
        "Average Package": "16.83 LPA",
        "Mean Package": "15.20 LPA",
        "Placement Rate": "88.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Army Institute of Technology (AIT), Pune",
        "Established": 1994,
        "Entrance Exam": "JEE Main",
        "Cutoff (General - CSE)": "All India Army Wards Rank: 50,000",
        "Cutoff (Minority/EWS)": "Strictly for Army Wards Only (Merit Based)",
        "Highest Package": "52.00 LPA",
        "Average Package": "14.20 LPA",
        "Mean Package": "12.80 LPA",
        "Placement Rate": "96.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Government College of Engineering, Jalgaon",
        "Established": 1996,
        "Entrance Exam": "MHT-CET",
        "Cutoff (General - CSE)": "95.20+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 94.10% | SC: 84.50% | ST: 71.00%",
        "Highest Package": "15.00 LPA",
        "Average Package": "4.80 LPA",
        "Mean Package": "4.20 LPA",
        "Placement Rate": "76.5%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Government College of Engineering, Chandrapur",
        "Established": 1996,
        "Entrance Exam": "MHT-CET",
        "Cutoff (General - CSE)": "92.80+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 91.50% | EWS: 90.90% | SC: 82.00%",
        "Highest Package": "12.00 LPA",
        "Average Package": "4.20 LPA",
        "Mean Package": "3.80 LPA",
        "Placement Rate": "72.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Government College of Engineering, Yavatmal",
        "Established": 2018,
        "Entrance Exam": "MHT-CET",
        "Cutoff (General - CSE)": "90.50+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 89.20% | SC: 78.00% | ST: 65.00%",
        "Highest Package": "10.00 LPA",
        "Average Package": "3.90 LPA",
        "Mean Package": "3.50 LPA",
        "Placement Rate": "68.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Sies Graduate School of Technology, Navi Mumbai",
        "Established": 2002,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "95.10+ Percentile",
        "Cutoff (Minority/EWS)": "South Indian Tamil Linguistic Minority: 74.00%",
        "Highest Package": "24.00 LPA",
        "Average Package": "5.80 LPA",
        "Mean Package": "5.20 LPA",
        "Placement Rate": "81.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "M.H. Saboo Siddik College of Engineering, Mumbai",
        "Established": 1984,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "88.50+ Percentile",
        "Cutoff (Minority/EWS)": "Muslim Religious Minority Quota: 72.30%",
        "Highest Package": "18.00 LPA",
        "Average Package": "4.80 LPA",
        "Mean Package": "4.20 LPA",
        "Placement Rate": "79.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Anjuman-I-Islam's Kalsekar Technical Campus, Navi Mumbai",
        "Established": 2011,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "82.40+ Percentile",
        "Cutoff (Minority/EWS)": "Muslim Religious Minority Quota: 61.00%",
        "Highest Package": "14.50 LPA",
        "Average Package": "4.10 LPA",
        "Mean Package": "3.60 LPA",
        "Placement Rate": "74.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Theem College of Engineering, Palghar",
        "Established": 2009,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "71.20+ Percentile",
        "Cutoff (Minority/EWS)": "Muslim Religious Minority Quota: 45.00%",
        "Highest Package": "9.00 LPA",
        "Average Package": "3.50 LPA",
        "Mean Package": "3.10 LPA",
        "Placement Rate": "66.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Vidyavardhini's College of Engineering (VCET), Vasai",
        "Established": 1994,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "92.10+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 90.30% | EWS: 89.90% | SC/ST: 76%",
        "Highest Package": "16.00 LPA",
        "Average Package": "4.80 LPA",
        "Mean Package": "4.40 LPA",
        "Placement Rate": "80.5%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Sanjay Ghodawat University, Kolhapur",
        "Established": 2009,
        "Entrance Exam": "MHT-CET / JEE Main / SGUEE",
        "Cutoff (General - CSE)": "81.50+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 78.20% | EWS: 79.00% | SC/ST: 62%",
        "Highest Package": "15.00 LPA",
        "Average Package": "4.20 LPA",
        "Mean Package": "3.80 LPA",
        "Placement Rate": "78.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Terna Engineering College, Navi Mumbai",
        "Established": 1991,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "90.40+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 88.50% | EWS: 87.90% | SC/ST: 72%",
        "Highest Package": "22.00 LPA",
        "Average Package": "5.00 LPA",
        "Mean Package": "4.30 LPA",
        "Placement Rate": "82.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "KC College of Engineering, Thane",
        "Established": 2001,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "87.30+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 84.10% | EWS: 83.50% | SC/ST: 68%",
        "Highest Package": "15.00 LPA",
        "Average Package": "4.50 LPA",
        "Mean Package": "4.00 LPA",
        "Placement Rate": "79.5%",
        "State": "Maharashtra"
    },
    {
        "College Name": "BITS Pilani (Main Campus)",
        "Established": 1964,
        "Entrance Exam": "BITSAT",
        "Cutoff (General - CSE)": "304 / 390 Score",
        "Cutoff (Minority/EWS)": "No Reservation Quotas (Pure Merit Based)",
        "Highest Package": "60.75 LPA",
        "Average Package": "18.20 LPA",
        "Mean Package": "17.40 LPA",
        "Placement Rate": "96.2%",
        "State": "Rajasthan"
    },
    {
        "College Name": "Walchand Institute of Technology (WIT), Solapur",
        "Established": 1983,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "91.80+ Percentile",
        "Cutoff (Minority/EWS)": "Jain Religious Minority Quota: 65.00%",
        "Highest Package": "35.00 LPA",
        "Average Package": "5.10 LPA",
        "Mean Package": "4.50 LPA",
        "Placement Rate": "84.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Shri Sant Gajanan Maharaj College of Engineering, Shegaon",
        "Established": 1983,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "92.40+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 90.50% | EWS: 90.10% | SC/ST: 78%",
        "Highest Package": "12.50 LPA",
        "Average Package": "4.20 LPA",
        "Mean Package": "3.90 LPA",
        "Placement Rate": "81.0%",
        "State": "Maharashtra"
    },
    {
        "College Name": "Prof. Ram Meghe Institute of Technology & Research, Badnera",
        "Established": 1983,
        "Entrance Exam": "MHT-CET / JEE Main",
        "Cutoff (General - CSE)": "88.10+ Percentile",
        "Cutoff (Minority/EWS)": "OBC: 85.30% | EWS: 84.90% | SC/ST: 71%",
