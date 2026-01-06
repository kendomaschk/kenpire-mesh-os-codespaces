"""
🛡️ Security Hardening - Production Core
Military-grade security with enterprise features
"""

import secrets
import hashlib
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SecurityHardening:
    """
    Production security hardening implementation
    Military-grade protocols with enterprise monitoring
    """

    def __init__(self):
        self.api_keys = {}
        self.rate_limits = {}
        self.security_events = []
        self.encryption_key = self._generate_master_key()

    def _generate_master_key(self) -> bytes:
        """Generate master encryption key"""
        return secrets.token_bytes(32)

    def generate_api_key(self, user_id: str, permissions: list = None) -> str:
        """Generate secure API key with permissions"""
        if permissions is None:
            permissions = ["basic_access"]

        api_key = f"kp_{secrets.token_urlsafe(32)}"

        key_data = {
            "user_id": user_id,
            "permissions": permissions,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=90)).isoformat(),
            "last_used": None,
            "usage_count": 0,
        }

        self.api_keys[api_key] = key_data

        self._log_security_event(
            "api_key_generated",
            {
                "user_id": user_id,
                "key_prefix": api_key[:15] + "...",
                "permissions": permissions,
            },
        )

        logger.info(f"Generated API key for user: {user_id}")
        return api_key

    def validate_api_key(
        self, api_key: str, required_permission: str = None
    ) -> Dict[str, Any]:
        """Validate API key and check permissions"""
        if api_key not in self.api_keys:
            self._log_security_event(
                "invalid_api_key", {"key_prefix": api_key[:15] + "..."}
            )
            return {"valid": False, "reason": "Invalid API key"}

        key_data = self.api_keys[api_key]

        # Check expiration
        expires_at = datetime.fromisoformat(key_data["expires_at"])
        if datetime.now() > expires_at:
            self._log_security_event(
                "expired_api_key", {"user_id": key_data["user_id"]}
            )
            return {"valid": False, "reason": "API key expired"}

        # Check permission
        if required_permission and required_permission not in key_data["permissions"]:
            self._log_security_event(
                "insufficient_permissions",
                {
                    "user_id": key_data["user_id"],
                    "required": required_permission,
                    "available": key_data["permissions"],
                },
            )
            return {
                "valid": False,
                "reason": f"Missing permission: {required_permission}",
            }

        # Update usage statistics
        key_data["last_used"] = datetime.now().isoformat()
        key_data["usage_count"] += 1

        return {
            "valid": True,
            "user_id": key_data["user_id"],
            "permissions": key_data["permissions"],
        }

    def apply_rate_limiting(
        self, identifier: str, limit: int = 100, window: int = 3600
    ) -> bool:
        """Apply rate limiting with sliding window"""
        now = time.time()
        window_start = now - window

        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []

        # Remove old entries
        self.rate_limits[identifier] = [
            timestamp
            for timestamp in self.rate_limits[identifier]
            if timestamp > window_start
        ]

        # Check limit
        if len(self.rate_limits[identifier]) >= limit:
            self._log_security_event(
                "rate_limit_exceeded",
                {"identifier": identifier, "limit": limit, "window": window},
            )
            logger.warning(f"Rate limit exceeded for: {identifier}")
            return False

        # Add current request
        self.rate_limits[identifier].append(now)
        return True

    def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events for monitoring"""
        event = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "details": details,
        }

        self.security_events.append(event)

        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]

    def get_security_headers(self) -> Dict[str, str]:
        """Generate production security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
            "X-KenPire-Security": "hardened",
        }

    def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics"""
        return {
            "api_keys_active": len(self.api_keys),
            "rate_limited_identifiers": len(
                [k for k, v in self.rate_limits.items() if v]
            ),
            "security_events_count": len(self.security_events),
            "recent_events": self.security_events[-10:] if self.security_events else [],
            "timestamp": datetime.now().isoformat(),
        }


class ProofLock:
    """
    ProofLock cryptographic validation system
    Production-ready proof-of-work with integrity verification
    """

    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.target = "0" * difficulty

    def generate_proof(self, data: Any) -> Dict[str, Any]:
        """Generate ProofLock proof for data integrity"""
        start_time = time.time()

        # Convert data to string for hashing
        if isinstance(data, dict):
            data_string = str(sorted(data.items()))
        else:
            data_string = str(data)

        nonce = 0
        while True:
            # Create hash with nonce
            hash_input = f"{data_string}{nonce}".encode()
            hash_result = hashlib.sha256(hash_input).hexdigest()

            # Check if hash meets difficulty requirement
            if hash_result.startswith(self.target):
                end_time = time.time()

                proof = {
                    "data_hash": hashlib.sha256(data_string.encode()).hexdigest(),
                    "nonce": nonce,
                    "proof_hash": hash_result,
                    "difficulty": self.difficulty,
                    "mining_time": round(end_time - start_time, 3),
                    "timestamp": datetime.now().isoformat(),
                }

                logger.info(
                    f"ProofLock generated: nonce={nonce}, time={proof['mining_time']}s"
                )
                return proof

            nonce += 1

            # Prevent infinite loops
            if nonce > 1000000:
                raise Exception("ProofLock mining timeout")

    def verify_proof(self, data: Any, proof: Dict[str, Any]) -> bool:
        """Verify ProofLock proof"""
        try:
            # Reconstruct data string
            if isinstance(data, dict):
                data_string = str(sorted(data.items()))
            else:
                data_string = str(data)

            # Verify data hash
            expected_data_hash = hashlib.sha256(data_string.encode()).hexdigest()
            if expected_data_hash != proof["data_hash"]:
                return False

            # Verify proof hash
            hash_input = f"{data_string}{proof['nonce']}".encode()
            expected_proof_hash = hashlib.sha256(hash_input).hexdigest()

            if expected_proof_hash != proof["proof_hash"]:
                return False

            # Verify difficulty
            target = "0" * proof["difficulty"]
            if not proof["proof_hash"].startswith(target):
                return False

            logger.info(
                f"ProofLock verified successfully: {proof['proof_hash'][:16]}..."
            )
            return True

        except Exception as e:
            logger.error(f"ProofLock verification failed: {e}")
            return False
