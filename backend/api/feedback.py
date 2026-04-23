from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth.dependencies import get_optional_current_user, require_admin_user
from db.database import get_db
from db.models import Feedback, User
from backend.schemas.feedback import FeedbackCreate, FeedbackOut
from services.assistant_personality import (
    apply_feedback_to_profile,
    parse_profile,
    serialize_profile,
)

router = APIRouter(prefix="/feedback", tags=["Feedback"])


def _safe_parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return None


@router.post("", response_model=FeedbackOut)
def record_feedback(
    body: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    user = current_user
    effective_user_id = user.id if user is not None else None

    feedback = (
        db.query(Feedback)
        .filter(Feedback.session_id == body.session_id, Feedback.message_id == body.message_id)
        .first()
    )

    if feedback is None:
        feedback = Feedback(
            session_id=body.session_id,
            message_id=body.message_id,
            user_id=effective_user_id,
            reaction=body.reaction,
            rating=body.rating,
            page_context=body.page_context,
            response_category=body.response_category,
            response_text=body.response_text,
            comment=body.comment,
        )
        db.add(feedback)
    else:
        feedback.user_id = effective_user_id if effective_user_id is not None else feedback.user_id
        feedback.reaction = body.reaction
        feedback.rating = body.rating
        feedback.page_context = body.page_context
        feedback.response_category = body.response_category
        feedback.response_text = body.response_text
        feedback.comment = body.comment

    if user is not None:
        profile = parse_profile(user.assistant_style_profile)
        updated_profile = apply_feedback_to_profile(
            profile,
            reaction=body.reaction,
            rating=body.rating,
            comment=body.comment,
        )
        user.assistant_style_profile = serialize_profile(updated_profile)

    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/session/{session_id}", response_model=list[FeedbackOut])
def list_session_feedback(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    query = db.query(Feedback).filter(Feedback.session_id == session_id)
    if not bool(current_user.is_admin):
        query = query.filter(Feedback.user_id == current_user.id)

    return query.order_by(Feedback.updated_at.desc()).all()


@router.get("/analytics")
def feedback_analytics(
    session_id: str | None = None,
    response_category: str | None = None,
    current_user: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    _ = current_user

    base_query = db.query(Feedback)
    if session_id:
        base_query = base_query.filter(Feedback.session_id == session_id)
    if response_category:
        base_query = base_query.filter(Feedback.response_category == response_category)

    total_feedback = base_query.count()
    average_rating = base_query.with_entities(func.avg(Feedback.rating)).scalar()

    category_rows = (
        base_query.with_entities(
            Feedback.response_category,
            func.count(Feedback.id),
            func.avg(Feedback.rating),
        )
        .group_by(Feedback.response_category)
        .all()
    )
    reaction_rows = (
        base_query.with_entities(
            Feedback.reaction,
            func.count(Feedback.id),
        )
        .group_by(Feedback.reaction)
        .all()
    )

    return {
        "total_feedback": total_feedback,
        "average_rating": round(float(average_rating), 3) if average_rating is not None else None,
        "by_category": [
            {
                "response_category": category,
                "count": count,
                "average_rating": round(float(avg), 3) if avg is not None else None,
            }
            for category, count, avg in category_rows
        ],
        "by_reaction": [
            {
                "reaction": reaction,
                "count": count,
            }
            for reaction, count in reaction_rows
        ],
    }


@router.get("/analytics/weekly")
def feedback_weekly_report(
    days: int = 7,
    session_id: str | None = None,
    response_category: str | None = None,
    current_user: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    _ = current_user

    days = max(1, min(days, 30))
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=days - 1)

    base_query = db.query(Feedback)
    if session_id:
        base_query = base_query.filter(Feedback.session_id == session_id)
    if response_category:
        base_query = base_query.filter(Feedback.response_category == response_category)

    feedback_rows = base_query.order_by(Feedback.updated_at.desc()).all()

    day_buckets: dict[str, dict[str, float | int]] = {}
    for offset in range(days):
        day = (since + timedelta(days=offset)).date().isoformat()
        day_buckets[day] = {
            "count": 0,
            "rating_sum": 0,
        }

    for row in feedback_rows:
        row_dt = _safe_parse_timestamp(row.updated_at or row.created_at)
        if row_dt is None:
            continue
        if row_dt < since or row_dt > now:
            continue

        day_key = row_dt.date().isoformat()
        if day_key not in day_buckets:
            continue

        day_buckets[day_key]["count"] += 1
        day_buckets[day_key]["rating_sum"] += row.rating

    by_day = []
    for day_key, values in day_buckets.items():
        count = int(values["count"])
        rating_sum = float(values["rating_sum"])
        by_day.append({
            "date": day_key,
            "count": count,
            "average_rating": round(rating_sum / count, 3) if count > 0 else None,
        })

    total_feedback = sum(entry["count"] for entry in by_day)
    overall_average = None
    if total_feedback > 0:
        weighted_sum = sum((entry["average_rating"] or 0) * entry["count"] for entry in by_day)
        overall_average = round(weighted_sum / total_feedback, 3)

    return {
        "window_days": days,
        "from_date": since.date().isoformat(),
        "to_date": now.date().isoformat(),
        "total_feedback": total_feedback,
        "average_rating": overall_average,
        "by_day": by_day,
    }