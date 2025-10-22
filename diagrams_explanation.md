# Practical Career Navigator - System Diagrams

## 1. Basic Flow Diagram (flow1.mmd)

The flow diagram presents the step-by-step process of how data moves through the system, from resume upload to displaying results:

1. **Upload Resume**: User uploads their resume document (PDF, DOCX, or image)
2. **Parse Resume**: System converts the document to processable text
3. **Extract Information**: System identifies and extracts key information from the text
4. **Create Profile**: Structured profile is created from the extracted information
5. **Match with Jobs**: Profile is compared against available job listings
6. **Score & Rank Jobs**: Jobs are scored and ranked based on matching criteria
7. **Generate Skill Roadmap**: System identifies skill gaps and creates a development roadmap
8. **Display Results**: Results are presented to the user in the UI

## 2. System Design Diagram (system_design1.mmd)

The system design diagram shows the architecture and component relationships:

### Layers

1. **UI Layer**: 
   - Streamlit UI: The frontend interface where users interact with the system

2. **Application Layer**:
   - FastAPI Backend: Manages API endpoints and coordinates between components

3. **Core Components**:
   - Resume Parser: Handles document processing and information extraction
   - Job Recommender: Manages job matching and ranking
   - Roadmap Generator: Creates personalized skill development plans

4. **Data Layer**:
   - SQLite Database: Stores profiles, jobs, and other application data

5. **External Components**:
   - OCR Engine (pytesseract): Extracts text from images and PDFs
   - NLP Processing (spaCy): Performs named entity recognition and text analysis
   - ML Models (scikit-learn): Provides algorithms for scoring and ranking

### Key Connections

- UI communicates with the API via HTTP requests
- API interacts with core components and the database
- Resume Parser uses OCR and NLP components
- Job Recommender uses ML models for scoring

## Implementation Notes

The architecture follows a simple, monolithic design for ease of development and deployment. It avoids complex microservices or heavy dependencies like graph databases, making it accessible for beginners while still providing robust functionality.

The system is built with widely-used Python libraries, making it easy to understand, extend, and maintain.