import streamlit as st
from resume_parser import parse_resume_with_gemini
import PyPDF2
import docx2txt
import json

st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="centered",
    menu_items={
        "About": "Made with ❤️ by Joel Shibu"
    }
)

st.title("📄 Resume Parser using Gemini AI")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    # Extract text from uploaded file
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([page.extract_text() or "" for page in reader.pages])
    elif uploaded_file.name.endswith(".docx"):
        text = docx2txt.process(uploaded_file)
    else:
        st.error("Unsupported file format.")
        text = ""

    if text.strip():
        st.subheader("📃 Extracted Resume Text")
        st.text_area("Resume Content", text, height=300)

        if st.button("🔍 Parse Resume with Gemini"):
            with st.spinner("Sending to Gemini..."):
                parsed_output = parse_resume_with_gemini(text)

            st.subheader("✅ Extracted Information")
            if "error" in parsed_output:
                st.error(parsed_output["error"])
            else:
                st.markdown(f"**👤 Name:** {parsed_output.get('Full Name', 'N/A')}")
                st.markdown(f"**📧 Email:** {parsed_output.get('Email', 'N/A')}")
                st.markdown(f"**📞 Phone:** {parsed_output.get('Phone', 'N/A')}")
                st.markdown("**🛠️ Skills:**")
                st.write(parsed_output.get("Skills", []))
                st.markdown("**🎓 Education:**")
                st.write(parsed_output.get("Education", "N/A"))
                st.markdown("**💼 Experience:**")
                st.write(parsed_output.get("Experience", "N/A"))

                # Download as JSON
                st.download_button(
                    label="📥 Download Extracted Data as JSON",
                    data=json.dumps(parsed_output, indent=2),
                    file_name="parsed_resume.json",
                    mime="application/json"
                )
    else:
        st.warning("No readable text found in the uploaded file.")
