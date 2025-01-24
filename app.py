"""
Brand Media Analyzer using Streamlit and Vertex AI Gemini
"""

import os
import json
import tempfile
from datetime import datetime
import streamlit as st
from google.cloud import storage
from vertex_libs.gemini_client import GeminiClient
from google.api_core import exceptions as google_exceptions
from typing import Optional
from dotenv import load_dotenv
import subprocess
from pathlib import Path
from google.genai import types
from schemas.brand_analysis_schema import BRAND_ANALYSIS_SCHEMA
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import base64

# Load environment variables from .env file in development
if os.path.exists(".env"):
    load_dotenv()

# Initialize Vertex AI client
gemini_client = GeminiClient()

# Get environment variables with defaults for Cloud Run
bucket_name = os.environ.get("GCP_BUCKET_NAME")
project_id = os.environ.get("GCP_PROJECT")

# Configure Streamlit
st.set_page_config(
    page_title="Brand Media Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add health check endpoint for Cloud Run
def check_health():
    return {"status": "healthy"}

# Add debug logging for environment variables
if os.getenv("GCP_BUCKET_NAME"):
    print(f"Debug: GCP bucket name is set to: {os.getenv('GCP_BUCKET_NAME')}")
else:
    print("Debug: GCP_BUCKET_NAME is not set")

def upload_to_gcs(video_file, bucket_name: str) -> Optional[tuple[str, str]]:
    """
    Upload a video file to Google Cloud Storage.
    
    Args:
        video_file: The video file from st.file_uploader
        bucket_name: Name of the GCS bucket
        
    Returns:
        tuple: (public_url, gcs_path) of the uploaded file, or None if upload fails
    """
    try:
        # Create storage client
        storage_client = storage.Client()
        
        # Get bucket
        bucket = storage_client.bucket(bucket_name)
        
        # Create a unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"uploads/{timestamp}_{video_file.name}"
        blob = bucket.blob(blob_name)
        
        # Create a temporary file to store the video
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(video_file.getvalue())
            tmp_file.flush()
            
            # Upload the file
            blob.upload_from_filename(tmp_file.name)
        
        # Clean up the temporary file
        os.unlink(tmp_file.name)
        
        # Make the blob publicly accessible and get the URL
        blob.make_public()
        gcs_path = f"gs://{bucket_name}/{blob_name}"
        return blob.public_url, gcs_path
        
    except Exception as e:
        st.error(f"Error uploading to GCS: {str(e)}")
        return None

def analyze_brand_compatibility(gcs_path: str) -> Optional[dict]:
    """
    Analyze brand compatibility from the video using Vertex AI Gemini.
    
    Args:
        gcs_path: GCS path to the video (gs://bucket/path/to/video.mp4)
        
    Returns:
        dict: JSON response containing the brand analysis, or None if analysis fails
    """
    try:
        # Read the prompt template
        with open("prompts/branding_prompt.md", "r") as f:
            prompt_template = f.read()
        
        # Create the prompt with proper content types
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(prompt_template),
                    types.Part(
                        file_data=types.FileData(
                            mime_type="video/mp4",
                            file_uri=gcs_path
                        )
                    )
                ]
            )
        ]
        
        # Generate analysis using Gemini with JSON configuration
        response = gemini_client.generate_content(
            contents,
            return_json=True,
            json_schema=BRAND_ANALYSIS_SCHEMA
        )
        
        # Parse the response if it's a string
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                st.error("Failed to parse JSON response")
                return None
            
        return response
        
    except Exception as e:
        st.error(f"Error analyzing brand compatibility: {str(e)}")
        return None

def create_engagement_radar_chart(analysis: dict) -> go.Figure:
    """Create a radar chart for engagement metrics."""
    # Extract engagement metrics (this is an example, adjust based on your data)
    metrics = {
        "Audience Reach": 0.8,
        "Comments": 0.7,
        "Shares": 0.6,
        "Likes": 0.9,
        "Saves": 0.5
    }
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        name='Engagement Metrics'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title="Engagement Metrics"
    )
    return fig

def create_themes_bar_chart(analysis: dict) -> go.Figure:
    """Create a bar chart for content themes."""
    themes = analysis["temas_abordados"]
    # For this example, we'll assign random weights
    weights = [len(theme) for theme in themes]  # Using length as a proxy for weight
    
    fig = go.Figure(data=[
        go.Bar(
            x=themes,
            y=weights,
            marker_color='rgb(26, 118, 255)'
        )
    ])
    
    fig.update_layout(
        title="Content Themes Distribution",
        xaxis_title="Themes",
        yaxis_title="Relevance",
        template='plotly_white'
    )
    return fig

