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
