import streamlit as st
import requests

# FastAPI server URL
BASE_URL = "data.kreat.space"  # Update this with your FastAPI server URL

def main():
    st.title("Problem Analysis Tool")

    # Sidebar for navigation
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
