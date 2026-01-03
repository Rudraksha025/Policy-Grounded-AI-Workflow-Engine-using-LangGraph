import streamlit as st
import requests

st.set_page_config(page_title="Compliance AI", layout="centered")

st.title("Loan Compliance Review System")

text = st.text_area("Enter loan explanation or question")

if st.button("Submit for Review"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/review",
            json={"input": text}
        )

        if response.status_code == 200:
            result = response.json()

            st.subheader("Review Outcome")

            status_map = {
                "APPROVED": "COMPLIANT RESPONSE GENERATED",
                "REJECTED": "NON-COMPLIANT RESPONSE",
                "PENDING_HUMAN_REVIEW": "AWAITING HUMAN APPROVAL"
            }

            st.write(status_map.get(result["status"], result["status"]))

            st.subheader("Final Output")
            st.write(result.get("final_output", "No output available."))

            if result.get("violations"):
                st.subheader("Policy Violations Detected")
                for v in result["violations"]:
                    st.write("•", v)
        else:
            st.error("Backend error occurred.")

st.divider()
st.subheader("Pending Human Reviews")

try:
    reviews = requests.get("http://127.0.0.1:8000/reviews").json()
except:
    reviews = {}

if not reviews:
    st.info("No cases pending human review.")
else:
    for task_id, task in reviews.items():
        st.markdown(f"**Task ID:** `{task_id}`")
        st.write(task["final_output"])

        edited = st.text_area("Edit Output (optional)", value=task["final_output"], key=task_id)

        if st.button(f"Approve {task_id}"):
            requests.post(
                f"http://127.0.0.1:8000/approve/{task_id}",
                params={"edited_output": edited}
            )
            st.success("Approved by human reviewer.")
            st.rerun()
