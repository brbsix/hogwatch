from bottle import (
    Bottle,
    route,
    run,
    template,
    static_file,
    redirect,
    debug,
    request,
    abort
)

from Queue import Queue
from pprint import pprint

def web_service(
        report_queue=Queue(),
        host='0.0.0.0',
        port=8080,
        debugMode=True,
        reloader=True,
        ws=True
    ):
    app=Bottle()

    #static routes
    @app.route('/')
    def home():
        redirect('/index.html')

    @app.route('/<filename:path>')
    def send_static(filename):
        return static_file(
            filename,
            root='/home/akshay/Documents/hogwatch/application/static/'
        )

        ## ^^ have to use full path for static folder. relative one will
        ## not work with run.py -- NEED TO FIX 


    if ws:
        @app.route('/websocket')
        def handle_websocket():
            wsock = request.environ.get('wsgi.websocket')
            if not wsock:
                abort(400, 'Expected WebSocket request.')

            while True:
                try:
                    report=report_queue.get()
                    pprint(report)
                    #message = wsock.receive()
                    wsock.send("Your message was: %r" % message)
                except WebSocketError:
                    break


        from gevent.pywsgi import WSGIServer
        from geventwebsocket import WebSocketError
        from geventwebsocket.handler import WebSocketHandler
        server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        server.serve_forever()
    else:
        port=str(port)
        app.run(host=host, port=port, debug=debugMode, reloader=reloader)



if __name__ == '__main__':
    web_service()