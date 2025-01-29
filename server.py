from bottle import Bottle, static_file, template


app = Bottle()

@app.route('/')
def index():
    context = {
        "title": "Painel de Tendência",
        "items": ["Item 1", "Item 2", "Item 3"]
    }
    return template('templates/index.html', **context)

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
