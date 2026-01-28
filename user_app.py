import streamlit as st
import requests

st.set_page_config(page_title="Compliance Portal", layout="centered")

st.markdown("## Loan Compliance Submission")
st.caption("Submit your loan case for automated compliance review.")

with st.container(border=True):
    user_input = st.text_area(
        "Case description",
        placeholder="Describe applicant income, credit score, defaults, employment history..."
    )

    submit = st.button("Submit for Compliance Review")

if submit:
    if not user_input.strip():
        st.warning("Please provide a case description.")
    else:
        r = requests.post("http://127.0.0.1:8000/policy/review", json={"input": user_input})
        data = r.json()
        st.session_state["request_id"] = data["request_id"]
        st.success("Request submitted successfully.")
        st.code(data["request_id"], language="text")

if "request_id" in st.session_state:
    with st.container(border=True):
        st.subheader("Review Status")

        if st.button("Refresh Status"):
            res = requests.get(f"http://127.0.0.1:8000/policy/result/{st.session_state['request_id']}")
            out = res.json()

            if out["status"] == "APPROVED":
                st.metric("Review Status", "COMPLETED")
            else:
                st.metric("Review Status", out["status"])


            if out["status"] == "APPROVED":
                st.subheader("Compliance Decision")
                st.success("Decision finalized by Compliance Engine")
                st.text_area(
                    "Final Outcome",
                    out["final_output"],
                    height=200,
                    disabled=True
                )
            else:
                st.info("Your case is under review. Please check back shortly.")
