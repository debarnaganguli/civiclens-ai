import re

def analyze_document(original_text, summary_text):
    original_words = len(original_text.split())
    summary_words = len(summary_text.split())
    
    if original_words == 0:
        reduction_percentage = 0
    else:
        reduction_percentage = max(0, int((1 - (summary_words / original_words)) * 100))
        
    sentences = re.split(r'[.!?]+', original_text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    return {
        "original_word_count": original_words,
        "summary_word_count": summary_words,
        "reduction_percentage": reduction_percentage,
        "sentence_count": sentence_count
    }

def extract_important_info(text):
    info = {
        "dates": [],
        "requirements": [],
        "actions": []
    }
    
    lines = text.split('\n')
    for line in lines:
        lower_line = line.lower()
        
        # Simple date extraction
        date_patterns = [
            r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?\b',
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, lower_line)
            for match in matches:
                # Add capitalized version for cleaner UI
                clean_match = match.title()
                if clean_match not in info["dates"]:
                    info["dates"].append(clean_match)
                    
        # Simple requirements extraction
        req_keywords = ["must", "require", "mandatory", "necessary", "eligible"]
        req_pattern = r'\b(?:' + '|'.join(req_keywords) + r')\b'
        if re.search(req_pattern, lower_line):
            if 5 < len(line.split()) < 35: # Exclude headers or very long paragraphs
                if line.strip() not in info["requirements"]:
                    info["requirements"].append(line.strip())
                
        # Simple actions extraction
        action_keywords = ["submit", "apply", "register", "action", "deadline", "please"]
        action_pattern = r'\b(?:' + '|'.join(action_keywords) + r')\b'
        if re.search(action_pattern, lower_line):
            if 5 < len(line.split()) < 35:
                if line.strip() not in info["actions"] and line.strip() not in info["requirements"]:
                    info["actions"].append(line.strip())
                
    # Deduplicate and limit to top 5 items
    info["dates"] = list(dict.fromkeys(info["dates"]))[:5]
    info["requirements"] = list(dict.fromkeys(info["requirements"]))[:5]
    info["actions"] = list(dict.fromkeys(info["actions"]))[:5]
    
    return info
