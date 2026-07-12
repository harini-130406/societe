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

print("Ground truth topics:")
gt_topics = set(ob['topic'] for ob in gt_obligations)
print(gt_topics)

print("\nExtracted topics:")
ext_topics = set()
for ob in extracted_obligations:
    if isinstance(ob['topic'], str):
        ext_topics.add(ob['topic'])
    elif isinstance(ob['topic'], list) and ob['topic']:
        ext_topics.add(ob['topic'][0])
print(ext_topics)

print("\nGround truth scopes:")
gt_scopes = set(ob['scope'] for ob in gt_obligations)
print(gt_scopes)

print("\nExtracted scopes:")
ext_scopes = set()
for ob in extracted_obligations:
    if isinstance(ob['scope'], str):
        ext_scopes.add(ob['scope'])
    elif isinstance(ob['scope'], list) and ob['scope']:
        ext_scopes.add(ob['scope'][0])
print(ext_scopes)
