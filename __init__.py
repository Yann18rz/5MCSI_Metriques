from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/contact/")
def mapagecontact():
    return render_template("contact.html")                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2
  
if __name__ == "__main__":
  app.run(debug=True)
async function fetchCommits() {
  const response = await fetch('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits');
  const commits = await response.json();
  return commits;
}
async function getCommitData() {
  const commits = await fetchCommits();
  const minuteCount = {};

  commits.forEach(commit => {
    const dateString = commit.commit.author.date;
    const dateObject = new Date(dateString);
    const minute = dateObject.getUTCMinutes(); // Extraire la minute

    if (minuteCount[minute]) {
      minuteCount[minute] += 1; // Incrémente le nombre de commits pour cette minute
    } else {
      minuteCount[minute] = 1; // Initialiser à 1 si c'est le premier commit de cette minute
    }
  });

  return minuteCount;
}
