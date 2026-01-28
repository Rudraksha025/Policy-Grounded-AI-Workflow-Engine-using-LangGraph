import streamlit as st
import requests

st.set_page_config(page_title="Compliance Review Desk", layout="wide")

# ---------------- AUTH GATE ----------------

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("Reviewer Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        r = requests.get(
            "http://127.0.0.1:8000/policy/pending_reviews",
            auth=(username, password)
        )

        if r.status_code == 200:
            st.session_state.auth = True
            st.session_state.creds = (username, password)
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- REVIEW DASHBOARD ----------------

st.markdown("## Pending Human Reviews")
st.caption("Cases awaiting manual compliance approval.")

reviews = requests.get(
    "http://127.0.0.1:8000/policy/pending_reviews",
    auth=st.session_state.creds
).json()

if not reviews:
    st.success("No pending reviews.")
else:
    for r in reviews:
        with st.container(border=True):
            st.markdown(f"### Request ID: `{r['request_id']}`")

            col1, col2 = st.columns(2)
            with col1:
                st.text_area("User Input", r["user_input"], height=150, disabled=True)
            with col2:
                edited = st.text_area("Final Compliance Decision", r["ai_draft"], height=150, key=r["request_id"])

            approve = st.button("Approve Decision", key=f"approve_{r['request_id']}", disabled=False)

            if approve:
                res = requests.post(
                    f"http://127.0.0.1:8000/policy/approve/{r['request_id']}",
                    params={"edited_output": edited},
                    auth=st.session_state.creds
                )

                if res.status_code == 200:
                    st.success("Decision approved.")
                    st.rerun()
                else:
                    st.error(res.json().get("detail", "Approval failed"))
