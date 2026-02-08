from flask import Flask, jsonify
import os
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.getenv('PORT', 8080))

@app.route('/')
def index():
    """Página principal"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Bot</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .status { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🤖 Trading Bot</h1>
        <p class="status">✅ Servidor funcionando correctamente</p>
        <p>Puerto: {PORT}</p>
        <p><a href="/health">Ver estado de salud</a></p>
    </body>
    </html>
    '''.format(PORT=PORT)

@app.route('/health')
def health():
    """Endpoint de health check para Koyeb"""
    return jsonify({
        'status': 'healthy',
        'service': 'trading-bot',
        'version': '1.0.0'
    })

@app.route('/status')
def status():
    """Endpoint de estado"""
    return jsonify({
        'telegram': 'connected',
        'web_server': 'running',
        'port': PORT
    })

if __name__ == '__main__':
    logger.info(f"🚀 Iniciando servidor web en puerto {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
