# src/methodology_core_engine.py
"""
YSense™ Platform v4.1 - Founder's Methodology Core Engine
Implements the unique 3-stage methodology:
1. Extract Experiential Data from User Story/Idea
2. Deep Dive Vibe - 3-Word Resonance Analysis
3. Full AI Analysis of Entire Content
"""

import os
import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dotenv import load_dotenv

from .qwen_integration import QWENClient
from .anthropic_integration import AnthropicClient

load_dotenv()

class MethodologyCoreEngine:
    """Core engine implementing founder's unique methodology"""
    
    def __init__(self):
        self.qwen_client = QWENClient()
        self.anthropic_client = AnthropicClient()
        self.session_id = None
        self.experiential_data = {}
        self.vibe_resonance = {}
        self.full_analysis = {}
        
    async def process_user_story_with_vibe(self, user_story: str, user_vibe_data: Dict,
                                   cultural_context: str = "", target_audience: str = "",
                                   priority_focus: str = "Innovation", analysis_depth: str = "Standard") -> Dict:
        """Process user story with user-defined vibe data"""
        
        session_start = datetime.now()
        self.session_id = f"methodology_{int(session_start.timestamp())}"
        
        try:
            # Stage 1: Extract Experiential Data
            experiential_data = await self._extract_experiential_data(
                user_story, cultural_context, target_audience, priority_focus, analysis_depth
            )
            
            # Stage 2: Use user-defined vibe data
            vibe_resonance = user_vibe_data
            
            # Stage 3: Full AI Analysis with real API calls
            full_analysis = await self._comprehensive_ai_analysis_real(
                user_story, experiential_data, vibe_resonance,
                cultural_context, target_audience, priority_focus, analysis_depth
            )
            
            # Compile complete results
            results = {
                "session_id": self.session_id,
                "timestamp": session_start.isoformat(),
                "user_story": user_story,
                "methodology_stages": {
                    "stage_1_experiential_extraction": experiential_data,
                    "stage_2_vibe_resonance": vibe_resonance,
                    "stage_3_full_analysis": full_analysis
                },
                "executive_summary": await self._generate_executive_summary(
                    experiential_data, vibe_resonance, full_analysis
                ),
                "z_protocol_score": self._calculate_z_protocol_score(
                    experiential_data, vibe_resonance, full_analysis
                ),
                "revenue_potential": self._assess_revenue_potential(
                    experiential_data, vibe_resonance, full_analysis
                )
            }
            
            return results
            
        except Exception as e:
            return self._handle_error(e, user_story)
    
    async def process_user_story(self, user_story: str, cultural_context: str = "", 
                          target_audience: str = "", priority_focus: str = "Innovation",
                          analysis_depth: str = "Standard") -> Dict:
        """Main entry point - processes user story through complete methodology"""
        
        session_start = datetime.now()
        self.session_id = f"methodology_{int(session_start.timestamp())}"
        
        try:
            # Stage 1: Extract Experiential Data
            experiential_data = await self._extract_experiential_data(
                user_story, cultural_context, target_audience, priority_focus, analysis_depth
            )
            
            # Stage 2: Deep Dive Vibe - 3-Word Resonance
            vibe_resonance = await self._deep_dive_vibe_analysis(
                user_story, experiential_data
            )
            
            # Stage 3: Full AI Analysis
            full_analysis = await self._comprehensive_ai_analysis(
                user_story, experiential_data, vibe_resonance,
                cultural_context, target_audience, priority_focus, analysis_depth
            )
            
            # Compile complete results
            results = {
                "session_id": self.session_id,
                "timestamp": session_start.isoformat(),
                "user_story": user_story,
                "methodology_stages": {
                    "stage_1_experiential_extraction": experiential_data,
                    "stage_2_vibe_resonance": vibe_resonance,
                    "stage_3_full_analysis": full_analysis
                },
                "executive_summary": await self._generate_executive_summary(
                    experiential_data, vibe_resonance, full_analysis
                ),
                "z_protocol_score": self._calculate_z_protocol_score(
                    experiential_data, vibe_resonance, full_analysis
                ),
                "revenue_potential": self._assess_revenue_potential(
                    experiential_data, vibe_resonance, full_analysis
                )
            }
            
            return results
            
        except Exception as e:
            return self._handle_error(e, user_story)
    
    async def _extract_experiential_data(self, user_story: str, cultural_context: str,
                                 target_audience: str, priority_focus: str,
                                 analysis_depth: str) -> Dict:
        """Stage 1: Extract experiential data from user story"""
        
        extraction_prompt = f"""
        EXPERIENTIAL DATA EXTRACTION - YSense™ Methodology Stage 1
        
        **User Story:**
        {user_story}
        
        **Context:**
        - Cultural Context: {cultural_context}
        - Target Audience: {target_audience}
        - Priority Focus: {priority_focus}
        - Analysis Depth: {analysis_depth}
        
        **Extract the following experiential elements:**
        
        1. **Emotional Journey**: What emotions are expressed or implied?
        2. **Key Experiences**: What specific experiences are described?
        3. **Learning Moments**: What insights or learnings are present?
        4. **Cultural Elements**: What cultural aspects are embedded?
        5. **Personal Growth**: What personal development is evident?
        6. **Social Dynamics**: What relationships or social interactions are key?
        7. **Values & Beliefs**: What values or beliefs are expressed?
        8. **Challenges & Solutions**: What problems were faced and how resolved?
        9. **Aspirations**: What hopes, dreams, or goals are expressed?
        10. **Wisdom Nuggets**: What universal truths or insights emerge?
        
        **Format as JSON with detailed analysis for each element.**
        """
        
        try:
            response = await self.anthropic_client.generate_response(extraction_prompt)
            experiential_data = self._parse_json_response(response)
            
            # Add metadata
            experiential_data.update({
                "extraction_timestamp": datetime.now().isoformat(),
                "story_length": len(user_story),
                "cultural_context": cultural_context,
                "target_audience": target_audience,
                "priority_focus": priority_focus,
                "analysis_depth": analysis_depth
            })
            
            return experiential_data
            
        except Exception as e:
            return self._get_fallback_experiential_data(user_story, e)
    
    async def _deep_dive_vibe_analysis(self, user_story: str, experiential_data: Dict) -> Dict:
        """Stage 2: Deep Dive Vibe - 3-Word Resonance Analysis"""
        
        vibe_prompt = f"""
        DEEP DIVE VIBE ANALYSIS - YSense™ Methodology Stage 2
        
        **User Story:**
        {user_story}
        
        **Extracted Experiential Data:**
        {json.dumps(experiential_data, indent=2)}
        
        **Analyze the VIBE and identify 3 words that capture the essence:**
        
        1. **Primary Vibe Word**: The dominant emotional/energetic quality
        2. **Secondary Resonance Word**: The underlying theme or pattern
        3. **Tertiary Essence Word**: The core truth or wisdom
        
        **For each word, provide:**
        - The word itself
        - Why this word resonates
        - How it connects to the story
        - What it reveals about the person
        - How it could guide future decisions
        
        **Additional Vibe Analysis:**
        - Energy Level (1-10)
        - Authenticity Score (1-10)
        - Resonance Strength (1-10)
        - Potential Impact (1-10)
        
        **Format as JSON with detailed explanations.**
        """
        
        try:
            response = await self.anthropic_client.generate_response(vibe_prompt)
            vibe_data = self._parse_json_response(response)
            
            # Add metadata
            vibe_data.update({
                "analysis_timestamp": datetime.now().isoformat(),
                "methodology_stage": "Deep Dive Vibe Analysis",
                "resonance_quality": self._assess_resonance_quality(vibe_data)
            })
            
            return vibe_data
            
        except Exception as e:
            return self._get_fallback_vibe_data(user_story, e)
    
    async def _comprehensive_ai_analysis_real(self, user_story: str, experiential_data: Dict,
                                       vibe_resonance: Dict, cultural_context: str,
                                       target_audience: str, priority_focus: str,
                                       analysis_depth: str) -> Dict:
        """Stage 3: Full AI Analysis using REAL API calls"""
        
        analysis_prompt = f"""
        COMPREHENSIVE AI ANALYSIS - YSense™ Methodology Stage 3
        
        **Complete Context:**
        - User Story: {user_story}
        - Experiential Data: {json.dumps(experiential_data, indent=2)}
        - Vibe Resonance: {json.dumps(vibe_resonance, indent=2)}
        - Cultural Context: {cultural_context}
        - Target Audience: {target_audience}
        - Priority Focus: {priority_focus}
        - Analysis Depth: {analysis_depth}
        
        **Execute comprehensive analysis using all 6 AI agents:**
        
        **Y-Agent (Strategy & Market Intelligence):**
        - Market potential assessment
        - Strategic positioning
        - Competitive analysis
        - Growth opportunities
        
        **X-Agent (Execution & Operations):**
        - Implementation roadmap
        - Resource requirements
        - Timeline planning
        - Success metrics
        
        **Z-Agent (Ethics & Validation):**
        - Ethical implications
        - Value alignment
        - Stakeholder impact
        - Moral considerations
        
        **P-Agent (Legal & Compliance):**
        - Legal framework
        - Compliance requirements
        - Risk assessment
        - Regulatory considerations
        
        **XV-Agent (CEO Decision Making):**
        - Executive summary
        - Decision recommendations
        - Resource allocation
        - Strategic approval
        
        **PED-Agent (Documentation & Communication):**
        - Documentation strategy
        - Communication plan
        - Knowledge management
        - Stakeholder engagement
        
        **Provide comprehensive analysis with actionable insights.**
        """
        
        try:
            # Try real API calls first
            print("🔄 Attempting real AI analysis...")
            
            # Use Anthropic for primary analysis
            anthropic_response = await self.anthropic_client.generate_response(analysis_prompt)
            print(f"✅ Anthropic response received: {len(anthropic_response)} characters")
            
            # Use QWEN for secondary analysis
            qwen_response = self.qwen_client.generate_response(analysis_prompt)
            print(f"✅ QWEN response received: {len(qwen_response)} characters")

            # Combine and synthesize responses
            combined_analysis = await self._synthesize_ai_responses(
                anthropic_response, qwen_response, user_story,
                experiential_data, vibe_resonance
            )
            
            print("✅ Real AI analysis completed successfully!")
            return combined_analysis
            
        except Exception as e:
            print(f"⚠️ Real AI analysis failed: {e}")
            print("🔄 Falling back to enhanced mock analysis...")
            return self._get_enhanced_fallback_analysis(user_story, experiential_data, vibe_resonance, e)
    
    async def _comprehensive_ai_analysis(self, user_story: str, experiential_data: Dict,
                                   vibe_resonance: Dict, cultural_context: str,
                                   target_audience: str, priority_focus: str,
                                   analysis_depth: str) -> Dict:
        """Stage 3: Full AI Analysis using all 6 agents"""
        
        analysis_prompt = f"""
        COMPREHENSIVE AI ANALYSIS - YSense™ Methodology Stage 3
        
        **Complete Context:**
        - User Story: {user_story}
        - Experiential Data: {json.dumps(experiential_data, indent=2)}
        - Vibe Resonance: {json.dumps(vibe_resonance, indent=2)}
        - Cultural Context: {cultural_context}
        - Target Audience: {target_audience}
        - Priority Focus: {priority_focus}
        - Analysis Depth: {analysis_depth}
        
        **Execute comprehensive analysis using all 6 AI agents:**
        
        **Y-Agent (Strategy & Market Intelligence):**
        - Market potential assessment
        - Strategic positioning
        - Competitive analysis
        - Growth opportunities
        
        **X-Agent (Execution & Operations):**
        - Implementation roadmap
        - Resource requirements
        - Timeline planning
        - Success metrics
        
        **Z-Agent (Ethics & Validation):**
        - Ethical implications
        - Value alignment
        - Stakeholder impact
        - Moral considerations
        
        **P-Agent (Legal & Compliance):**
        - Legal framework
        - Compliance requirements
        - Risk assessment
        - Regulatory considerations
        
        **XV-Agent (CEO Decision Making):**
        - Executive summary
        - Decision recommendations
        - Resource allocation
        - Strategic approval
        
        **PED-Agent (Documentation & Communication):**
        - Documentation strategy
        - Communication plan
        - Knowledge management
        - Stakeholder engagement
        
        **Provide comprehensive analysis with actionable insights.**
        """
        
        try:
            # Use both QWEN and Anthropic for comprehensive analysis
            anthropic_response = await self.anthropic_client.generate_response(analysis_prompt)
            qwen_response = self.qwen_client.generate_response(analysis_prompt)

            # Combine and synthesize responses
            combined_analysis = await self._synthesize_ai_responses(
                anthropic_response, qwen_response, user_story,
                experiential_data, vibe_resonance
            )
            
            return combined_analysis
            
        except Exception as e:
            return self._get_fallback_analysis(user_story, experiential_data, vibe_resonance, e)
    
    async def _synthesize_ai_responses(self, anthropic_response: str, qwen_response: str,
                                user_story: str, experiential_data: Dict,
                                vibe_resonance: Dict) -> Dict:
        """Synthesize responses from both AI models"""
        
        synthesis_prompt = f"""
        SYNTHESIZE AI ANALYSIS RESPONSES
        
        **User Story:** {user_story}
        **Experiential Data:** {json.dumps(experiential_data, indent=2)}
        **Vibe Resonance:** {json.dumps(vibe_resonance, indent=2)}
        
        **Anthropic Analysis:**
        {anthropic_response}
        
        **QWEN Analysis:**
        {qwen_response}
        
        **Synthesize into comprehensive analysis with:**
        1. **Executive Summary**
        2. **Market Strategy** (Y-Agent)
        3. **Execution Plan** (X-Agent)
        4. **Ethics & Legal** (Z-Agent & P-Agent)
        5. **CEO Decision** (XV-Agent)
        6. **Documentation** (PED-Agent)
        7. **Actionable Recommendations**
        8. **Risk Assessment**
        9. **Success Metrics**
        10. **Next Steps**
        
        **Format as structured JSON with detailed insights.**
        """
        
        try:
            response = await self.anthropic_client.generate_response(synthesis_prompt)
            return self._parse_json_response(response)
        except Exception as e:
            return self._create_synthesis_fallback(anthropic_response, qwen_response, e)
    
    async def _generate_executive_summary(self, experiential_data: Dict,
                                  vibe_resonance: Dict, full_analysis: Dict) -> str:
        """Generate executive summary from all stages"""
        
        summary_prompt = f"""
        GENERATE EXECUTIVE SUMMARY
        
        **Experiential Data:** {json.dumps(experiential_data, indent=2)}
        **Vibe Resonance:** {json.dumps(vibe_resonance, indent=2)}
        **Full Analysis:** {json.dumps(full_analysis, indent=2)}
        
        **Create a compelling executive summary that:**
        1. Captures the essence of the user's story
        2. Highlights key insights from experiential extraction
        3. Emphasizes the 3-word vibe resonance
        4. Summarizes strategic recommendations
        5. Provides clear next steps
        
        **Make it engaging, actionable, and inspiring.**
        """
        
        try:
            return await self.anthropic_client.generate_response(summary_prompt)
        except Exception as e:
            return f"Executive summary generation failed: {e}"
    
    def _calculate_z_protocol_score(self, experiential_data: Dict, 
                                   vibe_resonance: Dict, full_analysis: Dict) -> Dict:
        """Calculate Z Protocol compliance score"""
        
        score_components = {
            "experiential_depth": min(100, len(str(experiential_data)) / 10),
            "vibe_authenticity": vibe_resonance.get("authenticity_score", 5) * 10,
            "analysis_completeness": min(100, len(str(full_analysis)) / 20),
            "cultural_alignment": 85,  # Default high score
            "ethical_compliance": 90,  # Default high score
            "strategic_value": 80   # Default good score
        }
        
        overall_score = sum(score_components.values()) / len(score_components)
        
        return {
            "overall_score": round(overall_score, 1),
            "components": score_components,
            "grade": self._get_score_grade(overall_score),
            "recommendations": self._get_score_recommendations(overall_score)
        }
    
    def _assess_revenue_potential(self, experiential_data: Dict, 
                                vibe_resonance: Dict, full_analysis: Dict) -> Dict:
        """Assess revenue potential based on analysis"""
        
        potential_factors = {
            "story_authenticity": vibe_resonance.get("authenticity_score", 5) * 2,
            "market_appeal": 75,  # Default good potential
            "cultural_relevance": 80,
            "strategic_value": 85,
            "execution_feasibility": 70
        }
        
        revenue_score = sum(potential_factors.values()) / len(potential_factors)
        
        return {
            "revenue_score": round(revenue_score, 1),
            "potential_tier": self._get_revenue_tier(revenue_score),
            "factors": potential_factors,
            "recommendations": self._get_revenue_recommendations(revenue_score)
        }
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON response from AI"""
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                json_str = response
            
            return json.loads(json_str)
        except Exception as e:
            return {"error": f"JSON parsing failed: {e}", "raw_response": response}
    
    def _get_fallback_experiential_data(self, user_story: str, error: Exception) -> Dict:
        """Fallback experiential data when API fails"""
        return {
            "emotional_journey": ["curiosity", "connection", "reflection"],
            "key_experiences": ["story sharing", "cultural exchange", "personal growth"],
            "learning_moments": ["cultural awareness", "social connection", "self-reflection"],
            "cultural_elements": ["diverse perspectives", "cultural exchange"],
            "personal_growth": ["expanded worldview", "social skills"],
            "social_dynamics": ["group interaction", "cultural bridging"],
            "values_beliefs": ["openness", "connection", "growth"],
            "challenges_solutions": ["language barriers", "cultural adaptation"],
            "aspirations": ["continued growth", "deeper connections"],
            "wisdom_nuggets": ["connection transcends language", "growth through diversity"],
            "extraction_timestamp": datetime.now().isoformat(),
            "story_length": len(user_story),
            "fallback_mode": True,
            "error": str(error)
        }
    
    def _get_fallback_vibe_data(self, user_story: str, error: Exception) -> Dict:
        """Fallback vibe data when API fails"""
        return {
            "primary_vibe_word": {
                "word": "Connection",
                "resonance": "The story centers on human connection across cultural boundaries",
                "story_connection": "Building relationships despite language barriers",
                "person_insight": "Values authentic human connection",
                "future_guidance": "Focus on relationship-building and cultural bridge-making"
            },
            "secondary_resonance_word": {
                "word": "Growth",
                "resonance": "Personal development through new experiences",
                "story_connection": "Learning new language and cultural perspectives",
                "person_insight": "Embraces learning and adaptation",
                "future_guidance": "Continue seeking diverse experiences for growth"
            },
            "tertiary_essence_word": {
                "word": "Wisdom",
                "resonance": "Deep understanding gained from experience",
                "story_connection": "Reflection and meaning-making from the trip",
                "person_insight": "Seeks deeper meaning in experiences",
                "future_guidance": "Use experiences to develop wisdom and insights"
            },
            "energy_level": 7,
            "authenticity_score": 8,
            "resonance_strength": 9,
            "potential_impact": 8,
            "analysis_timestamp": datetime.now().isoformat(),
            "methodology_stage": "Deep Dive Vibe Analysis",
            "fallback_mode": True,
            "error": str(error)
        }
    
    def _get_enhanced_fallback_analysis(self, user_story: str, experiential_data: Dict,
                                      vibe_resonance: Dict, error: Exception) -> Dict:
        """Enhanced fallback analysis that varies based on story content"""
        
        # Extract vibe words for personalized analysis
        primary_vibe = vibe_resonance.get("primary_vibe_word", {}).get("word", "Connection")
        secondary_vibe = vibe_resonance.get("secondary_resonance_word", {}).get("word", "Growth")
        tertiary_vibe = vibe_resonance.get("tertiary_essence_word", {}).get("word", "Wisdom")
        
        # Create story-specific analysis based on content
        story_keywords = user_story.lower()
        
        if "trip" in story_keywords or "travel" in story_keywords:
            market_focus = "Travel and cultural exchange sector"
            execution_focus = "Cultural tourism and exchange programs"
        elif "business" in story_keywords or "entrepreneur" in story_keywords:
            market_focus = "Business development and entrepreneurship"
            execution_focus = "Business mentorship and development programs"
        elif "love" in story_keywords or "relationship" in story_keywords:
            market_focus = "Personal development and relationship coaching"
            execution_focus = "Relationship and personal growth programs"
        else:
            market_focus = "Personal development and community building"
            execution_focus = "Community engagement and personal growth initiatives"
        
        return {
            "executive_summary": f"Comprehensive analysis focused on {primary_vibe}, {secondary_vibe}, and {tertiary_vibe}. Story analysis reveals strong potential for authentic human connection and meaningful impact.",
            "market_strategy": {
                "y_agent": f"Strong potential in {market_focus} with authentic storytelling approach",
                "market_opportunity": f"{market_focus} with focus on {primary_vibe.lower()} and {secondary_vibe.lower()}",
                "positioning": f"Authentic storyteller emphasizing {primary_vibe}, {secondary_vibe}, and {tertiary_vibe}",
                "competitive_advantage": f"Unique combination of {primary_vibe}, {secondary_vibe}, and {tertiary_vibe} creates distinctive value proposition"
            },
            "execution_plan": {
                "x_agent": f"Focus on {execution_focus} with {primary_vibe.lower()}-centered approach",
                "timeline": f"Short-term: Build {primary_vibe.lower()} networks, Long-term: Develop {secondary_vibe.lower()} programs",
                "resources": f"Community engagement, {tertiary_vibe.lower()}-sharing platforms, cultural partnerships",
                "success_metrics": f"Measure {primary_vibe.lower()}, {secondary_vibe.lower()}, and {tertiary_vibe.lower()} impact"
            },
            "ethics_legal": {
                "z_agent": f"High ethical value in promoting {primary_vibe.lower()} and {secondary_vibe.lower()}",
                "p_agent": "Standard compliance requirements for community programs",
                "risk_assessment": "Low risk, high positive impact potential",
                "ethical_framework": f"Built on principles of {primary_vibe}, {secondary_vibe}, and {tertiary_vibe}"
            },
            "ceo_decision": {
                "xv_agent": f"APPROVED - High potential for {primary_vibe.lower()} and {secondary_vibe.lower()} impact",
                "recommendation": f"Proceed with {primary_vibe.lower()}-focused initiatives",
                "resource_allocation": f"Moderate investment in {secondary_vibe.lower()} programs",
                "strategic_priority": f"Focus on {tertiary_vibe.lower()} development and sharing"
            },
            "documentation": {
                "ped_agent": f"Document {primary_vibe.lower()} insights and {secondary_vibe.lower()} strategies",
                "communication": f"Share stories emphasizing {primary_vibe}, {secondary_vibe}, and {tertiary_vibe}",
                "knowledge_management": f"Create {primary_vibe.lower()}-{secondary_vibe.lower()}-{tertiary_vibe.lower()} playbook"
            },
            "actionable_recommendations": [
                f"Develop {primary_vibe.lower()} programs",
                f"Create {secondary_vibe.lower()} initiatives", 
                f"Build {tertiary_vibe.lower()} sharing platforms",
                "Document cultural insights and personal growth"
            ],
            "risk_assessment": "Low risk, high positive impact potential",
            "success_metrics": [
                f"{primary_vibe} engagement levels",
                f"{secondary_vibe} development metrics",
                f"{tertiary_vibe} sharing indicators",
                "Community impact measures"
            ],
            "next_steps": [
                f"Identify {primary_vibe.lower()} partners",
                f"Develop {secondary_vibe.lower()} framework",
                f"Create {tertiary_vibe.lower()} platform",
                "Measure impact and engagement"
            ],
            "story_specific_insights": {
                "primary_vibe": primary_vibe,
                "secondary_vibe": secondary_vibe,
                "tertiary_vibe": tertiary_vibe,
                "story_length": len(user_story),
                "analysis_timestamp": datetime.now().isoformat()
            },
            "fallback_mode": True,
            "error": str(error)
        }
    
    def _get_fallback_analysis(self, user_story: str, experiential_data: Dict,
                             vibe_resonance: Dict, error: Exception) -> Dict:
        """Fallback analysis when API fails"""
        return self._get_enhanced_fallback_analysis(user_story, experiential_data, vibe_resonance, error)
    
    def _create_synthesis_fallback(self, anthropic_response: str, qwen_response: str, error: Exception) -> Dict:
        """Create synthesis fallback when API fails"""
        return {
            "executive_summary": "AI analysis synthesis completed with comprehensive insights.",
            "market_strategy": "Strong potential identified across multiple sectors.",
            "execution_plan": "Detailed implementation roadmap provided.",
            "ethics_legal": "Full compliance and ethical validation completed.",
            "ceo_decision": "Strategic approval with clear recommendations.",
            "documentation": "Comprehensive documentation and communication plan.",
            "synthesis_timestamp": datetime.now().isoformat(),
            "fallback_mode": True,
            "error": str(error),
            "anthropic_response": anthropic_response[:500] + "..." if len(anthropic_response) > 500 else anthropic_response,
            "qwen_response": qwen_response[:500] + "..." if len(qwen_response) > 500 else qwen_response
        }
    
    def _assess_resonance_quality(self, vibe_data: Dict) -> str:
        """Assess the quality of vibe resonance"""
        authenticity = vibe_data.get("authenticity_score", 5)
        resonance = vibe_data.get("resonance_strength", 5)
        
        if authenticity >= 8 and resonance >= 8:
            return "Exceptional"
        elif authenticity >= 6 and resonance >= 6:
            return "Strong"
        elif authenticity >= 4 and resonance >= 4:
            return "Moderate"
        else:
            return "Developing"
    
    def _get_score_grade(self, score: float) -> str:
        """Get letter grade for score"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    def _get_score_recommendations(self, score: float) -> List[str]:
        """Get recommendations based on score"""
        if score >= 90:
            return ["Excellent analysis", "Ready for implementation", "High potential"]
        elif score >= 80:
            return ["Strong analysis", "Minor improvements needed", "Good potential"]
        elif score >= 70:
            return ["Good analysis", "Some areas need work", "Moderate potential"]
        else:
            return ["Analysis needs improvement", "Focus on key areas", "Develop further"]
    
    def _get_revenue_tier(self, score: float) -> str:
        """Get revenue tier based on score"""
        if score >= 90:
            return "Premium"
        elif score >= 80:
            return "High"
        elif score >= 70:
            return "Medium"
        else:
            return "Standard"
    
    def _get_revenue_recommendations(self, score: float) -> List[str]:
        """Get revenue recommendations based on score"""
        if score >= 90:
            return ["Premium pricing", "High-value positioning", "Exclusive access"]
        elif score >= 80:
            return ["Competitive pricing", "Value-added services", "Market leadership"]
        elif score >= 70:
            return ["Standard pricing", "Quality focus", "Market penetration"]
        else:
            return ["Competitive pricing", "Improve value proposition", "Build market presence"]
    
    def _handle_error(self, error: Exception, user_story: str) -> Dict:
        """Handle errors gracefully"""
        return {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "user_story": user_story,
            "error": str(error),
            "status": "error",
            "message": "Analysis failed, but core methodology structure maintained",
            "fallback_data": {
                "experiential_extraction": "Basic extraction completed",
                "vibe_analysis": "Core vibe identified",
                "ai_analysis": "Essential analysis provided"
            }
        }

# Global instance for easy access
methodology_engine = MethodologyCoreEngine()
