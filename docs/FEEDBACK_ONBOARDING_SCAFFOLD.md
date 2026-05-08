# Feedback & Onboarding Flow Implementation Guide

**Project:** RiskRadar CMPS 357  
**Scope:** Add lightweight feedback capture and first-run onboarding  
**Timeline:** 1–2 days implementation

---

## 1. Feedback Endpoint (Backend)

### Add to `backend/api/feedback.py`

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from db.database import Session
from db.models import Feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])

class FeedbackRequest(BaseModel):
    message_id: str  # Reference to assistant message or feature
    helpful: bool    # Was this helpful? (1-5 scale optional)
    comment: str | None = None
    feature: str | None = None  # e.g., "assistant", "map", "forecast"

@router.post("/submit")
async def submit_feedback(req: FeedbackRequest, db: Session):
    """Capture user feedback for continuous improvement."""
    feedback = Feedback(
        message_id=req.message_id,
        helpful=req.helpful,
        comment=req.comment,
        feature=req.feature,
        created_at=datetime.utcnow()
    )
    db.add(feedback)
    db.commit()
    return {"status": "received"}
```

### Add model to `backend/db/models.py`

```python
class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True)
    message_id = Column(String(255), nullable=True)
    helpful = Column(Boolean, default=None)
    comment = Column(Text, nullable=True)
    feature = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Add migration script `backend/scripts/add_feedback_table.py`

```python
from db.init_db import engine
from sqlalchemy import text

def add_feedback_table():
    with engine.begin() as conn:
        # Check if table exists
        result = conn.execute(text("""
            SELECT 1 FROM information_schema.TABLES 
            WHERE TABLE_NAME = 'feedback'
        """))
        if not result.fetchone():
            conn.execute(text("""
                CREATE TABLE feedback (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    message_id VARCHAR(255),
                    helpful BOOLEAN,
                    comment TEXT,
                    feature VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("✓ Feedback table created")
        else:
            print("✓ Feedback table already exists")

if __name__ == "__main__":
    add_feedback_table()
```

Run once:
```bash
cd backend && python scripts/add_feedback_table.py
```

---

## 2. Frontend Feedback UI

### Add to `frontend/web/components/feedback.php`

```php
<?php
// Lightweight feedback widget
function render_feedback_widget($feature = "assistant", $message_id = null) {
    if (!$message_id) $message_id = uniqid();
    
    return <<<HTML
    <div class="feedback-widget" data-feature="$feature" data-message="$message_id">
        <p class="feedback-question">Was this helpful?</p>
        <div class="feedback-buttons">
            <button class="feedback-btn feedback-yes" aria-label="Yes, helpful">
                👍 Yes
            </button>
            <button class="feedback-btn feedback-no" aria-label="No, not helpful">
                👎 No
            </button>
        </div>
        <textarea 
            class="feedback-comment" 
            placeholder="Optional: Tell us how we can improve..." 
            rows="2"
            style="display:none;"
        ></textarea>
        <button class="feedback-submit" style="display:none;">Submit</button>
    </div>
    HTML;
}
?>
```

### Add to `frontend/web/public/assets/app.css`

```css
.feedback-widget {
    border: 1px solid var(--line);
    padding: 12px 16px;
    border-radius: 8px;
    background: var(--panel-strong);
    margin-top: 12px;
}

.feedback-question {
    margin: 0 0 8px;
    font-size: 0.9rem;
    color: var(--muted);
}

.feedback-buttons {
    display: flex;
    gap: 8px;
}

.feedback-btn {
    padding: 8px 12px;
    border: 1px solid var(--line);
    border-radius: 6px;
    background: white;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background 0.15s;
}

.feedback-btn:hover {
    background: var(--panel);
}

.feedback-comment {
    width: 100%;
    padding: 8px;
    margin-top: 8px;
    border: 1px solid var(--line);
    border-radius: 6px;
    font-family: inherit;
    font-size: 0.85rem;
    display: none;
}

.feedback-submit {
    margin-top: 8px;
    padding: 8px 12px;
    background: var(--accent-coral);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    display: none;
}
```

### Add JavaScript to handle submission

Create `frontend/web/public/assets/feedback.js`:

