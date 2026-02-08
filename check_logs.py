"""
Script para diagnosticar problemas de logging
"""
import os
import logging
from pathlib import Path
from datetime import datetime

def test_logging():
    print("🔍 DIAGNÓSTICO DE LOGGING")
    print("=" * 50)
    
    # 1. Check logs directory
    logs_dir = Path("logs")
    print(f"1. Directorio logs/: {'✅ EXISTE' if logs_dir.exists() else '❌ NO EXISTE'}")
    
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("   ✅ Creado directorio logs/")
    
    # 2. Test basic logging
    print("\n2. Probando logging básico...")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Este es un mensaje de prueba INFO")
    logging.error("Este es un mensaje de prueba ERROR")
    
    # 3. Check module logging
    print("\n3. Probando logging por módulo...")
    test_logger = logging.getLogger("test_module")
    test_logger.setLevel(logging.DEBUG)
    
    # Add file handler
    fh = logging.FileHandler(f"logs/module_test.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    test_logger.addHandler(fh)
    
    test_logger.debug("Debug message from module")
    test_logger.info("Info message from module")
    
    # 4. List existing log files
    print("\n4. Archivos de log existentes:")
    if logs_dir.exists():
        for file in logs_dir.glob("*.log"):
            size_kb = file.stat().st_size / 1024
            print(f"   📄 {file.name} ({size_kb:.1f} KB)")
    
    # 5. Test actual imports
    print("\n5. Probando importaciones...")
    try:
        from telegram.ext import Application
        print("   ✅ telegram.ext importado correctamente")
    except ImportError as e:
        print(f"   ❌ Error importando telegram.ext: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Diagnóstico completo")
    print(f"📁 Los logs se guardan en: {logs_dir.absolute()}")

if __name__ == "__main__":
    test_logging()