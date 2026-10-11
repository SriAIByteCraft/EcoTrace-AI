import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

st.set_page_config(page_title="EcoTrace AI", page_icon="♻️", layout="wide")

FILE = "eco_waste_records.csv"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

WASTE = {
    "Plastic": ("Recyclable where accepted", "Keep clean and dry."),
    "Food waste": ("Organic waste", "Separate scraps for composting."),
    "Paper": ("Recyclable if clean and dry", "Reuse or recycle where accepted."),
    "E-waste": ("Special collection", "Use an authorised e-waste collection service."),
    "Glass": ("Depends on local facilities", "Check local collection rules."),
    "Batteries": ("Special collection", "Use a suitable battery collection point."),
    "Mixed waste": ("General waste", "Check local municipal guidance.")
}

st.title("EcoTrace AI")
st.write("Track waste. Make informed environmental choices.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Waste Guide", "AI Assistant", "Record Action", "Dashboard"]
)

with tab1:
    kind = st.selectbox("Choose waste type", list(WASTE))
    st.success(WASTE[kind][0])
    st.write(WASTE[kind][1])

with tab2:
    st.subheader("Ask the EcoTrace AI Assistant")
    question = st.text_area(
        "Ask about waste reduction, recycling, or disposal",
        placeholder="Example: How should I dispose of old batteries?"
    )

    if st.button("Ask AI"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("AI is preparing an answer..."):
                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json={
                            "model": MODEL,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": (
                                        "You are EcoTrace AI, an environmental waste guidance assistant "
                                        "for users in India. Give simple, safe and practical advice. "
                                        "Recommend checking local municipal rules and authorised collection "
                                        "centres. For batteries and e-waste, recommend authorised collection "
                                        "points and applicable Indian government guidance. Do not invent "
                                        "specific collection centres, phone numbers or links. "
                                        "If local rules are unknown, clearly say so."
                                    )
                                },
                                {"role": "user", "content": question}
                            ],
                            "stream": False
                        },
                        timeout=120
                    )
                    response.raise_for_status()
                    answer = response.json()["message"]["content"]
                    st.markdown("### AI Response")
                    st.write(answer)
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to Ollama. Make sure Ollama is running "
                        "on this computer."
                    )
                except requests.exceptions.RequestException as error:
                    st.error(f"AI request failed: {error}")

with tab3:
    with st.form("waste_form"):
        kind = st.selectbox("Waste type", list(WASTE), key="record_kind")
        weight = st.number_input("Weight (kg)", min_value=0.1, value=1.0)
        action = st.selectbox(
            "Action taken",
            ["Reused", "Recycled", "Composted",
             "Special collection", "Other"]
        )
        submitted = st.form_submit_button("Save Record")

    if submitted:
        row = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Waste Type": kind,
            "Weight (kg)": weight,
            "Action": action
        }])

        if os.path.exists(FILE):
            old = pd.read_csv(FILE)
            row = pd.concat([old, row], ignore_index=True)

        row.to_csv(FILE, index=False)
        st.success("Record saved!")

with tab4:
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        st.metric(
            "Total waste recorded (kg)",
            round(df["Weight (kg)"].sum(), 2)
        )
        st.metric("Number of records", len(df))
        st.bar_chart(df.groupby("Waste Type")["Weight (kg)"].sum())
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records yet. Add one in Record Action.")

st.caption(
    "Prototype: follow local waste-disposal guidance. "
    "AI suggestions should be checked against local rules."
)
