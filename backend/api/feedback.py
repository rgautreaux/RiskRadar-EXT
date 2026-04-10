from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Feedback, User
from schemas.feedback import FeedbackCreate, FeedbackOut

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("", response_model=FeedbackOut)
def record_feedback(body: FeedbackCreate, db: Session = Depends(get_db)):
    if body.user_id is not None:
        user = db.query(User).filter(User.id == body.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    feedback = (
        db.query(Feedback)
        .filter(Feedback.session_id == body.session_id, Feedback.message_id == body.message_id)
        .first()
    )

    if feedback is None:
        feedback = Feedback(
            session_id=body.session_id,
            message_id=body.message_id,
            user_id=body.user_id,
            reaction=body.reaction,
            rating=body.rating,
            page_context=body.page_context,
            response_category=body.response_category,
            response_text=body.response_text,
            comment=body.comment,
        )
        db.add(feedback)
    else:
        feedback.user_id = body.user_id if body.user_id is not None else feedback.user_id
        feedback.reaction = body.reaction
        feedback.rating = body.rating
        feedback.page_context = body.page_context
        feedback.response_category = body.response_category
        feedback.response_text = body.response_text
        feedback.comment = body.comment

    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/session/{session_id}", response_model=list[FeedbackOut])
def list_session_feedback(session_id: str, db: Session = Depends(get_db)):
    return (
        db.query(Feedback)
        .filter(Feedback.session_id == session_id)
        .order_by(Feedback.updated_at.desc())
        .all()
    )