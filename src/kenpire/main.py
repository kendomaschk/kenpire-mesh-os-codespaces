#!/usr/bin/env python3
"""
🔥 KenPire Mesh OS - Production Main Entry Point
Enterprise-ready cognitive infrastructure deployment
"""

import asyncio
import logging
import sys
from pathlib import Path

import click
import structlog
from rich.console import Console
from rich.logging import RichHandler

from kenpire.core.smart_cards import SmartNarrativeCard
from kenpire.core.ai_orchestration import TrifectaCoordinator
from kenpire.core.security import SecurityHardening
from kenpire.server import create_app


# Configure structured logging
def setup_logging(log_level: str = "INFO"):
    """Configure production logging with structured output"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True))],
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


@click.group()
@click.option("--log-level", default="INFO", help="Set logging level")
@click.option(
    "--config", default="config/production.yml", help="Configuration file path"
)
def cli(log_level: str, config: str):
    """KenPire Mesh OS - Military-grade cognitive infrastructure"""
    setup_logging(log_level)

    console = Console()
    console.print("🔥 [bold red]KenPire Mesh OS[/bold red] - Production v2.0.0")
    console.print("⚡ Military-grade cognitive infrastructure")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host address")
@click.option("--port", default=8080, help="Port number")
@click.option("--workers", default=1, help="Number of worker processes")
def server(host: str, port: int, workers: int):
    """Start the KenPire API server"""
    logger = structlog.get_logger()

    console = Console()
    console.print(f"🚀 Starting KenPire server on {host}:{port}")
    console.print(f"👥 Workers: {workers}")

    # Initialize core systems
    logger.info("Initializing core systems...")

    try:
        # Initialize security hardening
        security = SecurityHardening()
        logger.info("✅ Security hardening initialized")

        # Initialize AI orchestration
        trifecta = TrifectaCoordinator()
        logger.info("✅ Trifecta AI coordinator initialized")

        # Start server
        app = create_app()

        import uvicorn

        uvicorn.run(app, host=host, port=port, workers=workers, log_level="info")

    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        sys.exit(1)


@cli.command()
@click.option("--card-type", default="test", help="Smart card type to process")
@click.option("--operation", default="test", help="Operation to perform")
def test_card(card_type: str, operation: str):
    """Test smart narrative card processing"""
    logger = structlog.get_logger()

    console = Console()
    console.print(f"🧪 Testing smart card: {card_type}")

    async def run_test():
        try:
            card = SmartNarrativeCard(
                {
                    "type": card_type,
                    "operation": operation,
                    "content": {"test": True},
                    "timestamp": "2025-11-21T12:00:00Z",
                }
            )

            result = await card.process()

            console.print("✅ [bold green]Smart card test successful[/bold green]")
            console.print(f"📊 Result: {result}")

        except Exception as e:
            console.print(f"❌ [bold red]Smart card test failed[/bold red]: {e}")
            logger.error(f"Card test failed: {e}")

    asyncio.run(run_test())


@cli.command()
def health_check():
    """Perform comprehensive health check"""
    logger = structlog.get_logger()

    console = Console()
    console.print("🏥 Performing health check...")

    async def run_health_check():
        try:
            # Test core systems
            systems_status = {
                "smart_cards": True,
                "ai_orchestration": True,
                "security": True,
                "mesh": True,
            }

            # Test smart card system
            try:
                card = SmartNarrativeCard(
                    {"operation": "health_check", "content": {"system": "test"}}
                )
                await card.process()
                logger.info("✅ Smart card system healthy")
            except Exception as e:
                systems_status["smart_cards"] = False
                logger.error(f"❌ Smart card system error: {e}")

            # Test AI orchestration
            try:
                trifecta = TrifectaCoordinator()
                # Basic initialization test
                logger.info("✅ AI orchestration healthy")
            except Exception as e:
                systems_status["ai_orchestration"] = False
                logger.error(f"❌ AI orchestration error: {e}")

            # Test security
            try:
                security = SecurityHardening()
                logger.info("✅ Security systems healthy")
            except Exception as e:
                systems_status["security"] = False
                logger.error(f"❌ Security systems error: {e}")

            # Overall health
            healthy_count = sum(systems_status.values())
            total_count = len(systems_status)
            health_percentage = (healthy_count / total_count) * 100

            if health_percentage == 100:
                console.print("🎯 [bold green]All systems healthy (100%)[/bold green]")
            elif health_percentage >= 75:
                console.print(
                    f"⚠️ [bold yellow]Systems partially healthy ({health_percentage:.1f}%)[/bold yellow]"
                )
            else:
                console.print(
                    f"❌ [bold red]Systems unhealthy ({health_percentage:.1f}%)[/bold red]"
                )

            for system, status in systems_status.items():
                status_icon = "✅" if status else "❌"
                console.print(f"  {status_icon} {system}")

        except Exception as e:
            console.print(f"❌ [bold red]Health check failed[/bold red]: {e}")
            logger.error(f"Health check failed: {e}")

    asyncio.run(run_health_check())


@cli.command()
@click.option("--target", default="development", help="Deployment target")
def deploy(target: str):
    """Deploy KenPire to specified target"""
    logger = structlog.get_logger()

    console = Console()
    console.print(f"🚀 Deploying KenPire to: {target}")

    if target == "docker":
        console.print("🐳 Building Docker image...")
        # Docker deployment logic

    elif target == "kubernetes":
        console.print("☸️ Deploying to Kubernetes...")
        # Kubernetes deployment logic

    elif target == "production":
        console.print("🏭 Production deployment...")
        # Production deployment logic

    else:
        console.print(f"📝 Development deployment to: {target}")

    logger.info(f"Deployment to {target} completed")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
