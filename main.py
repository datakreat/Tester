import streamlit as st
import requests
from pymongo import MongoClient
import json
from datetime import datetime

# FastAPI server URL
BASE_URL = "https://data.kreat.space"  # Update this with your FastAPI server URL

def main():
    st.title("Data Kreat Check Tool")

    # Sidebar for navigation
    menu = st.sidebar.radio(
        "Menu",
        ["Endpoint Testing(not updated)", "See History", "See Feedback", "Delete Data"]
    )

    if menu == "Endpoint Testing(not updated)":
        endpoint_testing()
    elif menu == "See History":
        display_db_contents()
    elif menu == "See Feedback":
        display_feedback()
    elif menu == "Delete Data":
        clear_database()

def display_feedback():
    # Connect to MongoDB
    uri = "mongodb+srv://data:TI18vXaNXBUAkn6T@cluster0.peeh3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client["kreat_feedback"]  # Use the kreat_feedback database
    feedback_collection = db.feedback  # Use the feedback collection

    # Fetch distinct session IDs from the feedback collection
    session_ids = feedback_collection.distinct("session_id")
    
    if not session_ids:
        st.warning("No sessions found.")
        return

    # Let the user select a session ID
    session_id = st.sidebar.selectbox("Select a Session ID", session_ids)

    # Fetch feedback entries for the selected session
    feedback_entries = list(feedback_collection.find({"session_id": session_id}))

    if not feedback_entries:
        st.warning("No feedback found for this session.")
        return

    # Sort feedback by creation date (if available)
    feedback_entries.sort(key=lambda x: x.get("created_at", datetime.min), reverse=True)

    # Display feedback in a structured format
    st.header(f"Feedback for Session ID: {session_id}")
    
    for entry in feedback_entries:
        with st.expander(f"Feedback: {entry.get('feedback_type', 'Unknown')}"):

            # Display creation date if available, else use 'Unknown'
            created_at = entry.get('created_at', 'Unknown')
            if isinstance(created_at, datetime):
                created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
            st.write(f"**Date Created:** {created_at}")

            st.write(f"**Feedback Type:** {entry.get('feedback_type', 'N/A')}")
            st.write(f"**Feedback Message:** {entry.get('feedback', 'No feedback provided')}")
            st.write(f"**Message Block:** {entry.get('message_block', 'No message block provided')}")
            st.write(f"**Conversation History:**")
            display_conv_hist(entry.get('conversation_history', 'No conversation history'))
            
            st.markdown("---")  # Separator for each feedback entry

