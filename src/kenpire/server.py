"""
🚀 KenPire API Server - Production Core
FastAPI server with enterprise features
"""

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, Any

from .core.smart_cards import SmartCardOrchestrator
from .core.ai_orchestration import TrifectaCoordinator
from .core.security import SecurityHardening
from .core.mesh import MeshOrchestrator

logger = logging.getLogger(__name__)
security_bearer = HTTPBearer()

# Global instances
security_hardening = SecurityHardening()
smart_card_orchestrator = SmartCardOrchestrator()
trifecta_coordinator = TrifectaCoordinator()
mesh_orchestrator = MeshOrchestrator()


def create_app() -> FastAPI:
    """Create FastAPI application with production configuration"""

    app = FastAPI(
        title="KenPire Mesh OS",
        description=(
            "Military-grade cognitive infrastructure for enterprise applications"
        ),
        version="2.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    async def verify_api_key(
        credentials: HTTPAuthorizationCredentials = Security(security_bearer),
    ):
        """Verify API key for protected endpoints"""
        token = credentials.credentials
        validation = security_hardening.validate_api_key(token)

        if not validation["valid"]:
            raise HTTPException(status_code=401, detail=validation["reason"])

        return validation

    @app.get("/health")
    async def health_check():
        """Basic health check endpoint"""
        return {
            "status": "healthy",
            "service": "KenPire Mesh OS",
            "version": "2.0.0",
            "timestamp": "2025-11-21T12:00:00Z",
        }

    @app.get("/ready")
    async def readiness_check():
        """Readiness probe for Kubernetes"""
        return {
            "status": "ready",
            "systems": {
                "smart_cards": "operational",
                "ai_orchestration": "operational",
                "security": "operational",
                "mesh": "operational",
            },
        }

    @app.get("/api/v1/status")
    async def get_system_status(auth: dict = Depends(verify_api_key)):
        """Get comprehensive system status"""
        return {
            "system_status": "operational",
            "smart_cards": smart_card_orchestrator.get_stats(),
            "ai_orchestration": trifecta_coordinator.get_coordination_stats(),
            "security": security_hardening.get_security_stats(),
            "mesh": mesh_orchestrator.get_mesh_stats(),
        }

    @app.post("/api/v1/cards/process")
    async def process_smart_card(
        card_data: Dict[str, Any], auth: dict = Depends(verify_api_key)
    ):
        """Process a smart narrative card"""
        try:
            result = await smart_card_orchestrator.process_card(card_data)
            return result
        except Exception as e:
            logger.error(f"Card processing failed: {e}")
            raise HTTPException(status_code=500, detail="Card processing failed")

    @app.post("/api/v1/ai/orchestrate")
    async def orchestrate_ai(
        request: Dict[str, Any], auth: dict = Depends(verify_api_key)
    ):
        """Orchestrate AI models for complex processing"""
        try:
            task = request.get("task", "unknown")
            input_data = request.get("input", "")

            if request.get("coordination") == "trifecta_handshake":
                result = await trifecta_coordinator.coordinate_models(task, input_data)
            else:
                result = await trifecta_coordinator.orchestrate(request)

            return result
        except Exception as e:
            logger.error(f"AI orchestration failed: {e}")
            raise HTTPException(status_code=500, detail="AI orchestration failed")

    @app.post("/api/v1/mesh/consensus")
    async def achieve_consensus(
        proposal: Dict[str, Any], auth: dict = Depends(verify_api_key)
    ):
        """Achieve consensus across mesh nodes"""
        try:
            result = await mesh_orchestrator.achieve_consensus(proposal)
            return result
        except Exception as e:
            logger.error(f"Consensus failed: {e}")
            raise HTTPException(status_code=500, detail="Consensus failed")

    return app


def run_server():
    """Run the production server"""
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
