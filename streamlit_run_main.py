import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px

# Initialize login data
login_file = 'login_data.json'
if not os.path.exists(login_file):
    with open(login_file, 'w') as f:
        json.dump({}, f)

def load_login_data():
    with open(login_file, 'r') as f:
        return json.load(f)

def save_login_data(data):
    with open(login_file, 'w') as f:
        json.dump(data, f)

def signup(name, email, password):
    data = load_login_data()
    if email in data:
        st.error("User with this email already exists!")
        return False
    else:
        data[email] = {'name': name, 'password': password}
        save_login_data(data)
        st.success("Signup successful! You can now login.")
        return True

def login(email, password):
    data = load_login_data()
    if email in data and data[email]['password'] == password:
        st.success(f"Welcome {data[email]['name']}!")
        return data[email]['name']
    else:
        st.error("Invalid email or password!")
        return None

def create_user_folder(user_name):
    folder = f'users/{user_name}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def save_marks_to_csv(user_name, marks):
    folder = create_user_folder(user_name)
    df = pd.DataFrame(marks, index=[0])
    df.to_csv(f'{folder}/marks.csv', index=False)
    st.success(f"Marks saved to {folder}/marks.csv")

def save_marks_to_csv(user_name, marks):
    # Define the folder path
    folder = f'users/{user_name.strip()}'  # Strip spaces in username to avoid issues
    
    # Ensure the directory exists
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Debugging: Print the folder path to verify it
    print("Folder Path:", os.path.abspath(folder))
    
    # Save the marks to a CSV file
    df = pd.DataFrame([marks], columns=["Math", "Science", "English", "History", "Geography"])
    csv_file_path = os.path.join(folder, 'marks.csv')
    
    # Debugging: Print the CSV file path
    print("CSV File Path:", os.path.abspath(csv_file_path))
    
    # Save to CSV
    df.to_csv(csv_file_path, index=False)

def load_marks_from_csv(user_name):
    folder = f'users/{user_name.strip()}'
    csv_file_path = os.path.join(folder, 'marks.csv')
    
    if os.path.exists(csv_file_path):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        return df
    else:
        # Handle the case where the marks CSV does not exist
        st.error(f"No marks file found for user {user_name}")
        return None

def generate_report(user_name):
    df = load_marks_from_csv(user_name)
    
    if df is not None:
        st.write(f"Report for {user_name}")
        
        # Debug: Display the dataframe
        st.write("Marks Data:")
        st.dataframe(df)

        # Create the graphs using Plotly if the data is valid
        if not df.empty:
            # Bar chart for average marks
            st.write("Average Marks Chart (Bar Graph)")
            avg_marks = df.mean(axis=1)
            st.bar_chart(avg_marks)
            
            # Line chart for marks per subject
            st.write("Marks as per each subject (Line Graph)")
            st.line_chart(df)
            
            # Pie chart for marks distribution
            st.write("Marks as per each subject (Pie Chart)")
            fig = px.pie(df, names=df.columns, values=df.iloc[0])
            st.plotly_chart(fig)

# Streamlit UI
st.title("Student Report System")

# Page navigation
page = st.sidebar.selectbox("Select Page", ["Sign Up", "Login", "Marks Entry", "Generate Report"])

if page == "Sign Up":
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Sign Up"):
        if name and email and password:
            signup(name, email, password)

elif page == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user_name = login(email, password)
        if user_name:
            st.session_state.user_name = user_name

elif page == "Marks Entry":
    if 'user_name' in st.session_state:
        st.subheader(f"Welcome {st.session_state.user_name}")
        marks = {}
        marks['Math'] = st.slider('Math Marks', 0, 100, 50)
        marks['Science'] = st.slider('Science Marks', 0, 100, 50)
        marks['English'] = st.slider('English Marks', 0, 100, 50)
        marks['History'] = st.slider('History Marks', 0, 100, 50)
        marks['Geography'] = st.slider('Geography Marks', 0, 100, 50)
        if st.button("Submit Marks"):
            save_marks_to_csv(st.session_state.user_name, marks)
    else:
        st.warning("Please login to enter marks.")

elif page == "Generate Report":
    if 'user_name' in st.session_state:
        st.subheader(f"Report for {st.session_state.user_name}")
        generate_report(st.session_state.user_name)
    else:
        st.warning("Please login to view your report.")

