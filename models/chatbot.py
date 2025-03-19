from mistralai.client import MistralClient #type:ignore
from mistralai.models.chat_completion import ChatMessage #type:ignore
from config.config import MISTRAL_API_KEY, LLM_MODEL, TEMPERATURE, MAX_TOKENS, END_KEYWORDS
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.tech_questions import get_tech_questions
from utils.prompt_manager import format_messages
import re
import json

client = MistralClient(api_key=MISTRAL_API_KEY)

class HiringAssistant:
    def __init__(self):
        self.model = LLM_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.system_prompt = SYSTEM_PROMPT
        self.current_state = "greeting"
        self.required_fields = ["name", "email", "phone", "experience", "position", "location", "tech_stack"]
        
    def get_initial_greeting(self):
        greeting_messages = [
            ChatMessage(role="system", content=self.system_prompt),
            ChatMessage(role="user", content="Start the conversation")
        ]
        
        response = client.chat(
            model=self.model,
            messages=greeting_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return response.choices[0].message.content.strip()
    
    def _extract_candidate_info(self, message, current_info):
        extraction_prompt = f"""
        Extract the following information from the candidate's message if present.
        Do not infer information that is not explicitly mentioned.
        Return a JSON object with only the fields that can be extracted from the message.
        
        Message: {message}
        
        Expected fields:
        - name: Full name
        - email: Email address
        - phone: Phone number
        - experience: Years of experience (just the number)
        - position: Desired position
        - location: Current location
        - tech_stack: List of technologies the candidate is proficient in
        """
        
        extraction_messages = [
            ChatMessage(role="system", content="You are a helpful assistant that extracts structured information from text."),
            ChatMessage(role="user", content=extraction_prompt)
        ]
        
        response = client.chat(
            model=self.model,
            messages=extraction_messages,
            max_tokens=self.max_tokens,
            temperature=0.1  
        )
        
        try:
            extracted_info = json.loads(response.choices[0].message.content)
            
            updated_info = current_info.copy()
            for key, value in extracted_info.items():
                if value and key in updated_info:
                    if key == "tech_stack" and isinstance(value, list):
                        for tech in value:
                            if tech not in updated_info["tech_stack"]:
                                updated_info["tech_stack"].append(tech)
                    else:
                        updated_info[key] = value
            
            return updated_info
        except:
            return current_info
    
    def _check_conversation_end(self, message):
        for keyword in END_KEYWORDS:
            if re.search(r'\b' + keyword + r'\b', message.lower()):
                return True
        return False
    
    def _determine_conversation_state(self, candidate_info):
        missing_fields = [field for field in self.required_fields if not candidate_info[field]]
        
        if missing_fields:
            return "gathering_info"
        elif candidate_info["tech_stack"] and not candidate_info.get("questions_asked", False):
            return "ask_technical_questions"
        else:
            return "conversation_complete"
    
    def _generate_tech_questions(self, tech_stack):
        all_questions = []
        for tech in tech_stack:
            tech_specific_questions = get_tech_questions(tech)
            if tech_specific_questions:
                all_questions.extend(tech_specific_questions)
        
        if not all_questions:
            question_prompt = f"""
            Generate 3-5 technical interview questions to assess proficiency in the following technologies:
            {', '.join(tech_stack)}
            
            The questions should be challenging but appropriate for an initial screening. Include a mix of conceptual 
            and practical questions. Return only the numbered questions without explanations.
            """
            
            question_messages = [
                ChatMessage(role="system", content="You are a technical interviewer creating questions for a tech screening."),
                ChatMessage(role="user", content=question_prompt)
            ]
            
            response = client.chat(
                model=self.model,
                messages=question_messages,
                max_tokens=self.max_tokens,
                temperature=0.7  
            )
            
            generated_questions = response.choices[0].message.content.strip().split("\n")
            all_questions = [q.strip() for q in generated_questions if q.strip()]
        
        return all_questions[:5]
    
    def process_message(self, message, candidate_info, conversation_history):
        if self._check_conversation_end(message):
            return "Thank you for your time. The conversation has ended.", candidate_info, "end"
        
        updated_info = self._extract_candidate_info(message, candidate_info)
        
        current_state = self._determine_conversation_state(updated_info)
        
        formatted_messages = format_messages(
            self.system_prompt, 
            conversation_history, 
            updated_info, 
            current_state
        )
        
        mistral_messages = [
            ChatMessage(role=msg["role"], content=msg["content"]) 
            for msg in formatted_messages
        ]
        
        if current_state == "ask_technical_questions" and not updated_info.get("questions_asked", False):
            tech_questions = self._generate_tech_questions(updated_info["tech_stack"])
            
            question_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(tech_questions)])
            
            question_prompt = f"""
            Now I'd like to ask you some technical questions based on your declared tech stack:
            
            {question_text}
            
            Please take your time to answer these questions to the best of your ability.
            """
            
            mistral_messages.append(ChatMessage(role="assistant", content=question_prompt))
            updated_info["questions_asked"] = True
        
        response = client.chat(
            model=self.model,
            messages=mistral_messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        response_text = response.choices[0].message.content.strip()
        
        conversation_status = "active"
        if current_state == "conversation_complete" and updated_info.get("questions_asked", False):
            conversation_status = "end"
        
        return response_text, updated_info, conversation_status