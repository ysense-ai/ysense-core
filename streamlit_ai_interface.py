# 🌟 YSense Platform v4.0 - AI-Powered Story Interface

import streamlit as st
import asyncio
from datetime import datetime
import json
import random

# ==================== AI Recommendation Functions ====================

def generate_ai_vibe_recommendations(story: str, layers: dict) -> list:
    """Generate AI vibe word recommendations based on story analysis"""
    
    # Based on SAMPLE SHOWCASE patterns, create intelligent recommendations
    vibe_patterns = {
        "joy": ["Joy", "Wonder", "Awe", "Happiness", "Delight"],
        "love": ["Love", "Eternity", "Presence", "Connection", "Belonging"],
        "growth": ["Possibility", "Awakening", "Energy", "Transformation", "Discovery"],
        "peace": ["Stillness", "Enlightenment", "Connection", "Calm", "Serenity"],
        "struggle": ["Struggle", "Resilience", "Enjoyment", "Perseverance", "Strength"],
        "heritage": ["Roots", "Reverence", "Belonging", "Tradition", "Wisdom"],
        "music": ["Melodic", "Rhythmic", "Harmonic", "Sonic", "Musical"],
        "family": ["Warmth", "Togetherness", "Nurturing", "Bonding", "Care"],
        "nature": ["Natural", "Organic", "Pure", "Fresh", "Vital"],
        "creative": ["Creative", "Inspiring", "Imaginative", "Artistic", "Expressive"]
    }
    
    # Analyze story content for themes
    story_lower = story.lower()
    themes = []
    
    if any(word in story_lower for word in ["happy", "joy", "smile", "laugh", "delight"]):
        themes.append("joy")
    if any(word in story_lower for word in ["love", "heart", "care", "affection", "family"]):
        themes.append("love")
    if any(word in story_lower for word in ["grow", "learn", "discover", "new", "change"]):
        themes.append("growth")
    if any(word in story_lower for word in ["calm", "peace", "quiet", "still", "zen"]):
        themes.append("peace")
    if any(word in story_lower for word in ["sing", "music", "song", "melody", "sound"]):
        themes.append("music")
    if any(word in story_lower for word in ["daughter", "child", "family", "parent"]):
        themes.append("family")
    if any(word in story_lower for word in ["create", "art", "imagine", "design", "make"]):
        themes.append("creative")
    
    # Default themes if none detected
    if not themes:
        themes = ["joy", "love", "growth"]
    
    # Generate recommendations
    recommendations = []
    for theme in themes[:3]:  # Take first 3 themes
        if theme in vibe_patterns:
            recommendations.append(random.choice(vibe_patterns[theme]))
    
    # Fill remaining slots if needed
    while len(recommendations) < 3:
        remaining_themes = [t for t in vibe_patterns.keys() if t not in themes]
        if remaining_themes:
            theme = random.choice(remaining_themes)
            recommendations.append(random.choice(vibe_patterns[theme]))
        else:
            recommendations.append("Meaningful")
    
    return recommendations[:3]

