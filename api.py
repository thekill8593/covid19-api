from datetime import date
import flask
import sqlite3 as sql
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/all', methods=['GET'])
def api_all():
  conn = sql.connect('example.db')
  cur = conn.cursor()
  today = date.today()
  query = f"SELECT Country_Region, sum(Confirmed) as Total_Cases, sum(Deaths) as Total_Deaths, sum(Recovered) as Recovered FROM example WHERE date(Last_Update) = '{today}' GROUP BY Country_Region ORDER BY Total_Cases DESC"
  cur.execute(query)

  rows = cur.fetchall();

  data = list()
  for row in rows:
    data.append({ 'Country': row[0], 'Total_Cases': row[1], 'Total_Deaths': row[2], 'Recovered': row[3] })

  return jsonify(data)
  
@app.route('/api/country/', methods=['GET'])
def api_country():
  country = request.args.get('country', None)
  
  if not country:
    return jsonify({
		"error": "You must send country name e.g /api/country?country=US"
	})
	
  conn = sql.connect('example.db')
  cur = conn.cursor()
  today = date.today()
  query = f"SELECT Province_State, Country_Region, sum(Confirmed) as Total_Cases, sum(Deaths) as Total_Deaths, sum(Recovered) as Recovered, (sum(Confirmed) - (sum(Deaths) + sum(Recovered))) as Active_Cases, round((100 / sum(Confirmed) * sum(Deaths)), 2) as Mortality_Rate FROM example WHERE date(Last_Update) = '{today}' and Country_Region = '{country}' GROUP BY Province_State HAVING Total_Cases > 0 ORDER BY Total_Cases DESC"
  cur.execute(query)

  rows = cur.fetchall();
  
  data = list()
  for row in rows:
    data.append({ 'Province_State': row[0], 'Country_Region': row[1], 'Total_Cases': row[2], 'Total_Deaths': row[3], 'Recovered': row[4], 'Active_Cases': row[5], 'Mortality_Rate': row[6] })

  return jsonify(data)

app.run()
