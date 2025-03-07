# 🚀 AI Fax Classification 

## 📝 Introduction

This project is a Python-based solution for processing and classifying fax emails using an AI model (GPT-4o-Mini). The system is designed to:
- Read emails from a test dataset (included in this Repository for convinience).
- Identify valid fax emails as those who come from `fax@example.com`.
- Extract fax attachments.
- Classify the fax content into one of three categories: **Patient Referrals**, **Prior Authorization Responses**, or **Patient Records**.
- Store the fax in the corresponding folder with a timestamped filename.
- Simulate a notification by printing the classification result and storage location.

## ⚙️ Setup Instructions

### Prerequisites

- **Python 3.8+**
- **Pip** (Python package manager)
- An **OpenAI API key** (to be set in a `.env` file)

> [!IMPORTANT]  
> If your missing Python/Pip, go [here](https://www.python.org/downloads/) to install it for your OS. If you need an OpenAI API key, go [here](https://openai.com/index/openai-api/).

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/UmairK5669/fax-classification.git
    cd fax_classification
    ```

2. **Install Dependencies**

    ```bash
    pip install python-dotenv openai
    ```

3. **Configure the Environment**

    Create a `.env` file in the root directory and add your OpenAI API key: 

    ```bash
    OPENAI_API_KEY=your_api_key_here
    ```

### 🚀 Usage Instructions 

To run the script, simply execute the following:

```bash
python fax_classification.py
```

And that's it, once the script is done exeucting, you can find the classified faxes in the `classified_faxes` directory. As the script progresses through the emails, "notifications" will be printed to the console, notifying when a new fax is classified, including what it was classified as, and where the fax is now saved.

**Script Workflow:**

1. **Output Directories Creation:**
    The script creates categorized folders under classified_faxes/ if they don't exist.

2. **Email Processing:**
    It reads each email from the test_dataset/emails/ directory and checks if it is from fax@example.com.

3. **Attachment Extraction:**
    Using regex, the script extracts the attachment filename and reads the corresponding fax file from test_dataset/faxes/.

4. **Fax Classification:**
    The fax content is sent to GPT-4o-Mini for classification. The model is prompted to return one of the following:

    - "Patient Referral"
    - "Prior Authorization Response"
    - "Patient Records"

    If the classification is unclear, it returns "Uncertain".

5. **File Storage:**
    Based on the classification, the fax is copied into the correct folder under classified_faxes/ with a timestamped filename.

6. **Notification:**
    A notification is printed to the console indicating the classification result and the file's new location.
