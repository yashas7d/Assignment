from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import process_company_news
import uvicorn

app = FastAPI(title="News Summarization and Sentiment API")

class CompanyRequest(BaseModel):
    company: str

@app.post("/analyze")
def analyze_news(request: CompanyRequest):
    try:
        result = process_company_news(request.company)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
