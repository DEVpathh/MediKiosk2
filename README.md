# MediKiosk — SIH Prototype

A production-oriented prototype for AI-assisted clinical history intake in Indian hospital OPDs. It follows the attached MediKiosk specification and keeps the safety principle **“AI assists. Doctor decides.”**

## Included
- React/Next.js responsive kiosk UI
- 8-language selector (English, Hindi, Punjabi, Marathi, Tamil, Telugu, Gujarati, Bengali)
- Voice-first / zero-literacy mode with Web Speech API + mock Bhashini adapter
- Touch MCQs, repeat, skip, “I don't know”, caregiver mode and senior accessibility mode
- Interactive body-area selector
- Complaint-specific adaptive questioning for chest pain, fever, headache, injury, cough/cold and abdominal pain
- Red-flag interruption and triage alert UX
- AYUSH/Ayurveda mode toggle
- Mock ABHA/ABDM authentication
- Mock OCR for prescriptions/reports with confidence, entities, abnormal-value flagging and timeline
- Editable physician-ready clinical summary with source labels
- Patient confirmation audio
- Doctor, triage and hospital-admin dashboards
- Queue management and operational analytics
- Offline simulation / connection status
- Consent + audit endpoint, session auto-clear endpoint and FHIR-ready mock bundle endpoint
- Fictional SIH demo data only

## Stack
- Frontend: Next.js 14 + TypeScript + React
- Backend: FastAPI (Python)
- Database: PostgreSQL schema included
- Integrations: mock abstraction endpoints for ABDM, ASR, OCR and LLM

## Run

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

Optional:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## Demo
Use the top-right role buttons to switch between Patient Kiosk, Doctor, Triage and Admin views. In Patient Kiosk, choose a complaint, grant consent, answer questions, optionally upload a fictional report, review the structured summary, and submit.

## Safety
This is a demo/prototype. ABHA/ABDM, Bhashini, OCR and LLM endpoints are mocks. Do not enter real patient information. The prototype does not autonomously diagnose or prescribe; physician verification is required.
