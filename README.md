# TalentScout Hiring Assistant

## Introduction

TalentScout Hiring Assistant is a conversational application developed to facilitate the recruitment process for technology positions. This solution employs natural language processing capabilities to conduct preliminary candidate assessments through structured dialogue, collecting essential information and evaluating technical knowledge based on candidates' declared expertise.

## Functional Overview

The application systematically performs the following functions:

1. Acquisition of candidate biographical and contact information
2. Documentation of technical proficiencies and experience levels
3. Administration of technology-specific assessment questions
4. Maintenance of conversational context throughout the interaction
5. Secure storage of candidate profiles for subsequent evaluation

## Demonstration

A visual demonstration of the system's capabilities is available via the following link:
[Demonstration Video](https://youtu.be/VUKI_HvpkR0)

## Implementation Requirements

### System Prerequisites

- Python 3.8 or later versions
- Valid Mistral AI API credentials

### Configuration Process

1. Repository acquisition:
   ```bash
   git clone https://github.com/raneshrk02/talent_hiring.git
   cd talent_hiring
   ```

2. Environment preparation:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows systems: venv\Scripts\activate
   ```

3. Dependency installation:
   ```bash
   pip install -r requirements.txt
   ```

4. API configuration:
   Create a `.env` file containing the following parameter:
   ```
   MISTRAL_API_KEY=[authentication_key]
   ```

### Application Execution

To initiate the application:

```bash
streamlit run app.py
```

The interface will be accessible via web browser at http://localhost:8501.

## Operational Guidelines

1. **Initialization**: Execute the application using the specified command
2. **Engagement Protocol**: The system will initiate the dialogue and guide the assessment process
3. **Information Provision**: Respond to prompts to provide biographical and technical information
4. **Technical Assessment**: Address the automatically generated technical inquiries
5. **Session Termination**: The system will conclude the interaction upon completion of the assessment protocol, or enter "exit" to terminate prematurely

## Technical Architecture

### Structural Components

The application implements a modular design comprising:

- **Interface Layer (`app.py`)**: Manages user interaction via Streamlit framework
- **Conversation Management (`models/chatbot.py`)**: Orchestrates dialogue flow and language model integration
- **Prompt Engineering (`utils/prompt_manager.py`)**: Structures communication with the language model
- **Data Management (`utils/data_handler.py`)**: Handles information persistence and retrieval
- **Configuration Management (`config/config.py`)**: Centralizes application parameters
- **Dialogue Templates (`prompts/`)**: Houses system instructions and assessment questions

### Technological Implementation

- **Streamlit**: Interface rendering and interaction handling
- **Mistral AI**: Natural language processing capabilities
- **Pandas**: Data manipulation and storage operations
- **Python-dotenv**: Environment variable management

### Language Model Integration

The system leverages the Mistral Small model via API integration. The process encompasses:

1. Contextual formatting of conversation history
2. Transmission of structured prompts to the language model
3. Processing of model-generated responses
4. Extraction of structured information from unstructured candidate inputs

## Conversation Design Methodology

The dialogue architecture is engineered to ensure:

1. **Professional Communication**: Maintaining appropriate formality with conversational elements
2. **Topical Consistency**: Ensuring relevance to the assessment objectives
3. **Information Extraction**: Efficiently identifying and documenting pertinent candidate details
4. **Targeted Evaluation**: Generating assessment questions aligned with specific technical domains
5. **Contextual Awareness**: Maintaining conversation history and adapting responses accordingly

## Future Development Roadmap

- **Sentiment Analysis**: Implementation of response tone and confidence evaluation
- **Internationalization**: Extension of support for multiple languages
- **Adaptive Difficulty**: Dynamic adjustment of question complexity based on demonstrated proficiency
- **Scheduling Integration**: Connection with calendar systems for subsequent interview coordination
- **Performance Analytics**: Development of metrics visualization for recruitment process optimization
