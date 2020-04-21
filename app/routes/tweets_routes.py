from flask import Blueprint, jsonify, request, render_template , flash, redirect
from app.models import Tweet, parse_records, db

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets.json")
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
    return redirect(f"/tweets")
