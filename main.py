import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)

sheet_id = st.secrets["sheets"]["sheet_id"]
workbook = client.open_by_key(sheet_id)


st.title("GPA Calculater")
name = st.text_input("Enter your Name")
marks = st.number_input("Enter your marks",min_value=0,max_value=100)
rollNo = st.text_input("Enter the roll no")
choose = st.radio("select one subject",["CP","OWO"])


def calc(df,marks):
    if not name or not rollNo:
        st.warning("Please enter both Name and RollNo.")
        return
    std_dev = df['Marks'].std()
    st.write(f"Standard Deviation: {std_dev:.2f}")
    if std_dev == 0:
        st.warning("Standard deviation is zero, cannot calculate normalized score.")
        return None
    mean = df['Marks'].mean()
    st.write(f"Mean: {mean:.2f}")
    normal = (marks - mean)/std_dev
    if marks>=95:
        cgpa = 10
    elif marks<40:
        return "Go and prepare for Backpaper"
    elif normal > 1.5 and marks>85:
        cgpa = 10
    elif 1 < normal <= 1.5:
        cgpa = 9
    elif 0.5 < normal <= 1:
        cgpa = 8
    elif 0 < normal <= 0.5:
        cgpa = 7
    elif -0.5 < normal <= 0:
        cgpa = 6
        st.write("Chud gye Guru")
    elif -1 < normal <= -0.5:
        cgpa = 5
    elif -1.5 < normal <= -1:
        cgpa = 4
    elif normal <= -1.5:
        return "You are Fail"
    else:
        return "Unable to calculate SGPA"

    return f"Your Subject GPA is {cgpa} ☠️☠️"


if choose == 'CP':
    
    st.write("CP selected")
    # try:
    df_maths = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
    df_maths['Marks'] = pd.to_numeric(df_maths['Marks'], errors='coerce')
    # except FileNotFoundError:
    #     df_maths = pd.DataFrame(columns=['Name', 'Marks', 'Rollno'])
    if st.button("Submit"):
        if rollNo.startswith("2024UEA"):
            new_data = [name, marks, rollNo]
            # Append to Google Sheet using gspread
            worksheet = workbook.worksheet("CP")  # Change "Sheet1" to your actual sheet name
            if new_data[2] not in worksheet.col_values(3):     
                worksheet.append_row(new_data)
                df_maths = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
                df_maths['Marks'] = pd.to_numeric(df_maths['Marks'], errors='coerce')
                st.success("Data saved successfully!")
                cg_show = (calc(df_maths,marks))
                st.header(cg_show)
            else:
                st.write("RollNo already exists in Database")
                all_data = worksheet.get_all_values()
                matching_rows = [row for row in all_data[1:] if row[2] == new_data[2]]
                marks2 = float(matching_rows[0][1])
                cg_show = (calc(df_maths,marks2))
                st.header(cg_show)
                st.write(f"Your Marks in Database are {marks2}")
            bins = [0,10,20,30,40,50,60,70,80,90,100]
            labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
            df_maths['Range'] = pd.cut(df_maths['Marks'], bins=bins, labels=labels, right=False)
            counts = df_maths['Range'].value_counts().sort_index()
            
            fig, ax = plt.subplots()
            counts.plot(kind='bar', ax=ax)
            ax.set_xlabel('Marks Range')
            ax.set_ylabel('Number of Students')
            ax.set_title('Distribution of Marks')
            st.pyplot(fig)
            st.write(f"To Update Marks Contact Admin😊")
            row_count = len(df_maths)
            st.write(f"Based on Data of {row_count} Students")
            st.write("Come Back later for precise results")
        else:
            st.header("Your RollNo must startwith 2024UEA____")
if choose == 'OWO':
    st.write("OWO selected")
    # try:
    worksheet = workbook.worksheet("OWO")  # Change "Sheet1" to your actual sheet name
   
    
    df_OWO = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=93641859")
    df_OWO['Marks'] = pd.to_numeric(df_OWO['Marks'], errors='coerce')
    # except FileNotFoundError:
    #     df_maths = pd.DataFrame(columns=['Name', 'Marks', 'Rollno'])
    if st.button("Submit"):
        if rollNo.startswith("2024UEA"):
            new_data = [name, marks, rollNo]
            # Append to Google Sheet using gspread
            if new_data[2] not in worksheet.col_values(3):     
               
                df_owo = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=93641859")
                df_owo['Marks'] = pd.to_numeric(df_owo['Marks'], errors='coerce')
                worksheet.append_row(new_data)
                st.success("Data saved successfully!")
                cg_show = (calc(df_OWO,marks))
                st.header(cg_show)
            else:
                st.write("RollNo already exists in Database")
                all_data = worksheet.get_all_values()
                matching_rows = [row for row in all_data[1:] if row[2] == new_data[2]]
                marks2 = float(matching_rows[0][1])
                cg_show = (calc(df_OWO,marks2))
                st.header(cg_show)
                st.write(f"Your Marks in Database are {marks2}")
                st.write(f"To Update Marks Contact Admin😊")
            bins = [0,10,20,30,40,50,60,70,80,90,100]
            labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
            df_OWO['Range'] = pd.cut(df_OWO['Marks'], bins=bins, labels=labels, right=False)
            counts = df_OWO['Range'].value_counts().sort_index()

            fig, ax = plt.subplots()
            counts.plot(kind='bar', ax=ax)
            ax.set_xlabel('Marks Range')
            ax.set_ylabel('Number of Students')
            ax.set_title('Distribution of Marks')
            st.pyplot(fig)
            row_count = len(df_OWO)
            st.write(f"Based on Data of {row_count} Students")
            st.write("Come Back later for precise results")
                
        else:
            st.header("Your RollNo must startwith 2024UEA____")
    
