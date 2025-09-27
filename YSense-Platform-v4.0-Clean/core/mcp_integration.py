# core/mcp_integration.py
"""
YSense Platform v3.0 MCP (Model Context Protocol) Integration
Enables AI agents to interact with YSense attribution infrastructure
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import hashlib

from src.models import WisdomDrop, User, UsageRecord, get_session
from src.z_protocol_enhanced import ZProtocolValidator

@dataclass
class MCPResource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mime_type: str
    metadata: Dict[str, Any]

@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]

class YSenseMCPServer:
    """
    MCP Server for YSense Platform
    Allows AI assistants to query and use wisdom drops with attribution
    """
    
    def __init__(self):
        self.name = "ysense-attribution"
        self.version = "2.0.0"
        self.z_validator = ZProtocolValidator()
        
    def get_server_info(self) -> Dict:
        """Return MCP server information"""
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": {
                "resources": True,
                "tools": True,
                "prompts": True,
                "sampling": False
            },
            "description": "YSense Attribution Infrastructure for Ethical AI Training"
        }
    
    def list_resources(self) -> List[MCPResource]:
        """List available wisdom resources"""
        
        db = get_session()
        
        # Get published wisdom drops
        wisdom_drops = db.query(WisdomDrop).filter(
            WisdomDrop.published == True
        ).limit(100).all()
        
        resources = []
        for drop in wisdom_drops:
            resource = MCPResource(
                uri=f"wisdom://{drop.id}",
                name=drop.title,
                description=f"Wisdom by {drop.attribution_text}",
                mime_type="application/json",
                metadata={
                    "cultural_context": drop.cultural_context,
                    "quality_score": drop.quality_score,
                    "z_protocol_score": drop.z_protocol_score,
                    "vibe_words": drop.vibe_words,
                    "attribution_required": True
                }
            )
            resources.append(resource)
        
        db.close()
        
        return resources
    
    def list_tools(self) -> List[MCPTool]:
        """List available MCP tools"""
        
        tools = [
            MCPTool(
                name="query_wisdom",
                description="Search for wisdom drops by topic or cultural context",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "cultural_context": {"type": "string", "description": "Cultural filter"},
                        "min_quality_score": {"type": "number", "description": "Minimum quality score"}
                    },
                    "required": ["query"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "title": {"type": "string"},
                                    "content": {"type": "object"},
                                    "attribution": {"type": "string"},
                                    "usage_fee": {"type": "number"}
                                }
                            }
                        }
                    }
                }
            ),
            MCPTool(
                name="check_attribution",
                description="Verify attribution requirements for wisdom usage",
                input_schema={
                    "type": "object",
                    "properties": {
                        "wisdom_id": {"type": "string", "description": "Wisdom drop ID"},
                        "usage_type": {"type": "string", "description": "Type of usage"}
                    },
                    "required": ["wisdom_id", "usage_type"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "attribution_required": {"type": "boolean"},
                        "attribution_text": {"type": "string"},
                        "attribution_hash": {"type": "string"},
                        "usage_fee": {"type": "number"},
                        "z_protocol_compliant": {"type": "boolean"}
                    }
                }
            ),
            MCPTool(
                name="report_usage",
                description="Report usage of wisdom drop for revenue distribution",
                input_schema={
                    "type": "object",
                    "properties": {
                        "wisdom_id": {"type": "string"},
                        "usage_type": {"type": "string"},
                        "client_id": {"type": "string"},
                        "attribution_included": {"type": "boolean"}
                    },
                    "required": ["wisdom_id", "usage_type", "client_id"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "usage_id": {"type": "string"},
                        "revenue_generated": {"type": "number"},
                        "attribution_verified": {"type": "boolean"}
                    }
                }
            ),
            MCPTool(
                name="validate_z_protocol",
                description="Validate content against Z Protocol ethical standards",
                input_schema={
                    "type": "object",
                    "properties": {
                        "content": {"type": "object"},
                        "consent_provided": {"type": "boolean"},
                        "attribution_included": {"type": "boolean"}
                    },
                    "required": ["content"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "z_protocol_score": {"type": "number"},
                        "certification": {"type": "string"},
                        "failures": {"type": "array", "items": {"type": "string"}},
                        "recommendations": {"type": "array", "items": {"type": "string"}}
                    }
                }
            )
        ]
        
        return tools
    
    async def execute_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Execute MCP tool"""
        
        if tool_name == "query_wisdom":
            return await self._query_wisdom(arguments)
        elif tool_name == "check_attribution":
            return await self._check_attribution(arguments)
        elif tool_name == "report_usage":
            return await self._report_usage(arguments)
        elif tool_name == "validate_z_protocol":
            return await self._validate_z_protocol(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def _query_wisdom(self, args: Dict) -> Dict:
        """Query wisdom drops"""
        
        db = get_session()
        
        query = db.query(WisdomDrop).filter(WisdomDrop.published == True)
        
        # Apply filters
        if "cultural_context" in args:
            query = query.filter(WisdomDrop.cultural_context == args["cultural_context"])
        
        if "min_quality_score" in args:
            query = query.filter(WisdomDrop.quality_score >= args["min_quality_score"])
        
        # Search in title and layers (basic text search)
        search_term = args["query"].lower()
        wisdom_drops = query.all()
        
        results = []
        for drop in wisdom_drops:
            # Basic relevance check
            if (search_term in drop.title.lower() or
                search_term in (drop.layer_narrative or "").lower() or
                search_term in (drop.layer_somatic or "").lower()):
                
                # Calculate usage fee
                usage_fee = self._calculate_usage_fee(drop)
                
                results.append({
                    "id": drop.id,
                    "title": drop.title,
                    "content": {
                        "layers": {
                            "narrative": drop.layer_narrative[:200] + "..." if drop.layer_narrative else None,
                            "somatic": drop.layer_somatic[:200] + "..." if drop.layer_somatic else None,
                            "attention": drop.layer_attention[:200] + "..." if drop.layer_attention else None,
                            "synesthetic": drop.layer_synesthetic[:200] + "..." if drop.layer_synesthetic else None,
                            "temporal_auditory": drop.layer_temporal_auditory[:200] + "..." if drop.layer_temporal_auditory else None
                        },
                        "vibe_words": drop.vibe_words,
                        "essence": drop.essence
                    },
                    "attribution": drop.attribution_text,
                    "attribution_hash": drop.attribution_hash[:16] + "...",
                    "cultural_context": drop.cultural_context,
                    "quality_score": drop.quality_score,
                    "usage_fee": usage_fee
                })
        
        db.close()
        
        return {"results": results[:10]}  # Limit to 10 results
    
    async def _check_attribution(self, args: Dict) -> Dict:
        """Check attribution requirements"""
        
        db = get_session()
        
        wisdom_drop = db.query(WisdomDrop).filter(
            WisdomDrop.id == args["wisdom_id"]
        ).first()
        
        if not wisdom_drop:
            db.close()
            return {
                "error": "Wisdom drop not found",
                "attribution_required": False
            }
        
        user = db.query(User).filter(User.id == wisdom_drop.user_id).first()
        
        # Calculate usage fee
        usage_fee = self._calculate_usage_fee(wisdom_drop, args.get("usage_type", "default"))
        
        db.close()
        
        return {
            "attribution_required": True,  # Always required
            "attribution_text": wisdom_drop.attribution_text,
            "attribution_hash": wisdom_drop.attribution_hash,
            "attribution_format": f"Source: {wisdom_drop.attribution_text} via YSense™ ({wisdom_drop.attribution_hash[:8]})",
            "usage_fee": usage_fee,
            "z_protocol_compliant": wisdom_drop.z_protocol_score >= 80,
            "cultural_context": wisdom_drop.cultural_context,
            "contributor_tier": user.z_protocol_tier if user else "Unknown"
        }
    
    async def _report_usage(self, args: Dict) -> Dict:
        """Report wisdom usage"""
        
        db = get_session()
        
        # Verify wisdom drop exists
        wisdom_drop = db.query(WisdomDrop).filter(
            WisdomDrop.id == args["wisdom_id"]
        ).first()
        
        if not wisdom_drop:
            db.close()
            return {"error": "Wisdom drop not found"}
        
        # Check attribution
        if not args.get("attribution_included", False):
            db.close()
            return {
                "error": "Attribution is required for all usage",
                "attribution_required": True,
                "attribution_text": wisdom_drop.attribution_text
            }
        
        # Create usage record
        usage_id = f"MCP_USAGE_{hashlib.md5(f'{args["wisdom_id"]}_{args["client_id"]}_{datetime.utcnow()}'.encode()).hexdigest()[:8].upper()}"
        
        user = db.query(User).filter(User.id == wisdom_drop.user_id).first()
        revenue = self._calculate_usage_fee(wisdom_drop, args["usage_type"])
        
        usage_record = UsageRecord(
            id=usage_id,
            wisdom_drop_id=args["wisdom_id"],
            usage_type=args["usage_type"],
            usage_context="MCP Integration",
            client_id=args["client_id"],
            attribution_included=True,
            attribution_format=f"Via YSense MCP ({wisdom_drop.attribution_hash[:8]})",
            revenue_generated=revenue
        )
        
        db.add(usage_record)
        
        # Update metrics
        wisdom_drop.times_accessed += 1
        wisdom_drop.revenue_generated += revenue
        
        if user:
            user.pending_earnings += revenue
            user.total_earnings += revenue
        
        db.commit()
        db.close()
        
        return {
            "usage_id": usage_id,
            "revenue_generated": revenue,
            "attribution_verified": True,
            "message": "Usage recorded successfully"
        }
    
    async def _validate_z_protocol(self, args: Dict) -> Dict:
        """Validate content with Z Protocol"""
        
        validation_data = {
            "consent_record": {
                "data_collection": args.get("consent_provided", False),
                "commercial_use": args.get("consent_provided", False),
                "ai_training": args.get("consent_provided", False),
                "revenue_sharing": args.get("consent_provided", False),
                "attribution": args.get("attribution_included", False),
                "terms_accepted": args.get("consent_provided", False),
                "timestamp": datetime.utcnow().isoformat()
            },
            "attribution": {
                "contributor_id": "MCP_CLIENT",
                "contributor_name": args.get("client_name", "MCP Client"),
                "culture": args.get("cultural_context", "Global"),
                "location": "Digital",
                "contribution_date": datetime.utcnow().isoformat()
            },
            "authenticity_declaration": {
                "is_original": args.get("is_original", True),
                "contains_copyrighted": False,
                "accept_liability": args.get("consent_provided", False)
            },
            "contributor_verified": args.get("verified", False),
            "contributor_age": 18,
            "gdpr_compliant": True,
            "copyright_cleared": True,
            "terms_accepted": args.get("consent_provided", False),
            "usage_disclosed": True,
            "revenue_explained": True,
            "retention_explained": True,
            "sharing_disclosed": True,
            "audit_trail": {
                "submission_timestamp": datetime.utcnow().isoformat(),
                "ip_address": "MCP_CLIENT",
                "user_agent": "MCP/2.0",
                "consent_timestamp": datetime.utcnow().isoformat(),
                "validation_history": []
            },
            "content": args.get("content", {})
        }
        
        result = await self.z_validator.validate_wisdom_drop(validation_data)
        
        return {
            "z_protocol_score": result["z_protocol_score"],
            "certification": result["certification"],
            "failures": result.get("failures", []),
            "warnings": result.get("warnings", []),
            "recommendations": self._get_recommendations(result),
            "compliant": result["z_protocol_score"] >= 80
        }
    
    def _calculate_usage_fee(self, wisdom_drop: WisdomDrop, usage_type: str = "default") -> float:
        """Calculate usage fee for wisdom drop"""
        
        base_rates = {
            "ai_training": 0.20,
            "research": 0.15,
            "commercial": 0.30,
            "educational": 0.10,
            "default": 0.10
        }
        
        base_rate = base_rates.get(usage_type, base_rates["default"])
        quality_multiplier = wisdom_drop.quality_score / 100.0
        
        return round(base_rate * quality_multiplier, 2)
    
    def _get_recommendations(self, validation_result: Dict) -> List[str]:
        """Get recommendations from validation result"""
        
        recommendations = []
        
        if validation_result["z_protocol_score"] < 80:
            recommendations.append("Ensure all required consents are provided")
            recommendations.append("Include proper attribution in all usage")
        
        if validation_result.get("failures"):
            for failure in validation_result["failures"][:3]:
                recommendations.append(f"Fix: {failure}")
        
        return recommendations

# MCP Client for testing
class YSenseMCPClient:
    """Client for testing MCP integration"""
    
    def __init__(self):
        self.server = YSenseMCPServer()
    
    async def test_integration(self):
        """Test MCP server integration"""
        
        print("Testing YSense MCP Integration")
        print("=" * 50)
        
        # Get server info
        info = self.server.get_server_info()
        print(f"Server: {info['name']} v{info['version']}")
        print(f"Description: {info['description']}")
        
        # List tools
        tools = self.server.list_tools()
        print(f"\nAvailable Tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test query
        print("\n" + "=" * 50)
        print("Testing wisdom query...")
        result = await self.server.execute_tool("query_wisdom", {
            "query": "wisdom",
            "min_quality_score": 50
        })
        
        if result.get("results"):
            print(f"Found {len(result['results'])} wisdom drops")
            for drop in result["results"][:3]:
                print(f"  - {drop['title']}")
                print(f"    Attribution: {drop['attribution']}")
                print(f"    Fee: €{drop['usage_fee']}")
        
        # Test Z Protocol validation
        print("\n" + "=" * 50)
        print("Testing Z Protocol validation...")
        validation = await self.server.execute_tool("validate_z_protocol", {
            "content": {"test": "content"},
            "consent_provided": True,
            "attribution_included": True
        })
        
        print(f"Z Protocol Score: {validation['z_protocol_score']}/100")
        print(f"Certification: {validation['certification']}")
        print(f"Compliant: {validation['compliant']}")

# Core init
def initialize_mcp():
    """Initialize MCP server"""
    server = YSenseMCPServer()
    print(f"✅ MCP Server initialized: {server.name} v{server.version}")
    return server

if __name__ == "__main__":
    # Test MCP integration
    client = YSenseMCPClient()
    asyncio.run(client.test_integration())
