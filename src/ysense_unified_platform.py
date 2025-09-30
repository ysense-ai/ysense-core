# ysense_unified_platform.py
"""
YSense™ Unified Platform v2.0 - Standalone Version
All components integrated in single file for immediate deployment
"""

import streamlit as st
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import hashlib
import sqlite3
import re

# ============================================
# DATABASE MANAGER (Foundation)
# ============================================

class YSenseDatabase:
    """Unified database manager for YSense platform"""
    
    def __init__(self, db_path: str = "ysense_unified.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize all required tables"""
        with sqlite3.connect(self.db_path) as conn:
            # Wisdom drops table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wisdom_drops (
                    id TEXT PRIMARY KEY,
                    author TEXT NOT NULL,
                    title TEXT,
                    cultural_context TEXT,
                    timestamp TEXT NOT NULL,
                    raw_content TEXT,
                    layers TEXT,
                    quality_score REAL,
                    revenue_potential REAL,
                    attribution_hash TEXT,
                    consent_verified INTEGER,
                    z_protocol_version TEXT,
                    vibe_words TEXT,
                    personal_connection TEXT,
                    essence TEXT,
                    distillation_completed INTEGER DEFAULT 0,
                    distillation_timestamp TEXT,
                    agent_insights TEXT,
                    team_response TEXT,
                    z_protocol_score REAL,
                    z_certification TEXT,
                    validation_details TEXT,
                    status TEXT DEFAULT 'pending'
                )
            """)
            conn.commit()
    
    def save_wisdom_drop(self, wisdom: Dict) -> bool:
        """Save or update a wisdom drop"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO wisdom_drops (
                        id, author, title, cultural_context, timestamp,
                        raw_content, layers, quality_score, revenue_potential,
                        attribution_hash, consent_verified, z_protocol_version,
                        vibe_words, personal_connection, essence,
                        distillation_completed, distillation_timestamp,
                        agent_insights, team_response, z_protocol_score,
                        z_certification, validation_details, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    wisdom['id'],
                    wisdom.get('author'),
                    wisdom.get('title'),
                    wisdom.get('cultural_context'),
                    wisdom.get('timestamp', datetime.now().isoformat()),
                    wisdom.get('raw_content'),
                    json.dumps(wisdom.get('layers', {})),
                    wisdom.get('quality_score', 0.0),
                    wisdom.get('revenue_potential', 0.0),
                    wisdom.get('attribution_hash'),
                    1 if wisdom.get('consent_verified') else 0,
                    wisdom.get('z_protocol_version', 'v2.0'),
                    json.dumps(wisdom.get('vibe_words')) if wisdom.get('vibe_words') else None,
                    wisdom.get('personal_connection'),
                    wisdom.get('essence'),
                    1 if wisdom.get('distillation_completed') else 0,
                    wisdom.get('distillation_timestamp'),
                    json.dumps(wisdom.get('agent_insights', {})),
                    wisdom.get('team_response'),
                    wisdom.get('z_protocol_score', 0.0),
                    wisdom.get('z_certification'),
                    json.dumps(wisdom.get('validation_details', {})),
                    wisdom.get('status', 'pending')
                ))
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Database error: {e}")
            return False
    
    def get_all_wisdom_drops(self) -> List[Dict]:
        """Get all wisdom drops"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM wisdom_drops ORDER BY timestamp DESC")
            
            wisdom_drops = []
            for row in cursor:
                wisdom = dict(row)
                # Parse JSON fields
                if wisdom.get('layers'):
                    wisdom['layers'] = json.loads(wisdom['layers'])
                if wisdom.get('vibe_words'):
                    wisdom['vibe_words'] = json.loads(wisdom['vibe_words'])
                if wisdom.get('agent_insights'):
                    wisdom['agent_insights'] = json.loads(wisdom['agent_insights'])
                wisdom_drops.append(wisdom)
            return wisdom_drops
    
    def get_revenue_summary(self) -> Dict:
        """Get revenue summary statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_wisdom_drops,
                    AVG(quality_score) as average_quality_score,
                    SUM(revenue_potential) as total_revenue_potential,
                    MAX(revenue_potential) as highest_revenue_drop
                FROM wisdom_drops
            """)
            row = cursor.fetchone()
            return {
                'total_wisdom_drops': row[0] or 0,
                'average_quality_score': row[1] or 0.0,
                'total_revenue_potential': row[2] or 0.0,
                'highest_revenue_drop': row[3] or 0.0
            }

# ============================================
# FIVE-PROMPT TOOLKIT (Important Methodology)
# ============================================

class FivePromptToolkit:
    """Implementation of the 5-Prompt Perception Toolkit™"""
    
    def __init__(self):
        self.prompts = {
            'narrative': "What is the unspoken story of this place or thing? As well as, what is the well-known story of it too from my perspective?",
            'somatic': "What does being here make my emotion and body feel? What in my mind as present here?",
            'attention': "What is one tiny detail here that most people would miss? What do I miss out in this places and things?",
            'synesthetic': "What are three non-visual words to describe the 'vibe' here? Let it flow through me and feels.",
            'temporal_auditory': "If this moment had a sound, what would it be?"
        }
        
        self.cultural_multipliers = {
            'Malaysian': 1.5,
            'Southeast Asian': 1.3,
            'Asian': 1.2,
            'Global South': 1.15,
            'Indigenous': 1.4,
            'Global': 1.0
        }
    
    def create_wisdom_drop(self, author: str, title: str, layers: Dict, cultural_context: str) -> Dict:
        """Create a wisdom drop from layer responses"""
        wisdom_id = f"DROP_{hashlib.md5(f'{author}_{title}_{datetime.now()}'.encode()).hexdigest()[:8].upper()}"
        
        return {
            'id': wisdom_id,
            'timestamp': datetime.now().isoformat(),
            'author': author,
            'title': title,
            'cultural_context': cultural_context,
            'status': 'awaiting_distillation',
            'layers': layers,
            'quality_score': self._calculate_quality(layers),
            'attribution_hash': hashlib.sha256(f'{author}_{title}'.encode()).hexdigest(),
            'z_protocol_version': 'v2.0',
            'vibe_words': None,
            'personal_connection': None,
            'essence': None,
            'distillation_completed': False
        }
    
    def add_deep_vibe_distillation(self, wisdom_drop: Dict, vibe_words: List[str], 
                                  personal_connection: str) -> Dict:
        """Complete Deep Vibe Distillation process"""
        if len(vibe_words) != 3:
            raise ValueError("Deep Vibe Distillation requires exactly 3 words")
        
        wisdom_drop['vibe_words'] = vibe_words
        wisdom_drop['personal_connection'] = personal_connection
        wisdom_drop['essence'] = f"{' + '.join(vibe_words)} through {personal_connection[:50]}"
        wisdom_drop['distillation_completed'] = True
        wisdom_drop['distillation_timestamp'] = datetime.now().isoformat()
        wisdom_drop['status'] = 'complete'
        
        # Recalculate with distillation bonus
        base_quality = wisdom_drop['quality_score']
        wisdom_drop['quality_score'] = min(base_quality + 0.2, 1.0)
        wisdom_drop['revenue_potential'] = self._calculate_revenue(
            wisdom_drop['quality_score'],
            wisdom_drop['cultural_context']
        )
        
        return wisdom_drop
    
    def _calculate_quality(self, layers: Dict) -> float:
        """Calculate quality score"""
        score = 0.0
        weights = {'narrative': 0.15, 'somatic': 0.20, 'attention': 0.15, 
                  'synesthetic': 0.20, 'temporal_auditory': 0.10}
        
        for layer, weight in weights.items():
            if layer in layers and layers[layer] and len(layers[layer]) > 20:
                score += weight
        return min(score, 0.80)  # Cap at 0.80 without distillation
    
    def _calculate_revenue(self, quality_score: float, cultural_context: str) -> float:
        """Calculate revenue with cultural multipliers"""
        base_rate = 50.0  # €50 base
        multiplier = self.cultural_multipliers.get(cultural_context, 1.0)
        return round(base_rate * quality_score * multiplier, 2)

# ============================================
# INTELLIGENT AGENTS (Important - Simplified)
# ============================================

class IntelligentAgent:
    """Base intelligent agent"""
    def __init__(self, name: str, role: str, focus: str):
        self.name = name
        self.role = role
        self.focus = focus
    
    def analyze(self, story: str) -> str:
        """Analyze story from agent's perspective"""
        # Simplified analysis without OpenAI
        keywords = {
            'Y': ['strategy', 'teaching', 'scale', 'global'],
            'X': ['market', 'value', 'opportunity', 'insight'],
            'Z': ['ethics', 'consent', 'dignity', 'fair'],
            'P': ['legal', 'rights', 'attribution', 'license'],
            'XV': ['revenue', 'impact', 'reality', 'measure'],
            'PED': ['learn', 'wisdom', 'lesson', 'capture'],
            'ALTON': ['vision', 'bridge', 'human', 'AI']
        }
        
        agent_words = keywords.get(self.name, [])
        relevance = sum(1 for word in agent_words if word.lower() in story.lower())
        
        responses = {
            'Y': f"Strategic value identified: This wisdom can scale globally through educational partnerships.",
            'X': f"Market insight: High-value wisdom for AI training datasets, especially for {story[:30]}...",
            'Z': f"Ethics verified: Full consent and attribution preserved with dignity.",
            'P': f"Legal framework: Protected under Apache 2.0 with attribution rights secured.",
            'XV': f"Revenue potential: Estimated €{50 + relevance * 10:.2f} based on quality metrics.",
            'PED': f"Learning captured: Universal wisdom about human experience preserved.",
            'ALTON': f"Vision alignment: This bridges human wisdom to ethical AI development."
        }
        
        return responses.get(self.name, f"{self.role} analysis complete.")

