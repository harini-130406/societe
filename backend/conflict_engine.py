import os
from openai import OpenAI

NEGATION_WORDS = ["not", "never", "prohibited", "no", "except", "exempt"]

def has_negation_conflict(text_a: str, text_b: str) -> bool:
    a_lower = text_a.lower()
    b_lower = text_b.lower()
    
    neg_a = any(word in a_lower.split() for word in NEGATION_WORDS) or "may not" in a_lower or "prohibited" in a_lower
    neg_b = any(word in b_lower.split() for word in NEGATION_WORDS) or "may not" in b_lower or "prohibited" in b_lower
    
    return neg_a != neg_b

def run_llm_conflict_adjudication(ob_a: dict, ob_b: dict, similarity: float) -> tuple:
    """
    Optional LLM fallback to adjudicate relationship types and explanations.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, None, None
        
    try:
        client = OpenAI(api_key=api_key)
        prompt = f"""
Analyze the relationship between these two compliance/security obligations:

Obligation A:
- Text: "{ob_a['obligation_sentence']}"
- Topic: {ob_a['topic']}
- Scope: {ob_a['scope']}
- Action: {ob_a['action']}
- Object: {ob_a['object']}
- Strength: {ob_a['obligation_strength']}
- Params: {ob_a['parameters']}

Obligation B:
- Text: "{ob_b['obligation_sentence']}"
- Topic: {ob_b['topic']}
- Scope: {ob_b['scope']}
- Action: {ob_b['action']}
- Object: {ob_b['object']}
- Strength: {ob_b['obligation_strength']}
- Params: {ob_b['parameters']}

Classify their relationship into exactly one of these labels:
1. Direct Conflict: Polar opposites, contradiction of access/action.
2. Parameter Conflict: Same action but mismatching configuration values (length, frequency, etc.).
3. Strength Conflict: Different compliance levels (e.g. Mandatory vs Recommended).
4. Scope Conflict: Contradictory instructions for the same actor or system.
5. Temporal Conflict: Contradictory timing constraints (duration, frequency, inactivity limit).
6. Exception Relationship: One acts as a general rule, and the other is a specific exemption/exclusion for a subgroup (e.g. developers).
7. Complementary: They add different details without contradiction.
8. Unrelated: No direct connection.

Provide a JSON response with fields:
- "label": Selected relationship label (exactly one of the labels above).
- "confidence_score": Float between 0.0 and 1.0.
- "reason": One-line plain English explanation of the relation.

JSON response:
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1,
            timeout=5.0
        )
        import json
        res_data = json.loads(response.choices[0].message.content)
        return res_data["label"], res_data["confidence_score"], res_data["reason"]
    except Exception as e:
        print(f"LLM conflict adjudication failed: {e}")
        return None, None, None

