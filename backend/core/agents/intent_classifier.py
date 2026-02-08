"""
Intent classification logic for the Todo AI Chatbot application.
"""
from typing import Dict, Any, Tuple, Optional
import re
from enum import Enum
from pydantic import BaseModel


class Intent(str, Enum):
    """
    Enumeration of recognized intents in the Todo AI Chatbot.
    """
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"
    HELP = "help"
    UNKNOWN = "unknown"


class ClassifiedIntent(BaseModel):
    """
    Model for representing a classified intent with confidence and extracted entities.
    """
    intent: Intent
    confidence: float
    entities: Dict[str, Any]
    original_text: str


class IntentClassifier:
    """
    Class responsible for analyzing user input to determine intent
    and extracting relevant entities for task operations.
    """

    def __init__(self):
        # Define intent patterns with associated keywords and regex
        self.intent_patterns = {
            Intent.ADD_TASK: [
                r'\b(add|create|make|new|establish|setup)\b.*\b(task|todo|item|thing|note|reminder)\b',
                r'\b(task|todo|item|thing|note|reminder)\b.*\b(add|create|make|new|establish|setup)\b',
                r'\b(remind me to|need to|want to|should|must|have to)\b',
                r'\b(make a note|write down|put in my list)\b'
            ],
            Intent.LIST_TASKS: [
                r'\b(show|list|view|see|display|fetch|get)\b.*\b(task|todo|item|things|notes|reminders)\b',
                r'\b(what are|do i have|show me|display|list)\b.*\b(task|todo|item|things|notes|reminders)\b',
                r'\b(my tasks|my todos|my list|current tasks)\b'
            ],
            Intent.COMPLETE_TASK: [
                r'\b(mark|complete|finish|done|check off|tick off)\b.*\b(task|todo|item|thing)\b',
                r'\b(task|todo|item|thing)\b.*\b(mark|complete|finish|done|as done)\b',
                r'\b(is done|finished|completed|checked|ticked)\b',
                r"\b(i'm done with|i finished|completed|done with)\b"
            ],
            Intent.DELETE_TASK: [
                r'\b(delete|remove|erase|cancel|eliminate|get rid of)\b.*\b(task|todo|item|thing)\b',
                r'\b(task|todo|item|thing)\b.*\b(delete|remove|erase|cancel|eliminate|get rid of)\b'
            ],
            Intent.UPDATE_TASK: [
                r'\b(update|change|modify|edit|adjust|alter|redo|revise)\b.*\b(task|todo|item|thing)\b',
                r'\b(task|todo|item|thing)\b.*\b(update|change|modify|edit|adjust|alter|redo|revise)\b',
                r'\b(rename|change to|modify to|update to)\b'
            ],
            Intent.HELP: [
                r'\b(help|support|assistance|instruction|how to|what can you do|can you|could you)\b',
                r'\b(tutorial|guide|assist|aid|manual)\b'
            ]
        }

        # Define entity extraction patterns
        self.entity_patterns = {
            'title': [
                # After task creation verbs
                r'(?:add|create|make|new)\s+(?:a\s+)?(?:task|todo|note|item|reminder)\s+to\s+(.*?)(?:\s+and|\s+for|\s+by|\s+on|\s+at|\.|$)',
                r'(?:remind me to|need to|want to)\s+(.*?)(?:\s+and|\s+for|\s+by|\s+on|\s+at|\.|$)',
                # After update verbs
                r'(?:update|change|modify|edit|rename)\s+(?:task|todo|item)\s+(?:named\s+|called\s+|titled\s+)?(.*)',
            ],
            'date': [
                r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
                r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b',  # MM/DD/YYYY or MM-DD-YYYY
                r'\b(today|tomorrow|yesterday|tonight|now)\b',
                r'\b(next\s+(?:week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b',
                r'\b(this\s+(?:week|month|weekend))\b'
            ],
            'priority': [
                r'\b(urgent|high|top|critical|important|medium|normal|low|lowest)\b',
                r'\b(priority\s+(?:is\s+)?(high|medium|low|urgent))\b'
            ],
            'category': [
                r'\b(in\s+(?:work|personal|shopping|health|finance|home|school|other))\b',
                r'\b(for\s+(?:work|personal|shopping|health|finance|home|school|other))\b',
                r'\b(category\s+(?:is\s+)?(work|personal|shopping|health|finance|home|school|other))\b'
            ]
        }

    def classify_intent(self, text: str) -> ClassifiedIntent:
        """
        Classify the intent of the given text and extract relevant entities.

        Args:
            text: The input text to classify

        Returns:
            ClassifiedIntent object with detected intent and extracted entities
        """
        original_text = text.lower().strip()
        if not original_text:
            return ClassifiedIntent(
                intent=Intent.UNKNOWN,
                confidence=0.0,
                entities={},
                original_text=text
            )

        # Calculate scores for each intent
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = self._calculate_intent_score(original_text, patterns)
            intent_scores[intent] = score

        # Find the intent with the highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        best_score = intent_scores[best_intent]

        # If no intent exceeds threshold, return unknown
        threshold = 0.1
        if best_score < threshold:
            return ClassifiedIntent(
                intent=Intent.UNKNOWN,
                confidence=best_score,
                entities={},
                original_text=text
            )

        # Extract entities from the text
        entities = self._extract_entities(original_text)

        # Calculate confidence as normalized score
        confidence = min(best_score, 1.0)

        return ClassifiedIntent(
            intent=best_intent,
            confidence=confidence,
            entities=entities,
            original_text=text
        )

    def _calculate_intent_score(self, text: str, patterns: list) -> float:
        """
        Calculate a score for how well the text matches the given patterns.

        Args:
            text: The input text
            patterns: List of regex patterns to match

        Returns:
            Score between 0 and infinity (higher is better)
        """
        score = 0.0

        # Count direct keyword matches (higher weight)
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            score += len(matches) * 2.0  # Give higher weight to pattern matches

        # Count word overlaps (lower weight)
        words = text.split()
        for pattern in patterns:
            compiled_pattern = re.compile(pattern, re.IGNORECASE)
            if compiled_pattern.search(text):
                # Count overlapping words between pattern and text
                pattern_words = set(re.findall(r'\w+', pattern))
                text_words = set(words)
                overlap = len(pattern_words.intersection(text_words))
                score += overlap * 0.5

        return score

    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract named entities from the text based on predefined patterns.

        Args:
            text: The input text to extract entities from

        Returns:
            Dictionary mapping entity types to extracted values
        """
        entities = {}

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Store the first match for each entity type
                    # Convert to lowercase for consistency, except for dates which should preserve format
                    if entity_type != 'date':
                        processed_matches = [match.lower() if isinstance(match, str) else match for match in matches]
                    else:
                        processed_matches = matches

                    entities[entity_type] = processed_matches[0] if len(processed_matches) == 1 else processed_matches
                    break  # Stop at first match for each entity type

        # Special handling for task titles
        if 'title' not in entities:
            # Try to extract title from common phrases
            title_match = re.search(r'(?:add|create|make|new)\s+(?:a\s+)?(?!task|todo|item|note|reminder)(\w+(?:\s+\w+)*?)(?:\s+and|\s+for|\s+by|\s+on|\s+at|\.|$)', text, re.IGNORECASE)
            if title_match:
                entities['title'] = title_match.group(1).strip()

        return entities

    def refine_intent_with_entities(self, classified_intent: ClassifiedIntent) -> ClassifiedIntent:
        """
        Refine the classified intent based on extracted entities.

        Args:
            classified_intent: The initially classified intent

        Returns:
            Possibly refined ClassifiedIntent
        """
        # If we couldn't classify an intent but have a title, assume it's an add_task
        if classified_intent.intent == Intent.UNKNOWN and 'title' in classified_intent.entities:
            return ClassifiedIntent(
                intent=Intent.ADD_TASK,
                confidence=0.8,
                entities=classified_intent.entities,
                original_text=classified_intent.original_text
            )

        # If we have update entities, refine to update_task
        if classified_intent.intent == Intent.UNKNOWN:
            update_indicators = ['title', 'date', 'priority', 'category']
            if any(indicator in classified_intent.entities for indicator in update_indicators):
                return ClassifiedIntent(
                    intent=Intent.UPDATE_TASK,
                    confidence=0.7,
                    entities=classified_intent.entities,
                    original_text=classified_intent.original_text
                )

        return classified_intent


# Global classifier instance
classifier = IntentClassifier()


def classify_intent(text: str) -> ClassifiedIntent:
    """
    Convenience function to classify intent using the global classifier instance.

    Args:
        text: The input text to classify

    Returns:
        ClassifiedIntent object with detected intent and extracted entities
    """
    result = classifier.classify_intent(text)
    return classifier.refine_intent_with_entities(result)