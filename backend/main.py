import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import pipeline
import evaluation
import pdf_report

app = FastAPI(title="PolicyGuard Backend", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "sample_data")
POLICIES_DIR = os.path.join(SAMPLE_DATA_DIR, "policies")

# Ensure directories exist
os.makedirs(POLICIES_DIR, exist_ok=True)

@app.get("/")
def read_root():
    frontend_path = os.path.join(os.path.dirname(BASE_DIR), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "PolicyGuard Backend is running. Frontend index.html not found."}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": "2026-07-11T15:35:40Z"}

@app.get("/api/analyze")
def analyze_policies():
    """
    Scans the policies directory, extracts obligations, calculates health, 
    and checks conflicts, redundancies, and staleness.
    """
    try:
        results = pipeline.analyze_policies_in_directory(POLICIES_DIR)
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_policy(file: UploadFile = File(...)):
    """
    Uploads a markdown/text policy file to the scanning directory.
    """
    if not (file.filename.endswith(".md") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only .md and .txt files are supported.")
        
    file_path = os.path.join(POLICIES_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "message": "Policy uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/policies/{filename}")
def delete_policy(filename: str):
    """
    Deletes a policy file from the scanning directory.
    """
    file_path = os.path.join(POLICIES_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Policy file '{filename}' not found.")
        
    try:
        os.remove(file_path)
        return {"message": f"Policy '{filename}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/policies")
def list_policies():
    """
    Lists all policy files currently stored in the backend scanning folder.
    """
    try:
        import parser
        files = [f for f in os.listdir(POLICIES_DIR) if f.endswith(".md") or f.endswith(".txt")]
        policy_list = []
        for filename in files:
            filepath = os.path.join(POLICIES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract basic metadata from content
            obligations = parser.parse_obligations_from_document(content, filename)
            if obligations:
                title = obligations[0].get("policy_name", filename)
                owner = obligations[0].get("owner", "Unknown")
                last_reviewed = obligations[0].get("review_date", "Unknown")
            else:
                title = filename
                owner = "Unknown"
                last_reviewed = "Unknown"
            
            policy_list.append({
                "filename": filename,
                "title": title,
                "owner": owner,
                "last_reviewed": last_reviewed,
                "size_bytes": os.path.getsize(filepath)
            })
        return policy_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/eval")
def get_evaluation_metrics():
    """
    Runs the self-evaluation script and returns the latest model metrics.
    """
    try:
        metrics = evaluation.run_evaluation()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export-pdf")
def export_pdf_report():
    """
    Generates a PDF audit report and sends it as a file response.
    """
    try:
        results = pipeline.analyze_policies_in_directory(POLICIES_DIR)
        temp_pdf_path = os.path.join(SAMPLE_DATA_DIR, "PolicyGuard_Audit_Report.pdf")
        pdf_report.generate_pdf_report(results, temp_pdf_path)
        
        return FileResponse(
            path=temp_pdf_path,
            filename="PolicyGuard_Audit_Report.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