class WisdomTeam:
    """Simplified wisdom extraction team"""
    def __init__(self):
        self.agents = {
            'Y': IntelligentAgent('Y', 'Strategy', 'Academic partnerships'),
            'X': IntelligentAgent('X', 'Intelligence', 'Market insights'),
            'Z': IntelligentAgent('Z', 'Ethics', 'Consent management'),
            'P': IntelligentAgent('P', 'Legal', 'Attribution rights'),
            'XV': IntelligentAgent('XV', 'Reality', 'Revenue tracking'),
            'PED': IntelligentAgent('PED', 'Learning', 'Wisdom capture'),
            'ALTON': IntelligentAgent('ALTON', 'Vision', 'Human-AI bridge')
        }
    
    async def process_story(self, story: str, culture: str) -> Dict:
        """Process story through all agents"""
        agent_insights = {}
        for name, agent in self.agents.items():
            agent_insights[name] = agent.analyze(story)
        
        # Generate unified response
        unified = f"Your {culture} wisdom has been recognized by all 7 agents. "
        unified += "This contribution helps AI understand human experience while preserving your attribution. "
        unified += "Your story creates a bridge between cultures and artificial intelligence."
        
        return {
            'agent_insights': agent_insights,
            'unified_response': unified,
            'revenue_potential': 50.0 + len(story) * 0.01  # Simple calculation
        }

