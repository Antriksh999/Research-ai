from datetime import datetime
from pathlib import Path
from textwrap import dedent
import os

from agno.agent import Agent
from agno.models.ollama import Ollama

from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.googlesearch import GoogleSearchTools

from dotenv import load_dotenv
import streamlit as st

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="Research Content Extractor Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    # API Key input
    st.subheader("🔑 API Key")
    api_key_input = st.text_input(
        "Google Gemini API Key:",
        value="",
        type="password",
        help="Required for Gemini model. Not saved and use for security after web-app tab close.",
    )

    # Model configuration
    st.subheader("Model Selection")
    model_input1 = st.text_input(
        "Ollama Model ID:",
        value="llama3.1",
        help="Default: llama3.1 (local model)"
    )

    model_input2 = st.text_input(
        "Google Gemini Model ID:",
        value="gemini-2.0-flash",
        help="Default: gemini-2.0-flash (requires API key)"
    )
    
    # Model preference
    model_preference = st.radio(
        "Model Preference:",
        ["Gemini Only", "Auto (Gemini first, fallback to Ollama)", "Ollama Only"],
        index=0,
        help="Note: Ollama requires local installation and won't work on Streamlit Cloud"
    )
    
    if api_key_input:
        # Only set for current session, don't persist
        os.environ["GOOGLE_API_KEY"] = api_key_input
        st.success("✅ Gemini API Key configured (session only)")
    else:
        # Check if API key exists in environment (from Streamlit secrets)
        if os.getenv("GOOGLE_API_KEY"):
            api_key_input = os.getenv("GOOGLE_API_KEY")
            st.success("✅ Gemini API Key loaded from environment")
        elif model_preference in ["Auto (Gemini first, fallback to Ollama)", "Gemini Only"]:
            st.warning("⚠️ Gemini requires API key")
        else:
            st.info("💡 Using Ollama (local model)")
        
    # Cloud deployment warning
    if model_preference == "Ollama Only":
        st.warning("⚠️ Note: Ollama won't work on Streamlit Cloud. Please use Gemini or Auto mode.")
        
    
    # Web search tools selection
    st.subheader("Search Tools")
    use_wikipedia = st.checkbox(
        "📚 Wikipedia Search", 
        value=True,
        help="Access comprehensive encyclopedia content"
    )
    use_duckduckgo = st.checkbox(
        "🦆 DuckDuckGo Search", 
        value=True,
        help="Privacy-focused web search engine"
    )
    use_googlesearch = st.checkbox(
        "🔍 Google Search", 
        value=False,
        help="Use Google Search for additional information (requires API key)"
    )
    
    if not use_wikipedia and not use_duckduckgo and not use_googlesearch:
        st.error("❌ Please select at least one search tool")
    
    # Report settings
    st.subheader("Report Settings")
    report_length = st.selectbox(
        "Report Length:",
        ["Standard (5+ pages)", "Extended (8+ pages)", "Comprehensive (10+ pages)"],
        index=0
    )
    
    include_citations = st.checkbox(
        "Include detailed citations", 
        value=True
    )
    
    # About section
    st.subheader("About")
    st.info("This AI-powered research assistant generates comprehensive academic reports using multiple search tools and Google Gemini AI.")
    
    # Instructions
    with st.expander("💡 How to use"):
        st.write("""
        1. Enter your API key above and add your key from google or use ollama for local llm.
        2. Select your preferred search tools.
        3. Enter your research topic in the main area.
        4. The report will be generated and saved automatically.
        5. Use the download button to get your report.
        """)

today = datetime.now().strftime("%Y-%m-%d")

st.title("Research Content Extractor Agent")
st.markdown("*AI-Powered Academic Research Report Generator*")

# Check if we need to clear the input after successful generation
if st.session_state.get('clear_input', False):
    st.session_state['research_topic'] = ""
    st.session_state['clear_input'] = False

