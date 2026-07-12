import re
import yaml
import spacy
import topic_classifier
import scope_extractor

# Lazy loading of spaCy model
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

# Obligation modal keywords regex
OBLIGATION_KEYWORDS = re.compile(
    r"\b(must|shall|required|should|recommended|expected|may|prohibited|may not)\b",
    re.IGNORECASE
)

def parse_yaml_metadata(file_content: str, filename: str) -> dict:
    """
    Extracts YAML frontmatter from a markdown file.
    Fields parsed: policy_id (or id), policy_name (or title), owner, review_date (or last_reviewed), version, review_history.
    """
    metadata = {
        "policy_id": filename.replace(".md", "").replace(".txt", "").upper(),
        "policy_name": filename.replace(".md", "").replace(".txt", "").replace("_", " ").title(),
        "owner": "Unknown Owner",
        "review_date": "2026-01-01",
        "version": "1.0",
        "review_history": []
    }
    
    body = file_content
    if file_content.strip().startswith("---"):
        parts = file_content.split("---", 2)
        if len(parts) >= 3:
            try:
                yml = yaml.safe_load(parts[1])
                if yml:
                    # Parse policy ID
                    pid = yml.get("policy_id") or yml.get("id")
                    if pid: metadata["policy_id"] = str(pid).strip()
                    
                    # Parse policy name
                    pname = yml.get("policy_name") or yml.get("title") or yml.get("name")
                    if pname: metadata["policy_name"] = str(pname).strip()
                    
                    # Parse owner
                    owner = yml.get("owner")
                    if owner: metadata["owner"] = str(owner).strip()
                    
                    # Parse review date
                    rdate = yml.get("review_date") or yml.get("last_reviewed")
                    if rdate: metadata["review_date"] = str(rdate).strip()
                    
                    # Parse version
                    ver = yml.get("version")
                    if ver: metadata["version"] = str(ver).strip()
                    
                    # Parse review history
                    history = yml.get("review_history")
                    if history:
                        if isinstance(history, list):
                            metadata["review_history"] = history
                        else:
                            metadata["review_history"] = [str(history)]
                            
                body = parts[2]
            except Exception as e:
                print(f"Error parsing frontmatter in {filename}: {e}")
                
    return metadata, body.strip()

def determine_strength(sentence: str) -> str:
    """
    Converts:
    - must, shall, required, prohibited, may not -> Mandatory
    - should, recommended, expected -> Recommended
    - may -> Optional
    """
    sent_lower = sentence.lower()
    mandatory_terms = ["must", "shall", "required", "prohibited", "may not"]
    recommended_terms = ["should", "recommended", "expected"]
    
    for term in mandatory_terms:
        if term in sent_lower:
            return "Mandatory"
            
    for term in recommended_terms:
        if term in sent_lower:
            return "Recommended"
            
    if "may" in sent_lower:
        return "Optional"
        
    return "Mandatory" # Default fallback

def extract_action_and_object(doc, topic: str):
    """
    Extracts action verb and its object target from the sentence dependency tree.
    """
    action = "comply"
    obj = "policy rule"
    
    # 1. Simple verb extraction (look for verbs that fit the compliance context)
    actions_mapping = {
        "rotate": ["rotate", "rotation", "change"],
        "hash": ["hash", "store", "encrypt", "ciphers"],
        "backup": ["backup", "restore", "replicate", "save"],
        "terminate": ["terminate", "logout", "lock", "close"],
        "encrypt": ["encrypt", "transit", "protocols", "use"],
        "require": ["require", "enforce", "mandate"],
        "exempt": ["exempt", "exception", "exclude"]
    }
    
    # Extract action
    found_action = False
    for token in doc:
        if token.pos_ == "VERB":
            lemma = token.lemma_
            # Check if this verb matches our actions
            for mapped_act, synonyms in actions_mapping.items():
                if lemma in synonyms or lemma == mapped_act:
                    action = mapped_act
                    found_action = True
                    break
            if found_action:
                break
                
    if not found_action:
        # Fallback verb
        verbs = [t.lemma_ for t in doc if t.pos_ == "VERB"]
        if verbs:
            action = verbs[0]

    # 2. Extract object target (dobj or pobj of the verb)
    verb_token = None
    for token in doc:
        if token.lemma_ == action and token.pos_ == "VERB":
            verb_token = token
            break
            
    if verb_token:
        # Search direct objects
        for child in verb_token.children:
            if child.dep_ == "dobj":
                obj = child.text.strip()
                # Grab surrounding noun modifiers
                for chunk in doc.noun_chunks:
                    if child in chunk:
                        obj = chunk.text.strip()
                        break
                break
        else:
            # Search preposition objects
            for child in verb_token.children:
                if child.dep_ == "prep":
                    for prep_child in child.children:
                        if prep_child.dep_ == "pobj":
                            obj = prep_child.text.strip()
                            for chunk in doc.noun_chunks:
                                if prep_child in chunk:
                                    obj = chunk.text.strip()
                                    break
                            break
    
    # Fallback to key nouns matching the topic domain
    if obj in ["policy rule", "it"]:
        topic_nouns = {
            "Password": "password",
            "Encryption": "encryption protocols",
            "Access Control": "sessions",
            "Backup": "databases",
            "MFA": "multi-factor authentication",
            "Logging": "audit logs",
            "Network": "network traffic",
            "Firewall": "ports",
            "VPN": "remote connections"
        }
        obj = topic_nouns.get(topic, "policy rule")
        
    return action.title(), obj.title()

