from flask import Flask, request

app = Flask(__name__)

@app.route('/')
    def homepage():
        """
        Defines a basic homepage for the website
        """
        with open("./homepage.html") as f:
            homepage_local = f.read()
        return homepage_local

if __name__ == "__main__":
    app.run()