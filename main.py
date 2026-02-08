import os
import time
import logging
from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import NetworkError, TelegramError

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PORT = int(os.getenv('PORT', 8080))

# Configuración de timeouts para Telegram
REQUEST_KWARGS = {
    'read_timeout': 30,
    'connect_timeout': 30,
    'pool_timeout': 30
}

def start(update, context):
    """Maneja el comando /start"""
    update.message.reply_text('¡Hola! Soy tu bot de trading.')

def handle_message(update, context):
    """Maneja mensajes de texto"""
    text = update.message.text
    update.message.reply_text(f'Recibí: {text}')

def start_bot_with_retry():
    """Inicia el bot con reintentos automáticos"""
    max_retries = 5
    wait_time = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"🤖 Intentando conectar con Telegram (intento {attempt + 1}/{max_retries})...")
            
            # Crear updater con timeouts configurados
            updater = Updater(
                token=TELEGRAM_TOKEN, 
                use_context=True,
                request_kwargs=REQUEST_KWARGS
            )
            
            # Configurar handlers
            dp = updater.dispatcher
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
            
            # Iniciar polling
            updater.start_polling(
                drop_pending_updates=True,
                timeout=30,
                poll_interval=0.5
            )
            
            logger.info("✅ Bot de Telegram iniciado correctamente")
            return updater
            
        except NetworkError as e:
            logger.warning(f"⚠️ Error de red: {e}")
            if attempt < max_retries - 1:
                logger.info(f"⏱️ Esperando {wait_time} segundos antes de reintentar...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
            else:
                logger.error(f"❌ Fallo después de {max_retries} intentos: {e}")
                raise e
        except TelegramError as e:
            logger.error(f"❌ Error de Telegram: {e}")
            raise e
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            raise e
    
    return None

@app.route('/')
def home():
    """Endpoint principal para health checks"""
    return '✅ Trading Bot está funcionando'

@app.route('/health')
def health():
    """Endpoint de health check"""
    return {'status': 'healthy', 'service': 'trading-bot'}

def run_web_server():
    """Inicia el servidor web Flask"""
    logger.info(f"🌐 Iniciando servidor web en puerto {PORT}")
    app.run(host='0.0.0.0', port=PORT)

def main():
    """Función principal"""
    logger.info("==================================================")
    logger.info("🤖 INICIANDO TRADING BOT")
    logger.info("==================================================")
    
    # Verificar token
    if not TELEGRAM_TOKEN:
        logger.error("❌ Token de Telegram no encontrado")
        return
    
    logger.info(f"✅ Token encontrado: {TELEGRAM_TOKEN[:10]}...")
    
    # 1. Iniciar servidor web
    logger.info("\n1. 🔧 Iniciando servidor web...")
    # El servidor web se inicia en un thread o proceso separado
    # Para Koyeb, Flask se ejecuta en el mismo proceso
    
    # 2. Conectar con Telegram
    logger.info("\n2. 🤖 Conectando con Telegram...")
    logger.info("   (Esto puede tomar algunos segundos)")
    
    try:
        updater = start_bot_with_retry()
        
        if updater:
            logger.info("\n" + "="*50)
            logger.info("✅ BOT INICIADO CORRECTAMENTE")
            logger.info("="*50)
            logger.info(f"🌐 Web: http://0.0.0.0:{PORT}")
            logger.info("🤖 Telegram: Conectado")
            logger.info("🚀 Koyeb: Listo")
            logger.info("="*50)
            
            # Mantener el bot ejecutándose
            updater.idle()
        else:
            logger.error("❌ No se pudo iniciar el bot después de múltiples intentos")
            
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        raise

if __name__ == '__main__':
    # Para Koyeb, necesitamos iniciar Flask y el bot juntos
    import threading
    
    # Iniciar servidor web en un thread separado
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Esperar un momento para que el servidor web inicie
    time.sleep(2)
    
    # Iniciar el bot principal
    main()
