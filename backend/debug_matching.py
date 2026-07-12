import json
import os
import pipeline

# Load ground truth
sample_data_dir = os.path.join('..', 'sample_data')
gt_ob_path = os.path.join(sample_data_dir, 'obligation_extracts_labels.json')

with open(gt_ob_path, 'r', encoding='utf-8') as f:
    gt_obligations = json.load(f)

# Run pipeline
policies_dir = os.path.join('..', 'sample_data', 'policies')
results = pipeline.analyze_policies_in_directory(policies_dir)
extracted_obligations = results['obligations']

# Try to match with lower threshold
def jaccard_similarity(a, b):
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a.intersection(words_b)) / len(words_a.union(words_b))

print("Trying to match ground truth with extracted obligations (threshold 0.3):")
matches = 0
for gt_ob in gt_obligations[:20]:
    gt_text = gt_ob['obligation_text'].lower().strip()
    gt_doc = gt_ob['policy_file']
    
    best_match = None
    best_score = 0.0
    
    for ext_ob in extracted_obligations:
        ext_text = ext_ob['raw_text'].lower().strip()
        ext_doc = ext_ob['source_doc']
        
        if ext_doc == gt_doc:
            score = jaccard_similarity(gt_text, ext_text)
            if score > best_score:
                best_score = score
                best_match = ext_ob
    
    if best_score > 0.3:
        matches += 1
        print(f"✓ Match: {gt_doc}")
        print(f"  GT: '{gt_ob['obligation_text']}'")
        print(f"  Ext: '{best_match['raw_text']}'")
        print(f"  Score: {best_score:.2f}")
    else:
        print(f"✗ No match: {gt_doc}")
        print(f"  GT: '{gt_ob['obligation_text']}'")
        print(f"  Best score: {best_score:.2f}")
    print()

print(f"Matches found: {matches}/20")
