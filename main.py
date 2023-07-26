import random
import string
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_urls = {}


def generate_short_url(length=6):
    # Generate a random short URL using a combination of letters and digits
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # If the form is submitted with POST method, retrieve the long URL from the form
        long_url = request.form['long_url']

        # Generate a unique short URL and ensure it doesn't already exist in the dictionary
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        # Add the long URL and its corresponding short URL to the dictionary
        shortened_urls[short_url] = long_url

        # Return the shortened URL to the user
        return f"Shortened URL: {request.url_root}{short_url}"

    # If the request method is GET, render the index.html template
    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    # Retrieve the long URL associated with the given short URL from the dictionary
    long_url = shortened_urls.get(short_url)

    if long_url:
        # If the long URL exists, redirect the user to the original URL
        return redirect(long_url)
    else:
        # If the short URL is not found in the dictionary, return a 404 error
        return "URL NOT FOUND", 404

if __name__ == "__main__":
    # Start the Flask application in debug mode for development
    app.run(debug=True)
