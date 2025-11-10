from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..mongodb import get_candidates_collection
import pandas as pd
import io

router = APIRouter()

@router.get("/export/csv")
async def export_csv():
    candidates_collection = get_candidates_collection()
    candidates = list(candidates_collection.find())

    data = []
    for c in candidates:
        # Format Q&A responses as readable text
        qa_responses = c.get("qa_responses", [])
        qa_text = ""
        if qa_responses:
            qa_pairs = []
            for idx, qa in enumerate(qa_responses, 1):
                question = qa.get("question", "")
                answer = qa.get("answer", "")
                qa_pairs.append(f"Q{idx}: {question}\nA{idx}: {answer}")
            qa_text = "\n\n".join(qa_pairs)
        
        data.append({
            "ID": c.get("id"),
            "Name": c.get("name"),
            "Email": c.get("email"),
            "Phone": c.get("phone"),
            "Years Experience": c.get("years_experience"),
            "Position": c.get("desired_position"),
            "Location": c.get("location"),
            "Tech Skills": ", ".join(c.get("tech_skills", [])) if c.get("tech_skills") else "",
            "Technical Q&A": qa_text,
            "English Score": c.get("english_proficiency_score"),
            "Created At": c.get("created_at")
        })

    df = pd.DataFrame(data)

    # Create CSV in memory
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=candidates.csv"}
    )