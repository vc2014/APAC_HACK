import streamlit as st
import pandas as pd
import time
import numpy as np
import base64


def transform(df):
    time.sleep(1)
    return 0

def fillExcel(df):
    time.sleep(1)
    return 0

def generatePdf(df):
    time.sleep(1)
    df['Status'] = 'Completed'
    return 0

@st.cache(allow_output_mutation=True)
def get_data(uploaded_file):
    return pd.read_excel(uploaded_file)

def returnUniqueDF(df):
    columns = ["Invoice Id", "Invoice Date", "Requester Id", "Requester Name", "Status"]
    df = df[columns]
    df = df.drop_duplicates()
    return df


def highlight_row(s):

    return ['background-color: green']*len(s) if s['Invoice Id'] == invoiceId else ['background-color: white']*len(s)

def color_status(val):

    if val == 'In Progress':
        color = 'yellow'
    elif val == 'Completed':
        color = 'green'
    elif val == 'Failed':
        color = 'red'
    else:
        color = 'white'

    return f'background-color: {color}'


st.sidebar.empty()
st.sidebar.title("Upload File")
uploaded_file = st.sidebar.file_uploader("Choose a XLS file", type="xls")
st.sidebar.title("Navigation")
nav = st.sidebar.radio("Go to", ["Upload Transaction", "Result Report"])

try:
    df = get_data(uploaded_file)
except:
    print("Upload a file")
    st.warning("Upload a file")

if nav == 'Upload Transaction':
    if uploaded_file:
        #df = uploadDF
        st.sidebar.info("Inside Upload Transactions")
        st.title("Title")
        st.header("Header")

        listInvoiceId = df['Invoice Id'].unique()
        if len(listInvoiceId) > 0 :
            st.success("The uploaded file contains " + str(len(listInvoiceId)) + " invoices")
            st.table(df)

            if st.button("progress"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                process_text = st.empty()

                for i in range(len(listInvoiceId)):
                    # Update progress bar.

                    filteredDF = df[df["Invoice Id"] == listInvoiceId[i]]

                    # Update status text.
                    status_text.text(
                        'Processing invoice id : %s' % listInvoiceId[i])

                    # Append data to the chart.
                    process_text.text(
                        'Transforming invoice id : %s' % listInvoiceId[i])
                    transform(df)
                    process_text.text(
                        'Filling template invoice id : %s' % listInvoiceId[i])
                    fillExcel(df)
                    process_text.text(
                        'Generating pdf invoice id : %s' % listInvoiceId[i])
                    generatePdf(df)

                    # Pretend we're doing some computation that takes time.
                    time.sleep(0.1)
                    progress_bar.progress(int((i + 1) * 100 / len(listInvoiceId)))

                status_text.text('Done!')
                process_text.text('Completed!')
                st.balloons()
                st.success("Invoice pdfs generated successfully !!")
        else:
            st.error("The uploaded file contains " + str(len(listInvoiceId)) + " invoices")
else:
    st.sidebar.info("Inside Result Report")

    #df = uploadDF

    listInvoiceId = df['Invoice Id'].unique()

    invoiceId = st.sidebar.selectbox('Invoice Id', listInvoiceId)

    status = st.sidebar.radio('Status', ['Not Processed', 'In Progress', 'Completed', 'Failed'])

    uniqueDF = returnUniqueDF(df)

    st.title("List of Invoices")

    # st.dataframe(uniqueDF.style.apply(highlight_row, axis=1))

    stTable = st.table(uniqueDF.style.apply(highlight_row, axis=1))

    df = df[df['Invoice Id'] == invoiceId]

    columns = ["Description", "Amount", "Status"]

    df = df[columns]

    st.header("Items in an Invoice Id : " + str(invoiceId))

    st.dataframe(df.style.applymap(color_status, subset=['Status']))

    sub_section = st.beta_expander("Filled Invoice Template")
    #sub_section.markdown("[Excel Template](data.xls)", unsafe_allow_html=True)
    #xls_file = open(r"d:/2020/dev/python/camelotDemo/data.xls", 'rb')
    #base64_xls = base64.b64encode(xls_file.read()).decode('utf-8')
    #xls_display = f'<embed src="data:application/octet-stream;base64,{base64_xls}" width="700" height="1000" type="application/octet-stream">'
    #sub_section.markdown(xls_display, unsafe_allow_html=True)

    sub_section = st.beta_expander("Generated Invoice PDF")
    pdf_file = open(r"d:/2020/dev/python/camelotDemo/fallguy_bill.pdf", 'rb')
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    sub_section.markdown(pdf_display, unsafe_allow_html=True)

st.sidebar.title("About")
st.sidebar.info(
    """
    This app is maintained by Vishal Chauhan.
"""
)