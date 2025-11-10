from fastapi import APIRouter, Depends, HTTPException
import logging
from ..mongodb import get_candidates_collection
from typing import Dict
import re
import uuid
from ..models import Candidate
from ..schemas import SendMessageRequest, SendMessageResponse, CandidateData
from ..services.groq_service import GroqService
from ..services.scoring_service import ScoringService
from ..models import Candidate
from ..system_prompt import (
    GREETING_PROMPT, NAME_EXTRACTION_PROMPT, ASK_EMAIL_PROMPT, REPEAT_NAME_PROMPT,
    EMAIL_EXTRACTION_PROMPT, RETRY_EMAIL_PROMPT, ASK_PHONE_PROMPT, PHONE_EXTRACTION_PROMPT, 
    RETRY_PHONE_PROMPT, ASK_EXPERIENCE_PROMPT, EXPERIENCE_EXTRACTION_PROMPT, ASK_POSITION_PROMPT,
    POSITION_EXTRACTION_PROMPT, ASK_LOCATION_PROMPT, LOCATION_EXTRACTION_PROMPT, ASK_TECH_STACK_PROMPT, 
    TECH_STACK_EXTRACTION_PROMPT, TECH_QUESTIONS_INTRO_PROMPT, TECHNICAL_QUESTION_PROMPT, 
    INTERVIEW_COMPLETE_MESSAGE,INTERVIEW_ALREADY_COMPLETE_MESSAGE
)

mrouter = APIRouter()
router = APIRouter()
llama2 = GroqService()
scorer = ScoringService()

sessions: Dict[str, Dict] = {}

def clean_llm_output(text, value_type="text"):
    """Remove extra sentences, instructions, or context from LLM output"""
    if value_type == "email":
        email = text.strip().lower()
        email = email.replace(' ', '').replace('mailto:', '').replace('email:', '').replace('e-mail:', '').replace('E-mail:', '').replace('E-Mail:', '').replace('E mail:', '').replace('E-mail address:', '').replace('e-mail address:', '').replace('E-Mail address:', '').replace('E mail address:', '').replace('Email Address:', '').replace('Email address:', '').replace('Email ID:', '').replace('Email id:', '').replace('EmailId:', '').replace('Emailid:', '').replace('\n', '').replace('\r', '').replace('\t', '').replace(',', '').replace(';', '').replace('=', '').replace('?', '').replace('"', '').replace("'", '')
        match = re.search(r"[\w\.-]+@[\w\.-]+", email)
        return match.group(0) if match else ""
    elif value_type == "phone":
        match = re.search(r"\d{8,}", text)
        return match.group(0) if match else ""
    elif value_type == "years":
        match = re.search(r"\d+", text)
        return int(match.group(0)) if match else 0
    elif value_type == "skills":
        skills = [skill.strip() for skill in text.split(",") if skill.strip()]
        return [s for s in skills if re.match(r"^[A-Za-z0-9_\-\.]+$", s)]
    elif value_type == "location":
        line = text.strip().split(". ")[0].split("\n")[0]
        return line.title()
    else:
        line = text.strip().split("\n")[0]
        # Preserve original capitalization for general text (avoid title-casing names)
        return line.strip()


def build_candidate_summary(info):
    """Standardize and format the candidate summary"""
    summary = {
        "Full Name": info.get("fullName", "-"),
        "Email": info.get("email", "-"),
        "Phone": info.get("phone", "-"),
        "Years of Experience": str(info.get("yearsExperience", "-")),
        "Desired Position": info.get("desiredPosition", "-"),
        "Location": info.get("location", "-"),
        "Tech Stack": info.get("techStack", [])
    }
    return summary


def get_next_valid_skill_index(tech_stack, start_index):
    """Find the next valid skill index, skipping empty/invalid skills."""
    invalid_skills = {"", "none", "not applicable", "n/a", "-"}
    for i in range(start_index, len(tech_stack)):
        skill = tech_stack[i]
        if skill and skill.lower() not in invalid_skills:
            return i
    return None


