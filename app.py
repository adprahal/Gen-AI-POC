from flask import Flask, render_template, request, redirect, url_for
import subprocess
import sys
venv_python = sys.executable  # This will use the current interpreter (should be .venv if Flask is running in it)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_question = request.form['question_input']
        # Execute main.py as a separate process and pass the question as an argument
        try:
            # For demonstration, we're capturing stdout. In a real app, you might want to handle this differently.
            result = subprocess.run([venv_python, 'main.py', user_question], capture_output=True, text=True, check=True)
            output = result.stdout 
            #output = print(result) 
            
            return render_template('index.html', output=output, question=user_question)
        except subprocess.CalledProcessError as e:
            #error_message = print({e.stderr})
            error_message = f"Error running main.py: {e}\n{e.stderr}"
            return render_template('index.html', output=error_message, question=user_question)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555) # debug=True allows for automatic reloading on code changes