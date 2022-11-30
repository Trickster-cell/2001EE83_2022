import tut07
import streamlit as st
import os
import pandas as pd
from datetime import datetime
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import shutil


def compufun(uploaded_file, zipObj):
    data = pd.read_excel(uploaded_file)        
    # path = os.getcwd()
    open('temp.xlsx', 'w').close()
    open('temp2.xlsx', 'w').close()
    fname = uploaded_file.name
    # print(fname)
    namef = str(fname)
    oname = namef[:-5]
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    finname = f"{oname}_{number}_{dt_string}.xlsx"
    # print(finname)
    writer = pd.ExcelWriter('temp.xlsx')
    data.to_excel(writer)
    writer.save()
    tut07.mainfun("temp.xlsx", number)
    shutil.copy("temp2.xlsx", finname)
    zipObj.write(finname)
    os.remove(finname)





st.title("Octant Batch Processing", anchor='center')
st.text("Upload the input files below and you can get the Octant processing of the whole file.")
number = int(st.number_input('Insert the MOD value'))
# MOD = number
if number <= 1:
    st.text("Choose MOD value greater or equal to 1.\nFor proper functioning currently its set to 1.")

# print(number)
# f = open('writer.xlsx', 'w')
uploaded_files = st.file_uploader("Choose a XLSX file", accept_multiple_files=True)
# uploaded_file = st.file_uploader("Choose a XLSX file")
x = 0
list = []
for uploaded_file in uploaded_files:
    # bytes_data = uploaded_file.getvalue()
    # x+=1
    if uploaded_file is not None:
        list.append(uploaded_file)
        
if st.button(f"Compute", key=x, disabled= False):
    zipObj = ZipFile('BulkProcess.zip', 'w')
    if len(list) == 0:
        st.text("Please upload a file first.")
    elif len(list)>1:
        for file in list:
            compufun(file, zipObj)
        zipObj.close()
        st.text("files computed")
        now = datetime.now()
        dt_string2 = now.strftime("%Y-%m-%d-%H-%M-%S")
        with open('BulkProcess.zip', 'rb') as f:
            st.download_button('Download Processed File', f, file_name=f"BulkProcess_{dt_string2}.zip")
    else:
        uploaded_file = list[0]
        data = pd.read_excel(uploaded_file)        
        open('temp.xlsx', 'w').close()
        open('temp2.xlsx', 'w').close()
        fname = uploaded_file.name
        # print(fname)
        namef = str(fname)
        oname = namef[:-5]
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        finname = f"{oname}_{number}_{dt_string}.xlsx"
        print(finname)
        writer = pd.ExcelWriter('temp.xlsx')
        data.to_excel(writer)
        writer.save()
        tut07.mainfun("temp.xlsx", number)
        now = datetime.now()
        dt_string2 = now.strftime("%Y-%m-%d-%H-%M-%S")
        with open('temp2.xlsx', 'rb') as f:
            st.download_button('Download Processed File', f, file_name=f"{finname}")