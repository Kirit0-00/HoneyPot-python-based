import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

@dataclass
class ConnectionEvent:
    timestamp: str
    ip: str
    port: int
    data: str
    enriched_data: Dict[str, Any] = field(default_factory=dict)
    protocol: str = "TCP"
    reputation_score: Optional[int] = None
    severity: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "ip": self.ip,
            "port": self.port,
            "data": self.data,
            "enriched_data": self.enriched_data
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConnectionEvent':
        return cls(**data)

@dataclass(frozen=True)
class Report:
    generated_at: str
    total_events: int
    top_attackers: Dict[str, int]
    targeted_ports: Dict[int, int]
    high_severity_ips: List[str] = field(default_factory=list)
