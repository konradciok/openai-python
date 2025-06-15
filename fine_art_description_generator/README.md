# Fine Art Print Description Generator

A Streamlit application that helps fine art print sellers create professional, compelling product descriptions for their Shopify e-commerce store using AI image analysis and natural language generation.

## Features

- Upload and analyze artwork images using OpenAI's Vision API
- AI-powered visual analysis detects style, medium, colors, subject, and mood
- Generate tailored product descriptions based on image analysis and user input
- Customize description tone and length
- Edit and export descriptions for use in Shopify

## Project Structure

```
fine_art_description_generator/
├── app.py                     # Main application entry point
├── pages/                     # Application pages
│   ├── home.py                # Home page with image upload, form, and preview
│   └── about.py               # About page with app information
├── components/                # Reusable UI components
│   ├── image_upload.py        # Image upload component
│   ├── description_form.py    # Form for collecting print details
│   └── description_preview.py # Preview and editing of descriptions
├── utils/                     # Utility functions
│   ├── session_state.py       # Session state management
│   ├── image_analyzer.py      # AI image analysis
│   └── description_generator.py # AI description generation
├── styles/                    # CSS styling
│   └── main.css               # Main stylesheet
├── data/                      # Data storage (if needed)
├── requirements.txt           # Python dependencies
└── .env.example               # Example environment variables
```

## Setup and Installation

### Automatic Setup

1. Clone this repository
2. Run the setup script:
   ```
   python setup.py
   ```
3. Edit the `.env` file to add your OpenAI API key
4. Run the application using one of these methods:
   ```
   # Option 1: Using the run script
   python run.py
   
   # Option 2: Using Streamlit directly
   streamlit run app.py
   ```

### Manual Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key (see `.env.example`)
4. Run the application using one of these methods:
   ```
   # Option 1: Using the run script
   python run.py
   
   # Option 2: Using Streamlit directly
   streamlit run app.py
   ```

### Verify Setup

You can verify that all dependencies are installed correctly by running:
```
python setup_check.py
```

## Usage

1. Upload an image of your fine art print
2. The AI will analyze the image and detect visual elements
3. Fill in additional details about your print
4. Customize the description tone and length
5. Generate a product description
6. Edit the description if needed
7. Copy or download the final text for use in your Shopify store

## Requirements

- Python 3.7+
- Streamlit
- OpenAI API key with access to Vision API
- Internet connection for API access

## Privacy

Uploaded images are processed for analysis but not stored permanently. Your data is used only for generating descriptions and is not shared with third parties.