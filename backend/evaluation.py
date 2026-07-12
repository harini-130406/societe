import os
import json
import pipeline

def run_evaluation():
    # 1. Load ground truth
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_data_dir = os.path.join(base_dir, "sample_data")
    policies_dir = os.path.join(sample_data_dir, "policies")
    
    gt_ob_path = os.path.join(sample_data_dir, "obligation_extracts_labels.json")
    gt_findings_path = os.path.join(sample_data_dir, "findings_labels.json")
    
    with open(gt_ob_path, "r", encoding="utf-8") as f:
        gt_obligations = json.load(f)
        
    with open(gt_findings_path, "r", encoding="utf-8") as f:
        gt_findings = json.load(f)
        
    # 2. Run actual pipeline
    results = pipeline.analyze_policies_in_directory(policies_dir)
    extracted_obligations = results["obligations"]
    extracted_relations = results["relations"]
    
    # --- EVALUATE OBLIGATION EXTRACTION ---
    # Match by policy_file + topic only (ignoring scope since ground truth scopes are synthetic)
    tp_ob = 0
    fp_ob = 0
    fn_ob = 0
    
    gt_matched_obs = set()
    
    # Index ground truth by (policy_file, topic)
    gt_index = {}
    for idx, gt_ob in enumerate(gt_obligations):
        key = (gt_ob["policy_file"], gt_ob["topic"])
        if key not in gt_index:
            gt_index[key] = []
        gt_index[key].append(idx)
    
    for ext_ob in extracted_obligations:
        matched = False
        ext_doc = ext_ob["source_doc"]
        ext_topic = ext_ob["topic"].lower() if isinstance(ext_ob["topic"], str) else ext_ob["topic"][0].lower() if ext_ob["topic"] else "unknown"
        
        # Try to find matching ground truth
        key = (ext_doc, ext_topic)
        if key in gt_index and gt_index[key]:
            # Match found
            tp_ob += 1
            gt_matched_obs.add(gt_index[key].pop(0))
            matched = True
        
        if not matched:
            fp_ob += 1
            
    fn_ob = len(gt_obligations) - len(gt_matched_obs)
    
    precision_ob = tp_ob / (tp_ob + fp_ob) if (tp_ob + fp_ob) > 0 else 0.0
    recall_ob = tp_ob / (tp_ob + fn_ob) if (tp_ob + fn_ob) > 0 else 0.0
    f1_ob = 2 * (precision_ob * recall_ob) / (precision_ob + recall_ob) if (precision_ob + recall_ob) > 0 else 0.0
    
    # --- EVALUATE FINDINGS (CONFLICT, REDUNDANCY, STALE) ---
    # Findings: we match based on policy pairs for conflicts/redundancies, single policy for staleness
    tp_conflict = 0
    fn_conflict = 0
    tp_redundancy = 0
    fn_redundancy = 0
    tp_stale = 0
    fn_stale = 0
    
    fp_relations = 0
    
    # Index GT findings
    gt_conflict_pairs = set()
    gt_redundancy_pairs = set()
    gt_stale_policies = set()
    
    for gt in gt_findings:
        if gt["finding_type"] == "CONFLICT":
            policy_a = gt.get("policy_a", "")
            policy_b = gt.get("policy_b", "")
            if policy_a and policy_b:
                pair = tuple(sorted([policy_a, policy_b]))
                gt_conflict_pairs.add(pair)
        elif gt["finding_type"] == "REDUNDANCY":
            policy_a = gt.get("policy_a", "")
            policy_b = gt.get("policy_b", "")
            if policy_a and policy_b:
                pair = tuple(sorted([policy_a, policy_b]))
                gt_redundancy_pairs.add(pair)
        elif gt["finding_type"] == "STALE":
            policy = gt.get("policy", "")
            if policy:
                gt_stale_policies.add(policy)
                
    # Index Extracted findings
    predicted_conflict_pairs = set()
    predicted_redundancy_pairs = set()
    predicted_stale_policies = set()
    
    for ext in extracted_relations:
        policy_a = ext["source_doc"]
        policy_b = ext["target_doc"]
        pair = tuple(sorted([policy_a, policy_b]))
        
        if ext["type"] in ["CONFLICT", "POTENTIAL_CONFLICT"]:
            predicted_conflict_pairs.add(pair)
        elif ext["type"] == "REDUNDANT":
            predicted_redundancy_pairs.add(pair)
    
    # Check stale policies from extracted obligations
    for ext_ob in extracted_obligations:
        if ext_ob["is_stale"]:
            predicted_stale_policies.add(ext_ob["source_doc"])
            
    # Calculate Conflict Metrics
    for pair in gt_conflict_pairs:
        if pair in predicted_conflict_pairs:
            tp_conflict += 1
        else:
            fn_conflict += 1
            
    # Calculate Redundancy Metrics
    for pair in gt_redundancy_pairs:
        if pair in predicted_redundancy_pairs:
            tp_redundancy += 1
        else:
            fn_redundancy += 1
            
    # Calculate Staleness Metrics
    for policy in gt_stale_policies:
        if policy in predicted_stale_policies:
            tp_stale += 1
        else:
            fn_stale += 1
            
    # Calculate False Positives
    for pair in predicted_conflict_pairs:
        if pair not in gt_conflict_pairs:
            fp_relations += 1
            
    for pair in predicted_redundancy_pairs:
        if pair not in gt_redundancy_pairs:
            fp_relations += 1
            
    conflict_recall = tp_conflict / len(gt_conflict_pairs) if gt_conflict_pairs else 1.0
    redundancy_recall = tp_redundancy / len(gt_redundancy_pairs) if gt_redundancy_pairs else 1.0
    stale_recall = tp_stale / len(gt_stale_policies) if gt_stale_policies else 1.0
    
    # Calculate Precision
    total_predicted_conflicts = len(predicted_conflict_pairs)
    total_predicted_redundancies = len(predicted_redundancy_pairs)
    total_predicted_stale = len(predicted_stale_policies)
    
    conflict_precision = tp_conflict / total_predicted_conflicts if total_predicted_conflicts > 0 else 0.0
    redundancy_precision = tp_redundancy / total_predicted_redundancies if total_predicted_redundancies > 0 else 0.0
    stale_precision = tp_stale / total_predicted_stale if total_predicted_stale > 0 else 0.0
    
    # Calculate F1 Scores
    conflict_f1 = 2 * (conflict_precision * conflict_recall) / (conflict_precision + conflict_recall) if (conflict_precision + conflict_recall) > 0 else 0.0
    redundancy_f1 = 2 * (redundancy_precision * redundancy_recall) / (redundancy_precision + redundancy_recall) if (redundancy_precision + redundancy_recall) > 0 else 0.0
    stale_f1 = 2 * (stale_precision * stale_recall) / (stale_precision + stale_recall) if (stale_precision + stale_recall) > 0 else 0.0
    
    # Overall metrics
    total_tp = tp_conflict + tp_redundancy + tp_stale
    total_fp = fp_relations
    total_fn = fn_conflict + fn_redundancy + fn_stale
    
    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0.0
    overall_accuracy = total_tp / (total_tp + total_fp + total_fn) if (total_tp + total_fp + total_fn) > 0 else 0.0
    
    # False Positive Rate
    total_predicted_positives = total_predicted_conflicts + total_predicted_redundancies + total_predicted_stale
    false_positive_rate = fp_relations / total_predicted_positives if total_predicted_positives > 0 else 0.0
    
    
    # Compile final metrics - match frontend expected field names
    metrics = {
        "obligation_extraction_accuracy": round(f1_ob * 100, 2),
        "conflict_detection_rate": round(conflict_f1 * 100, 2),  # Frontend expects this
        "conflict_detection": {
            "precision": round(conflict_precision * 100, 2),
            "recall": round(conflict_recall * 100, 2),
            "f1_score": round(conflict_f1 * 100, 2),
            "tp": tp_conflict,
            "fn": fn_conflict
        },
        "redundancy_detection_rate": round(redundancy_f1 * 100, 2),  # Frontend expects this
        "redundancy_detection": {
            "precision": round(redundancy_precision * 100, 2),
            "recall": round(redundancy_recall * 100, 2),
            "f1_score": round(redundancy_f1 * 100, 2),
            "tp": tp_redundancy,
            "fn": fn_redundancy
        },
        "staleness_detection_rate": round(stale_f1 * 100, 2),  # Frontend expects this
        "staleness_detection": {
            "precision": round(stale_precision * 100, 2),
            "recall": round(stale_recall * 100, 2),
            "f1_score": round(stale_f1 * 100, 2),
            "tp": tp_stale,
            "fn": fn_stale
        },
        "overall_metrics": {
            "precision": round(overall_precision * 100, 2),
            "recall": round(overall_recall * 100, 2),
            "f1_score": round(overall_f1 * 100, 2),
            "accuracy": round(overall_accuracy * 100, 2)
        },
        "false_positive_rate": round(false_positive_rate * 100, 2),
        "details": {
            "obligation_precision": round(precision_ob * 100, 2),
            "obligation_recall": round(recall_ob * 100, 2),
            "obligation_f1": round(f1_ob * 100, 2),
            "fp_relations_count": fp_relations
        }
    }
    
    # Save to JSON
    output_path = os.path.join(sample_data_dir, "evaluation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print("=== SELF-EVALUATION RESULTS ===")
    print(f"Obligation Extraction Accuracy: {metrics['obligation_extraction_accuracy']}%  (Target: >80%)")
    print(f"Conflict Detection - Precision: {metrics['conflict_detection']['precision']}%  Recall: {metrics['conflict_detection']['recall']}%  F1: {metrics['conflict_detection']['f1_score']}%")
    print(f"Redundancy Detection - Precision: {metrics['redundancy_detection']['precision']}%  Recall: {metrics['redundancy_detection']['recall']}%  F1: {metrics['redundancy_detection']['f1_score']}%")
    print(f"Staleness Detection - Precision: {metrics['staleness_detection']['precision']}%  Recall: {metrics['staleness_detection']['recall']}%  F1: {metrics['staleness_detection']['f1_score']}%")
    print(f"Overall - Precision: {metrics['overall_metrics']['precision']}%  Recall: {metrics['overall_metrics']['recall']}%  F1: {metrics['overall_metrics']['f1_score']}%  Accuracy: {metrics['overall_metrics']['accuracy']}%")
    print(f"False Positive Rate:            {metrics['false_positive_rate']}%  (Target: <20%)")
    print("===============================")
    
    return metrics

if __name__ == "__main__":
    run_evaluation()
