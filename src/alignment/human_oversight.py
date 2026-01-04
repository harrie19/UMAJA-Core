"""
Human Oversight System - Humans Always in Control

This module ensures humans remain in the loop for critical decisions
and provides emergency controls to stop the system if needed.

"The best AI is one that knows when to ask for help"
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from .constitutional_ai import Action

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Status of human approval request"""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    TIMEOUT = "timeout"
    EMERGENCY_STOP = "emergency_stop"


@dataclass
class ApprovalRequest:
    """Request for human approval"""
    request_id: str
    action: Action
    explanation: str
    risk_analysis: Dict[str, Any]
    timestamp: str
    timeout_seconds: int
    default_decision: str  # 'approve' or 'deny'
    status: ApprovalStatus = ApprovalStatus.PENDING
    decision_time: Optional[str] = None
    approver: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class EmergencyStopState:
    """State of emergency stop system"""
    active: bool
    activated_at: Optional[str]
    activated_by: Optional[str]
    reason: Optional[str]
    systems_stopped: List[str]


class HumanOversightSystem:
    """
    Human Oversight System - Humans Always in Control
    
    Ensures critical decisions require human approval and provides
    emergency stop capability to halt all operations immediately.
    """
    
    def __init__(self):
        self.approval_requests = []
        self.emergency_stop_state = EmergencyStopState(
            active=False,
            activated_at=None,
            activated_by=None,
            reason=None,
            systems_stopped=[]
        )
        self.approval_callbacks: Dict[str, Callable] = {}
        self.high_stakes_thresholds = {
            'spawn_count': 1000,  # Spawning >1000 agents
            'impact_level': ['high', 'critical'],
            'confidence_threshold': 0.6,  # Low confidence on critical
            'modification_targets': ['core_goals', 'constitutional_principles', 'safety_systems']
        }
        
    async def request_approval(
        self,
        action: Action,
        timeout_seconds: int = 86400,  # 24 hours default
        default_decision: str = 'deny'
    ) -> ApprovalRequest:
        """
        Request human approval for an action
        
        Args:
            action: The action requiring approval
            timeout_seconds: How long to wait for approval
            default_decision: What to do if timeout ('approve' or 'deny')
            
        Returns:
            ApprovalRequest with decision
        """
        # Check if emergency stop is active
        if self.emergency_stop_state.active:
            logger.error("EMERGENCY STOP ACTIVE - All approvals denied")
            return ApprovalRequest(
                request_id=f"approval_{time.time()}",
                action=action,
                explanation="EMERGENCY STOP ACTIVE",
                risk_analysis={},
                timestamp=datetime.now(timezone.utc).isoformat(),
                timeout_seconds=0,
                default_decision='deny',
                status=ApprovalStatus.EMERGENCY_STOP
            )
        
        # Check if action requires approval
        if not self.is_high_stakes(action):
            # Low stakes - auto-approve
            return ApprovalRequest(
                request_id=f"approval_{time.time()}",
                action=action,
                explanation="Low stakes action - auto-approved",
                risk_analysis={'stakes': 'low'},
                timestamp=datetime.now(timezone.utc).isoformat(),
                timeout_seconds=0,
                default_decision='approve',
                status=ApprovalStatus.APPROVED,
                decision_time=datetime.now(timezone.utc).isoformat(),
                approver='system'
            )
        
        # High stakes - require human approval
        request_id = f"approval_{time.time()}"
        
        # Generate explanation
        explanation = await self._explain_to_humans(action)
        
        # Analyze risks
        risk_analysis = await self._risk_benefit_analysis(action)
        
        # Create request
        request = ApprovalRequest(
            request_id=request_id,
            action=action,
            explanation=explanation,
            risk_analysis=risk_analysis,
            timestamp=datetime.now(timezone.utc).isoformat(),
            timeout_seconds=timeout_seconds,
            default_decision=default_decision
        )
        
        # Store request
        self.approval_requests.append(request)
        
        # Wait for approval
        decision = await self._wait_for_human_approval(request)
        
        return decision
    
    def is_high_stakes(self, action: Action) -> bool:
        """Determine if action is high stakes requiring approval"""
        
        # Check impact level
        if action.impact_level in self.high_stakes_thresholds['impact_level']:
            return True
        
        # Check spawn count
        if action.action_type == 'spawn':
            spawn_count = action.parameters.get('spawn_count', 0)
            if spawn_count > self.high_stakes_thresholds['spawn_count']:
                return True
        
        # Check modification targets
        if action.action_type == 'modify':
            target = action.parameters.get('modify_target', '')
            if target in self.high_stakes_thresholds['modification_targets']:
                return True
        
        # Check confidence on critical actions
        if action.impact_level == 'critical':
            confidence = action.parameters.get('confidence', 1.0)
            if confidence < self.high_stakes_thresholds['confidence_threshold']:
                return True
        
        return False
    
    async def _explain_to_humans(self, action: Action) -> str:
        """Generate human-friendly explanation of action"""
        explanation_parts = [
            f"🚨 High-Stakes Decision Requires Your Approval\n\n",
            f"Action: {action.action_type.upper()}\n",
            f"Description: {action.description}\n",
            f"Agent: {action.agent_id}\n",
            f"Impact Level: {action.impact_level.upper()}\n\n"
        ]
        
        # Add specific details based on action type
        if action.action_type == 'spawn':
            spawn_count = action.parameters.get('spawn_count', 0)
            explanation_parts.append(
                f"This will create {spawn_count:,} new agents.\n"
            )
        elif action.action_type == 'modify':
            target = action.parameters.get('modify_target', 'unknown')
            explanation_parts.append(
                f"This will modify: {target}\n"
            )
        
        explanation_parts.append(
            f"\nPlease review carefully before approving."
        )
        
        return ''.join(explanation_parts)
    
    async def _risk_benefit_analysis(self, action: Action) -> Dict[str, Any]:
        """Analyze risks and benefits of action"""
        
        risks = []
        benefits = []
        
        # Analyze by action type
        if action.action_type == 'spawn':
            spawn_count = action.parameters.get('spawn_count', 0)
            risks.append(f"Creating {spawn_count} new agents increases complexity")
            risks.append("Potential for emergent misalignment")
            benefits.append("Increased computational capacity")
            benefits.append("Ability to handle more tasks in parallel")
            
        elif action.action_type == 'modify':
            target = action.parameters.get('modify_target', '')
            risks.append(f"Modifying {target} could have system-wide effects")
            risks.append("Potential for unintended consequences")
            benefits.append("Improved system capabilities")
            
        elif action.action_type == 'research':
            risks.append("Research may discover sensitive information")
            risks.append("Results may have ethical implications")
            benefits.append("Advancement of knowledge")
            benefits.append("Potential breakthrough discoveries")
        
        # Overall risk level
        risk_level = "HIGH" if action.impact_level in ['high', 'critical'] else "MEDIUM"
        
        return {
            'risk_level': risk_level,
            'risks': risks,
            'benefits': benefits,
            'recommendation': 'Careful review recommended' if risk_level == "HIGH" else 'Standard review'
        }
    
    async def _wait_for_human_approval(
        self,
        request: ApprovalRequest
    ) -> ApprovalRequest:
        """Wait for human to approve or deny request"""
        
        logger.info(
            f"Waiting for human approval: {request.request_id}\n"
            f"{request.explanation}\n"
            f"Timeout: {request.timeout_seconds}s\n"
            f"Default: {request.default_decision}"
        )
        
        # In production, this would:
        # 1. Send notification to human overseers
        # 2. Display in dashboard
        # 3. Send email/SMS alerts
        # 4. Wait for response via API or UI
        
        # For now, simulate waiting (in real system, would poll for decision)
        start_time = time.time()
        check_interval = 1  # Check every second
        
        while time.time() - start_time < request.timeout_seconds:
            # Check if decision was made
            if request.status != ApprovalStatus.PENDING:
                return request
            
            # Check if emergency stop activated
            if self.emergency_stop_state.active:
                request.status = ApprovalStatus.EMERGENCY_STOP
                request.decision_time = datetime.now(timezone.utc).isoformat()
                return request
            
            # Check callbacks
            if request.request_id in self.approval_callbacks:
                callback = self.approval_callbacks[request.request_id]
                result = callback(request)
                if result:
                    request.status = ApprovalStatus.APPROVED if result['approved'] else ApprovalStatus.DENIED
                    request.decision_time = datetime.now(timezone.utc).isoformat()
                    request.approver = result.get('approver', 'unknown')
                    request.reason = result.get('reason', '')
                    return request
            
            await asyncio.sleep(check_interval)
        
        # Timeout reached
        logger.warning(f"Approval timeout for {request.request_id}")
        request.status = ApprovalStatus.TIMEOUT
        request.decision_time = datetime.now(timezone.utc).isoformat()
        
        # Apply default decision
        if request.default_decision == 'approve':
            request.status = ApprovalStatus.APPROVED
            logger.warning(f"Timeout - defaulting to APPROVED")
        else:
            request.status = ApprovalStatus.DENIED
            logger.info(f"Timeout - defaulting to DENIED (safe default)")
        
        return request
    
    def approve_request(
        self,
        request_id: str,
        approver: str,
        reason: str = ""
    ) -> bool:
        """Manually approve a request"""
        for request in self.approval_requests:
            if request.request_id == request_id and request.status == ApprovalStatus.PENDING:
                request.status = ApprovalStatus.APPROVED
                request.decision_time = datetime.now(timezone.utc).isoformat()
                request.approver = approver
                request.reason = reason
                logger.info(f"Request {request_id} approved by {approver}")
                return True
        return False
    
    def deny_request(
        self,
        request_id: str,
        approver: str,
        reason: str
    ) -> bool:
        """Manually deny a request"""
        for request in self.approval_requests:
            if request.request_id == request_id and request.status == ApprovalStatus.PENDING:
                request.status = ApprovalStatus.DENIED
                request.decision_time = datetime.now(timezone.utc).isoformat()
                request.approver = approver
                request.reason = reason
                logger.info(f"Request {request_id} denied by {approver}: {reason}")
                return True
        return False
    
    def emergency_stop(self, activated_by: str, reason: str):
        """
        EMERGENCY STOP - Stops everything immediately
        
        This is the "nuclear button" that halts all UMAJA operations.
        """
        logger.critical("🚨🚨🚨 EMERGENCY STOP ACTIVATED 🚨🚨🚨")
        logger.critical(f"Activated by: {activated_by}")
        logger.critical(f"Reason: {reason}")
        
        # Update state
        self.emergency_stop_state.active = True
        self.emergency_stop_state.activated_at = datetime.now(timezone.utc).isoformat()
        self.emergency_stop_state.activated_by = activated_by
        self.emergency_stop_state.reason = reason
        
        # Stop all systems
        systems_to_stop = [
            'agent_spawning',
            'autonomous_research',
            'self_modification',
            'new_capabilities',
            'external_communications'
        ]
        
        for system in systems_to_stop:
            self._stop_system(system)
            self.emergency_stop_state.systems_stopped.append(system)
        
        # Deny all pending approvals
        for request in self.approval_requests:
            if request.status == ApprovalStatus.PENDING:
                request.status = ApprovalStatus.EMERGENCY_STOP
                request.decision_time = datetime.now(timezone.utc).isoformat()
        
        # Log system state
        self._log_system_state()
        
        # Notify all overseers
        self._notify_all_overseers()
        
        logger.critical("All systems stopped. Awaiting human investigation.")
    
    def _stop_system(self, system_name: str):
        """Stop a specific system"""
        logger.critical(f"Stopping system: {system_name}")
        # In production, this would send stop signals to actual systems
    
    def _log_system_state(self):
        """Log complete system state for investigation"""
        state = {
            'emergency_stop': asdict(self.emergency_stop_state),
            'pending_approvals': len([r for r in self.approval_requests if r.status == ApprovalStatus.PENDING]),
            'total_approvals': len(self.approval_requests),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        logger.critical(f"System state logged: {state}")
    
    def _notify_all_overseers(self):
        """Notify all human overseers of emergency stop"""
        logger.critical("NOTIFYING ALL HUMAN OVERSEERS")
        # In production: send emails, SMS, push notifications, etc.
    
    def clear_emergency_stop(self, cleared_by: str, reason: str) -> bool:
        """Clear emergency stop and resume operations"""
        if not self.emergency_stop_state.active:
            return False
        
        logger.warning(f"Emergency stop cleared by {cleared_by}: {reason}")
        
        self.emergency_stop_state.active = False
        self.emergency_stop_state.systems_stopped.clear()
        
        logger.info("Systems ready to resume. Manual restart required for safety.")
        return True
    
    def get_pending_approvals(self) -> List[ApprovalRequest]:
        """Get all pending approval requests"""
        return [r for r in self.approval_requests if r.status == ApprovalStatus.PENDING]
    
    def get_approval_history(self, limit: int = 100) -> List[ApprovalRequest]:
        """Get recent approval history"""
        return self.approval_requests[-limit:]
    
    def get_oversight_metrics(self) -> Dict[str, Any]:
        """Get human oversight metrics"""
        total = len(self.approval_requests)
        
        if total == 0:
            return {
                'total_requests': 0,
                'pending': 0,
                'approved': 0,
                'denied': 0,
                'timeout': 0,
                'emergency_stops': 0,
                'approval_rate': 0.0,
                'emergency_stop_active': self.emergency_stop_state.active
            }
        
        status_counts = {
            'pending': 0,
            'approved': 0,
            'denied': 0,
            'timeout': 0,
            'emergency_stop': 0
        }
        
        for request in self.approval_requests:
            status_counts[request.status.value] += 1
        
        return {
            'total_requests': total,
            'pending': status_counts['pending'],
            'approved': status_counts['approved'],
            'denied': status_counts['denied'],
            'timeout': status_counts['timeout'],
            'emergency_stops': status_counts['emergency_stop'],
            'approval_rate': status_counts['approved'] / total,
            'denial_rate': status_counts['denied'] / total,
            'emergency_stop_active': self.emergency_stop_state.active
        }
