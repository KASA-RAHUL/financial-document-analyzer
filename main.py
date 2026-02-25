from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import verification, analyze_financial_document, risk_assessment, investment_analysis
from database import init_db, create_job, update_job, get_job

app = FastAPI(title="Financial Document Analyzer Pro")

# Initialize SQLite database
init_db()

def run_crew(query: str, file_path: str, job_id: str):
    """Executes the CrewAI process and updates the database upon completion."""
    try:
        financial_crew = Crew(
            agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
            tasks=[verification, analyze_financial_document, risk_assessment, investment_analysis],
            process=Process.sequential,
            verbose=True
        )
        
        # Pass dynamic inputs to tasks
        result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
        
        # Update DB on success
        update_job(job_id, "COMPLETED", str(result))
        
    except Exception as e:
        # Update DB on failure
        update_job(job_id, "FAILED", f"Error processing crew: {str(e)}")
        
    finally:
        # Cleanup uploaded file securely
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running. Check /docs for Swagger UI."}

@app.post("/analyze")
async def process_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Uploads a PDF and queues it for asynchronous analysis."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    job_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = f"data/financial_document_{job_id}.pdf"
    
    # Save the file locally
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    # Create tracking record in DB
    create_job(job_id, file.filename)
    
    # Add to FastAPI Background Queue
    background_tasks.add_task(run_crew, query.strip(), file_path, job_id)
    
    return {
        "status": "Queued",
        "job_id": job_id,
        "message": "Your document is being processed. Use the /status endpoint to retrieve results."
    }

@app.get("/status/{job_id}")
async def get_analysis_status(job_id: str):
    """Retrieve the status and results of a job."""
    row = get_job(job_id)
    if not row:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    status, result, filename = row
    
    response = {
        "job_id": job_id,
        "filename": filename,
        "status": status
    }
    
    if status == "COMPLETED":
        response["analysis"] = result
    elif status == "FAILED":
        response["error"] = result
        
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)