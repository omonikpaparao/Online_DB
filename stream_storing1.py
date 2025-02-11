import streamlit as st
import requests
import base64
import os
# GitHub Credentials
TOKEN = "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"
BRANCH = "main"

#TOKEN = os.getenv("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")
# Function to check if repository exists
def repository_exists(repo):
    url = f"https://api.github.com/repos/vinay223344/{repo}"
    response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
    return response.status_code == 200

# Function to list files in the repository
def list_files(repo):
    url = f"https://api.github.com/repos/vinay223344/{repo}/contents/"
    response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
    if response.status_code == 200:
        return response.json()
    return []
def create_repository(repo_name):
    url = "https://api.github.com/user/repos"
    payload = {"name": repo_name, "private": False}
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 201
# Function to upload a file
def upload_file(repo, uploaded_file):
    try:
        file_content = uploaded_file.read()
        content = base64.b64encode(file_content).decode()
        github_file_path = f"{uploaded_file.name}"
        url = f"https://api.github.com/repos/vinay223344/{repo}/contents/{github_file_path}"
        response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
        sha = response.json().get("sha", "")
        
        payload = {
            "message": f"Uploading {uploaded_file.name} via API",
            "content": content,
            "branch": BRANCH,
        }
        if sha:
            payload["sha"] = sha
        
        response = requests.put(url, json=payload, headers={"Authorization": f"token {TOKEN}"})
        
        if response.status_code in [200, 201]:
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            st.rerun()# Refresh file list dynamically
        else:
            st.error("❌ Failed to upload: " + str(response.json()))
    except Exception as e:
        st.error(f"⚠ Error uploading file: {str(e)}")

# Function to delete a file
def delete_file(repo, filename):
    try:
        github_file_path = f"{filename}"
        url = f"https://api.github.com/repos/vinay223344/{repo}/contents/{github_file_path}"
        response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
        
        if response.status_code == 200:
            sha = response.json().get("sha")
            delete_payload = {
                "message": f"Deleting {filename} via API",
                "sha": sha,
                "branch": BRANCH,
            }
            delete_response = requests.delete(url, json=delete_payload, headers={"Authorization": f"token {TOKEN}"})
            
            if delete_response.status_code == 200:
                st.success(f"✅ Deletion Success!")
                st.rerun()
            else:
                st.error("❌ Failed to delete: " + str(delete_response.json()))
        else:
            st.error("❌ File not found or failed to get SHA: " + str(response.json()))
    except Exception as e:
        st.error(f"⚠ Error deleting file: {str(e)}")

# Streamlit UI
st.title("📂 Online DB")
st.write("⚠️ You can use this to save Your Files Online...")
st.write("⚠️ By Providing a Unique Folder Name and can Manupulate Futher...")
st.markdown("[Click Here to see the Disclaimer and Demo](https://drive.google.com/file/d/142UNajeSQOtsJdKy6zQ7etUSwj7FqqCJ/view?usp=sharing)")

repo_name = st.text_input("Enter your unique Folder Name and Press Enter:")

if repo_name:
    if repository_exists(repo_name):
        st.subheader("📜 Files in Your Folder")
        
        files = list_files(repo_name)
        if files:
            for file in files:
                file_name = file['name']
                file_url = file['html_url']
                
                col1, col2, col3 = st.columns([2.5, 1,3])
                with col1:
                    st.write(f"📄 {file_name}")
                   
                with col2:
                    if st.button(f"X Delete", key=f"delete_{file_name}"):
                        delete_file(repo_name, file_name)
                        
                with col3:
                    st.download_button(label=f"📥 Download", data=requests.get(file['download_url']).content, file_name=file_name)
        else:
            st.write("There are No Files to Display!!!")
        
        st.subheader("📂 Upload a File")
        uploaded_file = st.file_uploader("Choose a file to upload")
        if uploaded_file and st.button("Upload to Online Folder"):
            upload_file(repo_name, uploaded_file)
            st.session_state["uploaded_file"] = None
            st.rerun()
            list_files(repo_name)
    else:
        st.write("Folder given is not Available Before. \n So we created a new Folder with the given Name. \nYou can use this for further usage!!!")
        create_repository(repo_name)
        st.subheader("📜 Files in Your Folder")
        
        files = list_files(repo_name)
        if files:
            for file in files:
                file_name = file['name']
                file_url = file['html_url']
                
                col1, col2, col3 = st.columns([2.5,  1,3])
                with col1:
                    st.write(f"📄 {file_name}")
                    
                
                with col2:
                    if st.button(f"X Delete", key=f"delete_{file_name}"):
                        delete_file(repo_name, file_name)
                        
                with col3:
                    st.download_button(label=f"📥 Download", data=requests.get(file['download_url']).content, file_name=file_name)
        else:
            st.write("There are No Files to Display!!!")
        
        st.subheader("📂 Upload a File")
        uploaded_file = st.file_uploader("Choose a file to upload")
        if uploaded_file and st.button("Upload to your Online Folder"):
            upload_file(repo_name, uploaded_file)
            st.session_state["uploaded_file"] = None
            st.rerun()
            list_files(repo_name)