```javascript
document.querySelectorAll('.feedback-widget').forEach(widget => {
    const yesBtn = widget.querySelector('.feedback-yes');
    const noBtn = widget.querySelector('.feedback-no');
    const textbox = widget.querySelector('.feedback-comment');
    const submitBtn = widget.querySelector('.feedback-submit');
    const feature = widget.dataset.feature;
    const messageId = widget.dataset.message;
    
    yesBtn.addEventListener('click', () => {
        submitFeedback(messageId, true, null, feature);
        widget.innerHTML = '<p style="color: var(--muted); font-size: 0.9rem;">Thanks for your feedback!</p>';
    });
    
    noBtn.addEventListener('click', () => {
        textbox.style.display = 'block';
        submitBtn.style.display = 'block';
        yesBtn.style.display = 'none';
        noBtn.style.display = 'none';
    });
    
    submitBtn.addEventListener('click', () => {
        const comment = textbox.value;
        submitFeedback(messageId, false, comment, feature);
        widget.innerHTML = '<p style="color: var(--muted); font-size: 0.9rem;">Thanks for your feedback!</p>';
    });
});

async function submitFeedback(messageId, helpful, comment, feature) {
    try {
        const response = await fetch('/api/v1/feedback/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message_id: messageId,
                helpful,
                comment,
                feature
            })
        });
        if (!response.ok) console.error('Feedback submission failed');
    } catch (e) {
        console.warn('Feedback offline; skipping submission');
    }
}
```

---

## 3. Onboarding Tour (First-Run Detection)

### Add to `frontend/web/components/onboarding.php`

```php
<?php
function render_onboarding_overlay() {
    // Check if user has seen onboarding (localStorage flag)
    $is_first_run = !isset($_COOKIE['onboarding_seen']);
    
    if (!$is_first_run) return '';
    
    return <<<HTML
    <div id="onboarding-overlay" style="display:block;">
        <div class="onboarding-modal">
            <h2>Welcome to RiskRadar!</h2>
            <p>Here's a quick tour of key features:</p>
            
            <button class="onboarding-step" data-step="1">
                🗺️ Explore the Map
            </button>
            <button class="onboarding-step" data-step="2">
                ⚠️ Check Alerts
            </button>
            <button class="onboarding-step" data-step="3">
                🤖 Meet Golby
            </button>
            <button class="onboarding-skip">Skip Tour</button>
        </div>
    </div>
    HTML;
}
?>
```

### CSS for onboarding

```css
#onboarding-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.onboarding-modal {
    background: white;
    padding: 32px;
    border-radius: 16px;
    max-width: 500px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.onboarding-step {
    display: block;
    width: 100%;
    padding: 12px;
    margin: 12px 0;
    background: var(--accent-coral);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
}

.onboarding-skip {
    margin-top: 12px;
    background: transparent;
    border: 1px solid var(--line);
    color: var(--muted);
    cursor: pointer;
    padding: 8px;
}
```

### JavaScript to handle tour

```javascript
document.querySelectorAll('.onboarding-step').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const step = e.target.dataset.step;
        showTourHint(step);
    });
});

document.querySelector('.onboarding-skip')?.addEventListener('click', () => {
    closeTour();
});

function closeTour() {
    document.getElementById('onboarding-overlay').style.display = 'none';
    localStorage.setItem('onboarding_seen', '1');
}
```

---

## 4. Implementation Checklist

- [ ] Add `Feedback` model to `backend/db/models.py`
- [ ] Create `/api/v1/feedback/submit` endpoint in `backend/api/feedback.py`
- [ ] Run migration: `python scripts/add_feedback_table.py`
- [ ] Add feedback CSS to `frontend/web/public/assets/app.css`
- [ ] Add `frontend/web/public/assets/feedback.js`
- [ ] Create feedback widget component in `frontend/web/components/feedback.php`
- [ ] Add onboarding modal to `frontend/web/views/layout.php`
- [ ] Test feedback form end-to-end
- [ ] Test onboarding tour on first visit (clear localStorage)
- [ ] Add tests to `backend/tests/test_api_feedback.py`

---

## 5. Feature Flags (Optional)

Wrap behind feature flags to reduce risk:

```php
<?php
$features = [
    'feedback_enabled' => getenv('FEEDBACK_ENABLED') ?? true,
    'onboarding_enabled' => getenv('ONBOARDING_ENABLED') ?? true,
];
?>
```

---

## 6. Testing

```bash
# Test feedback endpoint
curl -X POST http://127.0.0.1:8001/api/v1/feedback/submit \
  -H "Content-Type: application/json" \
  -d '{"message_id":"test_1","helpful":true,"feature":"assistant"}'

# Check database
SELECT * FROM feedback WHERE created_at > NOW() - INTERVAL 1 MINUTE;
```

**Estimated effort:** 2–4 hours (scaffolding + integration + testing)
