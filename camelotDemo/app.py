import streamlit as st
import pandas as pd
import time
import numpy as np

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


def processDF(df):
    return 0


uploaded_file = st.sidebar.file_uploader("Choose a XLS file", type="xls")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    #df['Status'] = 'Completed'

    listInvoiceId = df['Invoice Id'].unique()

    invoiceId = st.sidebar.selectbox('Invoice Id', listInvoiceId)

    status = st.sidebar.radio('Status', ['Not Processed', 'In Progress', 'Completed', 'Failed'])

    uniqueDF = returnUniqueDF(df)

    st.text("List of Invoices")

    #st.dataframe(uniqueDF.style.apply(highlight_row, axis=1))

    stTable = st.table(uniqueDF.style.apply(highlight_row, axis=1))

    df = df[df['Invoice Id'] == invoiceId]

    columns = ["Description", "Amount", "Status"]

    df = df[columns]

    st.text("Items in an Invoice Id : " + str(invoiceId))

    st.dataframe(df.style.applymap(color_status, subset=['Status']))



if st.button("progress"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    chart = st.line_chart(np.random.randn(10, 2))

    for i in range(100):
        # Update progress bar.
        progress_bar.progress(i + 1)

        new_rows = np.random.randn(10, 2)

        # Update status text.
        status_text.text(
            'The latest random number is: %s' % new_rows[-1, 1])

        # Append data to the chart.
        chart.add_rows(new_rows)

        # Pretend we're doing some computation that takes time.
        time.sleep(0.1)

    status_text.text('Done!')
    st.balloons()
