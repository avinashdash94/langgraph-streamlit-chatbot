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

### `requirements.txt`

Keep this file in the **same folder** as `setup.bat`:

```text
jupyter
ipykernel
python-dotenv
groq
langgraph
langchain
langchain-openai
```

### Your project structure

```text
MyAIProject/
│
├── setup.bat
├── requirements.txt
├── README.md
├── .env
│
└── langgraph_demo.ipynb
```

Now, on a new machine, you only need to run:

```text
setup.bat
```

It will automatically:

1. Create `myenv`
2. Activate `myenv`
3. Upgrade `pip`
4. Install all packages from `requirements.txt`

**One small point:** `call myenv\Scripts\activate` activates the environment only for the `setup.bat` process. When the script finishes, your existing terminal will **not** remain activated. For subsequent terminal sessions, run:

```bash
myenv\Scripts\activate
```
