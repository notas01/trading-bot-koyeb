"""
Servidor web para health checks de Koyeb
"""
from flask import Flask, jsonify
import threading
import os
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado del bot
bot_status = {
    "status": "initializing",
    "uptime": 0,
    "commands_processed": 0,
    "users_active": 0
}

@app.route('/')
def home():
    """Página principal"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Trading Bot</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                text-align: center;
                max-width: 600px;
                width: 90%;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .status {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
            .endpoints {
                text-align: left;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 20px;
                margin-top: 30px;
            }
            code {
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: monospace;
            }
            .badge {
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                margin: 5px;
            }
            .online { background: #10B981; }
            .offline { background: #EF4444; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Trading Bot</h1>
            <p>Bot de trading automatizado para Telegram</p>
            
            <div class="status">
                <h3>Estado del Sistema</h3>
                <p><strong>Status:</strong> 
                    <span class="badge online">🟢 EN LINEA</span>
                </p>
                <p><strong>Tiempo activo:</strong> {{ uptime }} segundos</p>
                <p><strong>Comandos procesados:</strong> {{ commands }}</p>
                <p><strong>Usuarios activos:</strong> {{ users }}</p>
            </div>
            
            <div class="endpoints">
                <h4>Endpoints disponibles:</h4>
                <ul>
                    <li><code>GET /</code> - Esta página</li>
                    <li><code>GET /health</code> - Health check para Koyeb</li>
                    <li><code>GET /status</code> - Estado detallado del bot</li>
                    <li><code>GET /metrics</code> - Métricas del sistema</li>
                </ul>
            </div>
            
            <div style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                <p>🚀 Desplegado en Koyeb | 📊 40+ comandos disponibles</p>
            </div>
        </div>
    </body>
    </html>
    """.replace(
        "{{ uptime }}", str(bot_status["uptime"])
    ).replace(
        "{{ commands }}", str(bot_status["commands_processed"])
    ).replace(
        "{{ users }}", str(bot_status["users_active"])
    )

@app.route('/health')
def health():
    """Endpoint de health check para Koyeb"""
    if bot_status["status"] == "running":
        return jsonify({"status": "healthy"}), 200
    else:
        return jsonify({"status": "unhealthy"}), 503

@app.route('/status')
def status():
    """Endpoint de estado detallado"""
    return jsonify(bot_status)

@app.route('/metrics')
def metrics():
    """Métricas del sistema"""
    import psutil
    import time
    
    metrics = {
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "bot_status": bot_status
    }
    return jsonify(metrics)

def update_status(status, commands=0, users=0):
    """Actualizar estado del bot"""
    import time
    bot_status["status"] = status
    if commands:
        bot_status["commands_processed"] = commands
    if users:
        bot_status["users_active"] = users
    bot_status["uptime"] = int(time.time() - start_time)

def run_web_server():
    """Ejecutar servidor web en segundo plano"""
    app.run(host='0.0.0.0', port=8080, debug=False)

# Tiempo de inicio
import time
start_time = time.time()

# Iniciar servidor web en segundo plano
web_thread = threading.Thread(target=run_web_server, daemon=True)
web_thread.start()
logger.info("🌐 Servidor web iniciado en puerto 8080")