from openai import OpenAI
import tkinter as tk
from tkinter import messagebox
import re

# Set up the OpenAI API
client = OpenAI(api_key="")

# Base system role message
base_system_role_message = "You are a test case writer, write a test case for each main scenario with numbered test steps under each test case. Each step should have an Expected Result attached."

def submit_test_case():
    # Extract the content of the test case entry
    test_case_content = test_case_entry.get("1.0", "end").strip()

    # Extract the number of scenarios if provided by the user
    num_scenarios_entry_text = num_scenarios_entry.get().strip()
    if not num_scenarios_entry_text:
        tk.messagebox.showerror("Error", "Please enter the number of scenarios.")
        return
    
    if test_case_content:
        # Extract the number of scenarios, test steps, and additional system role message entered by the user
        num_scenarios = int(num_scenarios_entry.get())
        min_test_steps = int(min_test_steps_spinbox.get())
        max_test_steps = int(max_test_steps_spinbox.get())
        additional_system_role_message = system_role_entry.get()

        # Ensure that minimum test steps cannot be greater than maximum test steps
        if min_test_steps > max_test_steps:
            tk.messagebox.showerror("Error", "Minimum test steps cannot be greater than maximum test steps.")
            return

        # Construct the complete system role message
        system_role_message = f"{base_system_role_message}\n{additional_system_role_message}"

        # Include number of scenarios, minimum test steps, and maximum test steps per scenario in the user message
        user_message = f"Write exactly {num_scenarios} test scenarios where each scenario has between {min_test_steps} and {max_test_steps} test steps |  Define Additional System Role Message: {additional_system_role_message}\n{test_case_content}"

        # Prepare messages for ChatGPT
        messages = [{"role": "user", "content": user_message},
                    {"role": "system", "content": system_role_message}]
        
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

        # Generate test case coverage summary
        test_coverage_summary = generate_coverage_summary(chatGPT_response_text, test_case_content)
        test_case_coverage_output.delete("1.0", tk.END)  # Clear previous content
        test_case_coverage_output.insert(tk.END, test_coverage_summary + "\n")

def generate_coverage_summary(generated_test_cases, acceptance_criteria):
    # Calculate coverage percentage
    coverage_percentage = calculate_coverage_percentage(generated_test_cases, acceptance_criteria)
    
    # Extract scenario titles using regex
    scenario_titles = re.findall(r'Test Scenario \d+: (.+)', generated_test_cases)
    
    # Add scenario numbers to each scenario title
    formatted_scenario_titles = [f"Scenario {i+1}: {title}" for i, title in enumerate(scenario_titles)]
    
    test_scenario_overview = "\n".join(formatted_scenario_titles)
    
    # Initialize the summary variable
    summary = ""
    
    # Construct coverage summary
    summary += f"Coverage Percentage: {coverage_percentage}%\n"
    summary += f"\nTest Scenario Overview:\n{test_scenario_overview}\n"
    
    return summary


def calculate_coverage_percentage(generated_test_cases, acceptance_criteria):
    if not generated_test_cases or not acceptance_criteria:
        raise ValueError("Both generated test cases and acceptance criteria must be non-empty strings")

    generated_words = generated_test_cases.split()
    acceptance_words = acceptance_criteria.split()
    
    if not acceptance_words:
        raise ValueError("Acceptance criteria must contain at least one word")

    num_matched_words = len(set(generated_words) & set(acceptance_words))
    total_words = len(acceptance_words)
    
    if total_words == 0:
        raise ValueError("Acceptance criteria cannot be empty")
    
    coverage_percentage = (num_matched_words / total_words) * 100
    return round(coverage_percentage, 2)

def generate_scenario_overview(generated_test_cases):
    pattern = r"Test Scenario \d+: (.+)"  # Regex pattern to match scenario titles
    scenario_titles = re.findall(pattern, generated_test_cases)
    test_scenario_overview = "\n".join(scenario_titles)
    return test_scenario_overview

def clear_text():
    test_case_output.delete("1.0", tk.END)
    test_case_coverage_output.delete("1.0", tk.END)

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
title_label = tk.Label(root, text="Test Case Generator", font=("Arial", 20, "bold"), bg="black", fg="#ADD8E6")
title_label.pack(side=tk.TOP, pady=10)

# Frame for Number of Scenarios and Define Additional System Role Message
num_system_role_frame = tk.Frame(root, bg="black")
num_system_role_frame.pack(side=tk.TOP, padx=10, pady=(0, 10), anchor="w")

