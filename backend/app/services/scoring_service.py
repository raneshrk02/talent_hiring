import logging
import spacy  # type: ignore
from typing import List, Dict

class ScoringService:
    def __init__(self):
        try:
            # Prefer the small English model for better tagging/lemmatization
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            # Graceful fallback to a blank English pipeline to avoid runtime crashes
            logging.warning(
                "Falling back to spacy.blank('en') because 'en_core_web_sm' is not available: %s",
                e,
            )
            self.nlp = spacy.blank("en")
            # Add a simple rule-based sentencizer for sentence boundaries
            if "sentencizer" not in self.nlp.pipe_names:
                self.nlp.add_pipe("sentencizer")
    
    def calculate_proficiency(self, responses: List[str]) -> float:
        scores = []
        
        for response in responses:
            doc = self.nlp(response)
            
            # Metrics
            word_count = len([token for token in doc if not token.is_punct])
            avg_word_length = sum(len(token.text) for token in doc if not token.is_punct) / max(word_count, 1)
            sentence_count = len(list(doc.sents))
            complex_words = len([token for token in doc if len(token.text) > 7])
            
            # Vocabulary diversity
            unique_words = len(set([token.lemma_ for token in doc if not token.is_stop and not token.is_punct]))
            vocab_diversity = unique_words / max(word_count, 1)
            
            # Grammar (approximate via dependency parsing)
            proper_structure = sum(1 for token in doc if token.dep_ in ['nsubj', 'ROOT', 'dobj'])
            grammar_score = proper_structure / max(word_count, 1)
            
            # Calculate individual score
            score = (
                min(word_count / 50, 1) * 0.2 +  # Length
                min(avg_word_length / 6, 1) * 0.15 +  # Word complexity
                vocab_diversity * 0.25 +  # Diversity
                grammar_score * 0.25 +  # Structure
                min(complex_words / 10, 1) * 0.15  # Advanced vocabulary
            ) * 100
            
            scores.append(score)
        
        return round(sum(scores) / len(scores), 2) if scores else 0.0