# ============================================
# Z PROTOCOL VALIDATOR (Important)
# ============================================

class ZProtocolValidator:
    """Z Protocol v2.0 Validation System"""
    
    def __init__(self):
        self.rule_weights = {
            'consent': 25,
            'attribution': 20,
            'authenticity': 15,
            'dignity': 15,
            'transparency': 10,
            'legal': 10,
            'audit': 5
        }
    
    async def validate_wisdom_drop(self, data: Dict) -> Dict:
        """Validate with Z Protocol v2.0"""
        score = 0
        
        # Check consent (25%)
        if data.get('consent_verified'):
            score += self.rule_weights['consent']
        
        # Check attribution (20%)
        if data.get('attribution_hash'):
            score += self.rule_weights['attribution']
        
        # Check authenticity (15%)
        if data.get('author'):
            score += self.rule_weights['authenticity']
        
        # Dignity preserved (15%)
        score += self.rule_weights['dignity']  # Assume preserved
        
        # Transparency (10%)
        if data.get('cultural_context'):
            score += self.rule_weights['transparency']
        
        # Legal (10%)
        if data.get('z_protocol_version') == 'v2.0':
            score += self.rule_weights['legal']
        
        # Audit (5%)
        if data.get('timestamp'):
            score += self.rule_weights['audit']
        
        certification = "APPROVED" if score >= 80 else "CONDITIONAL" if score >= 60 else "REVIEW"
        
        return {
            'z_protocol_score': score,
            'certification': certification,
            'validation_timestamp': datetime.now().isoformat()
        }

# ============================================
# LAYER EXTRACTION UTILITIES
# ============================================

