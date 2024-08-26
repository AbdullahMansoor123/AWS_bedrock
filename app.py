import streamlit as st
import requests
import json


# Streamlit app
st.title("RAG Application")
st.subheader("Generate a project plan using AWS Bedrock")
# Sidebar for AWS credentials
st.sidebar.title("AWS Credentials")
aws_access_key_id = st.sidebar.text_input("AWS Access Key ID", type="default")
aws_secret_access_key = st.sidebar.text_input("AWS Secret Access Key", type="password")
aws_api_url = st.sidebar.text_input("AWS GATEWAY API", type="default")

# Main section for project objectives input
# st.header("Enter your Project Objectives")
project_objective = st.text_area("Enter Your Project Objective",
                                 value="Building Advanced RAG With Multiple Data Source Using Langchain")

# Function to send data to AWS API
def send_to_aws_api(aws_api_url, data, headers):

    try:
        response = requests.post(aws_api_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")

    except Exception as e:
        st.error(f"Other error occurred: {e}")


if st.button("Submit"):
    if aws_access_key_id and aws_secret_access_key and project_objective:
        # Prepare the data to send to AWS API
        data = {
            "prompt": project_objective,
            "max_gen_len": 512,
            "top_p": 0.8,
            "temperature": 0.7
        }

        # Set headers for AWS API
        headers = {
            "Content-Type": "application/json",
            "x-api-key": aws_access_key_id,  # Adjust if your AWS API uses a different header for authentication
        }

        # Send data to AWS API
        result = send_to_aws_api(aws_api_url, data, headers)

        if result:
            st.success("Data submitted successfully!")
            st.markdown(f'''{result}''', )
            print(result)
    else:
        st.error("Please Re-enter both AWS credentials and Project Objective.")

