import pipeline
import pdf_report
import os

# Run pipeline to generate analysis.json
sample_data_dir = os.path.join('..', 'sample_data')
policies_dir = os.path.join(sample_data_dir, 'policies')

print("Running pipeline...")
results = pipeline.analyze_policies_in_directory(policies_dir)

print(f"Total obligations: {len(results['obligations'])}")
print(f"Total relations: {len(results['relations'])}")
print(f"Health score: {results['health_score']}")
print(f"Conflicts: {results['metrics']['conflicts']}")
print(f"Redundancies: {results['metrics']['redundancies']}")
print(f"Stale policies: {results['metrics']['stale_policies']}")

# Generate PDF report
print("\nGenerating PDF report...")
pdf_path = os.path.join(sample_data_dir, "PolicyGuard_Audit_Report.pdf")
pdf_report.generate_pdf_report(results, pdf_path)
print(f"PDF report saved to: {pdf_path}")

print("\n=== Generation Complete ===")
print("Outputs:")
print(f"1. analysis.json - backend/analysis.json")
print(f"2. PDF Report - {pdf_path}")
