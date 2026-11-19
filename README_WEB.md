# OS Resource Manager — Web Dashboard

This version keeps your original Python algorithm modules and adds a Flask backend plus a responsive HTML/CSS/JavaScript dashboard.

## Included modules
- CPU: FCFS, non-preemptive SJF, Round Robin, comparison
- Memory: First Fit, Best Fit, Worst Fit
- Deadlock: Banker's safety algorithm
- Disk: FCFS, SSTF, SCAN
- Performance Reports page linking to each live comparison

## Run on Windows
1. Extract the ZIP. Open the `OS-Resource-Manager` folder in VS Code.
2. Open Terminal in that folder.
3. Create environment (recommended): `py -m venv venv`
4. Activate: `venv\Scripts\activate`
5. Install: `pip install -r requirements.txt`
6. Start: `python app.py`
7. Open browser: `http://127.0.0.1:5000`

## Run on Ubuntu / WSL
`python3 -m venv venv && source venv/bin/activate`
`pip install -r requirements.txt`
`python app.py`
Then open `http://127.0.0.1:5000`.

The original terminal application remains available using `python main.py`.
