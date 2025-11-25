import streamlit as st
import json
from io import BytesIO
import base64
import pandas as pd

from azure_blob_io import (
    upload_input_blob,
    upload_output_blob,
    list_input_files,
    download_input_blob
)

from ocr_extract import extract_text
from llm_parse_local import parse_payslip_with_llm


# Page config
st.set_page_config(
    page_title="LEASETEQ – Payslip Extraction",
    layout="wide",
)


# Session store for all results
if "records" not in st.session_state:
    st.session_state["records"] = []


# Header
st.markdown(
    """
    <h1 style='font-family:Arial; font-size:32px; color:white; margin:0;'>
        Swiss Payslip → JSON Extractor
    </h1>
    <p style='font-family:Arial; font-size:18px; font-weight:600; color:white; margin:0;'>
        LEASETEQ
    </p>
    """,
    unsafe_allow_html=True
)


# Azure Blob Processing 

st.subheader("Process Files Already Stored in Azure Blob (inputfiles)")

azure_files = list_input_files()

with st.expander("Show Azure Input Files", expanded=False):

    if not azure_files:
        st.info("No files found in Azure inputfiles.")
        selected_blob = None
    else:
        selected_blob = st.radio(
            "Choose a file to process:",
            azure_files,
            index=None
        )

    if selected_blob and st.button("Process Selected Azure File"):
        blob_bytes = download_input_blob(selected_blob)

        if blob_bytes is None:
            st.error("Could not download this blob.")
        else:
            filename = selected_blob.split("/")[-1]
            st.success(f"Downloaded from Azure: {filename}")

            st.subheader(f"Document Preview: {filename}")

            if filename.lower().endswith(".pdf"):
                encoded = base64.b64encode(blob_bytes).decode("utf-8")
                st.markdown(
                    f"""
                    <embed 
                        src="data:application/pdf;base64,{encoded}" 
                        type="application/pdf"
                        width="100%"
                        height="380px"
                    />
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.image(blob_bytes, caption=filename, width=350)

            extracted_text = extract_text(BytesIO(blob_bytes))

            if extracted_text.strip():
                with st.expander("Show OCR details", expanded=False):
                    st.text_area("OCR Output", extracted_text, height=160)

                json_result = parse_payslip_with_llm(extracted_text, filename)

                output_filename = (
                    filename.replace(".pdf", "_summary.json")
                            .replace(".jpeg", "_summary.json")
                            .replace(".jpg", "_summary.json")
                            .replace(".png", "_summary.json")
                )

                upload_output_blob(
                    json.dumps(json_result, ensure_ascii=False).encode("utf-8"),
                    output_filename
                )

                st.success(f"Uploaded summary to Azure (outputfiles): {output_filename}")

                st.session_state["records"].append(json_result)
            else:
                st.error("No text extracted.")




# Local Upload Processing

st.subheader("Upload Payslips From Your Computer")

uploaded_files = st.file_uploader(
    "Select payslips (PDF, JPG, JPEG, PNG)",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:

        if any(r["PDF Name"] == uploaded_file.name for r in st.session_state["records"]):
            continue

        file_bytes = uploaded_file.read()

        if upload_input_blob(file_bytes, uploaded_file.name):
            st.success(f"Uploaded to Azure (inputfiles): {uploaded_file.name}")

        st.divider()
        st.subheader(f"Document Preview: {uploaded_file.name}")

        if uploaded_file.name.lower().endswith(".pdf"):
            encoded = base64.b64encode(file_bytes).decode("utf-8")
            st.markdown(
                f"""
                <embed 
                    src="data:application/pdf;base64,{encoded}" 
                    type="application/pdf"
                    width="100%"
                    height="380px"
                />
                """,
                unsafe_allow_html=True
            )
        else:
            st.image(file_bytes, caption=uploaded_file.name, width=350)

        st.subheader("OCR Extraction")
        with st.spinner("Extracting text..."):
            extracted_text = extract_text(BytesIO(file_bytes))

        if not extracted_text.strip():
            st.error("No text extracted.")
            continue

        with st.expander("Show OCR details", expanded=False):
            st.text_area("OCR Output", extracted_text, height=160)

        st.subheader("Parsing with LLM")
        with st.spinner("Extracting structured fields..."):
            json_result = parse_payslip_with_llm(extracted_text, uploaded_file.name)

        output_filename = (
            uploaded_file.name.replace(".pdf", "_summary.json")
            .replace(".jpeg", "_summary.json")
            .replace(".jpg", "_summary.json")
            .replace(".png", "_summary.json")
        )

        if upload_output_blob(
            json.dumps(json_result, ensure_ascii=False).encode("utf-8"),
            output_filename
        ):
            st.success(f"Uploaded to Azure (outputfiles): {output_filename}")

        st.session_state["records"].append(json_result)




# Combined Results

if st.session_state["records"]:

    st.divider()
    st.subheader("All Extracted Records")

    df = pd.DataFrame(st.session_state["records"])

    with st.expander("Show Combined JSON Output", expanded=False):
        json_array_str = json.dumps(st.session_state["records"], ensure_ascii=False, indent=2)
        st.code(json_array_str, language="json")

    st.table(df)

    st.download_button(
        "Download Combined JSON",
        json_array_str,
        file_name="all_payslips_summary.json",
        mime="application/json"
    )

    st.download_button(
        "Download Combined CSV",
        df.to_csv(index=False),
        file_name="all_payslips_summary.csv",
        mime="text/csv"
    )
