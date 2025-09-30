def add_header_image():
    """Add the header with logo and Human-AI collaboration banner"""
    try:
        import streamlit.components.v1 as components
        
        header_html = """
        <div style="position: relative; background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                    padding: 2rem; margin: -1rem -1rem 2rem -1rem; 
                    text-align: center; color: white; border-radius: 0 0 20px 20px; overflow: hidden; min-height: 200px;">
            
            <!-- Logo Area (Left) -->
            <div style="position: absolute; left: 2rem; top: 50%; transform: translateY(-50%); z-index: 10;">
                <!-- Water Droplet Logo -->
                <svg width="80" height="80" viewBox="0 0 80 80">
                    <!-- Water droplet -->
                    <ellipse cx="40" cy="25" rx="12" ry="18" fill="#60a5fa" opacity="0.9"/>
                    <ellipse cx="40" cy="25" rx="8" ry="12" fill="#93c5fd" opacity="0.7"/>
                    <ellipse cx="40" cy="25" rx="4" ry="6" fill="#dbeafe" opacity="0.8"/>
                    <!-- Water surface peak -->
                    <ellipse cx="40" cy="45" rx="8" ry="3" fill="#3b82f6" opacity="0.8"/>
                    <!-- Concentric ripples -->
                    <circle cx="40" cy="45" r="15" fill="none" stroke="#3b82f6" stroke-width="1.5" opacity="0.6"/>
                    <circle cx="40" cy="45" r="22" fill="none" stroke="#3b82f6" stroke-width="1" opacity="0.4"/>
                    <circle cx="40" cy="45" r="30" fill="none" stroke="#3b82f6" stroke-width="0.8" opacity="0.3"/>
                    <!-- Light reflection on droplet -->
                    <ellipse cx="36" cy="20" rx="3" ry="6" fill="#ffffff" opacity="0.6"/>
                    <!-- Animated ripples -->
                    <circle cx="40" cy="45" r="15" fill="none" stroke="#60a5fa" stroke-width="2" opacity="0.8">
                        <animate attributeName="r" values="15;25" dur="2s" repeatCount="indefinite"/>
                        <animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/>
                    </circle>
                </svg>
            </div>
            
            <!-- Human-AI Collaboration Banner (Center-Right) -->
            <svg width="100%" height="200" viewBox="0 0 800 200" style="position: absolute; top: 0; left: 0; opacity: 0.8; z-index: 1;">
                <!-- Neural network background -->
                <defs>
                    <pattern id="neuralNetwork" x="0" y="0" width="80" height="80" patternUnits="userSpaceOnUse">
                        <circle cx="40" cy="40" r="1" fill="#3b82f6" opacity="0.3"/>
                        <line x1="0" y1="0" x2="80" y2="80" stroke="#3b82f6" stroke-width="0.5" opacity="0.2"/>
                        <line x1="80" y1="0" x2="0" y2="80" stroke="#3b82f6" stroke-width="0.5" opacity="0.2"/>
                    </pattern>
                </defs>
                <rect width="800" height="200" fill="url(#neuralNetwork)"/>
                
                <!-- Data streams flowing to center -->
                <g opacity="0.6">
                    <path d="M0,100 Q200,80 400,100" stroke="#3b82f6" stroke-width="2" fill="none"/>
                    <path d="M800,100 Q600,120 400,100" stroke="#3b82f6" stroke-width="2" fill="none"/>
                    <path d="M400,0 Q350,50 400,100" stroke="#3b82f6" stroke-width="2" fill="none"/>
                    <path d="M400,200 Q450,150 400,100" stroke="#3b82f6" stroke-width="2" fill="none"/>
                </g>
                
                <!-- Human hand (left) -->
                <g transform="translate(200, 80)" opacity="0.8">
                    <path d="M0,0 Q-8,-4 -12,4 Q-16,12 -14,20 Q-12,28 -8,32 Q-4,36 0,32 Q4,28 6,20 Q8,12 4,4 Q0,-4 0,0 Z" fill="#fbbf24" stroke="#f59e0b" stroke-width="1.5"/>
                    <ellipse cx="-6" cy="12" rx="2" ry="6" fill="#fbbf24" transform="rotate(-15 -6 12)"/>
                    <ellipse cx="-2" cy="10" rx="2" ry="6" fill="#fbbf24" transform="rotate(-5 -2 10)"/>
                    <ellipse cx="2" cy="8" rx="2" ry="6" fill="#fbbf24" transform="rotate(5 2 8)"/>
                    <ellipse cx="6" cy="10" rx="2" ry="6" fill="#fbbf24" transform="rotate(15 6 10)"/>
                </g>
                
                <!-- AI/Robot hand (right) -->
                <g transform="translate(600, 80)" opacity="0.8">
                    <path d="M0,0 Q-8,-4 -12,4 Q-16,12 -14,20 Q-12,28 -8,32 Q-4,36 0,32 Q4,28 6,20 Q8,12 4,4 Q0,-4 0,0 Z" fill="#e5e7eb" stroke="#9ca3af" stroke-width="1.5"/>
                    <ellipse cx="-6" cy="12" rx="2" ry="6" fill="#e5e7eb" transform="rotate(-15 -6 12)"/>
                    <ellipse cx="-2" cy="10" rx="2" ry="6" fill="#e5e7eb" transform="rotate(-5 -2 10)"/>
                    <ellipse cx="2" cy="8" rx="2" ry="6" fill="#e5e7eb" transform="rotate(5 2 8)"/>
                    <ellipse cx="6" cy="10" rx="2" ry="6" fill="#e5e7eb" transform="rotate(15 6 10)"/>
                </g>
                
                <!-- Central light burst - The Genesis -->
                <g transform="translate(400, 100)" opacity="0.9">
                    <circle cx="0" cy="0" r="30" fill="#fbbf24" opacity="0.4"/>
                    <circle cx="0" cy="0" r="20" fill="#fbbf24" opacity="0.6"/>
                    <circle cx="0" cy="0" r="10" fill="#ffffff" opacity="0.9"/>
                    <g stroke="#ffffff" stroke-width="2" opacity="0.8">
                        <line x1="-20" y1="-20" x2="-28" y2="-28"/>
                        <line x1="20" y1="-20" x2="28" y2="-28"/>
                        <line x1="-20" y1="20" x2="-28" y2="28"/>
                        <line x1="20" y1="20" x2="28" y2="28"/>
                    </g>
                </g>
                
                <!-- Data particles -->
                <g opacity="0.7">
                    <circle cx="300" cy="80" r="1.5" fill="#3b82f6">
                        <animate attributeName="cx" values="300;400" dur="3s" repeatCount="indefinite"/>
                        <animate attributeName="cy" values="80;100" dur="3s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="500" cy="120" r="1.5" fill="#3b82f6">
                        <animate attributeName="cx" values="500;400" dur="3s" repeatCount="indefinite"/>
                        <animate attributeName="cy" values="120;100" dur="3s" repeatCount="indefinite"/>
                    </circle>
                </g>
            </svg>
            
            <!-- Main content -->
            <div style="position: relative; z-index: 10;">
                <h1 style="margin: 0; font-size: 2.5em; font-weight: bold; 
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    YSense™ v4.1 | 慧觉™
                </h1>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.1em; opacity: 0.9; 
                          text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                    The Genesis of Human-AI Wisdom Collaboration
                </p>
                
                <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 0.9em;">🤖 AI Analysis</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 0.9em;">📚 Wisdom Attribution</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem 1rem; border-radius: 20px; 
                                backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                        <span style="font-size: 0.9em;">⚖️ Z Protocol v2.0</span>
                    </div>
                </div>
            </div>
        </div>
        """
        components.html(header_html, height=200)
        
    except Exception as e:
        st.error(f"Error loading header: {e}")



