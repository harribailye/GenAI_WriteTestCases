from openai import OpenAI
import tkinter as tk

# Activate venv: source venv/bin/activate

# This will take in acceptance criteria, output all different test scenarios, of which the user can select which ones to generate test cases for



# Set up the OpenAI API
client = OpenAI(api_key="")

def generate_scenarios():

    # Base system role message
    base_system_role_message = "List all the possible test case scenarios from acceptance criteria, including negative scenarios in dot point. Brief overview of the scenario"

    # Extract the content of the test case entry
    test_case_content = acceptance_criteria_entry.get("1.0", "end").strip()

    if test_case_content:
        
        user_message = f"Write all the appropriate test case scenarios from this acceptance criteria\n{test_case_content}"

        # Prepare messages for ChatGPT
        messages = [{"role": "user", "content": user_message},
                    {"role": "system", "content": base_system_role_message}]
        
        # Call OpenAI API to generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract the content of the response message
        chatGPT_response = response.choices[0].message.content

        # Clear the Test Case Output widget
        test_case_scenarios.delete("1.0", tk.END)

        # Update the text area with ChatGPT response
        test_case_scenarios.insert(tk.END, chatGPT_response.strip() + "\n\n")


def submit_test_case():

    # Base system role message
    base_system_role_message = "You are a test case writer, write a test case for each main scenario with numbered test steps under each test case. Each step should have an Expected Result attached."

    # Extract the content of the test case entry
    test_case_content = acceptance_criteria_label.get("1.0", "end").strip()

    if test_case_content:
        # Include number of scenarios, minimum test steps, and maximum test steps per scenario in the user message
        user_message = f"Write exactly test scenarios where each scenario has between test steps\n{test_case_content}"

        # Prepare messages for ChatGPT
        messages = [{"role": "user", "content": user_message},
                    {"role": "system", "content": base_system_role_message}]
        
        # Call OpenAI API to generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract the content of the response message
        chatGPT_response = response.choices[0].message.content

        # Update the text area with ChatGPT response
        chatGPT_response_text = chatGPT_response.split('=')[-1].strip().strip("'").strip()
        test_case_output.insert(tk.END, chatGPT_response_text + "\n\n")


# Create the GUI window
root = tk.Tk()
root.title("Test Case Generator")

# Set window size and position
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Set window background color
root.configure(bg="black")

# Title Label
title_label = tk.Label(root, text="Test Case Generator", font=("Arial", 30, "bold"), bg="black", fg="#ADD8E6")
title_label.pack(side=tk.TOP, pady=10)

# AC Entry Label
acceptance_criteria_label = tk.Label(root, text="Enter Acceptance Criteria:", font=("Arial", 12), bg="black", fg="white", anchor="w")
acceptance_criteria_label.pack(side=tk.TOP, pady=(10, 0), padx=10, anchor="w")  

# Acceptance Criteria Entry Widget
acceptance_criteria_entry = tk.Text(root, font=("Arial", 12), wrap="word", height=5)
acceptance_criteria_entry.pack(expand=True, fill="both", padx=10, pady=(10, 5))  

# Generate Test Scenarios button
generate_scenarios_button = tk.Button(root, command = generate_scenarios, text="Generate Test Scenarios", font=("Arial", 12), bg="#4CAF50", fg="white", padx=5, pady=2)
generate_scenarios_button.pack(side=tk.TOP, pady=(10, 0), padx=10, anchor="w")

# Test Case Scenarios Label
test_case_scenarios_label = tk.Label(root, text="Test Case Scenarios:", font=("Arial", 12), bg="black", fg="red", anchor="w")
test_case_scenarios_label.pack(side=tk.TOP, pady=(10, 0), padx=10, anchor="w")  

# Test Case Scenarios Widget
test_case_scenarios = tk.Text(root, font=("Arial", 12), wrap="word", height=20)
test_case_scenarios.pack(expand=True, fill="both", padx=10, pady=(10, 5))  

# Generate Test Cases button
generate_tc_button = tk.Button(root, text="Generate Test Cases", command=submit_test_case, font=("Arial", 12), bg="#4CAF50", fg="white", padx=5, pady=2)
generate_tc_button.pack(side=tk.TOP, pady=(10, 0), padx=10, anchor="w")

# Test Case Output Label
test_case_output_label = tk.Label(root, text="Generated Test Cases:", font=("Arial", 12), bg="black", fg="red", anchor="w")
test_case_output_label.pack(side=tk.TOP, pady=(10, 0), padx=10, anchor="w")

# Test Case Output Widget
test_case_output = tk.Text(root, font=("Arial", 12), wrap="word", height=20)
test_case_output.pack(expand=True, fill="both", padx=10, pady=(0, 10))  

# Configure Text Colors
test_case_output.tag_configure("light_blue", foreground="#ADD8E6")

# Start GUI main loop
root.mainloop()
