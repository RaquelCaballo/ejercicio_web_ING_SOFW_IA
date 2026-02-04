# AI Coding Agent Instructions

## Project Overview

**Mergington High School API**: A minimal FastAPI application for managing extracurricular activities. Students can view available activities and sign up via a web interface.

**Architecture**: Full-stack with Python backend (FastAPI) + vanilla JavaScript frontend.
- Backend: FastAPI server serving API endpoints and static files
- Frontend: HTML/CSS/JS served from `src/static/`
- Data: In-memory activity database (no persistence)

## Essential Development Setup

```bash
# Environment setup (one-time)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the app (development)
.venv/bin/uvicorn src.app:app --reload
# Or use VS Code debugger

# Access at http://localhost:8000
```

## Architecture & Key Components

### Backend (`src/app.py`)
- **Framework**: FastAPI with Uvicorn
- **Data Store**: In-memory dict `activities` - no database
- **Static Files**: Mounted at `/static/` (served from `src/static/`)
- **Entry Point**: `@app.get("/")` redirects to `index.html`

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/activities` | Returns all activities as JSON |
| POST | `/activities/{activity_name}/signup` | Sign up student (query: `email`) |
| GET | `/static/...` | Serves HTML, CSS, JS files |

**Activity Schema**:
```python
{
  "activity_name": {
    "description": str,
    "schedule": str,
    "max_participants": int,
    "participants": [email_list]  # Always append, never validate duplicates
  }
}
```

### Frontend (`src/static/`)
- `index.html`: Single-page layout with activity list + signup form
- `app.js`: Fetches `/activities`, populates UI, handles form submission
- `styles.css`: Responsive design (flexbox, mobile-first)

**Key Flow**:
1. DOMContentLoaded triggers `fetchActivities()`
2. User fills email + selects activity
3. POST to `/activities/{name}/signup?email={email}`
4. API appends email to participants (no validation)
5. Message displayed for 5 seconds

## Project Conventions

### Code Patterns
- **No validation**: The signup endpoint never validates:
  - Duplicate emails
  - Capacity limits
  - Email format
  - Activity existence (only checks in dict, allows any typo)
  - These are intentional design gaps for a minimal exercise

- **Error Handling**: HTTPException for 404s; JavaScript catch-all error messages

- **Data Flow**: Unidirectional - frontend always fetches fresh data after actions

### File Organization
```
src/app.py           # Single backend file, no modularization
src/static/
  ├─ index.html      # DOM structure
  ├─ app.js          # All logic in one file
  └─ styles.css      # All styles, media queries for mobile
```

### Frontend Specifics
- **DOM IDs**: `activities-list`, `activity-select`, `signup-form`, `message`
- **CSS Classes**: `activity-card`, `form-group`, `hidden`, `success`, `error`
- **Fetch API**: Used for all HTTP (no axios/fetch wrappers)
- **Error Handling**: Non-blocking - errors logged to console, user sees message

## Testing

```bash
pytest.ini configured with pythonpath = .
# Run: pytest src/
# No test files currently exist
```

## Important Gotchas

1. **Static File Mounting**: Paths must match: `src/static/` on disk matches `/static/` in URL
2. **Redirect from Root**: `/` endpoint redirects to `/static/index.html`, must exist
3. **CORS**: No CORS headers - frontend and API same origin (localhost:8000)
4. **Capacity**: Activities can exceed `max_participants` (validation missing)
5. **Data Loss**: All data in memory - server restart clears everything
6. **URL Encoding**: Signup uses `encodeURIComponent()` for activity names with spaces

## When Making Changes

- **Adding API endpoints**: Keep simple; use HTTPException for errors
- **Modifying UI**: Update HTML structure + corresponding JS selectors
- **Styling changes**: Use mobile-first breakpoints (min-width: 768px)
- **Testing signup flow**: Manually verify email is appended correctly
- **Debugging**: Check browser console + uvicorn logs for errors
