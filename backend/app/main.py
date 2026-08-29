from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import re, uuid

app = FastAPI(title="MediKiosk API", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
SESSIONS: dict[str, dict[str, Any]] = {}
AUDIT: list[dict[str, Any]] = []

class ABHARequest(BaseModel): abha_id: str
class ConsentRequest(BaseModel): session_id: str; granted: bool; purpose: str = "clinical history intake"; granular: dict[str,bool] = Field(default_factory=dict)
class SummaryRequest(BaseModel): complaint: str; answers: dict[str,str] = Field(default_factory=dict); ayush: bool=False; document: str|None=None
class RedFlagRequest(BaseModel): text: str

RED_PATTERNS = {
    "Emergency indicator in response": r"chest pain|severe.*breath|difficulty breathing|faint|unconscious|heavy bleeding|one side.*weak|slurred speech|seizure",
    "Significant bleeding indicator": r"blood.*vomit|vomit.*blood|blood.*stool",
}

def audit(action: str, session_id: str, meta: dict[str,Any]|None=None):
    AUDIT.append({"id": str(uuid.uuid4()), "timestamp": datetime.now(timezone.utc).isoformat(), "action": action, "session_id": session_id, "meta": meta or {}})

@app.get("/health")
def health(): return {"status":"ok", "service":"MediKiosk", "mock_integrations": True}

@app.post("/api/abdm/abha/mock-auth")
def mock_abha(req: ABHARequest):
    sid=str(uuid.uuid4()); SESSIONS[sid]={"abha_id":req.abha_id,"created_at":datetime.now(timezone.utc).isoformat()}
    audit("ABHA_MOCK_AUTH",sid,{"sandbox":True}); return {"session_id":sid,"abha_id":req.abha_id,"status":"authenticated","sandbox":True}

@app.post("/api/consent")
def consent(req: ConsentRequest):
    audit("CONSENT_GRANTED" if req.granted else "CONSENT_DENIED", req.session_id, {"purpose":req.purpose,"granular":req.granular})
    return {"recorded":True,"timestamp":datetime.now(timezone.utc).isoformat(),"audit_id":AUDIT[-1]["id"]}

@app.post("/api/asr/mock")
async def asr_mock(audio: UploadFile=File(...)):
    return {"provider":"mock-bhashini","text":"Demo transcription: patient reports the selected complaint.","language":"en-IN","confidence":0.96,"mock":True}

@app.post("/api/ocr/mock")
async def ocr_mock(document: UploadFile=File(...)):
    return {"provider":"mock-tesseract-google-vision","mock":True,"confidence":0.92,"text":"Diagnosis: fever\nMedicine: paracetamol 500 mg\nLab: Hb 10.2 g/dL\nDate: 2026-08-27","entities":{"diagnosis":["fever"],"medicines":["paracetamol 500 mg"],"lab_values":[{"name":"Hb","value":10.2,"unit":"g/dL","reference":"12-16"}],"dates":["2026-08-27"]},"abnormal_flags":["Hb: outside the provided reference range"],"timeline":[{"date":"2026-08-27","event":"Medical document digitized"}]}

@app.post("/api/red-flags")
def red_flags(req: RedFlagRequest):
    matches=[label for label,pattern in RED_PATTERNS.items() if re.search(pattern, req.text, re.I)]
    return {"priority":bool(matches),"matches":matches,"action":"urgent clinical review" if matches else "routine workflow"}

@app.post("/api/summary")
def summary(req: SummaryRequest):
    hpi=[f"{k}: {v}" for k,v in req.answers.items()]
    return {"chief_complaint":req.complaint,"hpi":hpi,"past_history":"Not provided","past_surgical_history":"Not provided","drug_history":"Not reported","allergy_history":"Not reported","family_history":"Not provided","personal_history":"Not provided","ros":"Partial — review indicated","ayush_dashavidha_pariksha":"Enabled — clinician review required" if req.ayush else "Not requested","sources":["Patient responses"] + (["Uploaded document"] if req.document else []),"confidence":{"hpi":0.91,"overall":0.89},"clinician_review_required":True}

@app.post("/api/fhir/bundle")
def fhir_bundle(payload: dict[str,Any]):
    sid=payload.get("session_id",str(uuid.uuid4())); audit("FHIR_BUNDLE_CREATED",sid)
    return {"resourceType":"Bundle","type":"transaction","id":str(uuid.uuid4()),"timestamp":datetime.now(timezone.utc).isoformat(),"entry":[{"resource":{"resourceType":"Patient","id":"mock-patient"}},{"resource":{"resourceType":"QuestionnaireResponse","id":sid,"status":"completed"}},{"resource":{"resourceType":"Composition","id":str(uuid.uuid4()),"status":"preliminary","title":"MediKiosk Clinical History"}}],"mock":True}

@app.post("/api/session/clear")
def clear_session(session_id: str|None=None):
    if session_id: SESSIONS.pop(session_id,None)
    audit("SESSION_AUTO_CLEAR",session_id or "anonymous")
    return {"cleared":True,"timestamp":datetime.now(timezone.utc).isoformat()}

@app.get("/api/admin/queue")
def queue():
    return {"queue":[{"token":"K-1042","patient":"Demo Patient A","complaint":"Fever","priority":"GREEN","status":"Ready for doctor"},{"token":"K-1043","patient":"Demo Patient B","complaint":"Chest pain","priority":"RED","status":"Immediate attention"},{"token":"K-1044","patient":"Demo Patient C","complaint":"Headache","priority":"YELLOW","status":"Needs clarification"}],"red_flag_count":1}

@app.get("/api/admin/audit")
def audit_log(): return {"events":AUDIT[-100:]}