def show_ai_story_interface():
    """Show the new AI-powered story analysis interface"""
    st.markdown("## 🤖 AI-Powered Wisdom Creation")
    st.info("✨ **Revolutionary v4.0 Feature:** Simply tell your story, and our AI will analyze it with 7 intelligent agents!")
    
    # Story input section
    st.markdown("### 📖 Step 1: Tell Your Story")
    
    with st.form("story_input_form"):
        story = st.text_area(
            "Your Story",
            placeholder="Describe your experience in your own words... Don't worry about structure - just tell your story naturally. Our AI will extract the 5 layers for you!",
            height=200,
            help="Share your experience naturally. Our AI will analyze it and extract the structured layers."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            experience_title = st.text_input(
                "Experience Title (Optional)",
                placeholder="Give your experience a title"
            )
        
        with col2:
            cultural_context = st.selectbox(
                "Cultural Context",
                ["Malaysian", "Malaysian Chinese", "Hokkien", "Southeast Asian", "Global"],
                help="Select the cultural context for better AI analysis"
            )
        
        analyze_button = st.form_submit_button("🧠 Analyze with AI", type="primary", use_container_width=True)
        
        if analyze_button and story:
            if len(story.strip()) < 50:
                st.error("⚠️ Please provide a story with at least 50 characters for meaningful AI analysis.")
            else:
                # Process with AI
                with st.spinner("🤖 AI is analyzing your story with 7 intelligent agents..."):
                    try:
                        # Call AI analysis API
                        analysis_result = api_call("POST", "wisdom/analyze-story", {
                            "story": story,
                            "experience_title": experience_title,
                            "cultural_context": cultural_context
                        }, authenticated=True)
                        
                        if analysis_result and analysis_result.get("success"):
                            # Store results in session state
                            st.session_state.ai_analysis = analysis_result
                            st.success("✅ AI analysis completed!")
                            st.rerun()
                        else:
                            st.error("❌ AI analysis failed. Please try again.")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

def show_ai_analysis_results():
    """Show AI analysis results and allow user review"""
    if not st.session_state.get("ai_analysis"):
        return
    
    analysis = st.session_state.ai_analysis
    
    st.markdown("## 🤖 AI Analysis Results")
    st.success("✨ Your story has been analyzed by 7 intelligent agents!")
    
    # Overall score and status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Score", f"{analysis['overall_score']:.1f}/10")
    with col2:
        st.metric("Processing Time", f"{analysis['processing_time']:.1f}s")
    with col3:
        st.metric("Status", analysis['status'].title())
    
    # Agent feedback
    st.markdown("### 🎯 Agent Feedback")
    agent_feedback = analysis.get("agent_feedback", {})
    
    feedback_cols = st.columns(2)
    for i, (agent_name, feedback) in enumerate(agent_feedback.items()):
        with feedback_cols[i % 2]:
            st.info(f"**{agent_name.replace('_', ' ').title()}:** {feedback}")
    
    # Extracted layers
    st.markdown("### 📝 Extracted Five Layers")
    st.info("Review and edit the AI-extracted layers below:")
    
    layers = analysis.get("layers", {})
    user_edits = {}
    
    # Layer editing interface
    layer_names = {
        "narrative": "1️⃣ Narrative Layer",
        "somatic": "2️⃣ Somatic Layer", 
        "attention": "3️⃣ Attention Layer",
        "synesthetic": "4️⃣ Synesthetic Layer",
        "temporal_auditory": "5️⃣ Temporal-Auditory Layer"
    }
    
    for layer_key, layer_name in layer_names.items():
        st.markdown(f"#### {layer_name}")
        
        # Show original AI extraction
        original_content = layers.get(layer_key, "")
        st.text_area(
            f"AI Extracted Content",
            value=original_content,
            height=100,
            key=f"original_{layer_key}",
            disabled=True
        )
        
        # User edit area
        edited_content = st.text_area(
            f"Your Edit (Optional)",
            value=original_content,
            height=100,
            key=f"edit_{layer_key}",
            help="Edit the AI-extracted content or keep as is"
        )
        
        if edited_content != original_content:
            user_edits[layer_key] = edited_content
            
            # Character count
            char_count = len(edited_content.strip())
            if char_count < 20:
                st.warning(f"⚠️ Needs at least 20 characters. Current: {char_count}")
            else:
                st.success(f"✅ {char_count} characters")
    
    # Recommendations
    recommendations = analysis.get("recommendations", [])
    if recommendations:
        st.markdown("### 💡 AI Recommendations")
        for rec in recommendations:
            st.markdown(f"• {rec}")
    
    # Review and continue button
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Analyze Again", type="secondary"):
            st.session_state.ai_analysis = None
            st.rerun()
    
    with col2:
        if st.button("✅ Continue to Deep Vibe Distillation", type="primary"):
            # Store review data
            st.session_state.layer_review = {
                "layers": layers,
                "user_edits": user_edits,
                "approved": True
            }
            st.session_state.current_step = "deep_vibe"
            st.rerun()

def show_deep_vibe_distillation():
    """Show Deep Vibe Distillation interface - AI recommends, Human decides"""
    st.markdown("## 🌊 Deep Vibe Distillation")
    st.info("✨ **Human Experience is Most Valuable** - AI recommends, you decide!")
    
    analysis = st.session_state.get("ai_analysis", {})
    review = st.session_state.get("layer_review", {})
    
    # Get final layers
    final_layers = review.get("layers", {}).copy()
    final_layers.update(review.get("user_edits", {}))
    
    # AI Vibe Word Recommendations (based on SAMPLE SHOWCASE patterns)
    st.markdown("### 🤖 AI Vibe Word Recommendations")
    st.info("💡 **AI suggests these vibe words based on your story analysis. You can use them or choose your own!**")
    
    # Generate AI recommendations based on story content
    ai_recommendations = generate_ai_vibe_recommendations(analysis.get("story", ""), final_layers)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**AI Suggestion 1:**")
        st.info(f"💡 **{ai_recommendations[0]}**")
    with col2:
        st.markdown("**AI Suggestion 2:**")
        st.info(f"💡 **{ai_recommendations[1]}**")
    with col3:
        st.markdown("**AI Suggestion 3:**")
        st.info(f"💡 **{ai_recommendations[2]}**")
    
    st.markdown("---")
    
    with st.form("deep_vibe_form"):
        st.markdown("### 🎵 Your Vibe Words (Your Choice)")
        st.info("✨ **Choose YOUR 3 words that capture the essence of YOUR experience**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            vibe_word_1 = st.text_input(
                "Vibe Word 1", 
                placeholder="Your first word...",
                help="Choose a word that captures the essence of your experience"
            )
        with col2:
            vibe_word_2 = st.text_input(
                "Vibe Word 2", 
                placeholder="Your second word...",
                help="Choose a word that captures the essence of your experience"
            )
        with col3:
            vibe_word_3 = st.text_input(
                "Vibe Word 3", 
                placeholder="Your third word...",
                help="Choose a word that captures the essence of your experience"
            )
        
        st.markdown("### 💭 Why These Three Words?")
        st.info("🌟 **Share why you chose these specific words and what they mean to you**")
        
        vibe_words_explanation = st.text_area(
            "Your Vibe Words Explanation",
            placeholder="Explain why you chose these three words. What do they mean to you? How do they capture your experience? What feelings do they represent?",
            height=120,
            help="This is your personal interpretation - the most valuable part of your wisdom!"
        )
        
        st.markdown("### 💝 Personal Connection")
        personal_connection = st.text_area(
            "Personal Connection",
            placeholder="What does this experience mean to you personally? How does it connect to your life, values, or memories?",
            height=150,
            help="Share your personal connection to this experience"
        )
        
        st.markdown("### ✨ Essence Description (Optional)")
        essence = st.text_area(
            "Essence Description",
            placeholder="Describe the core essence or meaning of this experience...",
            height=100,
            help="Optional: Add a final essence description"
        )
        
        submit_button = st.form_submit_button("🌟 Complete Wisdom Drop", type="primary", use_container_width=True)
        
        if submit_button:
            vibe_words = [vibe_word_1, vibe_word_2, vibe_word_3]
            
            if not all(vibe_words):
                st.error("⚠️ Please provide all 3 vibe words")
            elif len(personal_connection.strip()) < 20:
                st.error("⚠️ Personal connection must contain at least 20 characters")
            elif len(vibe_words_explanation.strip()) < 20:
                st.error("⚠️ Please explain why you chose these three words (at least 20 characters)")
            else:
                # Create complete wisdom drop
                with st.spinner("🌟 Creating your wisdom drop..."):
                    try:
                        # Prepare data
                        story_data = {
                            "story": analysis.get("story", ""),
                            "experience_title": analysis.get("experience_title", ""),
                            "cultural_context": analysis.get("cultural_context", "Global")
                        }
                        
                        review_data = {
                            "layers": final_layers,
                            "user_edits": review.get("user_edits", {}),
                            "approved": True
                        }
                        
                        vibe_data = {
                            "vibe_words": vibe_words,
                            "vibe_words_explanation": vibe_words_explanation,
                            "personal_connection": personal_connection,
                            "essence_description": essence
                        }
                        
                        # Create wisdom drop
                        result = api_call("POST", "wisdom/create-wisdom-drop", {
                            "story_input": story_data,
                            "review": review_data,
                            "vibe_input": vibe_data
                        }, authenticated=True)
                        
                        if result and result.get("success"):
                            st.success("🎉 Wisdom drop created successfully!")
                            
                            # Show results
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Quality Score", f"{result['quality_score']:.1f}/10")
                            with col2:
                                st.metric("Revenue Potential", f"€{result['revenue_potential']:.0f}")
                            
                            # Show agent feedback
                            st.markdown("### 🎯 Final Agent Feedback")
                            agent_feedback = result.get("agent_feedback", {})
                            for agent_name, feedback in agent_feedback.items():
                                st.info(f"**{agent_name.replace('_', ' ').title()}:** {feedback}")
                            
                            # Clear session state
                            st.session_state.ai_analysis = None
                            st.session_state.layer_review = None
                            st.session_state.current_step = "dashboard"
                            
                            st.markdown("---")
                            if st.button("🏠 Return to Dashboard", type="primary"):
                                st.rerun()
                        
                        else:
                            st.error("❌ Failed to create wisdom drop")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

def show_ai_workflow_navigation():
    """Show navigation for AI workflow"""
    st.markdown("### 🤖 AI-Powered Workflow")
    
    steps = [
        ("📖 Story Input", "story_input"),
        ("🤖 AI Analysis", "ai_analysis"), 
        ("✏️ Review & Edit", "review"),
        ("🌊 Deep Vibe", "deep_vibe"),
        ("🌟 Complete", "complete")
    ]
    
    current_step = st.session_state.get("current_step", "story_input")
    
    # Create step indicators
    cols = st.columns(len(steps))
    for i, (step_name, step_key) in enumerate(steps):
        with cols[i]:
            if step_key == current_step:
                st.success(f"**{step_name}**")
            elif step_key in ["story_input"] or (current_step == "ai_analysis" and step_key == "review"):
                st.info(step_name)
            else:
                st.text(step_name)

def show_ai_analysis_history():
    """Show user's AI analysis history"""
    st.markdown("## 📊 AI Analysis History")
    
    try:
        with st.spinner("Loading your AI analysis history..."):
            history = api_call("GET", "wisdom/analysis-history", authenticated=True)
            
            if history and history.get("success"):
                history_data = history.get("history", [])
                
                if history_data:
                    st.info(f"📈 You have {len(history_data)} AI-analyzed wisdom drops")
                    
                    for item in history_data:
                        with st.expander(f"📖 {item['title']} - Score: {item['quality_score']:.1f}/10"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Quality Score", f"{item['quality_score']:.1f}/10")
                            with col2:
                                st.metric("Revenue Potential", f"€{item['revenue_potential']:.0f}")
                            with col3:
                                st.metric("Cultural Context", item['cultural_context'])
                            
                            st.caption(f"Created: {item['created_at']}")
                            if item.get('ai_generated'):
                                st.success("🤖 AI-Generated")
                else:
                    st.info("📝 No AI analysis history yet. Create your first AI-powered wisdom drop!")
            else:
                st.error("❌ Failed to load analysis history")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Main AI workflow function
def show_ai_wisdom_creation():
    """Main AI-powered wisdom creation interface"""
    
    # Show navigation
    show_ai_workflow_navigation()
    
    # Determine current step
    current_step = st.session_state.get("current_step", "story_input")
    
    if current_step == "story_input":
        show_ai_story_interface()
    elif current_step == "ai_analysis":
        show_ai_analysis_results()
    elif current_step == "deep_vibe":
        show_deep_vibe_distillation()
    else:
        show_ai_story_interface()
    
    # Show history in sidebar
    with st.sidebar:
        st.markdown("### 📊 Your AI History")
        show_ai_analysis_history()
