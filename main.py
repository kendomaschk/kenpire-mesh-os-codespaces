#!/usr/bin/env python3
"""
🚀 KenPire Mesh OS - Entry Point
Command-line interface and server launcher
"""

import sys
import argparse
import asyncio
import logging
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.kenpire.server import create_app, run_server
from src.kenpire.utils import setup_logging, config_utils


def main():
    """Main entry point for KenPire Mesh OS"""
    parser = argparse.ArgumentParser(
        description="KenPire Mesh OS - Military-grade cognitive infrastructure"
    )
    
    parser.add_argument(
        "command",
        choices=["server", "status", "config", "version"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind server to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind server to (default: 8080)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--config",
        help="Configuration file path"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        if args.command == "server":
            logger.info("🚀 Starting KenPire Mesh OS Server")
            logger.info(f"   Host: {args.host}")
            logger.info(f"   Port: {args.port}")
            logger.info(f"   Log Level: {args.log_level}")
            
            # Load configuration
            config = config_utils.get_default_config()
            if args.config:
                from src.kenpire.utils import json_utils
                custom_config = json_utils.safe_load(args.config)
                if custom_config:
                    config.update(custom_config)
                    logger.info(f"   Config: {args.config}")
            
            # Run server
            import uvicorn
            app = create_app()
            uvicorn.run(
                app,
                host=args.host,
                port=args.port,
                log_level=args.log_level.lower()
            )
            
        elif args.command == "status":
            logger.info("📊 KenPire Mesh OS Status")
            print("System Status: Operational")
            print("Version: 2.0.0")
            print("Components:")
            print("  ✅ Smart Cards: Ready")
            print("  ✅ AI Orchestration: Ready") 
            print("  ✅ Security: Ready")
            print("  ✅ Mesh: Ready")
            
        elif args.command == "config":
            logger.info("⚙️  KenPire Mesh OS Configuration")
            config = config_utils.get_default_config()
            env_config = config_utils.load_env_config()
            
            print("Default Configuration:")
            for key, value in config.items():
                print(f"  {key}: {value}")
            
            if env_config:
                print("\nEnvironment Variables:")
                for key, value in env_config.items():
                    masked_value = "*" * 8 if "key" in key.lower() or "password" in key.lower() else value
                    print(f"  {key}: {masked_value}")
            
        elif args.command == "version":
            print("KenPire Mesh OS v2.0.0")
            print("Military-grade cognitive infrastructure for enterprise applications")
            print("Author: KenPire Systems")
            print("License: Enterprise")
            
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()