CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TABLE IF NOT EXISTS patient_sessions (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), abha_id TEXT, language TEXT, started_at TIMESTAMPTZ NOT NULL DEFAULT now(), submitted_at TIMESTAMPTZ, cleared_at TIMESTAMPTZ);
CREATE TABLE IF NOT EXISTS consents (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), session_id UUID REFERENCES patient_sessions(id), purpose TEXT NOT NULL, granted BOOLEAN NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS encounters (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), session_id UUID REFERENCES patient_sessions(id), chief_complaint TEXT, fhir_bundle JSONB, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS documents (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), session_id UUID REFERENCES patient_sessions(id), filename TEXT, ocr_text TEXT, entities JSONB, abnormal_flags JSONB, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS audit_logs (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), session_id UUID, action TEXT NOT NULL, metadata JSONB, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
