# Career Navigator System Design Documentation

This directory contains simplified Mermaid diagram files that visualize the system architecture and process flows for the Practical Career Navigator project.

## Available Diagrams

1. **System Design** (`system_design.mmd`): 
   - Core components and their interactions
   - Simple, straightforward flow of data between components
   - Color coding for easy identification of component types

2. **Architecture Overview** (`architecture.mmd`):
   - High-level architecture showing the main system components
   - Linear flow from frontend through processing components to database

3. **Process Flow** (`process_flow.mmd`):
   - Step-by-step workflow from resume upload to final results display
   - Simple left-to-right flow of the user journey

## How to View These Diagrams

### Option 1: VS Code with Mermaid Extension
1. Install the [Mermaid extension](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) for VS Code
2. Open any `.mmd` file or use the Mermaid Preview feature

### Option 2: Online Mermaid Editor
1. Go to [Mermaid Live Editor](https://mermaid.live/)
2. Copy-paste the contents of any `.mmd` file
3. View the rendered diagram

## Core Components

### Frontend
- **Streamlit UI**: User interface for uploading resumes and viewing recommendations

### Backend
- **FastAPI Backend**: API service that handles requests and coordinates operations
- **Resume Parser**: Extracts structured information from resumes
- **Job Recommender**: Matches profiles with suitable job listings
- **Roadmap Generator**: Creates skill development plans

### Data Storage
- **SQLite Database**: Stores profiles, jobs, and other application data