input_prompt = st.text_area(
    "Enter Your Research Topic:",
    placeholder="Type your basic to detailed prompt here...",
    height=150,
    key="research_topic"
)

# Example topics
if not input_prompt:
    with st.expander("Example Research Topics", expanded=True):
        example_topics = [
            "The impact of artificial intelligence on healthcare delivery",
            "Sustainable energy solutions for urban environments", 
            "Climate change adaptation strategies in coastal cities",
            "The future of quantum computing in cybersecurity",
            "Blockchain technology applications beyond cryptocurrency",
            "Gene therapy advances in treating rare diseases"
        ]
        
        cols = st.columns(2)
        for i, topic in enumerate(example_topics):
            with cols[i % 2]:
                if st.button(f"{topic}", key=f"topic_{i}"):
                    st.session_state.selected_topic = topic
                    st.rerun()

# Handle selected topic
if hasattr(st.session_state, 'selected_topic'):
    input_prompt = st.session_state.selected_topic
    del st.session_state.selected_topic

# Create tools list based on user selection
tools = []

if use_wikipedia:
    tools.append(WikipediaTools())

if use_duckduckgo:
    tools.append(DuckDuckGoTools())

if use_googlesearch:
    tools.append(GoogleSearchTools())

# Only create agent if tools are selected
if not tools:
    st.warning("⚠️ Please select at least one search tool from the sidebar")
    st.stop()

# Model selection logic
def get_selected_model():
    """Select model based on user preference and availability"""
    
    if model_preference == "Ollama Only":
        if not model_input1:
            st.error("❌ Please specify Ollama model ID")
            return None
        try:
            return Ollama(id=model_input1)
        except Exception as e:
            st.error(f"❌ Ollama connection failed: {str(e)}")
            st.info("💡 Ollama requires local installation. Try using Gemini instead.")
            return None
    
    elif model_preference == "Gemini Only":
        if not api_key_input:
            st.error("❌ Gemini requires API key")
            return None
        if not model_input2:
            st.error("❌ Please specify Gemini model ID")
            return None
        try:
            return Gemini(id=model_input2)
        except Exception as e:
            st.error(f"❌ Gemini connection failed: {str(e)}")
            return None
    
    else:  # Auto mode - try Gemini first, fallback to Ollama
        if api_key_input and model_input2:
            try:
                return Gemini(id=model_input2)
            except Exception as e:
                st.warning(f"⚠️ Gemini failed: {str(e)}. Trying Ollama...")
                if model_input1:
                    try:
                        return Ollama(id=model_input1)
                    except Exception as e2:
                        st.error(f"❌ Both models failed. Gemini: {str(e)}, Ollama: {str(e2)}")
                        st.info("💡 Please check your API key or use Gemini Only mode")
                        return None
                else:
                    st.error("❌ No fallback model available")
                    return None
        elif model_input1:
            try:
                return Ollama(id=model_input1)
            except Exception as e:
                st.error(f"❌ Ollama failed: {str(e)}")
                st.info("💡 Ollama requires local installation. Please add Gemini API key or use Gemini Only mode")
                return None
        else:
            st.error("❌ No model configured")
            return None

# Get the selected model
selected_model = get_selected_model()
if not selected_model:
    st.stop()