# Number of Scenarios Entry Label
num_scenarios_label = tk.Label(num_system_role_frame, text="Number of Scenarios:", font=("Arial", 12), bg="black", fg="white")
num_scenarios_label.pack(side=tk.LEFT)

# Number of Scenarios Entry Widget
num_scenarios_entry = tk.Entry(num_system_role_frame, font=("Arial", 12), bg="white")
num_scenarios_entry.pack(side=tk.LEFT)

# Define Additional System Role Message Label
system_role_label = tk.Label(num_system_role_frame, text="Define Additional System Role Message:", font=("Arial", 12), bg="black", fg="white")
system_role_label.pack(side=tk.LEFT, padx=(20, 0))

# Define Additional System Role Message Widget
system_role_entry = tk.Entry(num_system_role_frame, font=("Arial", 12), bg="white", width=40)
system_role_entry.pack(side=tk.LEFT)

# Minimum Test Steps Label
min_test_steps_label = tk.Label(root, text="Minimum Test Steps:", font=("Arial", 12), bg="black", fg="white", anchor="w")
min_test_steps_label.place(x=10, y=100)

# Minimum Test Steps Spinbox
min_test_steps_var = tk.StringVar(root)
min_test_steps_var.set(1)  # Default value
min_test_steps_spinbox = tk.Spinbox(root, from_=1, to=50, textvariable=min_test_steps_var, font=("Arial", 12), bg="white", width=5)
# Spinbox placement continued
min_test_steps_spinbox.place(x=200, y=100)

# Maximum Test Steps Label
max_test_steps_label = tk.Label(root, text="Maximum Test Steps:", font=("Arial", 12), bg="black", fg="white", anchor="w")
max_test_steps_label.place(x=400, y=100)

# Maximum Test Steps Spinbox
max_test_steps_var = tk.StringVar(root)
max_test_steps_var.set(5)  # Default value
max_test_steps_spinbox = tk.Spinbox(root, from_=1, to=50, textvariable=max_test_steps_var, font=("Arial", 12), bg="white", width=5)
max_test_steps_spinbox.place(x=600, y=100)

# Test Case Entry Label
test_case_label = tk.Label(root, text="Add Your Acceptance Criteria Here:", font=("Arial", 12), bg="black", fg="white", anchor="w")
test_case_label.pack(side=tk.TOP, pady=(40, 0), padx=10, anchor="w")  # Adjusted pady value

# Test Case Entry Widget
test_case_entry = tk.Text(root, font=("Arial", 12), wrap="word", height=5)
test_case_entry.pack(expand=True, fill="both", padx=10, pady=(10, 5))  # Adjusted pady value

# Submit Button
submit_button = tk.Button(root, text="Submit Acceptance Criteria", command=submit_test_case, font=("Arial", 12), bg="#4CAF50",
                          fg="white", padx=5, pady=2)
submit_button.pack(side=tk.TOP, padx=10, pady=(5, 0), anchor="w")


# Clear Button
clear_button = tk.Button(root, text="Clear", command=clear_text, font=("Arial", 12), bg="red",
                         fg="white", padx=5, pady=2)
clear_button.pack(side=tk.TOP, padx=10, pady=(10, 0), anchor="w")

# Test Case Output Label
test_case_output_label = tk.Label(root, text="Generated Test Cases:", font=("Arial", 12), bg="black", fg="white",
                                  anchor="w")
test_case_output_label.pack(side=tk.TOP, pady=(10, 0), anchor="w")

# Test Case Output Widget
test_case_output = tk.Text(root, font=("Arial", 12), wrap="word", height=12)
test_case_output.pack(expand=True, fill="both", padx=10, pady=10)

# Test Case Coverage Summary Label
test_case_coverage_label = tk.Label(root, text="Test Case Coverage Summary:", font=("Arial", 12), bg="black", fg="white",
                                  anchor="w")
test_case_coverage_label.pack(side=tk.TOP, pady=(10, 0), anchor="w")

# Test Case Coverage Summary Widget
test_case_coverage_output = tk.Text(root, font=("Arial", 12), wrap="word", height=6)  # Adjust height as needed
test_case_coverage_output.pack(expand=True, fill="both", padx=10, pady=10)

# Configure Text Colors
test_case_output.tag_configure("light_blue", foreground="#ADD8E6")

# Start GUI main loop
root.mainloop()

