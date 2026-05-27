import streamlit as st
from modules.database import db
from datetime import datetime, timedelta
import calendar

st.title("✨ Manifestations")
st.markdown("---")

user_id = st.session_state.current_user['id']

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Today's Manifestation")
    manifest = st.text_area(
        "",
        placeholder="What are you manifesting today?\nBe specific and positive...",
        height=150,
        key="manifest_input"
    )

with col2:
    st.markdown("### Date")
    selected_date = st.date_input("", datetime.now().date())

if st.button("💾 Save Manifestation", use_container_width=True, type="primary"):
    if manifest.strip():
        existing = db.get_manifestation_by_date(user_id, str(selected_date))
        if existing:
            db.update_manifestation(existing['id'], manifest)
            st.success("✅ Updated!")
        else:
            db.create_manifestation(user_id, manifest, str(selected_date))
            st.success("✅ Saved!")
        st.rerun()
    else:
        st.error("Write your manifestation")

st.markdown("### 📅 Monthly Calendar")

now = datetime.now()
col1, col2 = st.columns([1, 1])

with col1:
    current_month = st.selectbox(
        "Month",
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"],
        index=now.month - 1
    )
    month_num = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"].index(current_month) + 1

with col2:
    year = st.number_input("Year", value=now.year, step=1)

manifestations = db.get_manifestations(user_id)
manifest_dates = {m['manifest_date'] for m in manifestations}

cal = calendar.monthcalendar(year, month_num)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

st.markdown(f"### {current_month} {year}")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
cols = [col1, col2, col3, col4, col5, col6, col7]

for i, day in enumerate(days):
    with cols[i]:
        st.markdown(f"**{day}**", help=day)

for week in cal:
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    cols = [col1, col2, col3, col4, col5, col6, col7]

    for i, day in enumerate(week):
        with cols[i]:
            if day == 0:
                st.markdown("")
            else:
                date_str = f"{year}-{month_num:02d}-{day:02d}"
                has_entry = date_str in manifest_dates

                if has_entry:
                    st.markdown(f"""
                    <div style="background: #667eea; color: white; padding: 0.5rem; border-radius: 8px; text-align: center; font-weight: bold;">
                        ✅ {day}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #f0f4f8; padding: 0.5rem; border-radius: 8px; text-align: center;">
                        {day}
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("### 📖 All Manifestations")

all_manifests = db.get_manifestations(user_id)

if all_manifests:
    for m in all_manifests:
        with st.container():
            st.markdown(f"""
            <div style="border-left: 4px solid #667eea; padding-left: 1rem; margin-bottom: 1rem;">
                <strong>📅 {m['manifest_date']}</strong><br>
                <p>{m['content']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Delete", key=f"del_m_{m['id']}", use_container_width=True):
                db.delete_manifestation(m['id'])
                st.rerun()
else:
    st.info("✨ Start manifesting your dreams!")
