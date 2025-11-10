from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
from ..mongodb import get_candidates_collection
from ..schemas import RejectCandidateRequest, RejectCandidateResponse

router = APIRouter()

@router.post("/candidate/reject", response_model=RejectCandidateResponse)
async def reject_candidate(payload: RejectCandidateRequest):
    """
    Mark a candidate as rejected in the database due to malpractice.
    This is called when a candidate exits fullscreen more than the allowed number of times.
    """
    try:
        candidates_collection = get_candidates_collection()
        
        # Find candidate by email
        candidate = candidates_collection.find_one({"email": payload.email})
        
        if not candidate:
            # If candidate doesn't exist yet in DB, log the rejection attempt
            logging.warning(f"Attempted to reject non-existent candidate: {payload.email}")
            # We'll create a minimal rejected candidate record
            rejection_record = {
                "email": payload.email,
                "status": "rejected",
                "rejection_reason": payload.reason,
                "updated_at": datetime.utcnow(),
                "created_at": datetime.utcnow(),
                "name": "Unknown (Rejected during interview)",
            }
            candidates_collection.insert_one(rejection_record)
            logging.info(f"Created rejection record for candidate: {payload.email}")
        else:
            # Update existing candidate
            update_result = candidates_collection.update_one(
                {"email": payload.email},
                {
                    "$set": {
                        "status": "rejected",
                        "rejection_reason": payload.reason,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if update_result.modified_count == 0:
                logging.warning(f"No candidate was updated for email: {payload.email}")
            else:
                logging.info(f"Successfully marked candidate as rejected: {payload.email}")
        
        return RejectCandidateResponse(
            success=True,
            message="Candidate has been marked as rejected due to malpractice",
            email=payload.email
        )
        
    except Exception as e:
        logging.error(f"Error rejecting candidate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reject candidate: {str(e)}")