agent = Agent(
    model=selected_model,
    tools=tools,
    description=dedent("""\
        You are Professor, a distinguished AI research scientist with expertise
        in analyzing and synthesizing complex information. Your specialty lies in creating
        compelling, fact-based reports and research papers that combine academic rigor with engaging narrative.

        Your writing style is:
        - Clear and authoritative
        - Engaging but professional
        - Fact-focused with proper citations
        - Accessible to educated non-specialists\
    """),
    instructions=dedent("""\
        Begin by running 5 distinct searches to gather comprehensive information.
        Analyze and cross-reference sources for accuracy and relevance.
        Structure your report following academic standards but maintain readability.
        Include only verifiable facts with proper citations.
        Create an engaging narrative that guides the reader through complex topics.
        End with actionable takeaways and future implications.
        Analyze and Mention real references links.\
    """),
    expected_output=dedent(f"""\
    A professional research report in markdown format and based on A4 paper size with atleast {report_length} content , with the following structure:

    # Compelling Title That Captures the Topic's Essence

    ## Abstract
    {{Brief summary of the report's content and findings}}

    ## Keywords
    {{List of relevant keywords for search optimization}}

    ## Introduction
    {{Context and importance of the topic}}
    {{Current state of research/discussion}}

    ## Literature Review
    {{Detail Overview of existing literature}}
    {{Key theories, models, or frameworks}}

    ## Methodology
    {{Description of research methods or analytical approaches used}}

    ## Research Gaps
    {{Identification of gaps in current research}}

    ## Problem Identification
    {{Specific problem or question addressed by the report}}

    ## Design and Implementation
    {{Description of design choices and implementation details}}

    ## Results
    {{Presentation of findings, data, or outcomes}}
    {{Visuals or tables if applicable}}

    ## Future Scope
    {{Discussion of potential future research directions or applications}}

    ## Conclusion
    {{Summary of key findings and their significance}}

    ## Key Takeaways
    - {{Bullet point 1}}
    - {{Bullet point 2}}
    - {{Bullet point 3}}
    - {{Bullet point 4}}
    - {{Bullet point 5}}

    ## References
    - [Source 1](link) - Key finding/quote
    - [Source 2](link) - Key finding/quote
    - [Source 3](link) - Key finding/quote
    - [Source 4](link) - Key finding/quote
    - [Source 5](link) - Key finding/quote

    ---
    Report generated by Antriksh Sharma's created Agent on {today}
    Tools: {', '.join([tool.__class__.__name__.replace('Tools', '') for tool in tools])}
    """),
    markdown=True,
    show_tool_calls=False,
    add_datetime_to_instructions=True,
)

if input_prompt:
    # Show current configuration
    with st.expander("🔧 Current Configuration", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🔍 Selected Search Tools:**")
            if use_wikipedia:
                st.write("✅ Wikipedia")
            if use_duckduckgo:
                st.write("✅ DuckDuckGo")
            if use_googlesearch:
                st.write("✅ Google Search")
        with col2:
            st.write("**Model Configuration:**")
            model_type = type(selected_model).__name__
            model_id = selected_model.id if hasattr(selected_model, 'id') else "Unknown"
            st.write(f"🧠 Model: {model_type} ({model_id})")
            st.write(f"📄 Length: {report_length}")
            st.write(f"📎 Citations: {'Enabled' if include_citations else 'Disabled'}")
    
    st.write("## 📊 Research Report")
    
    with st.spinner("Generating research report..."):
        try:
            # Generate the report
            with st.empty():
                st.info("Agent is researching your topic...")
                response = agent.run(input_prompt, stream=False)
            
            # Clear any intermediate outputs and display only the final result
            st.markdown("### Generated Research Report")
            st.markdown("---")
            
            # Display the response content
            st.markdown(response.content)
            
            # Download section
            st.markdown("---")
            st.markdown("### � Download Report")
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in input_prompt[:30] if c.isalnum() or c in (' ', '-')).strip().replace(' ', '_')
            filename = f"research_report_{timestamp}_{safe_prompt}.md"
            
            # Download button
            st.download_button(
                label="📥 Download Report",
                data=response.content,
                file_name=filename,
                mime="text/markdown",
                help="Download the research report as a markdown file"
            )
            
            # Set flag to clear input on next run
            st.session_state['clear_input'] = True
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            st.info("Try refreshing the page or checking your API key configuration")

else:
    # Welcome message when no input
    st.info("**Get started:** Enter a research topic above or select from example topics to generate a comprehensive academic report.")