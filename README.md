**Abstract**  
In the past couple of months popular users like ElonMusk have caused a great impact on the
prices of cryptocurrencies like Dogecoin and Bitcointhrough Twitter. The scope of this project
is to be able to gather tweets in real time in orderto find who are the most trending users and
which hashtags are being used most frequently in thecrypto world. As well as finding what the
sentiment is for cryptocurrencies at this presenttime. We believe being able to have access to all
of this knowledge in real time may be a deciding factorin making an investment in the world of
crypto.

**Relevant Work**  
We have researched how to perform Sentiment Analysison tweets. We found TextBlob [ 1 ] and
NLTK’s Sentiment Intensity Analyzer [ 2 ]; these areboth libraries which perform sentiment
analysis. Given these libraries are pre-trained machinelearning models we did some trial and
error and we realized that NLTK’s Sentiment IntensityAnalyzer seemed to give us a wider
variety of sentiment scores which were also more accuratethan those returned by TextBlob at
least when analyzing tweets sentiment.


**Description of Deliverables**  
To achieve this goal, we collect tweets containingcertain crypto keywords by using Twarc. We
then use Spark to allow incoming streaming tweetsfrom Twarc in iterations of 30 seconds. We
then display all our results for each one of the threegraphs:

● “Top Trending Hashtags” chart will display the amountof tweets containing different
hashtags regarding cryptocurrencies. For example “#Bitcoin”.
● “Top Trending Mentioned Users” chart will show themost mentioned users in tweets
in the context of cryptocurrencies.
● The third and last chart, “ Tweets Sentiment Analysis” will show the different types of
sentiment scores and how each is fluctuating regardinga specific cryptocurrency. The
tweets’ sentiment is broken down into 4 categories;positive sentiment, neutral, negative
sentiment and “compound” which consists of the averagesentiment score. Each of these
scores is used as a variable to update the chart live,as we keep receiving more tweets in
the stream, we keep analyzing the sentiment scoresof the new tweets and updating the
chart simultaneously.

**Implementation Details**    

**Collecting Tweets**  
We are using Python 3 Twarc API for collecting tweets.Our code can be easily configured to
switch between collecting newly posted tweets in realtime and collecting tweets posted in the
last week. We can pass any keyword (such as “Bitcoin”,or “Dogecoin”, etc.). For the purpose of
our sentiment analysis we are only collecting tweetsposted in English language. Every tweet we
have received from Twarc is immediately sent to ourPySpark application via TCP socket. Note:
we are not sending the entire tweet object via socketsince it can be way too large for sending via
socket. We are only sending the text of the tweet.

**Spark Structured Streaming [3]**  
Our PySpark application is continuously receivingdata from the TCP socket. We are then
splitting received data into separate tweets.