def clear_database():
    # MongoDB connection URIs and databases
    feedback_uri ="mongodb+srv://kreat:a5PgZPzgcO3wmCpi@kreatcluster.pbtxctd.mongodb.net/?retryWrites=true&w=majority&appName=KreatCluster"
    chatbot_uri = "mongodb+srv://kreat:a5PgZPzgcO3wmCpi@kreatcluster.pbtxctd.mongodb.net/?retryWrites=true&w=majority&appName=KreatCluster"
    
    # MongoDB Clients and Databases
    feedback_client = MongoClient(feedback_uri)
    chatbot_client = MongoClient(chatbot_uri)
    
    feedback_db = feedback_client["kreat_feedback"]  # Feedback database
    chatbot_db = chatbot_client["chatbot_database"]  # Chatbot database
    
    # Sidebar for selecting database to clear
    st.sidebar.header("Database Management")
    clear_option = st.sidebar.selectbox(
        "Choose database to clear:",
        ("Select an option", "Clear Feedback Database", "Clear Chatbot Database")
    )
    
    if clear_option != "Select an option":
        # Fetch and display rows before clearing
        st.header("Database Preview")
        
        if clear_option == "Clear Feedback Database":
            collection_names = feedback_db.list_collection_names()
            st.write("Fetching data from feedback database...")
            for collection_name in collection_names:
                st.subheader(f"Collection: {collection_name}")
                feedback_collection = feedback_db[collection_name]
                
                # Fetch the most recent 5 documents based on creation time
                documents = list(feedback_collection.find().sort("created_at", -1).limit(5))
                
                if not documents:
                    st.write("No documents found in this collection.")
                else:
                    for doc in documents:
                        st.write(f"**Feedback Type:** {doc.get('feedback_type', 'N/A')}")
                        st.write(f"**Feedback Message:** {doc.get('feedback', 'No feedback provided')}")
                        st.write(f"**Message Block:** {doc.get('message_block', 'No message block provided')}")
                        st.write(f"**Conversation History:** {doc.get('conversation_history', 'No conversation history')}")
                        
                        # Display creation date
                        created_at = doc.get('created_at', 'Unknown')
                        if isinstance(created_at, datetime):
                            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
                        st.write(f"**Date Created:** {created_at}")
                        
                        st.markdown("---")  # Separator for each document
        
        elif clear_option == "Clear Chatbot Database":
            collection_names = chatbot_db.list_collection_names()
            st.write("Fetching data from chatbot database...")
            for collection_name in collection_names:
                st.subheader(f"Collection: {collection_name}")
                chatbot_collection = chatbot_db[collection_name]
                
                # Fetch the most recent 5 documents based on creation time
                documents = list(chatbot_collection.find().sort("created_at", -1).limit(5))
                
                if not documents:
                    st.write("No documents found in this collection.")
                else:
                    for doc in documents:
                        st.write(f"**Document ID:** {doc.get('_id', 'N/A')}")
                        st.write(f"**Content:** {doc.get('content', 'No content provided')}")
                        
                        # Display creation date
                        created_at = doc.get('created_at', 'Unknown')
                        if isinstance(created_at, datetime):
                            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
                        st.write(f"**Date Created:** {created_at}")
                        
                        st.markdown("---")  # Separator for each document
        
        # Confirmation to clear database
        st.header("Confirmation")
        confirmation = st.checkbox("Are you sure you want to delete the selected database? This action is irreversible!")
        
        if confirmation:
            if st.button("Confirm and Clear Database"):
                if clear_option == "Clear Feedback Database":
                    for collection_name in collection_names:
                        feedback_db[collection_name].drop()  # Drop all collections in kreat_feedback
                    st.success("Feedback database cleared successfully!")
                elif clear_option == "Clear Chatbot Database":
                    for collection_name in collection_names:
                        chatbot_db[collection_name].drop()  # Drop all collections in chatbot_database
                    st.success("Chatbot database cleared successfully!")
        else:
            st.warning("Please confirm to proceed with clearing the database.")


