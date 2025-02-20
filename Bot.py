import subprocess
import os
import logging
import sys
from openai import OpenAI
import time

# Configure OpenAI client
client = OpenAI(api_key="sk-proj-2By770zviWsreq3LW7fDGkfGTaTOKYJT"
                        "-ljdUvR0fGvbkaMju9G00dWHEET3BlbkFJjDPJFC1edC9Lnbat6qWXpmZo3mNk_B1jiWyC5Tf-DY447H9qVwk0wOKOsA")

assistant_id = "asst_ohjld2zq70yjwOqIDCBIvWHM"

# Configure logging
# logging.basicConfig(filename="code_formatting_logs.log", level=logging.INFO, format="%(message)s")


def format_python_code(file_path):
    """Formats Python code using autopep8."""
    result = subprocess.run(["autopep8", "--in-place", file_path], shell=True, capture_output=True, text=True)
    return result


def check_code_with_flake8(file_path):
    """Checks Python code with flake8."""
    result = subprocess.Popen([
        r"flake8 --extend-ignore E501,W292,E302,F841,F401,F821", file_path
    ], stdout=subprocess.PIPE, text=True, shell=True)
    stdout = result.communicate()
    return stdout


def update_code_using_openai(file_path):
    """Updates Python code using OpenAI Assistant."""
    with open(file_path, "r") as file:
        original_code = file.read()

    # assistant = client.beta.assistants.create(
    #     name="Static_analysis_python",
    #     instructions="""You are a Python code reviewer specializing in enforcing Flake8 and Pylint standards. When 
    #     provided with Python code, you must:\n 1. Add module-level docstrings describing the purpose of the script.\n 
    #     2. Add function and method docstrings explaining their functionality, parameters, and return values.\n 3. 
    #     Ensure all naming conventions follow snake_case (convert variables, functions, and method names 
    #     accordingly).\n 4. Remove unused imports to maintain clean and efficient code.\n 5. Disable Pylint’s 
    #     'invalid-name' rule for the entire module using # pylint: disable=invalid-name.\n Provide only the modified 
    #     code, without any additional text.""",
    #     tools=[{"type": "code_interpreter"}],
    #     model="gpt-4o-mini"
    # )

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"""
            Code:\n
            {original_code}
        """
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while run.status not in ["completed", "failed"]:
        time.sleep(10)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        updated_code = messages.data[0].content[0].text.value  # Extract AI response
        cleaned_code = updated_code.replace("```python", "").replace("```", "")

        with open(file_path, "w") as file:
            file.write(cleaned_code)


def main(changed_files):
    """Processes only the changed Python files."""
    for file_path in changed_files:
        if file_path.endswith(".py") and os.path.exists(file_path):
            # logging.info(f"Processing file: {file_path}")
            # print(file_path)

            # Check for Flake8 issues
            flake8_result = check_code_with_flake8(file_path)
            print((f"Flake8 suggestions before updae:\n{flake8_result[0]}"))
            # logging.info(f"Flake8 suggestions:\n{flake8_result[0]}")

            # Update code using OpenAI Assistant
            update_code_using_openai(file_path)
            time.sleep(3)

            # Format the code using autopep8
            print("Formatting the code using autopep8...")
            format_python_code(file_path)

            # Check for Flake8 issues after the update
            flake8_result = check_code_with_flake8(file_path)
            print((f"Flake8 suggestions after update:\n{flake8_result[0]}"))


if __name__ == "__main__":
    changed_files = sys.argv[1:]
    if changed_files:
        main(changed_files)