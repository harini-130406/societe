import pipeline
import os

policies_dir = os.path.join('..', 'sample_data', 'policies')
results = pipeline.analyze_policies_in_directory(policies_dir)

print(f'Total obligations: {len(results["obligations"])}')
print(f'Total relations: {len(results["relations"])}')
print(f'Health score: {results["health_score"]}')
print(f'Metrics: {results["metrics"]}')