def evaluate_relationship(ob_a: dict, ob_b: dict, similarity: float) -> dict:
    """
    Compares two obligations and detects relationship type, confidence score, and reason.
    """
    # 1. Topic check: must share at least one topic
    topics_a = set(ob_a["topic"])
    topics_b = set(ob_b["topic"])
    common_topics = topics_a.intersection(topics_b)
    
    if not common_topics:
        return {
            "type": "Unrelated",
            "confidence_score": 0.0,
            "reason": "Obligations cover different topics."
        }
        
    # Check similarity threshold
    if similarity < 0.45:
        return {
            "type": "Unrelated",
            "confidence_score": 0.1,
            "reason": f"Topic similarity is too low ({similarity:.2f})."
        }

    # Extract properties
    action_a = ob_a["action"].lower()
    action_b = ob_b["action"].lower()
    strength_a = ob_a["obligation_strength"]
    strength_b = ob_b["obligation_strength"]
    scopes_a = set(ob_a["scope"])
    scopes_b = set(ob_b["scope"])
    params_a = ob_a["parameters"]
    params_b = ob_b["parameters"]

    # Check scopes relationship
    same_scope = scopes_a == scopes_b
    is_exception_scope = len(scopes_a.intersection(scopes_b)) > 0 and not same_scope
    is_one_general = "All Employees" in scopes_a or "All Employees" in scopes_b
    is_scope_subset = (scopes_a.issubset(scopes_b) or scopes_b.issubset(scopes_a)) and not same_scope
    
    # --- RULE ENGINE ---
    
    # 1. Exception Relationship (Scope exclusions / exemptions)
    # E.g. General rule vs specific role exception
    if (is_exception_scope or is_scope_subset or is_one_general) and not same_scope:
        if has_negation_conflict(ob_a["obligation_sentence"], ob_b["obligation_sentence"]) or params_a != params_b:
            narrow_scope = list(scopes_a)[0] if len(scopes_a) < len(scopes_b) else list(scopes_b)[0]
            if "All Employees" in narrow_scope and len(scopes_a) > 1:
                # Handle edge cases
                narrow_scope = list(scopes_b)[0] if "All Employees" in list(scopes_a)[0] else list(scopes_a)[0]
                
            return {
                "type": "Exception Relationship",
                "confidence_score": 0.85,
                "reason": f"Scope exemption detected: narrow scope '{narrow_scope}' is exempted or modified from the general policy."
            }

    # 2. Direct Conflict (Same action, same scope, opposite polarity)
    if action_a == action_b and same_scope:
        if has_negation_conflict(ob_a["obligation_sentence"], ob_b["obligation_sentence"]):
            return {
                "type": "Direct Conflict",
                "confidence_score": 0.95,
                "reason": "Direct contradiction: one policy mandates while the other prohibits or exempts the same action."
            }

    # 3. Temporal Conflict (Conflicts in timing, inactive timeouts, retention durations)
    # Check if temporal params are present
    temporal_keys = ["frequency", "inactivity", "retention"]
    has_temporal_diff = False
    temp_key_matched = None
    
    for key in temporal_keys:
        if key in params_a and key in params_b:
            if params_a[key] != params_b[key]:
                has_temporal_diff = True
                temp_key_matched = key
                break
                
    if has_temporal_diff and same_scope:
        return {
            "type": "Temporal Conflict",
            "confidence_score": 0.90,
            "reason": f"Temporal mismatch: different timing limits detected for '{temp_key_matched}' ({params_a[temp_key_matched]} vs {params_b[temp_key_matched]})."
        }

    # 4. Parameter Conflict (Same action, same scope, different numeric configuration params)
    # E.g. min_length 8 vs 14
    param_diff = False
    param_key_matched = None
    for k in params_a:
        if k in params_b and k not in temporal_keys:
            if params_a[k] != params_b[k]:
                param_diff = True
                param_key_matched = k
                break
                
    if param_diff and same_scope:
        return {
            "type": "Parameter Conflict",
            "confidence_score": 0.90,
            "reason": f"Parameter mismatch: conflicting value detected for '{param_key_matched}' ({params_a[param_key_matched]} vs {params_b[param_key_matched]})."
        }

    # 5. Strength Conflict (Same action, same params, different compliance levels)
    # E.g. Mandatory vs Recommended
    if action_a == action_b and params_a == params_b and same_scope and strength_a != strength_b:
        return {
            "type": "Strength Conflict",
            "confidence_score": 0.80,
            "reason": f"Strength level mismatch: one policy states action is '{strength_a}' while the other states it is '{strength_b}'."
        }

    # 6. Scope Conflict (Contradictory actions applying to the exact same scope)
    if same_scope and action_a != action_b and similarity > 0.70:
        if has_negation_conflict(ob_a["obligation_sentence"], ob_b["obligation_sentence"]):
            return {
                "type": "Scope Conflict",
                "confidence_score": 0.85,
                "reason": f"Scope execution conflict: same scope '{list(scopes_a)[0]}' is given contradictory instructions for related actions."
            }

    # --- LLM FALLBACK FOR AMBIGUOUS MID-BAND ---
    if 0.60 <= similarity <= 0.85:
        llm_type, llm_conf, llm_reason = run_llm_conflict_adjudication(ob_a, ob_b, similarity)
        if llm_type:
            return {
                "type": llm_type,
                "confidence_score": llm_conf,
                "reason": llm_reason
            }

    # 7. Complementary (Related topic, high similarity, no direct rule contradiction)
    if similarity >= 0.50:
        return {
            "type": "Complementary",
            "confidence_score": round(similarity, 2),
            "reason": f"Obligations are complementary and build upon the topic '{list(common_topics)[0]}'."
        }

    return {
        "type": "Unrelated",
        "confidence_score": 0.2,
        "reason": "Obligations are unrelated."
    }
