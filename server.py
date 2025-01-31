from bottle import Bottle, static_file, template
from app.models import Analysis


app = Bottle()

@app.route('/')
def index():
    context = {
        "title": "Painel de Tendência",
        "analysis_list": Analysis.select().order_by(Analysis.created_on.desc()).limit(5)
    }
    return template('templates/index.html', **context)


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
