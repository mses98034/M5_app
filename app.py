from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the CSV file once when the app starts
df = pd.read_csv('data_cleaned.csv')

def find_department_names(name, week):
    # Get the specific week value for the given name
    try:
        value = df.loc[df['姓名'] == name, week].values[0]
    except IndexError:
        return [], "No matching records found."

    # Find all names with the same value for the specified week
    output = df[df[week] == value]['姓名']
    num = len(output)
    department = df.loc[df['姓名'] == name, week].values[0]

    return f"科別：{department}", output.tolist(), f"{num}人"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        week = request.form['week']
        department, output, count = find_department_names(name, week)
        return render_template('index.html',department=department, output=output, count=count, name=name, week=week)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
