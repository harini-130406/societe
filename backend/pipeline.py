import os
import json
import datetime
import numpy as np
import networkx as nx

# Import new modular components
import parser
import topic_classifier
import scope_extractor
import stale_checker
import conflict_engine
import redundancy_engine

def map_strength_to_old(strength: str) -> str:
    """
    Maps 'Mandatory'/'Recommended'/'Optional' to old lowercase representation.
    """
    if strength == "Mandatory":
        return "mandatory"
    return "advisory"

def map_scope_to_old(scopes: list) -> str:
    """
    Maps scopes list to old string format.
    """
    if not scopes:
        return "all"
    primary = scopes[0].lower().replace(" ", "_")
    if len(scopes) > 1:
        return f"all_{primary}s_and_others"
    return primary

def map_params_to_old(parameters: dict) -> dict:
    """
    Maps parameters to old keys.
    """
    old_params = {}
    if "frequency" in parameters:
        old_params["frequency_days"] = parameters["frequency"]
    if "inactivity" in parameters:
        old_params["inactivity_minutes"] = parameters["inactivity"]
    if "retention" in parameters:
        old_params["retention_years"] = parameters["retention"]
    if "min_length" in parameters:
        old_params["min_length"] = parameters["min_length"]
    if "algorithm" in parameters:
        old_params["algorithm"] = parameters["algorithm"]
    return old_params

def map_relation_type_to_old(new_type: str) -> str:
    """
    Maps specific new relation types to the old high-level categories (CONFLICT, POTENTIAL_CONFLICT, REDUNDANT, COMPLEMENTARY).
    """
    mapping = {
        "Direct Conflict": "CONFLICT",
        "Parameter Conflict": "POTENTIAL_CONFLICT",
        "Temporal Conflict": "POTENTIAL_CONFLICT",
        "Scope Conflict": "CONFLICT",
        "Strength Conflict": "POTENTIAL_CONFLICT",
        "Exception Relationship": "COMPLEMENTARY",
        "Complementary": "COMPLEMENTARY",
        "Redundant": "REDUNDANT",
        "Unrelated": "UNRELATED"
    }
    return mapping.get(new_type, "COMPLEMENTARY")

