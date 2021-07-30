from flask import Flask,jsonify,request
from flask import render_template
import ast

app = Flask(__name__)
keyword = ""
hashtags = []
tags_count = []
mentions = []
mention_count = []

@app.route("/hashtags")
def get_chart_page():
  global hashtags, tags_count
  hashtags = []
  tags_count = []
  return render_template('chart.html', label="Top Trending Hashtags", values=tags_count, labels=hashtags)

@app.route("/hashtags/refreshData")
def refresh_graph_data():
  global hashtags, tags_count
  print("labels now: " + str(hashtags))
  print("data now: " + str(hashtags))
  return jsonify(sLabel=hashtags, sData=tags_count)

@app.route("/hashtags/updateData", methods=["POST"])
def update_data():
  global hashtags, tags_count
  if not request.form or "data" not in request.form:
    return "error", 400
  hashtags = ast.literal_eval(request.form['label'])
  tags_count = ast.literal_eval(request.form['data'])
  print("labels received: " + str(hashtags))
  print("data received: " + str(tags_count))
  return "success", 201

@app.route("/mentions")
def get_men_chart_page():
  global mentions, mention_count
  mentions = []
  mention_count = []
  return render_template('men_chart.html', label="Top Trending Mentioned Users", values=mention_count, labels=mentions)

@app.route("/mentions/refreshData")
def refresh_men_graph_data():
  global mentions, mention_count
  print("labels now: " + str(mentions))
  print("data now: " + str(mention_count))
  return jsonify(sLabel=mentions, sData=mention_count)

@app.route("/mentions/updateData", methods=["POST"])
def update_men_data():
  global mentions, mention_count
  if not request.form or "data" not in request.form:
    return "error", 400
  mentions = ast.literal_eval(request.form['label'])
  mention_count = ast.literal_eval(request.form['data'])
  print("labels received: " + str(mentions))
  print("data received: " + str(mention_count))
  return "success", 201

if __name__ == "__main__":
  app.run(host="localhost", port=5001)
