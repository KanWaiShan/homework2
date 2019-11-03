from flask import Flask, render_template, request
import csv
import json

app = Flask(__name__)
filename = 'results.csv'


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/thanks', methods=['POST'])
def save_to_csv():
    if request.method == 'POST':
        name = request.form['name']
        born = request.form['born']
        resident = request.form['resident']
        age = request.form['age']
        gender = request.form['gender']
        NS = request.form['NS']
        q1 = request.form['q1']
        q2 = request.form['q2']

        fin_form = 'Thank you!'
        fieldnames = ['NS', 'name', 'born', 'resident', 'age', 'gender', 'q1', 'q2']
        with open(filename, 'a+', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'NS': NS, 'name': name, 'born': born,
                             'resident': resident, 'age': age, 'gender': gender, 'q1': q1, 'q2': q2})
        return render_template("thanks.html", fin_form=fin_form)


@app.route('/search')
def do_search():
    return render_template("search.html")


@app.route('/result', methods=['POST'])
def show_result():
    dict_csv = {}
    if request.method == 'POST':
        NS = request.form['NS_search']
        what = request.form['what_search']
        fieldnames = ['NS', 'name', 'born', 'resident', 'age', 'gender', 'q1', 'q2']
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in reader:
                if row['NS'] == NS:
                    if (row['gender'] == what or row['born'] == what or
                            row['resident'] == what or row['age'] == what or row['q1'] == what or row['q2']):
                        name = row['name']
                    dict_csv[name] = json.loads(json.dumps(row))
            return render_template("result.html", result=dict_csv)


if __name__ == '__main__':
    app.run(debug=True)