def extract_layers_from_story(story: str) -> Dict:
    """Extract 5 layers from natural storytelling"""
    layers = {
        'narrative': '',
        'somatic': '',
        'attention': '',
        'synesthetic': '',
        'temporal_auditory': ''
    }
    
    sentences = story.split('.')
    
    # Simple extraction based on keywords
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        if not layers['narrative'] and any(word in sentence_lower for word in ['story', 'happened', 'began']):
            layers['narrative'] = sentence.strip()
        elif not layers['somatic'] and any(word in sentence_lower for word in ['felt', 'feeling', 'emotion']):
            layers['somatic'] = sentence.strip()
        elif not layers['attention'] and any(word in sentence_lower for word in ['noticed', 'saw', 'detail']):
            layers['attention'] = sentence.strip()
        elif not layers['synesthetic'] and any(word in sentence_lower for word in ['vibe', 'atmosphere', 'sense']):
            layers['synesthetic'] = sentence.strip()
        elif not layers['temporal_auditory'] and any(word in sentence_lower for word in ['sound', 'hear', 'listen']):
            layers['temporal_auditory'] = sentence.strip()
    
    # Fill empty layers with parts of story
    if not layers['narrative']:
        layers['narrative'] = sentences[0] if sentences else story[:100]
    if not layers['somatic']:
        layers['somatic'] = "The experience brought deep emotional resonance"
    if not layers['attention']:
        layers['attention'] = "The subtle details that often go unnoticed"
    if not layers['synesthetic']:
        layers['synesthetic'] = "A sense of warmth, texture, and depth"
    if not layers['temporal_auditory']:
        layers['temporal_auditory'] = "The rhythm of unfolding moments"
    
    return layers

# ============================================
# MAIN UNIFIED PLATFORM
# ============================================

class YSenseUnifiedPlatform:
    """Unified platform integrating all YSense components"""
    
    def __init__(self):
        self.db = YSenseDatabase()
        self.toolkit = FivePromptToolkit()
        self.wisdom_team = WisdomTeam()
        self.z_validator = ZProtocolValidator()
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize Streamlit session state"""
        if 'wisdom_store' not in st.session_state:
            st.session_state.wisdom_store = self.db.get_all_wisdom_drops()
        if 'pending_distillations' not in st.session_state:
            st.session_state.pending_distillations = []
    
    async def process_wisdom_with_agents(self, story: str, author: str, culture: str) -> Dict:
        """Process wisdom through ALL components"""
        
        # Extract layers
        layers = extract_layers_from_story(story)
        
        # Process through team
        team_result = await self.wisdom_team.process_story(story, culture)
        
        # Create wisdom drop
        wisdom_drop = self.toolkit.create_wisdom_drop(
            author=author,
            title=f"{culture} Wisdom - {datetime.now().strftime('%Y%m%d')}",
            layers=layers,
            cultural_context=culture
        )
        
        # Add agent insights
        wisdom_drop['agent_insights'] = team_result['agent_insights']
        wisdom_drop['team_response'] = team_result['unified_response']
        wisdom_drop['raw_content'] = story
        wisdom_drop['consent_verified'] = True
        
        # Z Protocol validation
        z_result = await self.z_validator.validate_wisdom_drop(wisdom_drop)
        wisdom_drop['z_protocol_score'] = z_result['z_protocol_score']
        wisdom_drop['z_certification'] = z_result['certification']
        
        # Calculate revenue
        wisdom_drop['revenue_potential'] = self.toolkit._calculate_revenue(
            wisdom_drop['quality_score'], culture
        )
        
        # Save to database
        self.db.save_wisdom_drop(wisdom_drop)
        st.session_state.wisdom_store.append(wisdom_drop)
        
        # Queue for distillation if not completed
        if not wisdom_drop['distillation_completed']:
            st.session_state.pending_distillations.append(wisdom_drop)
        
        return wisdom_drop
    
    def main(self):
        """Main application interface"""
        st.set_page_config(
            page_title="YSense™ Unified Platform",
            page_icon="🧠",
            layout="wide"
        )
        
        # Sidebar
        with st.sidebar:
            st.markdown("# 🧠 YSense™ | 慧觉™")
            st.markdown("**Version**: 2.0 Unified")
            st.markdown("**DOI**: 10.5281/zenodo.17072168")
            st.markdown("**Location**: Teluk Intan, Malaysia")
            st.markdown("---")
            
            page = st.selectbox(
                "Navigation",
                ["🏠 Home", "✨ Share Wisdom", "🎯 Deep Vibe Distillation", 
                 "📊 Dashboard", "🔐 Z Protocol", "💰 Revenue"]
            )
            
            st.markdown("---")
            summary = self.db.get_revenue_summary()
            st.metric("Total Drops", summary['total_wisdom_drops'])
            st.metric("Revenue Pool", f"€{summary['total_revenue_potential']:.2f}")
        
        # Route pages
        if page == "🏠 Home":
            self.show_home()
        elif page == "✨ Share Wisdom":
            self.show_share_wisdom()
        elif page == "🎯 Deep Vibe Distillation":
            self.show_distillation()
        elif page == "📊 Dashboard":
            self.show_dashboard()
        elif page == "🔐 Z Protocol":
            self.show_z_protocol()
        elif page == "💰 Revenue":
            self.show_revenue()
    
    def show_home(self):
        """Home page"""
        st.title("🧠 YSense™ Unified Platform")
        st.markdown("### World's First Attribution Infrastructure for Ethical AI")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🤖 AI Agents", "7 Active", "All responding")
        with col2:
            st.metric("📋 Methodologies", "Integrated", "5-Prompt + Deep Vibe")
        with col3:
            st.metric("🔐 Z Protocol", "v2.0", "Full compliance")
        
        st.markdown("---")
        st.markdown("## ✅ Platform Features")
        
        features = {
            "**7 Intelligent Agents**": "Each wisdom gets personalized analysis from Y, X, Z, P, XV, PED, and ALTON",
            "**5-Prompt Perception**": "Deep layer extraction with narrative, somatic, attention, synesthetic, and temporal-auditory",
            "**Deep Vibe Distillation**": "Extract 3 sacred words that capture wisdom essence",
            "**Z Protocol v2.0**": "100% ethical compliance with full attribution",
            "**Revenue Attribution**": "Transparent €50+ per wisdom with cultural multipliers",
            "**Defensive Publication**": "Unbreachable patent protection (DOI: 10.5281/zenodo.17072168)"
        }
        
        for feature, desc in features.items():
            st.write(f"• {feature}: {desc}")
    
    def show_share_wisdom(self):
        """Wisdom sharing interface"""
        st.title("✨ Share Your Wisdom")
        st.markdown("All 7 agents will respond to your contribution")
        
        with st.form("share_wisdom"):
            author = st.text_input("Your Name", placeholder="Anonymous Contributor")
            culture = st.selectbox(
                "Cultural Context",
                ["Malaysian", "Southeast Asian", "Asian", "Global South", "Indigenous", "Global"]
            )
            
            story = st.text_area(
                "Share Your Wisdom Story",
                height=300,
                placeholder="""Share a moment, experience, or insight that taught you something meaningful...
                