def clean_technical_question(question):
    """Remove common prefixes from LLM-generated questions"""
    if not question:
        return question
    
    question = question.strip()
    prefixes = [
        "Here it is:", "Sure:", "Of course:", "Okay:", 
        "Alright:", "Question:", "Here's a question:"
    ]
    
    for prefix in prefixes:
        if question.lower().startswith(prefix.lower()):
            question = question[len(prefix):].strip()
    
    return question


def extract_years_from_message(user_message, llm_response):
    """Extract years of experience from user message and LLM response"""
    numbers = re.findall(r"\d+", user_message)
    years = sum(int(n) for n in numbers) if numbers else 0
    
    word_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, 
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, 
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, 
        "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, 
        "eighteen": 18, "nineteen": 19, "twenty": 20
    }
    
    for word in user_message.strip().lower().split():
        if word in word_to_num:
            years += word_to_num[word]
    
    return years


def extract_skills_from_message(user_message, llm_response):
    """Extract technical skills from user message and LLM response"""
    skills_clean = re.sub(r"\(.*?\)", "", llm_response)
    
    commentary_phrases = [
        "The candidate's tech stack is", "Tech stack is", "Skills are", 
        "Main skills are", "Assuming", "It seems", "Probably", "Likely"
    ]
    for phrase in commentary_phrases:
        if phrase.lower() in skills_clean.lower():
            skills_clean = skills_clean.split(phrase)[-1].strip()
    
    skills_clean = skills_clean.replace('"', '').replace("'", '').replace('.', '').strip()
    
    split_skills = re.split(r",| and | & |/", skills_clean, flags=re.IGNORECASE)
    tech_skills = [s.strip() for s in split_skills if s.strip()]
    
    invalid_skills = {
        "sure", "okay", "yes", "no", "none", "nil", "nothing", 
        "not applicable", "n/a", "-", "", "hints", "hint", 
        "help", "solution", "answer", "code"
    }
    tech_skills = [s for s in tech_skills if s.lower() not in invalid_skills]
    
    tech_skills = list(dict.fromkeys(tech_skills))
    
    if not tech_skills:
        raw_skills = re.split(r",| and | & |/", user_message, flags=re.IGNORECASE)
        user_skills = [s.strip() for s in raw_skills if s.strip()]
        user_skills = [s for s in user_skills if s.lower() not in invalid_skills and len(s) > 1]
        tech_skills = list(dict.fromkeys(user_skills))

    # --- Additional normalization pass ---
    normalized = []
    for skill in tech_skills:
        original = skill
        # Remove trailing descriptive phrases like "are major", "are minor", "is primary"
        skill = re.sub(r"\b(are|is)\b.*$", "", skill, flags=re.IGNORECASE).strip()
        # Remove leading phrases like "primary", "major", "minor"
        skill = re.sub(r"^(primary|major|minor|main|core)\s+", "", skill, flags=re.IGNORECASE).strip()
        # Strip residual adjectives at end
        skill = re.sub(r"\b(major|minor|primary|secondary|main|core)$", "", skill, flags=re.IGNORECASE).strip()
        # If multi-word and first token is a single letter like 'c', keep only 'c'
        if re.match(r"^[cC]\b", skill) and len(skill.split()) > 1:
            skill = "C"
        # Common language canonicalization
        if skill.lower() == "js":
            skill = "JavaScript"
        if skill.lower() == "py":
            skill = "Python"
        if skill.lower() == "c++":
            skill = "C++"
        if skill.lower() == "c#":
            skill = "C#"
        # Remove any residual punctuation
        skill = skill.strip(".,;:! ")
        if skill and skill.lower() not in invalid_skills and skill not in normalized:
            normalized.append(skill)

    # If we lost everything due to over-cleaning, fall back to original list
    if normalized:
        tech_skills = normalized
    
    return tech_skills


def order_skills_by_user_input(user_message: str, skills):
    """Reorder extracted skills to follow the order they appeared in the original user message.
    If a skill is not found (LLM-added), it is appended at the end preserving relative order.
    """
    user_lower = user_message.lower()
    positions = []
    not_found = []
    for s in skills:
        idx = user_lower.find(s.lower())
        if idx == -1:
            not_found.append(s)
        else:
            positions.append((idx, s))
    ordered = [s for _, s in sorted(positions, key=lambda t: t[0])]
    ordered.extend([s for s in skills if s in not_found])
    return ordered


