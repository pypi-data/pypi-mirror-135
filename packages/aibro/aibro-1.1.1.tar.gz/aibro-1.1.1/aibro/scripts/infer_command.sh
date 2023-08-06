python -m venv repo_venv
. repo_venv/bin/activate
pip install -r $1/requirements.txt
echo "Dependencies installed!"
