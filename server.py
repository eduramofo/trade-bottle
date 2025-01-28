from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