**Hashtags and Mentions**   
● First part of our analysis consists of extractinghashtags and mentions from tweets along
with the count of occurrences of hashtags and mentions.After initial split, we end up
with a map such as: (‘#example’: 1), (‘#example2’:1).
● Second step is to aggregate the count of hashtagsand mentions so we don’t lose any
progress made before (Ex.: if we had (‘#example’:1) stored and we received another
‘#example’, we sum the count to get (‘#example’: 2).

● Third step is to run a hashtag / mention processing function for every rdd in our hashtag /
mention transformed data stream. Process for bothhashtags and mentions is very similar.
We are converting each RDD into rowRDD and into adataframe that consists of two
columns (‘hashtags’, ‘hashtag_count’) using sqlContext.We order our data by hashtag
count and extract only the top 20 values.
``` "𝑠𝑒𝑙𝑒𝑐𝑡 ℎ𝑎𝑠ℎ𝑡𝑎𝑔, ℎ𝑎𝑠ℎ𝑡𝑎𝑔_𝑐𝑜𝑢𝑛𝑡 𝑓𝑟𝑜𝑚 ℎ𝑎𝑠ℎ𝑡𝑎𝑔𝑠 𝑜𝑟𝑑𝑒𝑟 𝑏𝑦 ℎ𝑎𝑠ℎ𝑡𝑎𝑔_𝑐𝑜𝑢𝑛𝑡 𝑑𝑒𝑠𝑐 𝑙𝑖𝑚𝑖𝑡 20" ```
● Last step is to convert columns containing top tenhashtags and their count to the list of
strings, and finally send them to our Flask applicationfor plotting.

**Sentiment Analysis**  
For Sentiment Analysis we need to convert our tweetsinto the DataFrame of the form: (“Tweet”,
“Comp Score”, “Positive Score”, “Neutral Score”, “NegativeScore”).

● First step is to clean our tweets as much as we canusing PySparks built in regular
expressions. We are removing all links, hashtags,user mentions, punctuation marks.
Basically, we are removing everything that is notof alphanumeric value.
● Second step is to perform sentiment analysis on everytweet and store returned values
into the DataFrame.
● Third and last step is to get an average for all thesentiment scores and send them to the
Flask application.

**Flask Application**  
Our Flask Application consists of several endpoints(exactly three endpoints for every type of
analysis that we perform: hashtags, mentions, andsentiment analysis). We are going to give a
description of hashtags endpoint since the other twoare designed in a very similar way.
**Hashtags Endpoints**
``` /ℎ𝑎𝑠ℎ𝑡𝑎𝑔𝑠 𝐺𝐸𝑇 ```  
● Root endpoint for hashtags, renders initial emptygraph for hashtags using javascript
Chart library.
``` /ℎ𝑎𝑠ℎ𝑡𝑎𝑔𝑠/𝑟𝑒𝑓𝑟𝑒𝑠ℎ𝐷𝑎𝑡𝑎 𝐺𝐸𝑇 ```  
● This endpoint is called from within our javascriptcode with an interval of 1 second. If the
call is successful, an updated list of top hashtagsand an updated list of top hashtags count
will be returned as a json back to javascript code.Updated values are then used to update
our chart from javascript code.
``` /ℎ𝑎𝑠ℎ𝑡𝑎𝑔𝑠/𝑢𝑝𝑑𝑎𝑡𝑒𝐷𝑎𝑡𝑎 𝑃𝑂𝑆𝑇 ```  
● Our PySpark application uses this endpoint to sendan updated list of top hashtags and an
updated list of top hashtags count to the Flask application.Returns 200 on success, 400
on error.

**Results and Evaluation**  
We have achieved our goals in being able to continuouslycollect tweets, stream data to the
pyspark application, and visualize results in an appropriateway. The fact that we have separated
functionality of our project into separate applicationsmade it so no individual application is  
overwhelmed with the amount of tasks it has to do. This in turn results in increased efficiency of
each step of our project. Our application can runand keep updating graphs for as long as we
keep receiving tweets.

**Figure 1:** Shows which hashtags are used the most regardingcryptocurrency  

**Figure 2:** Shows the users that are mentioned the most in the context of crypto.  

**Figure 3:** Shows how the sentiment of a cryptocurrencychanges as time progresses (Bitcoin).  

**Future Work**  
To increase the accuracy of the sentiment scores wecould use the tweet tokenizer from NLTK
which is a function that takes care of splitting eachword and emoji in a tweet into an array
consisting of these elements, in which every elementhas a sentiment score. The upside to using
the tweet tokenizer is that it has been trained torecognize the impact of emojis on the sentiment
score whereas the Sentiment Intensity Analyzer libraryuses only text. We believe this would
improve the accuracy of the sentiment scores givenemojis can be a good indicative of a tweet’s
sentiment.

**Scalability Improvements [4]**  
This project has a potential to be scaled to a different level where the user of this project can
have flexibility and choice over which parts of thetweet should be extracted, and what kind of
analysis (using Spark) the user would like to performon the extracted data.
Ideally, there should be an interface that allowsthe user to use his own Twitter credentials and
specify various parameters used for collecting tweets.
Then, collected data should not be sent to Spark foranalysis via TCP socket but rather through
some data pipeline mechanism such asApache Sparkfor a much quicker, scalable, and reliable
data streaming.
One solution of improving the flexibility of dataanalysis can be an introduction of an interactive
console that accepts Spark code from the user. However,most of the users will have no prior
experience with Spark so some pre existing analysisoptions must be available as well. Besides,
queries entered by the user might contain errors orbugs so debugging and logging options
should be introduced as well.
Finally, the user must be able to visualize resultson the website in the form of graphs or samples
of his data after the analysis is performed. The usermust be able to either download batch results
of the analysis or stream results to his desired destination.

** References **  
1. “Simplified Text Processing¶.” _TextBlob_ ,www.textblob.readthedocs.io/en/dev/.
2. Real Python. “Sentiment Analysis: First Steps withPython's Nltk Library.” _Real Python_ ,
    Real Python, 13 Feb. 2021,www.realpython.com/python-nltk-sentiment-analysis/.
3. “Structured Streaming¶.” _Structured Streaming - PySpark3.1.2 Documentation_ ,
    [http://www.spark.apache.org/docs/latest/api/python/reference/pyspark.ss.html](http://www.spark.apache.org/docs/latest/api/python/reference/pyspark.ss.html)
4. Othman, Salem. _Emojiset Mining Research_ ,www.sogoresearch.com/emojiset.
