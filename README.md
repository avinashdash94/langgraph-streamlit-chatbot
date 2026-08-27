# Python Environment and LangGraph Setup

This guide explains how to create a Python virtual environment, install the required libraries, and configure Jupyter Notebook for the project.

## 1. Prerequisites

Make sure Python is installed on your system.

Verify the installation:

```bash
python --version
```

## 2. Create a Python Virtual Environment

Create a virtual environment named `myenv`:

```bash
python -m venv myenv
```

## 3. Activate the Virtual Environment

On Windows:

```bash
myenv\Scripts\activate
```

After activation, your terminal should show something similar to:

```text
(myenv)
```

> **Note:** If your project uses `.venv` instead of `myenv`, replace `myenv` with `.venv` in the commands below.

## 4. Upgrade pip

Upgrade pip to the latest version:

```bash
python -m pip install --upgrade pip
```

## 5. Install Required Libraries

All required Python packages are listed in `requirements.txt`.

Install them using:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
jupyter
ipykernel
python-dotenv
groq
langgraph
langchain
langchain-openai
```

### Jupyter and IPython Kernel

`jupyter` is used to run Jupyter Notebooks, while `ipykernel` allows the virtual environment to be selected as a Jupyter Notebook kernel.

`ipykernel` is required to run notebook cells using the project's Python environment.

## 6. Environment Variables

The `python-dotenv` package is used to load environment variables from a `.env` file.

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your-api-key
GROQ_API_KEY=your-api-key
```

Python example:

```python
from dotenv import load_dotenv

load_dotenv()
```

> **Note:** Install `python-dotenv`, not `dotenv`.

Do not commit the `.env` file to source control if it contains real API keys or other secrets.

## 7. Create a Jupyter Notebook

Create a file with the `.ipynb` extension, for example:

```text
langgraph_demo.ipynb
```

Jupyter Notebook can be used to experiment with, debug, and visualize LangGraph workflows.

## 8. Select the Python Environment in VS Code

Open the `.ipynb` file in VS Code.

1. Press **Ctrl + Shift + P**.
2. Search for **Jupyter: Select Notebook Kernel**.
3. Select **Select Another Kernel**.
4. Select **Python Environments**.
5. Select the virtual environment created for the project:

```text
myenv
```

### If the Environment Does Not Appear

Make sure `ipykernel` is installed in the selected environment:

```bash
python -m pip install ipykernel
```

Then restart VS Code or reload the notebook and select the kernel again.

## 9. Verify the Environment

Verify the Python version:

```bash
python --version
```

Check the installed packages:

```bash
python -m pip list
```

You can also verify that the correct Python executable is being used:

```bash
where python
```

The output should point to the project's `myenv` directory.

## 10. Quick Setup

For a new environment, run the following commands:

```bash
python -m venv myenv
myenv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

After installation, create your `.ipynb` file and select `myenv` as the Jupyter Notebook kernel.

## 11. One-Click Setup Using setup.bat

A `setup.bat` file is provided to automate the environment setup.

Run:

```text
setup.bat
```

The script will:

1. Create the `myenv` virtual environment.
2. Activate the virtual environment.
3. Upgrade pip.
4. Install all dependencies from `requirements.txt`.

Example `setup.bat`:

```bat
@echo off

echo ==========================================
echo Creating Python Virtual Environment
echo ==========================================

python -m venv myenv

echo.
echo ==========================================
echo Activating Virtual Environment
echo ==========================================

call myenv\Scripts\activate

echo.
echo ==========================================
echo Upgrading pip
echo ==========================================

python -m pip install --upgrade pip

echo.
echo ==========================================
echo Installing Required Packages
echo ==========================================

python -m pip install -r requirements.txt

echo.
echo ==========================================
echo Setup Completed Successfully!
echo ==========================================

echo.
echo To activate the environment later, run:
echo myenv\Scripts\activate

pause
```

> **Note:** Running `setup.bat` activates the environment only for the setup script. When the script finishes, activate the environment manually in a new terminal using:
>
> ```bash
> myenv\Scripts\activate
> ```

## 12. Project Structure

The recommended project structure is:

```text
MyAIProject/
│
├── myenv/
│
├── .env
├── requirements.txt
├── setup.bat
├── README.md
│
└── langgraph_demo.ipynb
```

### Summary

For a fresh setup, simply run:

```text
setup.bat
```

Then activate the environment:

```bash
myenv\Scripts\activate
```

Open the `.ipynb` file in VS Code and select **`myenv`** as the Jupyter Notebook kernel.


13. Frontend UI - Streamlit
This project uses Streamlit to create the frontend UI for the chatbot.

Streamlit allows us to quickly build an interactive web-based UI for the chatbot using Python, without requiring a separate frontend framework.

Install Streamlit

Install Streamlit using:

python -m pip install streamlit

Streamlit Chatbot UI

Streamlit provides built-in components that are useful for creating chatbot interfaces, such as:

Chat message display
Chat input
Buttons
Text input
File upload
Session state
Streaming responses

Run the Streamlit Frontend

streamlit run .\streamlit_frontend.py