from flask import Blueprint, jsonify, request, render_template , flash, redirect
from app.models import User, Tweet, parse_records, db
from app.services.twitter_service import twitter_api
from app.services.basilica_service import basilica_api_client

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    api = twitter_api()

    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    #print("STATUSES COUNT:", len(statuses))
    #return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    #return "OK"
    #breakpoint()

    basilica_api = basilica_api_client()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    #print("NUMBER OF EMBEDDINGS", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        #print(status.full_text)
        #print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        embedding = embeddings[counter]
        #print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()
    #breakpoint()
    return "OK"

"""@tweet_routes.route("/tweets.json")
def list_tweets():
    #tweets = [
    #    {"id": 1, "title": "Book 1"},
    #    {"id": 2, "title": "Book 2"},
    #    {"id": 3, "title": "Book 3"},
    #]
    tweet_records = Tweet.query.all()
    print(tweet_records)
    tweets = parsed_records(tweet_records)
    return jsonify(tweets)
@tweet_routes.route("/tweets")
def list_tweets_for_humans():
    #tweets = [
    #    {"id": 1, "title": "Book 1"},
    #    {"id": 2, "title": "Book 2"},
    #    {"id": 3, "title": "Book 3"},
    #]
    #return render_template("tweets.html", message="Here's some tweets", tweets=tweets)
    tweet_records = Tweet.query.all()
    print(tweet_records)
    return render_template("tweets.html", message="Here's some tweets", tweets=tweet_records)
@tweet_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")
@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))
    # todo: store in database
    new_tweet = Tweet(text=request.form["tweet_text"], author_id=request.form["tweeter"])
    db.session.add(new_tweet)
    db.session.commit()
    #return jsonify({
    #    "message": "TWEET CREATED OK (TODO)",
    #    "tweet": dict(request.form)
    #})
    flash(f"Tweet '{new_tweet.text}' created successfully!", "success")
    return redirect(f"/tweets")"""
