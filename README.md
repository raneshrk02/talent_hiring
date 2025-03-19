# TalentScout Hiring Assistant

A chatbot-based hiring assistant for TalentScout, a fictional recruitment agency specializing in technology placements. This application helps in the initial screening of candidates by gathering essential information and posing relevant technical questions based on the candidate's declared tech stack.

## Project Overview

The TalentScout Hiring Assistant is designed to streamline the initial candidate screening process through an interactive chat interface. The chatbot:

1. Collects essential candidate information (name, contact details, experience, etc.)
2. Gathers information about the candidate's tech stack
3. Generates and asks relevant technical questions based on the declared technologies
4. Maintains context throughout the conversation
5. Stores candidate information for later review

## Demo

[Link to demonstration video on youtube](https://youtu.be/VUKI_HvpkR0)

## Technical Details

### Architecture

The application follows a modular architecture:

- **Main Application (`app.py`)**: Handles the Streamlit UI and user interactions
- **Chatbot Model (`models/chatbot.py`)**: Core logic for conversation processing and LLM interaction
- **Prompt Management (`utils/prompt_manager.py`)**: Manages prompts for the LLM
- **Data Handling (`utils/data_handler.py`)**: Handles candidate data storage and retrieval
- **Configuration (`config/config.py`)**: Centralized configuration settings
- **Prompts (`prompts/`)**: Contains system prompts and technical questions

### Libraries Used

- **Streamlit**: For building the web interface
- **Mistral AI**: For accessing the LLM API
- **Pandas**: For data handling and storage
- **Python-dotenv**: For environment variable management

### LLM Integration

The application uses the Mistral AI API to interact with the Mistral Small model. The system:

1. Formats conversation history and context into appropriate prompts
2. Sends these prompts to the Mistral Small LLM
3. Processes the LLM's responses
4. Extracts relevant information from user inputs with the help of the LLM

### Data Privacy

- Candidate information is stored locally in CSV format
- No personal data is transmitted except to the LLM API
- The application complies with data privacy best practices

## Prompt Design

The prompts are designed to guide the LLM to:

1. **Maintain a professional tone**: Keeping conversations professional yet friendly
2. **Stay on topic**: Focusing on the screening process
3. **Extract information**: Gathering essential candidate details
4. **Generate relevant questions**: Creating technical questions based on the candidate's tech stack
5. **Maintain context**: Keeping track of the conversation flow and candidate information

## Future Enhancements

- **Sentiment Analysis**: Analyze candidate responses for confidence and enthusiasm
- **Multilingual Support**: Add support for multiple languages
- **Advanced Question Adaptation**: Adjust question difficulty based on candidate responses
- **Interview Scheduling**: Integration with calendar systems for scheduling follow-up interviews
- **Performance Analytics**: Dashboard for analyzing candidate performance and recruiter efficiency