@router.post("/conversation/message", response_model=SendMessageResponse)
async def conversation_message(payload: SendMessageRequest):
    """
    Main conversation endpoint for the AI interview chatbot.
    Handles all stages of the interview process.
    """
    user_message = payload.userMessage.strip()
    candidate_info = payload.candidateInfo
    current_stage = payload.currentStage
    current_tech_question_index = payload.currentTechQuestionIndex

    session_id = candidate_info.get("email", "default_session")
    if session_id not in sessions:
        sessions[session_id] = {
            "stage": current_stage,
            "data": candidate_info,
            "qa_pairs": [],
            "question_count": 0,
            "skill_index": -1,  # server-authoritative pointer to current skill index
        }
    session = sessions[session_id]
    session["stage"] = current_stage
    session["data"] = candidate_info

    next_stage = current_stage
    technical_question = ""
    is_complete = False
    updated_candidate_info = candidate_info.copy()
    message = ""

    # === GREETING STAGE ===
    if current_stage == "greeting":
        message = clean_llm_output(llama2.generate_response(GREETING_PROMPT))
        next_stage = "name"
        return SendMessageResponse(
            message=message,
            nextStage=next_stage,
            updatedCandidateInfo=updated_candidate_info,
            technicalQuestion=technical_question,
            isComplete=is_complete
        )

    # === NAME STAGE ===
    elif current_stage == "name":
        name_prompt = NAME_EXTRACTION_PROMPT.format(user_message=user_message)
        name_raw = llama2.generate_response(name_prompt)
        name = clean_llm_output(name_raw)
       
        name = re.sub(r"\(.*?\)", "", name)
        commentary_phrases = [
            "Assuming the candidate's full name is", "Assuming", 
            "It seems", "Probably", "Likely", "The candidate's name is"
        ]
        for phrase in commentary_phrases:
            if phrase.lower() in name.lower():
                name = name.split(phrase)[-1].strip()
        
        name = name.strip().split("\n")[0]
        # Remove common prefixes like "I'm", "I am", "My name is"
        name = re.sub(r"^(i\s*am|i'm|im|my name is|this is|name is|the name is)\s+",
                      "", name, flags=re.IGNORECASE)
        name = name.replace(".", "").replace(",", "").strip()
        
        if name and name.lower() not in ["", "your name", "full name", "candidate", "talentbot"]:
            updated_candidate_info["fullName"] = name
            message = clean_llm_output(llama2.generate_response(ASK_EMAIL_PROMPT))
            next_stage = "email"
        else:
            message = clean_llm_output(llama2.generate_response(REPEAT_NAME_PROMPT))
            next_stage = "name"

    # === EMAIL STAGE ===
    elif current_stage == "email":
        email_prompt = EMAIL_EXTRACTION_PROMPT.format(user_message=user_message)
        email_raw = llama2.generate_response(email_prompt)
        
        match = re.search(r"[\w\.-]+@[\w\.-]+", email_raw)
        email = match.group(0) if match else ""
        
        if not email or email.startswith('_') or email.count('@') != 1 or email.startswith('.'):
            match = re.search(r"[\w\.-]+@[\w\.-]+", user_message)
            email = match.group(0) if match else ""
        
        if not email or "@" not in email:
            message = clean_llm_output(llama2.generate_response(RETRY_EMAIL_PROMPT))
            next_stage = "email"
        else:
            updated_candidate_info["email"] = email
            message = clean_llm_output(llama2.generate_response(ASK_PHONE_PROMPT))
            next_stage = "phone"

    # === PHONE STAGE ===
    elif current_stage == "phone":
        phone_prompt = PHONE_EXTRACTION_PROMPT.format(user_message=user_message)
        phone = clean_llm_output(llama2.generate_response(phone_prompt), value_type="phone")
        
        if not phone or len(phone) < 8:
            message = clean_llm_output(llama2.generate_response(RETRY_PHONE_PROMPT))
            next_stage = "phone"
        else:
            updated_candidate_info["phone"] = phone
            message = clean_llm_output(llama2.generate_response(ASK_EXPERIENCE_PROMPT))
            next_stage = "experience"

    # === EXPERIENCE STAGE ===
    elif current_stage == "experience":
        exp_prompt = EXPERIENCE_EXTRACTION_PROMPT.format(user_message=user_message)
        years_raw = llama2.generate_response(exp_prompt)
        years = extract_years_from_message(user_message, years_raw)
        
        updated_candidate_info["yearsExperience"] = years
        message = clean_llm_output(llama2.generate_response(ASK_POSITION_PROMPT))
        next_stage = "position"

    # === POSITION STAGE ===
    elif current_stage == "position":
        pos_prompt = POSITION_EXTRACTION_PROMPT.format(user_message=user_message)
        position = clean_llm_output(llama2.generate_response(pos_prompt))
        
        updated_candidate_info["desiredPosition"] = position
        message = clean_llm_output(llama2.generate_response(ASK_LOCATION_PROMPT))
        next_stage = "location"

    # === LOCATION STAGE ===
    elif current_stage == "location":
        loc_prompt = LOCATION_EXTRACTION_PROMPT.format(user_message=user_message)
        location_raw = llama2.generate_response(loc_prompt)
        location = clean_llm_output(location_raw, value_type="location")
        
        commentary_phrases = [
            "The candidate's location is", "Location is", 
            "It seems", "Probably", "Likely", "Assuming"
        ]
        for phrase in commentary_phrases:
            if phrase.lower() in location.lower():
                location = location.split(phrase)[-1].strip()
        
        location = location.replace('"', '').replace("'", '').replace('.', '').replace(',', '').strip()
        updated_candidate_info["location"] = location
        message = clean_llm_output(llama2.generate_response(ASK_TECH_STACK_PROMPT))
        next_stage = "techStack"

    # === TECH STACK STAGE ===
    elif current_stage == "techStack":
        tech_prompt = TECH_STACK_EXTRACTION_PROMPT.format(user_message=user_message)
        raw_skills = llama2.generate_response(tech_prompt)
        tech_skills = extract_skills_from_message(user_message, raw_skills)
        # Ensure ordering respects candidate's original message order
        tech_skills = order_skills_by_user_input(user_message, tech_skills)
        
        updated_candidate_info["techStack"] = tech_skills
        # Initialize Q&A storage as a list
        updated_candidate_info["technicalQA"] = []
        logging.info(f"Extracted tech skills: {tech_skills}")
        
        tech_skills_str = ', '.join(tech_skills) if tech_skills else "your skills"
        tech_q_intro_prompt = TECH_QUESTIONS_INTRO_PROMPT.format(tech_skills=tech_skills_str)
        tech_q_intro = clean_llm_output(llama2.generate_response(tech_q_intro_prompt))
        
        if tech_skills:
            first_valid_index = get_next_valid_skill_index(tech_skills, 0)
            if first_valid_index is not None:
                first_skill = tech_skills[first_valid_index]
                tech_question_prompt = TECHNICAL_QUESTION_PROMPT.format(skill=first_skill)
                question = clean_llm_output(llama2.generate_response(tech_question_prompt))
                technical_question = clean_technical_question(question)
                
                # Start sequential question numbering (avoid confusion when skipping invalid skills)
                session["question_count"] = 1
                session["skill_index"] = first_valid_index
                session["last_question"] = technical_question  # Store the question for next answer
                message = (
                    f"{tech_q_intro}\n\n"
                    f"Question {session['question_count']} about {first_skill}:\n{technical_question}"
                )
                next_stage = "technicalQuestions"
                current_tech_question_index = first_valid_index
            else:
                message = INTERVIEW_COMPLETE_MESSAGE
                next_stage = "complete"
                is_complete = True
        else:
            message = tech_q_intro
            next_stage = "technicalQuestions"

    # === TECHNICAL QUESTIONS STAGE ===
    elif current_stage == "technicalQuestions":
        if "technicalQA" not in updated_candidate_info:
            updated_candidate_info["technicalQA"] = []
        
        tech_stack = updated_candidate_info.get("techStack", [])
        # Use server-authoritative index if available to avoid client desync
        idx_pointer = session.get("skill_index")
        effective_index = (
            idx_pointer if isinstance(idx_pointer, int) and 0 <= idx_pointer < len(tech_stack)
            else current_tech_question_index
        )
        
        # Store the previous question-answer pair
        if effective_index < len(tech_stack):
            current_skill = tech_stack[effective_index]
            answer = user_message.strip()
            last_question = session.get("last_question", f"Question about {current_skill}")
            
            if answer:
                # Append as a proper Q&A pair
                updated_candidate_info["technicalQA"].append({
                    "question": last_question,
                    "answer": answer
                })
        
        next_index = effective_index + 1
        next_valid_index = get_next_valid_skill_index(tech_stack, next_index)
        
        if next_valid_index is not None:
            next_skill = tech_stack[next_valid_index]
            tech_question_prompt = TECHNICAL_QUESTION_PROMPT.format(skill=next_skill)
            technical_question = clean_llm_output(llama2.generate_response(tech_question_prompt))
            technical_question = clean_technical_question(technical_question)
            
            # Increment sequential question counter for display
            session["question_count"] = session.get("question_count", 0) + 1
            session["skill_index"] = next_valid_index
            session["last_question"] = technical_question  # Store for next iteration
            message = (
                f"Question {session['question_count']} about {next_skill}:\n{technical_question}"
            )
            next_stage = "technicalQuestions"
            current_tech_question_index = next_valid_index
        else:
            message = INTERVIEW_COMPLETE_MESSAGE
            next_stage = "complete"
            is_complete = True

    # === COMPLETE STAGE ===
    elif current_stage == "complete":
        message = INTERVIEW_ALREADY_COMPLETE_MESSAGE
        is_complete = True

    # === SAVE TO MONGODB IF COMPLETE ===
    if is_complete:
        import json
        
        candidate_id = str(uuid.uuid4())
        tech_skills = updated_candidate_info.get("techStack")
        
        if isinstance(tech_skills, str):
            if "," in tech_skills:
                tech_skills = [s.strip() for s in tech_skills.split(",") if s.strip()]
            else:
                tech_skills = [tech_skills.strip()] if tech_skills.strip() else []
        elif not isinstance(tech_skills, list):
            tech_skills = []

        # Get Q&A responses - now properly structured
        qa_responses_list = updated_candidate_info.get("technicalQA", [])
        
        # Fallback to old format if technicalQA doesn't exist (backward compatibility)
        if not qa_responses_list:
            qa_responses = updated_candidate_info.get("technicalAnswers", {})
            if isinstance(qa_responses, str):
                try:
                    qa_responses = json.loads(qa_responses)
                except Exception:
                    qa_responses = {}
            
            qa_responses_list = []
            for q, a in qa_responses.items():
                qa_responses_list.append({"question": str(q).title(), "answer": str(a).strip()})

        years_experience = updated_candidate_info.get("yearsExperience")
        if isinstance(years_experience, str):
            match = re.search(r"\d+", years_experience)
            years_experience = int(match.group(0)) if match else 0

        # Calculate English proficiency score using ScoringService
        answer_texts = [item["answer"] for item in qa_responses_list if item.get("answer")]
        english_proficiency_score = scorer.calculate_proficiency(answer_texts) if answer_texts else 0.0

        candidate = Candidate(
            id=candidate_id,
            name=updated_candidate_info.get("fullName"),
            email=updated_candidate_info.get("email"),
            phone=updated_candidate_info.get("phone"),
            years_experience=years_experience,
            desired_position=updated_candidate_info.get("desiredPosition"),
            location=updated_candidate_info.get("location"),
            tech_skills=tech_skills,
            qa_responses=qa_responses_list,
            english_proficiency_score=english_proficiency_score,
            status="completed"
        )
        candidates_collection = get_candidates_collection()
        candidates_collection.insert_one(candidate.dict())

    return SendMessageResponse(
        message=message,
        nextStage=next_stage,
        updatedCandidateInfo=updated_candidate_info,
        technicalQuestion=technical_question,
        isComplete=is_complete
    )