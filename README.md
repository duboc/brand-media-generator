# Brand Media Analyzer 🎯

A powerful AI-powered tool that analyzes content creator videos to identify brand compatibility and collaboration opportunities. Built with Streamlit and Google's Vertex AI Gemini, this application helps brands find their perfect content creator match through intelligent analysis and detailed insights.

## Features

### 📊 Content Analysis
- Identifies content themes and style
- Analyzes creator's tone and values
- Maps primary content platforms
- Tracks previous brand collaborations

### 👥 Audience Insights
- Demographic analysis (age, gender, location)
- Interest mapping
- Engagement metrics
- Geographic distribution

### 🎯 Brand Matching
- Smart brand compatibility analysis
- Detailed match justifications
- Collaboration type recommendations
- Brand safety considerations

### 📈 Data Visualization
- Interactive engagement radar charts
- Content theme distribution
- Audience demographics breakdown
- Dynamic plotly-powered visualizations

### 📄 Professional Reporting
- Downloadable PDF reports
- Comprehensive analysis summary
- Professional formatting
- Shareable insights

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Vertex AI Gemini
- **Storage**: Google Cloud Storage
- **Visualization**: Plotly
- **PDF Generation**: ReportLab
- **Language**: Python 3.9+

## Prerequisites

- Google Cloud Project with Vertex AI API enabled
- Google Cloud Storage bucket
- Python 3.9 or higher
- Required environment variables:
  - `GCP_BUCKET_NAME`: Your Google Cloud Storage bucket name
  - `GCP_PROJECT`: Your Google Cloud project ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/brand-media-analyzer.git
cd brand-media-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload a content creator's video (max 200MB)
3. Click "Analyze Brand Compatibility"
4. Explore the analysis across different tabs:
   - Overview
   - Audience Analysis
   - Brand Matches
   - Visualization
   - Report

## Development

### Project Structure
```
brand-media-analyzer/
├── app.py                 # Main application file
├── prompts/              
│   └── branding_prompt.md # AI analysis prompt
├── schemas/
│   └── brand_analysis_schema.py # JSON schema for AI response
├── vertex_libs/
│   └── gemini_client.py   # Vertex AI client wrapper
├── requirements.txt       # Project dependencies
└── .env                  # Environment variables
```

### Adding New Features

1. **New Visualizations**:
   - Add new chart functions in `app.py`
   - Update the visualization tab in `display_brand_analysis()`

2. **Custom Analysis**:
   - Modify the `branding_prompt.md`
   - Update the schema in `brand_analysis_schema.py`

3. **Report Customization**:
   - Modify the `generate_pdf_report()` function in `app.py`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Vertex AI team for Gemini
- Streamlit team for the amazing framework
- Plotly team for visualization capabilities
- ReportLab team for PDF generation 