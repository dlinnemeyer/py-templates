from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    foo = request.args.get('foo', '')
    return foo + str(request.args)


if __name__ == "__main__":
    app.run()