def extract_parameters(text: str) -> dict:
    """
    Extracts numeric parameters, times, days, etc.
    """
    params = {}
    text_lower = text.lower()
    
    # Frequency days
    days_match = re.search(r"(\d+)\s*days?", text_lower)
    if days_match:
        params["frequency"] = int(days_match.group(1))
        
    # Inactivity minutes
    min_match = re.search(r"(\d+)\s*minutes?", text_lower)
    if min_match:
        params["inactivity"] = int(min_match.group(1))
        
    # Retention years
    years_match = re.search(r"(\d+)\s*years?", text_lower)
    if years_match:
        params["retention"] = int(years_match.group(1))
        
    # Password length
    len_match = re.search(r"(?:at least|minimum of|min)?\s*(\d+)\s*characters?", text_lower)
    if len_match:
        params["min_length"] = int(len_match.group(1))
        
    # Algorithm
    for alg in ["md5", "sha-256", "sha-1", "bcrypt", "aes-256", "tls 1.0", "windows server 2012"]:
        if alg in text_lower:
            params["algorithm"] = alg
            
    return params

def parse_obligations_from_document(content: str, filename: str) -> list:
    """
    Parses a document content and returns a list of parsed structured obligations.
    """
    nlp = get_nlp()
    metadata, body = parse_yaml_metadata(content, filename)
    
    lines = body.split("\n")
    current_section = "General"
    section_pattern = re.compile(r"^#+\s*(?:Section\s+)?([\d\.]+)?\s*[:\-]?\s*(.*)$", re.IGNORECASE)
    
    extracted_sents = []
    current_text_block = []
    
    def process_block(text, sec):
        if not text.strip():
            return
        doc = nlp(text)
        for sent in doc.sents:
            sent_text = sent.text.strip()
            if OBLIGATION_KEYWORDS.search(sent_text):
                extracted_sents.append({
                    "raw_text": sent_text,
                    "section": sec
                })

    for line in lines:
        match = section_pattern.match(line)
        if match:
            process_block(" ".join(current_text_block), current_section)
            current_text_block = []
            
            sec_num = match.group(1)
            sec_title = match.group(2)
            if sec_num:
                current_section = sec_num.strip()
            else:
                current_section = sec_title.strip()
        else:
            current_text_block.append(line)
            
    process_block(" ".join(current_text_block), current_section)
    
    # Construct obligation JSONs
    obligations = []
    for idx, item in enumerate(extracted_sents):
        raw_text = item["raw_text"]
        doc = nlp(raw_text)
        
        # 1. Topic
        topics = topic_classifier.classify_topics(raw_text)
        primary_topic = topics[0] if topics else "Access Control"
        
        # 2. Scope
        scopes = scope_extractor.extract_scopes(raw_text)
        
        # 3. Action and Object
        action, obj = extract_action_and_object(doc, primary_topic)
        
        # 4. Strength
        strength = determine_strength(raw_text)
        
        # 5. Parameters
        params = extract_parameters(raw_text)
        
        doc_id_clean = metadata["policy_id"]
        obligation_id = f"{doc_id_clean}-{item['section']}-{idx + 1}"
        
        obligations.append({
            "id": obligation_id,
            "policy_id": metadata["policy_id"],
            "policy_name": metadata["policy_name"],
            "owner": metadata["owner"],
            "review_date": metadata["review_date"],
            "version": metadata["version"],
            "review_history": metadata["review_history"],
            "section_number": item["section"],
            "obligation_sentence": raw_text,
            "topic": topics,
            "scope": scopes,
            "action": action,
            "object": obj,
            "obligation_strength": strength,
            "parameters": params
        })
        
    return obligations
