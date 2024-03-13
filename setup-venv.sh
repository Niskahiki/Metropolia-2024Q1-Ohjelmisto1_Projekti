#!/bin/bash
# This script should be run from inside the project root directory.
# Else the virtual environment will not be created in the proper location relative to "main.py".

echo "Please wait... Creating virtual environment for Python."
python -m venv .venv/

# Check if user is on Windows, otherwise activate via source.
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Update PIP and install dependencies.
pip install --upgrade pip
pip install -r requirements.txt

# Print some info for the user.
echo "Script has finished!"
echo ""
echo "Before running the application, please activate the VENV!"
echo "* users on Linux can run: \"source .venv/bin/activate\""
echo "* users on Windows can run: \".venv\\Scripts\\activate\""