def create_audience_pie_chart(analysis: dict) -> go.Figure:
    """Create a pie chart for audience demographics."""
    demographics = {
        "Age": analysis["publico_alvo_estimado"]["faixa_etaria"],
        "Gender": analysis["publico_alvo_estimado"]["genero"],
        "Location": analysis["publico_alvo_estimado"]["localizacao_geografica"]
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(demographics.keys()),
        values=[1, 1, 1],  # Equal weights for visualization
        hole=.3
    )])
    
    fig.update_layout(
        title="Audience Demographics"
    )
    return fig

def generate_pdf_report(analysis: dict) -> bytes:
    """Generate a PDF report from the analysis."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("Brand Compatibility Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Content Overview
    story.append(Paragraph("Content Overview", heading_style))
    story.append(Paragraph(f"Style: {analysis['estilo_conteudo']}", styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Themes
    story.append(Paragraph("Main Themes:", styles["Normal"]))
    for theme in analysis["temas_abordados"]:
        story.append(Paragraph(f"• {theme}", styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Values and Tone
    story.append(Paragraph("Values & Tone", heading_style))
    story.append(Paragraph("Values:", styles["Normal"]))
    for value in analysis["valores_e_tom"]["valores"]:
        story.append(Paragraph(f"• {value}", styles["Normal"]))
    story.append(Paragraph(f"Tone: {analysis['valores_e_tom']['tom']}", styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Audience Analysis
    story.append(Paragraph("Audience Analysis", heading_style))
    audience_data = [
        ["Age Range", analysis["publico_alvo_estimado"]["faixa_etaria"]],
        ["Gender", analysis["publico_alvo_estimado"]["genero"]],
        ["Location", analysis["publico_alvo_estimado"]["localizacao_geografica"]]
    ]
    audience_table = Table(audience_data)
    audience_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(audience_table)
    story.append(Spacer(1, 12))
    
    # Brand Matches
    story.append(Paragraph("Brand Matches", heading_style))
    for match in analysis["marcas_match"]:
        story.append(Paragraph(f"Type: {match['tipo_marca']}", styles["Normal"]))
        story.append(Paragraph("Examples:", styles["Normal"]))
        for example in match["exemplos"]:
            story.append(Paragraph(f"• {example}", styles["Normal"]))
        story.append(Paragraph(f"Justification: {match['justificativa']}", styles["Normal"]))
        story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def display_brand_analysis(analysis: dict):
    """Display the brand analysis in a user-friendly format."""
    
    # Create tabs for different views
    tab_overview, tab_audience, tab_brands, tab_viz, tab_report = st.tabs([
        "📊 Overview", 
        "👥 Audience Analysis", 
        "🎯 Brand Matches",
        "📈 Visualization",
        "📄 Report"
    ])
    
    # Overview Tab
    with tab_overview:
        st.header("Content Overview")
        
        # Content Style and Themes
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Content Style")
            st.write(analysis["estilo_conteudo"])
            
            st.subheader("Main Themes")
            for tema in analysis["temas_abordados"]:
                st.markdown(f"- {tema}")
        
        with col2:
            st.subheader("Values & Tone")
            st.write("**Values:**")
            for valor in analysis["valores_e_tom"]["valores"]:
                st.markdown(f"- {valor}")
            st.write(f"**Tone:** {analysis['valores_e_tom']['tom']}")
        
        # Platforms and Previous Collaborations
        st.subheader("Platforms & Collaborations")
        col3, col4 = st.columns(2)
        with col3:
            st.write("**Main Platforms:**")
            for platform in analysis["plataformas_principais"]:
                st.markdown(f"- {platform}")
        
        with col4:
            st.write("**Previous Collaborations:**")
            st.write(analysis["colaboracoes_anteriores"])
    
    # Audience Analysis Tab
    with tab_audience:
        st.header("Audience Analysis")
        
        # Audience Demographics
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Demographics")
            st.write(f"**Age Range:** {analysis['publico_alvo_estimado']['faixa_etaria']}")
            st.write(f"**Gender:** {analysis['publico_alvo_estimado']['genero']}")
            st.write(f"**Location:** {analysis['publico_alvo_estimado']['localizacao_geografica']}")
        
        with col2:
            st.subheader("Interests")
            for interesse in analysis["publico_alvo_estimado"]["interesses"]:
                st.markdown(f"- {interesse}")
        
        # Engagement
        st.subheader("Engagement")
        st.write(analysis["engajamento"])
        
        # Market Niches
        st.subheader("Market Niches")
        for nicho in analysis["nichos_de_mercado"]:
            st.markdown(f"- {nicho}")
    
    # Brand Matches Tab
    with tab_brands:
        st.header("Brand Match Analysis")
        
        # Display each brand match
        for match in analysis["marcas_match"]:
            with st.expander(f"🎯 {match['tipo_marca']}"):
                st.write("**Example Brands:**")
                for exemplo in match["exemplos"]:
                    st.markdown(f"- {exemplo}")
                st.write("**Match Justification:**")
                st.write(match["justificativa"])
        
        # Collaboration Types
        st.subheader("Recommended Collaboration Types")
        for tipo in analysis["tipos_de_colaboracao"]:
            st.markdown(f"- {tipo}")
        
        # Brand Image Considerations
        st.subheader("Brand Image Considerations")
        st.info(analysis["consideracoes_imagem_marca"])
    
    # Visualization Tab
    with tab_viz:
        st.header("Data Visualization")
        
        # Engagement Radar Chart
        st.subheader("Engagement Analysis")
        st.plotly_chart(create_engagement_radar_chart(analysis), use_container_width=True)
        
        # Themes Bar Chart
        st.subheader("Content Themes Analysis")
        st.plotly_chart(create_themes_bar_chart(analysis), use_container_width=True)
        
        # Audience Pie Chart
        st.subheader("Audience Demographics")
        st.plotly_chart(create_audience_pie_chart(analysis), use_container_width=True)
    
    # Report Tab
    with tab_report:
        st.header("Analysis Report")
        
        # Generate PDF
        pdf_bytes = generate_pdf_report(analysis)
        
        # Create download button
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="brand_compatibility_analysis.pdf",
            mime="application/pdf",
        )
        
        # Preview section
        st.subheader("Report Preview")
        # Convert PDF to base64 for preview
        b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    # Handle health check requests (Cloud Run requirement)
    if os.environ.get("K_SERVICE"):  # We're running in Cloud Run
        if "health" in st.query_params:
            st.json(check_health())
            return
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .main-title {
            text-align: center;
            margin-bottom: 2rem;
        }
        .stAlert {
            max-width: 800px;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("<h1 class='main-title'>🎯 Brand Media Analyzer</h1>", unsafe_allow_html=True)
    
    # Check for required environment variables
    if not bucket_name or not project_id:
        st.error("""
            Missing required environment variables. Please ensure the following are set:
            - GCP_BUCKET_NAME: The Google Cloud Storage bucket name
            - GCP_PROJECT: Your Google Cloud project ID
        """)
        return
    
    # Initialize session state for video URL
    if 'video_url' not in st.session_state:
        st.session_state.video_url = None
    
    # Sidebar for video upload
    with st.sidebar:
        st.markdown("### Upload Content")
        st.markdown("Upload a video to analyze for brand compatibility.")
        st.markdown("**Note:** Maximum file size is 200MB")
        video_file = st.file_uploader("", type=["mp4"])
        
        if video_file:
            file_size = len(video_file.getvalue()) / (1024 * 1024)  # Size in MB
            if file_size > 200:
                st.error("File size exceeds 200MB limit!")
                video_file = None
                st.session_state.video_url = None
            else:
                # Upload to GCS first
                upload_result = upload_to_gcs(video_file, bucket_name)
                if upload_result:
                    public_url, gcs_path = upload_result
                    st.session_state.video_url = public_url
                    st.session_state.gcs_path = gcs_path
                    
                    # Display video in sidebar
                    st.video(st.session_state.video_url)
                    
                    # Add some spacing
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Analyze button
                    process_button = st.button("Analyze Brand Compatibility", type="primary")
                else:
                    st.error("Failed to upload video")
                    process_button = False
        else:
            process_button = False
            st.session_state.video_url = None
    
    # Main content area
    if st.session_state.video_url:
        if process_button:
            try:
                with st.spinner("Analyzing your content..."):
                    # Analyze brand compatibility using the GCS path
                    analysis = analyze_brand_compatibility(st.session_state.gcs_path)
                    if not analysis:
                        return
                    
                    # Display results
                    display_brand_analysis(analysis)
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if os.environ.get("K_SERVICE"):  # We're running in Cloud Run
                    print(f"Error in Cloud Run: {str(e)}")  # Log to Cloud Run logs
    else:
        # Show welcome message and instructions
        st.markdown("""
            ### Welcome to Brand Media Analyzer! 👋
            
            This tool helps brands find the perfect content creator match by analyzing videos 
            and providing detailed insights about audience compatibility, brand alignment, 
            and collaboration opportunities.
            
            To get started:
            1. Upload a content creator's video using the sidebar (max 200MB)
            2. Click "Analyze Brand Compatibility"
            3. View the detailed analysis across different categories
            
            The AI will analyze the content and provide insights about:
            - Content themes and style
            - Audience demographics and engagement
            - Brand compatibility and collaboration opportunities
            - Market niches and potential matches
        """)

if __name__ == "__main__":
    main() 