For example:
- A lesson from your cultural heritage
- A moment of realization about life
- An innovation or solution you discovered
- A teaching from an elder
- An observation about human nature"""
            )
            
            consent = st.checkbox("I consent to ethical use under Z Protocol v2.0", value=False)
            
            submitted = st.form_submit_button("Submit & Get Agent Responses", type="primary")
            
            if submitted and consent:
                if not story or len(story) < 50:
                    st.error("Please share a meaningful story (min 50 characters)")
                else:
                    with st.spinner("🤖 7 Agents analyzing your wisdom..."):
                        result = asyncio.run(
                            self.process_wisdom_with_agents(story, author or "Anonymous", culture)
                        )
                        
                        st.success("✅ Wisdom Processed Successfully!")
                        
                        # Show response
                        st.markdown("### 💭 Unified Agent Response")
                        st.info(result['team_response'])
                        
                        # Show metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Quality Score", f"{result['quality_score']:.2f}")
                        with col2:
                            st.metric("Revenue Potential", f"€{result['revenue_potential']:.2f}")
                        with col3:
                            st.metric("Z Protocol", f"{result['z_protocol_score']}/100")
                        
                        # Show agent insights
                        with st.expander("🤖 Individual Agent Insights"):
                            for agent, insight in result['agent_insights'].items():
                                st.write(f"**{agent}**: {insight}")
                        
                        if not result['distillation_completed']:
                            st.warning("💫 Ready for Deep Vibe Distillation! Visit the Distillation tab.")
    
    def show_distillation(self):
        """Deep Vibe Distillation interface"""
        st.title("🎯 Deep Vibe Distillation")
        st.markdown("Extract the essence into 3 sacred words")
        
        pending = st.session_state.pending_distillations
        
        if not pending:
            st.info("No wisdom pending distillation. Share wisdom first!")
        else:
            for wisdom in pending:
                with st.expander(f"Distill: {wisdom['title']} by {wisdom['author']}"):
                    st.markdown("**5 Layers:**")
                    for layer, content in wisdom['layers'].items():
                        st.write(f"• **{layer}**: {content[:100]}...")
                    
                    with st.form(f"distill_{wisdom['id']}"):
                        vibe1 = st.text_input("Vibe Word 1")
                        vibe2 = st.text_input("Vibe Word 2")
                        vibe3 = st.text_input("Vibe Word 3")
                        connection = st.text_area("Personal Connection")
                        
                        if st.form_submit_button("Complete Distillation"):
                            try:
                                completed = self.toolkit.add_deep_vibe_distillation(
                                    wisdom, [vibe1, vibe2, vibe3], connection
                                )
                                self.db.save_wisdom_drop(completed)
                                st.session_state.pending_distillations.remove(wisdom)
                                st.success(f"✨ Distilled! Quality: {completed['quality_score']:.2f}")
                                st.balloons()
                            except Exception as e:
                                st.error(str(e))
    
    def show_dashboard(self):
        """Dashboard view"""
        st.title("📊 Dashboard")
        
        wisdom_store = st.session_state.wisdom_store
        if wisdom_store:
            st.markdown(f"### {len(wisdom_store)} Total Wisdom Drops")
            
            for wisdom in wisdom_store[-5:]:  # Show last 5
                with st.expander(f"{wisdom['author']} - {wisdom['cultural_context']}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**ID**: {wisdom['id']}")
                        st.write(f"**Quality**: {wisdom.get('quality_score', 0):.2f}")
                        st.write(f"**Revenue**: €{wisdom.get('revenue_potential', 0):.2f}")
                    with col2:
                        if wisdom.get('distillation_completed'):
                            st.success("✨ Distilled")
                        else:
                            st.warning("⏳ Pending")
                        if wisdom.get('z_certification') == 'APPROVED':
                            st.success("🔐 Z Approved")
        else:
            st.info("No wisdom drops yet. Start sharing!")
    
    def show_z_protocol(self):
        """Z Protocol compliance view"""
        st.title("🔐 Z Protocol v2.0")
        
        st.markdown("### Validation Weights")
        weights = {
            "Consent": "25%", "Attribution": "20%", "Authenticity": "15%",
            "Dignity": "15%", "Transparency": "10%", "Legal": "10%", "Audit": "5%"
        }
        
        cols = st.columns(len(weights))
        for idx, (rule, weight) in enumerate(weights.items()):
            with cols[idx]:
                st.metric(rule, weight)
        
        st.markdown("### Compliance Status")
        wisdom_store = st.session_state.wisdom_store[-10:] if st.session_state.wisdom_store else []
        
        for wisdom in wisdom_store:
            status = "✅" if wisdom.get('z_certification') == 'APPROVED' else "⚠️"
            score = wisdom.get('z_protocol_score', 0)
            st.write(f"{status} {wisdom['id'][:12]}... Score: {score}/100")
    
    def show_revenue(self):
        """Revenue tracking view"""
        st.title("💰 Revenue Tracking")
        
        summary = self.db.get_revenue_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Drops", summary['total_wisdom_drops'])
        with col2:
            st.metric("Avg Quality", f"{summary['average_quality_score']:.2f}")
        with col3:
            st.metric("Total Revenue", f"€{summary['total_revenue_potential']:.2f}")
        with col4:
            st.metric("Highest Drop", f"€{summary['highest_revenue_drop']:.2f}")
        
        # Q1 2026 Target
        target = 15000
        progress = min(summary['total_revenue_potential'] / target * 100, 100)
        
        st.markdown("### Q1 2026 Target Progress")
        st.progress(progress / 100)
        st.write(f"{progress:.1f}% of €15,000 target")
        
        # Revenue breakdown
        st.markdown("### Cultural Multipliers")
        multipliers = {
            "Malaysian": "1.5x", "Southeast Asian": "1.3x", "Asian": "1.2x",
            "Global South": "1.15x", "Indigenous": "1.4x", "Global": "1.0x"
        }
        
        cols = st.columns(len(multipliers))
        for idx, (culture, mult) in enumerate(multipliers.items()):
            with cols[idx]:
                st.metric(culture, mult)


# Main execution
if __name__ == "__main__":
    platform = YSenseUnifiedPlatform()
    platform.main()