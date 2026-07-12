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

# Index ground truth by (policy_file, topic, scope)
gt_index = {}
for idx, gt_ob in enumerate(gt_obligations):
    key = (gt_ob["policy_file"], gt_ob["topic"], gt_ob["scope"])
    if key not in gt_index:
        gt_index[key] = []
    gt_index[key].append(idx)

print("Ground truth index (first 10 keys):")
for i, (key, indices) in enumerate(list(gt_index.items())[:10]):
    policy, topic, scope = key
    print(f"{i+1}. ({policy}, '{topic}', '{scope}') -> {len(indices)} obligations")

print("\nExtracted obligations (first 10):")
for i, ext_ob in enumerate(extracted_obligations[:10]):
    ext_doc = ext_ob["source_doc"]
    ext_topic = ext_ob["topic"].lower() if isinstance(ext_ob["topic"], str) else ext_ob["topic"][0].lower() if ext_ob["topic"] else "unknown"
    ext_scope = ext_ob["scope"].lower() if isinstance(ext_ob["scope"], str) else ext_ob["scope"][0].lower() if ext_ob["scope"] else "unknown"
    print(f"{i+1}. ({ext_doc}, '{ext_topic}', '{ext_scope}')")

print("\nTrying to match:")
matches = 0
for ext_ob in extracted_obligations[:20]:
    ext_doc = ext_ob["source_doc"]
    ext_topic = ext_ob["topic"].lower() if isinstance(ext_ob["topic"], str) else ext_ob["topic"][0].lower() if ext_ob["topic"] else "unknown"
    ext_scope = ext_ob["scope"].lower() if isinstance(ext_ob["scope"], str) else ext_ob["scope"][0].lower() if ext_ob["scope"] else "unknown"
    
    key = (ext_doc, ext_topic, ext_scope)
    if key in gt_index and gt_index[key]:
        matches += 1
        print(f"✓ Match: {key}")
    else:
        print(f"✗ No match: {key}")

print(f"\nMatches: {matches}/20")
