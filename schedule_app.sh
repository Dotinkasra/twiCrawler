#!/opt/homebrew/bin/fish

source ./venv/bin/activate.fish
nohup python main.py > /dev/null 2>&1 &
