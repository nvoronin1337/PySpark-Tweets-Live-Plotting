from flask import Flask,jsonify,request
from flask import render_template
import ast

app = Flask(__name__)
keyword = ""

# hashtags data
hashtags = []
tags_count = []

# mentions data
mentions = []
mention_count = []

# sentiment analysis data
compound_avg = 0.0
pos_avg = 0.0
neu_avg = 0.0
neg_avg = 0.0

# Renders Hashtags Page (initial hashtags chart)
@app.route("/hashtags")
def get_hash_chart_page():
  global hashtags, tags_count
  hashtags = []
  tags_count = []
  return render_template('hash_chart.html', label="Top Trending Hashtags", values=tags_count, labels=hashtags)

# Re-Renders Hashtags Page (with current values in hashtags and tags_count lists)
@app.route("/hashtags/refreshData")
def refresh_hash_graph_data():
  global hashtags, tags_count
  print("hashtags now: " + str(hashtags))
  print("hashtags count now: " + str(hashtags))
  return jsonify(sLabel=hashtags, sData=tags_count)

# Receives 'label' and 'data' with new values for hashtags and tags_count lists
@app.route("/hashtags/updateData", methods=["POST"])
def update_hash_data():
  global hashtags, tags_count
  if not request.form or "data" not in request.form:
    return "error", 400
  hashtags = ast.literal_eval(request.form['label'])
  tags_count = ast.literal_eval(request.form['data'])
  print("hashtags received: " + str(hashtags))
  print("hashtags count received: " + str(tags_count))
  return "success", 201

# Renders Mentions Page (initial mentions chart)
@app.route("/mentions")
def get_men_chart_page():
  global mentions, mention_count
  mentions = []
  mention_count = []
  return render_template('men_chart.html', label="Top Trending Mentioned Users", values=mention_count, labels=mentions)

# Re-Renders Mentions Page (with current values in mentions and mention_count lists)
@app.route("/mentions/refreshData")
def refresh_men_graph_data():
  global mentions, mention_count
  print("mentions now: " + str(mentions))
  print("mentions count now: " + str(mention_count))
  return jsonify(sLabel=mentions, sData=mention_count)

# Receives 'label' and 'data' with new values for mentions and mention_count lists
@app.route("/mentions/updateData", methods=["POST"])
def update_men_data():
  global mentions, mention_count
  if not request.form or "data" not in request.form:
    return "error", 400
  mentions = ast.literal_eval(request.form['label'])
  mention_count = ast.literal_eval(request.form['data'])
  print("mentions received: " + str(mentions))
  print("mentions count received: " + str(mention_count))
  return "success", 201


# Renders Sentiment Analysis Page (initial sentiment analysis chart)
@app.route("/sentiment")
def get_sent_chart_page():
  global compound_avg, pos_avg, neu_avg, neg_avg
  compound_avg = 0.0
  pos_avg = 0.0
  neu_avg = 0.0
  neg_avg = 0.0
  return render_template('sent_chart.html', label="Tweet Sentiment Analysis", comp=compound_avg, pos=pos_avg, neu=neu_avg, neg=neg_avg)

# Re-Renders Sentiment Analysis Page (with current values in sentiment_labels and sentiment_values lists)
@app.route("/sentiment/refreshData")
def refresh_sent_graph_data():
  global compound_avg, pos_avg, neu_avg, neg_avg
  print("sentiment compound now: " + str(compound_avg))
  print("sentiment pos now: " + str(pos_avg))
  print("sentiment neu now: " + str(neu_avg))
  print("sentiment neg now: " + str(neg_avg))
  return jsonify(sComp=float(compound_avg), sPos=pos_avg, sNeu=neu_avg, sNeg=neg_avg)

# Receives 'label' and 'data' with new values for hashtags and tags_count lists
@app.route("/sentiment/updateData", methods=["POST"])
def update_sent_data():
  global compound_avg, pos_avg, neu_avg, neg_avg
  if not request.form or "comp" not in request.form:
    return "error", 400
  compound_avg = ast.literal_eval(request.form['comp'])
  pos_avg = ast.literal_eval(request.form['pos'])
  neu_avg = ast.literal_eval(request.form['neu'])
  neg_avg = ast.literal_eval(request.form['neg'])
  print("sentiment values received: " + str([compound_avg, pos_avg, neu_avg, neg_avg]))
  return "success", 201


if __name__ == "__main__":
  app.run(host="localhost", port=5001)
