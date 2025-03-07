import os
import re
import shutil
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load the OpenAI API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Directories for input and output
EMAILS_DIR = "test_dataset/emails"
FAXES_DIR = "test_dataset/faxes"
OUTPUT_BASE_DIR = "classified_faxes"

# Mapping from classification to folder name
CATEGORIES = {
    "Patient Referral": "patient_referrals",
    "Prior Authorization Response": "prior_authorizations",
    "Patient Records": "patient_records"
}

def create_output_dirs() -> None:
    """Ensure that all classification folders exist.

    :return: None
    """
    for folder in CATEGORIES.values():
        path = os.path.join(OUTPUT_BASE_DIR, folder)
        os.makedirs(path, exist_ok=True)

def classify_fax(fax_content: str) -> str:
    """
    Uses GPT-4o-Mini via the OpenAI API to classify the fax content.

    :param fax_content: The content of the fax to classify.
    :type fax_content: str

    :return: A classification string, "Patient Referral", "Prior Authorization Response", or "Patient Records". 
        If the response is unclear, returns "Uncertain".
    :rtype: str
    """
    system_message = (
        "You are an AI assistant that classifies faxes into specific categories. "
        "Only respond with one of the following classifications: "
        "'Patient Referral', 'Prior Authorization Response', or 'Patient Records'. "
        "If the category is unclear, respond with 'Uncertain'. Do not provide explanations."
    )

    user_message = f"Fax Content:\n{fax_content}:"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0
        )
        
        classification = response.choices[0].message.content.strip()

        # Match the known categories (case insensitive)
        for key in CATEGORIES.keys():
            if key.lower() in classification.lower():
                return key
        return "Uncertain"

    except Exception as e:
        print(f"Error during classification: {e}")
        return "Uncertain"

def process_email(email_file_path: str) -> None:
    """Processes a single email file to extract and classify the fax.
    
    :param email_file_path: The path to the email file.
    :type email_file_path: str

    :return: None
    """
    with open(email_file_path, "r") as f:
        email_content = f.read()

    # Check if the email is from the designated fax sender
    if "From: fax@example.com" not in email_content:
        return  # Not a fax email; skip processing

    # Extract the attachment filename using regex
    attachment_match = re.search(r"Attachment:\s*(\S+)", email_content)
    if not attachment_match:
        print(f"No attachment found in email: {email_file_path}")
        return

    attachment_filename = attachment_match.group(1).strip()
    fax_file_path = os.path.join(FAXES_DIR, attachment_filename)
    
    if not os.path.exists(fax_file_path):
        print(f"Fax file not found: {fax_file_path}")
        return

    # Read the fax file content
    with open(fax_file_path, "r") as fax_file:
        fax_content = fax_file.read()

    # Classify the fax using GPT-4o-Mini
    classification = classify_fax(fax_content)
    
    # Determine the output folder based on classification
    dest_folder = None
    for key, folder in CATEGORIES.items():
        if key.lower() in classification.lower():
            dest_folder = os.path.join(OUTPUT_BASE_DIR, folder)
            break

    if not dest_folder:
        print(f"Could not determine classification for fax: {fax_file_path}")
        return

    # Ensure destination directory exists
    os.makedirs(dest_folder, exist_ok=True)

    # Create a new filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"fax_{timestamp}.txt"
    dest_path = os.path.join(dest_folder, new_filename)

    # Copy the fax file to the classified folder
    shutil.copy2(fax_file_path, dest_path)

    # Print notification to simulate sending an email
    print(f'New fax classified as "{classification}" and saved in:\n  {dest_path}')

def main() -> None:
    """Main function to process all email files in the emails directory.

    :return: None
    """
    create_output_dirs()
    
    # Process each email file in the emails directory
    for email_file in os.listdir(EMAILS_DIR):
        email_file_path = os.path.join(EMAILS_DIR, email_file)
        process_email(email_file_path)

if __name__ == "__main__":
    main()