def analyze_policies_in_directory(directory_path: str) -> dict:
    """
    End-to-end analyzer: reads directory, runs modular parses, checks staleness,
    runs similarity, finds relationships, builds graph, dumps to analysis.json,
    and returns dashboard results.
    """
    # Ensure folder exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

    raw_obligations = []
    
    # 1. Read files and extract obligations using parser.py
    files = [f for f in os.listdir(directory_path) if f.endswith(".md") or f.endswith(".txt")]
    for filename in files:
        filepath = os.path.join(directory_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        parsed_obs = parser.parse_obligations_from_document(content, filename)
        # Add filename to each parsed obligation for tracking
        for obs in parsed_obs:
            obs["filename"] = filename
        raw_obligations.extend(parsed_obs)
            
    # 2. Check staleness & metadata issues using stale_checker.py
    stale_policies_count = 0
    stale_docs_set = set()
    total_superseded_refs = 0
    
    obligations_list = []
    
    for obj in raw_obligations:
        metadata = {
            "review_date": obj["review_date"],
            "owner": obj["owner"],
            "version": obj["version"],
            "review_history": obj["review_history"]
        }
        
        staleness_res = stale_checker.check_staleness(obj["obligation_sentence"], metadata, obj["filename"])
        
        # Add staleness status to parsed obligation
        obj["is_stale"] = staleness_res["is_stale"]
        obj["is_date_stale"] = staleness_res["is_date_stale"]
        obj["staleness_reasons"] = staleness_res["reasons"]
        
        if staleness_res["is_date_stale"]:
            stale_docs_set.add(obj["filename"])
            
        # Count EOL references
        if any("superseded" in r.lower() for r in staleness_res["reasons"]):
            total_superseded_refs += 1
            
        # Construct backward-compatible fields alongside the new ones
        compat_obj = obj.copy()
        # Use the actual filename from the file parameter
        compat_obj["source_doc"] = obj["filename"]
            
        compat_obj["section"] = obj["section_number"]
        compat_obj["raw_text"] = obj["obligation_sentence"]
        compat_obj["topic"] = obj["topic"][0].lower() if obj["topic"] else "access_control"
        compat_obj["action"] = obj["action"].lower()
        compat_obj["scope"] = map_scope_to_old(obj["scope"])
        compat_obj["strength"] = map_strength_to_old(obj["obligation_strength"])
        compat_obj["params"] = map_params_to_old(obj["parameters"])
        compat_obj["last_reviewed"] = obj["review_date"]
        
        obligations_list.append(compat_obj)
        
    stale_policies_count = len(stale_docs_set)

    # 3. Analyze relations using similarity + conflict engine
    relations_list = []
    n = len(obligations_list)
    
    if n >= 2:
        # Precompute sentence embeddings for all obligations to speed up calculations
        embedder = redundancy_engine.get_embedder()
        texts = [obj["obligation_sentence"] for obj in obligations_list]
        embeddings = embedder.encode(texts, show_progress_bar=False)
        
        # Similarity matrix
        similarity_matrix = np.dot(embeddings, embeddings.T) / (
            np.linalg.norm(embeddings, axis=1)[:, None] * np.linalg.norm(embeddings, axis=1)
        )
        
        for i in range(n):
            for j in range(i + 1, n):
                obj_a = obligations_list[i]
                obj_b = obligations_list[j]
                similarity = float(similarity_matrix[i, j])
                
                # Check if they share any topics (topic classifier returns lists)
                topics_a = set(obj_a["topic"] if isinstance(obj_a["topic"], list) else [obj_a["topic"]])
                topics_b = set(obj_b["topic"] if isinstance(obj_b["topic"], list) else [obj_b["topic"]])
                if not topics_a.intersection(topics_b):
                    # Direct check on legacy single topic string as fallback
                    if obj_a["topic"] != obj_b["topic"]:
                        continue
                
                # Evaluate relationship
                rel_res = conflict_engine.evaluate_relationship(obj_a, obj_b, similarity)
                
                # If they are Redundant, adjust type
                if rel_res["type"] == "Complementary" and similarity > 0.85 and obj_a["action"] == obj_b["action"] and obj_a["parameters"] == obj_b["parameters"] and obj_a["scope"] == obj_b["scope"]:
                    rel_res["type"] = "Redundant"
                    rel_res["reason"] = f"Both '{obj_a['source_doc']}' (Sec {obj_a['section']}) and '{obj_b['source_doc']}' (Sec {obj_b['section']}) set identical requirements for {obj_a['scope']}."
                
                if rel_res["type"] != "Unrelated":
                    mapped_type = map_relation_type_to_old(rel_res["type"])
                    
                    relations_list.append({
                        "id": f"rel-{obj_a['id']}-{obj_b['id']}",
                        "source_id": obj_a["id"],
                        "target_id": obj_b["id"],
                        "source_doc": obj_a["source_doc"],
                        "target_doc": obj_b["source_doc"],
                        "source_section": obj_a["section"],
                        "target_section": obj_b["section"],
                        "source_text": obj_a["raw_text"],
                        "target_text": obj_b["raw_text"],
                        "type": mapped_type,              # Old type for backward compatibility (CONFLICT, REDUNDANT, etc.)
                        "specific_type": rel_res["type"], # New custom type (Direct Conflict, Parameter Conflict, etc.)
                        "confidence_score": rel_res["confidence_score"],
                        "reason": rel_res["reason"],
                        "similarity": similarity,
                        "explanation": rel_res["reason"]
                    })

    # 4. Build NetworkX Graph
    graph_data = build_graph_data(obligations_list, relations_list)
    
    # 5. Dashboard indicators & Health Score calculation
    conflicts_count = sum(1 for r in relations_list if r["type"] == "CONFLICT")
    potential_conflicts_count = sum(1 for r in relations_list if r["type"] == "POTENTIAL_CONFLICT")
    redundancies_count = sum(1 for r in relations_list if r["type"] == "REDUNDANT")
    
    deductions = (
        (stale_policies_count * 15) +
        (conflicts_count * 10) +
        (potential_conflicts_count * 5) +
        (redundancies_count * 3) +
        (total_superseded_refs * 5)
    )
    health_score = max(0, min(100, 100 - deductions))
    
    analysis_results = {
        "health_score": health_score,
        "metrics": {
            "conflicts": conflicts_count + potential_conflicts_count,
            "redundancies": redundancies_count,
            "stale_policies": stale_policies_count + total_superseded_refs,
            "total_obligations": len(obligations_list)
        },
        "obligations": obligations_list,
        "relations": relations_list,
        "graph": graph_data
    }
    
    # 6. Store everything in analysis.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_json_path = os.path.join(base_dir, "analysis.json")
    try:
        with open(analysis_json_path, "w", encoding="utf-8") as json_file:
            json.dump(analysis_results, json_file, indent=2)
    except Exception as e:
        print(f"Failed to write analysis.json: {e}")
        
    return analysis_results

def build_graph_data(obligations: list, relations: list) -> dict:
    """
    Constructs relationship graph and exports JSON node/edge lists.
    """
    G = nx.Graph()
    
    topic_colors = {
        "password": "#4F46E5",
        "encryption": "#06B6D4",
        "access_control": "#10B981",
        "data_retention": "#3B82F6",
        "logging": "#8B5CF6",
        "network": "#EC4899",
        "mfa": "#F59E0B",
        "backup": "#14B8A6",
        "acceptable_use": "#6B7280",
        "data_classification": "#EF4444"
    }
    
    for obj in obligations:
        G.add_node(
            obj["id"],
            label=f"{obj['id']} ({obj['topic']})",
            title=f"Doc: {obj['source_doc']}<br>Sec: {obj['section']}<br>{obj['raw_text']}",
            color=topic_colors.get(obj["topic"], "#9CA3AF"),
            topic=obj["topic"],
            is_stale=obj["is_stale"]
        )
        
    edge_colors = {
        "CONFLICT": "#EF4444",
        "POTENTIAL_CONFLICT": "#F59E0B",
        "REDUNDANT": "#F97316",
        "COMPLEMENTARY": "#10B981"
    }
    
    for rel in relations:
        G.add_edge(
            rel["source_id"],
            rel["target_id"],
            type=rel["type"],
            color=edge_colors.get(rel["type"], "#9CA3AF"),
            title=rel["explanation"],
            weight=float(rel["similarity"])
        )
        
    nodes_list = []
    for node, attrs in G.nodes(data=True):
        nodes_list.append({
            "id": node,
            "label": attrs["label"],
            "title": attrs["title"],
            "color": attrs["color"],
            "topic": attrs["topic"],
            "is_stale": attrs["is_stale"]
        })
        
    edges_list = []
    for u, v, attrs in G.edges(data=True):
        edges_list.append({
            "from": u,
            "to": v,
            "type": attrs["type"],
            "color": attrs["color"],
            "title": attrs["title"],
            "weight": attrs["weight"]
        })
        
    return {
        "nodes": nodes_list,
        "edges": edges_list
    }