def display_db_contents():
    # MongoDB connection
    client = MongoClient("mongodb+srv://data:TI18vXaNXBUAkn6T@cluster0.peeh3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB connection string
    db = client["chatbot_database"]  # Access the correct database

    # Fetch all session collections and their creation dates
    session_collections = db.list_collection_names()
    
    session_dates = []
    for session_id in session_collections:
        session_data = db[session_id].find_one({"session_id": session_id})
        if session_data:
            created_at = session_data.get('created_at')
            if created_at:
                session_dates.append((session_id, created_at))

    # Sort sessions by creation date in descending order
    session_dates.sort(key=lambda x: x[1], reverse=True)

    # Create a list of tuples (display_name, session_id)
    display_sessions = [(f"{id} - {date.strftime('%Y-%m-%d %H:%M:%S')}", id) for id, date in session_dates]

    # Sidebar to select session
    selected_session_display_name = st.sidebar.selectbox("Select a Session by Date and ID", [s[0] for s in display_sessions])
    
    # Extract selected session ID from display name
    selected_session_id = next(s[1] for s in display_sessions if s[0] == selected_session_display_name)

    if selected_session_id:
        # Fetch the session data
        session_data = db[selected_session_id].find_one({"session_id": selected_session_id})

        if session_data:
            st.title(f"Session Details: {selected_session_id}")

            # Display session creation date
            created_at = session_data.get('created_at')
            if created_at:
                # Convert the date to a readable format
                created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
                st.write(f"**Created At:** {created_at}")
            else:
                st.write("**Created At:** N/A")

            updated_at = session_data.get('updated_at')
            if updated_at:
                # Convert the date to a readable format
                updated_at = updated_at.strftime('%Y-%m-%d %H:%M:%S')
                st.write(f"**Updated At:** {updated_at}")
            else:
                st.write("**Updated At:** N/A")

            # Display session fields in an organized manner
            st.subheader("Problem Details")
            st.write(f"**Problem:** {session_data.get('PROBLEM', 'N/A')}")
            st.write(f"**Title:** {session_data.get('TITLE', 'N/A')}")
            st.write(f"**Abstract:** {session_data.get('ABSTRACT', 'N/A')}")
            
            st.subheader("Stakeholders and Classification")
            st.write(f"**Stakeholders:** {session_data.get('STAKEHOLDERS', 'N/A')}")
            st.write(f"**Classification:** {session_data.get('CLASSIFICATION', 'N/A')}")
            
            st.subheader("Impact and Assumptions")
            st.write(f"**Problem Impact:** {session_data.get('PROBLEM_IMPACT', 'N/A')}")
            st.write(f"**Assumptions:** {session_data.get('ASSUMPTIONS', 'N/A')}")
            
            st.subheader("Constraints and Risks")
            st.write(f"**Constraints:** {session_data.get('CONSTRAINTS', 'N/A')}")
            st.write(f"**Risks:** {session_data.get('RISKS', 'N/A')}")
            
            st.subheader("Classification")
            st.write(f"**Problem Classification:** {session_data.get('PROBLEM_CLASSIFICATION', 'N/A')}")
            st.write(f"**Context Summary:** {session_data.get('CONTEXT_SUMMARY', 'N/A')}")

            st.subheader("PDB and Problem Landscape")
            st.write(f"**PDB Suggestion:** {session_data.get('PDB_SUGGESTION', 'N/A')}")
            st.write(f"**PDB Description:** {session_data.get('PDB_DESCRIPTION', 'N/A')}")
            st.write(f"**Problem Landscape:** {session_data.get('PROBLEM_LANDSCAPE', 'N/A')}")
            
            st.subheader("Function Map and History")
            st.write(f"**Function Map:** {session_data.get('FUNCTION_MAP', 'N/A')}")
            st.write(f"**Real Insights:** {session_data.get('REAL INSIGHTS', 'N/A')}")
            st.write(f"**Summary:** {session_data.get('SUMMARY', 'N/A')}")
            st.write(f"**Insights:** {session_data.get('INSIGHTS', 'N/A')}")
            st.write(f"**Conversation History:**")
            display_conv_hist(session_data.get('CONVERSATION_HISTORY', 'N/A'))
        else:
            st.error("No data found for the selected session.")

def display_conv_hist(conversation):
    # Custom CSS for the chat box
    st.markdown("""
        <style>
        .chat-box {
            background-color: #f1f1f1;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            margin: auto;
        }
        .user-message {
            color: #001F5A;
            font-weight: bold;
            text-align: left;
            margin-bottom: 5px;
        }
        .assistant-message {
            color: #198165;
            text-align: left;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)


    # Display conversation history in a box
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for entry in conversation:
        if entry['role'] == 'user':
            st.markdown(f'<div class="user-message">User: {entry["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">Assistant: {entry["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def endpoint_testing():
    operation = st.sidebar.selectbox(
        "Select Operation",
        ["Generate Title", "Check Title", "Update Title", "Generate Abstract", "Update Abstract",
         "Innovation Classification", "Update Innovation Classification", "Stakeholders Request",
         "Update Stakeholders", "Problem Impact", "Generate Assumptions", "Accept Hypothesis Results",
         "Generate Constraints", "Generate Risks", "Problem Classification", "Detailed Description",
         "PDB Model", "Update PDB Model", "Execute PDB Model", "Problem Landscape", "Function Map"]
    )

    if operation == "Generate Title":
        generate_title()
    elif operation == "Check Title":
        check_title()
    elif operation == "Update Title":
        update_title()
    elif operation == "Generate Abstract":
        generate_abstract()
    elif operation == "Update Abstract":
        update_abstract()
    elif operation == "Innovation Classification":
        innovation_classification()
    elif operation == "Update Innovation Classification":
        update_innovation_classification()
    elif operation == "Stakeholders Request":
        stakeholders_request()
    elif operation == "Update Stakeholders":
        update_stakeholders()
    elif operation == "Problem Impact":
        problem_impact()
    elif operation == "Generate Assumptions":
        generate_assumptions()
    elif operation == "Accept Hypothesis Results":
        accept_hypothesis_results()
    elif operation == "Generate Constraints":
        generate_constraints()
    elif operation == "Generate Risks":
        generate_risks()
    elif operation == "Problem Classification":
        problem_classification()
    elif operation == "Detailed Description":
        detailed_description()
    elif operation == "PDB Model":
        pdb_model()
    elif operation == "Update PDB Model":
        update_pdb_model()
    elif operation == "Execute PDB Model":
        execute_pdb_model()
    elif operation == "Problem Landscape":
        problem_landscape()
    elif operation == "Function Map":
        function_map()

def other_options():
    st.header("Other Options")
    st.write("Additional tools and functionalities can be added here.")

def display_json(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            st.markdown(f"{'&nbsp;' * indent}**{key}:**")
            display_json(value, indent + 2)
    elif isinstance(data, list):
        for item in data:
            display_json(item, indent + 2)
    else:
        st.markdown(f"{'&nbsp;' * indent}{data}")

def make_request(endpoint, data):
    response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None


def generate_title():
    st.header("Generate Title")
    extracted_problem = st.text_area("Enter the extracted problem:")
    if st.button("Generate Title"):
        result = make_request("generate_title", {"extracted_problem": extracted_problem})
        if result:
            st.subheader("Response:")
            display_json(result)

def check_title():
    st.header("Check Title")
    title = st.text_input("Enter the title:")
    if st.button("Check Title"):
        result = make_request("check_title", {"title": title})
        if result:
            st.subheader("Response:")
            display_json(result)

def update_title():
    st.header("Update Title")
    title = st.text_input("Enter the current title:")
    feedback = st.text_area("Enter feedback:")
    if st.button("Update Title"):
        result = make_request("update_title", {"title_or_abstract": title, "feedback": feedback})
        if result:
            st.subheader("Response:")
            display_json(result)

def generate_abstract():
    st.header("Generate Abstract")
    title = st.text_input("Enter the title:")
    if st.button("Generate Abstract"):
        result = make_request("generate_abstract", {"title": title})
        if result:
            st.subheader("Response:")
            display_json(result)

def update_abstract():
    st.header("Update Abstract")
    abstract = st.text_area("Enter the current abstract:")
    feedback = st.text_area("Enter feedback:")
    if st.button("Update Abstract"):
        result = make_request("update_abstract", {"abstract": abstract, "feedback": feedback})
        if result:
            st.subheader("Response:")
            display_json(result)

def innovation_classification():
    st.header("Innovation Classification")
    title = st.text_input("Enter the title:")
    if st.button("Classify Innovation"):
        result = make_request("innovation_classification", {"title": title})
        if result:
            st.subheader("Response:")
            display_json(result)

def update_innovation_classification():
    st.header("Update Innovation Classification")
    title = st.text_input("Enter the title:")
    prev_classification = st.text_input("Enter the previous classification:")
    suggestion = st.text_input("Enter the suggestion:")
    if st.button("Update Classification"):
        result = make_request("update_innovation_classification", 
                              {"title": title, "prev_classification": prev_classification, "suggestion": suggestion})
        if result:
            st.subheader("Response:")
            display_json(result)

def stakeholders_request():
    st.header("Stakeholders Request")
    title = st.text_input("Enter the title:")
    if st.button("Generate Stakeholders"):
        result = make_request("stakeholders_request", {"title": title})
        if result:
            st.subheader("Response:")
            display_json(result)

def update_stakeholders():
    st.header("Update Stakeholders")
    stakeholders = st.text_area("Enter the current stakeholders:")
    update = st.text_area("Enter the update:")
    if st.button("Update Stakeholders"):
        result = make_request("stakeholders_update_request", {"stakeholders": stakeholders, "update": update})
        if result:
            st.subheader("Response:")
            display_json(result)

def problem_impact():
    st.header("Problem Impact")
    problem = st.text_area("Enter the problem:")
    if st.button("Generate Problem Impact"):
        result = make_request("request_problem_impact", {"problem": problem})
        if result:
            st.subheader("Response:")
            display_json(result)

def generate_assumptions():
    st.header("Generate Assumptions")
    title = st.text_input("Enter the title:")
    abstract = st.text_area("Enter the abstract:")
    if st.button("Generate Assumptions"):
        result = make_request("request_assumptions", {"title": title, "abstract": abstract})
        if result:
            st.subheader("Response:")
            display_json(result)

def accept_hypothesis_results():
    st.header("Accept Hypothesis Results")
    user_input = st.text_area("Enter user input:")
    if st.button("Accept Results"):
        result = make_request("accept_hypothesis_results", {"user_input": user_input})
        if result:
            st.subheader("Response:")
            display_json(result)

def generate_constraints():
    st.header("Generate Constraints")
    title = st.text_input("Enter the title:")
    abstract = st.text_area("Enter the abstract:")
    if st.button("Generate Constraints"):
        result = make_request("request_constraints", {"title": title, "abstract": abstract})
        if result:
            st.subheader("Response:")
            display_json(result)

def generate_risks():
    st.header("Generate Risks")
    title = st.text_input("Enter the title:")
    abstract = st.text_area("Enter the abstract:")
    if st.button("Generate Risks"):
        result = make_request("request_risks", {"title": title, "abstract": abstract})
        if result:
            st.subheader("Response:")
            display_json(result)

def problem_classification():
    st.header("Problem Classification")
    title = st.text_input("Enter the title:")
    abstract = st.text_area("Enter the abstract:")
    if st.button("Classify Problem"):
        result = make_request("request_problem_classification", {"title": title, "abstract": abstract})
        if result:
            st.subheader("Response:")
            display_json(result)

def detailed_description():
    st.header("Detailed Description")
    conv_hist = st.text_area("Enter the conversation history:")
    if st.button("Generate Detailed Description"):
        result = make_request("request_detailed_description", {"conv_hist": conv_hist})
        if result:
            st.subheader("Response:")
            display_json(result)

def pdb_model():
    st.header("PDB Model")
    title = st.text_input("Enter the title:")
    if st.button("Generate PDB Model"):
        result = make_request("request_pdb_model", {"title": title})
        if result:
            st.subheader("Response:")
            display_json(result)

def update_pdb_model():
    st.header("Update PDB Model")
    prev_suggestion = st.text_area("Enter the previous suggestion:")
    feedback = st.text_area("Enter feedback:")
    if st.button("Update PDB Model"):
        result = make_request("request_pdb_update", {"prev_suggestion": prev_suggestion, "feedback": feedback})
        if result:
            st.subheader("Response:")
            display_json(result)

def execute_pdb_model():
    st.header("Execute PDB Model")
    problem = st.text_area("Enter the problem:")
    model = st.text_area("Enter the model:")
    if st.button("Execute PDB Model"):
        result = make_request("request_pdb_execution", {"problem": problem, "model": model})
        if result:
            st.subheader("Response:")
            display_json(result)

def problem_landscape():
    st.header("Problem Landscape")
    title = st.text_input("Enter the title:")
    abstract = st.text_area("Enter the abstract:")
    if st.button("Generate Problem Landscape"):
        result = make_request("request_problem_landscape", {"title": title, "abstract": abstract})
        if result:
            st.subheader("Response:")
            display_json(result)

def function_map():
    st.header("Function Map")
    title = st.text_input("Enter the title:")
    abstract = st.text_area("Enter the abstract:")
    if st.button("Generate Function Map"):
        result = make_request("request_function_map", {"title": title, "abstract": abstract})
        if result:
            st.subheader("Response:")
            display_json(result)

if __name__ == "__main__":
    main()
