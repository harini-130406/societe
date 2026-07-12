import json
import os

# Load ground truth
sample_data_dir = os.path.join('..', 'sample_data')
gt_ob_path = os.path.join(sample_data_dir, 'obligation_extracts_labels.json')

with open(gt_ob_path, 'r', encoding='utf-8') as f:
    gt_obligations = json.load(f)

print(f"Ground truth obligations: {len(gt_obligations)}")
print("\nSample ground truth obligations:")
for i, ob in enumerate(gt_obligations[:10]):
    print(f"{i+1}. {ob['policy_file']}: '{ob['obligation_text']}' (topic: {ob['topic']}, scope: {ob['scope']})")

# Load extracted results
import pipeline
policies_dir = os.path.join('..', 'sample_data', 'policies')
results = pipeline.analyze_policies_in_directory(policies_dir)
extracted_obligations = results['obligations']

print(f"\nExtracted obligations: {len(extracted_obligations)}")
print("\nSample extracted obligations:")
for i, ob in enumerate(extracted_obligations[:10]):
    print(f"{i+1}. {ob['source_doc']}: '{ob['raw_text']}' (topic: {ob['topic']}, scope: {ob['scope']})")
