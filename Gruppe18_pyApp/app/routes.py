from flask import Flask,  render_template


def configure_routes(app):

    @app.route("/")
    def home_page():
        return "<h1>Home Page</h1>"
        #return render_template("home.html")