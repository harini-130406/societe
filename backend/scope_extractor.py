import spacy

# Lazy loading of spaCy model
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

# Scope keywords mapping to normalized names (matching ground truth format)
SCOPE_MAPPING = {
    "all users": [
        "all users", "all employees", "all staff", "every employee", "all workers", 
        "general staff", "users", "all user"
    ],
    "employees": [
        "employee", "employees", "staff", "worker", "workers"
    ],
    "developers": [
        "developer", "developers", "engineer", "engineers", "dev team", 
        "programmer", "programmers", "development team"
    ],
    "admins": [
        "administrator", "administrators", "admin", "admins", "superuser", 
        "superusers", "sysadmin", "sysadmins", "root"
    ],
    "contractors": [
        "contractor", "contractors", "vendor", "consultant", "external worker", "third-party"
    ]
}

def extract_scopes(text: str) -> list:
    """
    Extracts one or more scopes from the text.
    If no matches are found, uses spaCy dependency parsing to extract the subject noun chunk.
    """
    nlp = get_nlp()
    text_lower = text.lower()
    extracted = []
    
    # 1. Keyword check
    for scope_name, patterns in SCOPE_MAPPING.items():
        for pattern in patterns:
            if pattern in text_lower:
                extracted.append(scope_name.lower())
                break
                
    if extracted:
        # Avoid duplicate general entries if specific ones are found
        if len(extracted) > 1 and "all employees" in extracted:
            extracted.remove("all employees")
        return list(set(extracted))
        
    # 2. Dependency parsing fallback: Extract nsubj (nominal subject) of the sentence
    doc = nlp(text)
    subjects = []
    for token in doc:
        if token.dep_ == "nsubj" and token.pos_ in ["NOUN", "PROPN", "PRON"]:
            # Get the full noun chunk containing the subject
            for chunk in doc.noun_chunks:
                if token in chunk:
                    subjects.append(chunk.text.strip().title())
                    break
            else:
                subjects.append(token.text.strip().title())
                
    if subjects:
        # Map dynamic subjects to ground truth scopes only
        cleaned_subjects = []
        for sub in subjects:
            s_lower = sub.lower()
            if "user" in s_lower:
                cleaned_subjects.append("all users")
            elif "employee" in s_lower or "staff" in s_lower:
                cleaned_subjects.append("employees")
            elif "developer" in s_lower or "engineer" in s_lower or "programmer" in s_lower:
                cleaned_subjects.append("developers")
            elif "admin" in s_lower:
                cleaned_subjects.append("admins")
            elif "contractor" in s_lower or "vendor" in s_lower:
                cleaned_subjects.append("contractors")
            else:
                cleaned_subjects.append("all users")  # Default fallback
        return list(set(cleaned_subjects))
        
    return ["all users"] # Default fallback
