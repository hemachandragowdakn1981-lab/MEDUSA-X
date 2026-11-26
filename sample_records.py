PATIENT_CASES = {
    "Case 1: Medication Allergy & Silent Drop (CRITICAL HALT)": {
        "patient_id": "PT-4092",
        "documents": [
            {
                "doc_type": "Emergency Admission Note",
                "timestamp": "2026-11-20 08:15",
                "author": "Dr. A. Sharma (ER)",
                "text": "64M presents with high fever (102.4F) and productive cough. History of Hypertension. SEVERE ALLERGY: Penicillin (anaphylaxis). Started on IV Azithromycin 500mg. Chest X-ray ordered."
            },
            {
                "doc_type": "Radiology & Lab Report",
                "timestamp": "2026-11-20 11:30",
                "author": "Central Diagnostics",
                "text": "Chest X-Ray: Right lower lobe consolidation consistent with community-acquired pneumonia. WBC: 16,400/uL (High)."
            },
            {
                "doc_type": "Ward Progress Note",
                "timestamp": "2026-11-21 09:00",
                "author": "Dr. R. Verma (Internal Med)",
                "text": "Patient fever subsiding. Switching from IV antibiotics to oral Amoxicillin-Clavulanate 875mg BID for 7 days. Continue Lisinopril 10mg daily for BP."
            },
            {
                "doc_type": "Draft Discharge Summary",
                "timestamp": "2026-11-22 14:00",
                "author": "Dr. K. Nair (Resident)",
                "text": "Diagnosis: Resolved Pneumonia. Allergies: NKDA (No Known Drug Allergies). Discharge Meds: Amoxicillin-Clavulanate 875mg BID. Follow up in 1 week."
            }
        ]
    },
    "Case 2: High Uncertainty & Missing Critical Lab (CRITICAL HALT)": {
        "patient_id": "PT-8810",
        "documents": [
            {
                "doc_type": "Triage Note",
                "timestamp": "2026-11-24 22:10",
                "author": "Nurse P. Rao",
                "text": "52F presents with acute substernal chest tightness radiating to left arm, diaphoresis. BP 165/98. ECG shows non-specific ST-T changes. Stat Troponin-I drawn."
            },
            {
                "doc_type": "Cardiology Consult Note",
                "timestamp": "2026-11-24 23:45",
                "author": "Dr. M. Reddy",
                "text": "Possible NSTEMI vs GERD. Hold anticoagulation until Troponin-I result and GI bleed history from outside hospital records are verified."
            },
            {
                "doc_type": "Lab System Status",
                "timestamp": "2026-11-25 01:15",
                "author": "Auto-Lab Interface",
                "text": "Troponin-I: SAMPLE HEMOLYZED - RESULT DELAYED / PENDING REDRAW. Outside hospital records: NOT RECEIVED."
            },
            {
                "doc_type": "Morning Shift Handover",
                "timestamp": "2026-11-25 07:00",
                "author": "Dr. S. Joshi",
                "text": "Plan: Discharge patient with antacids for GERD if stable."
            }
        ]
    },
    "Case 3: Clean Reconstruction (VERIFIED SAFE)": {
        "patient_id": "PT-1024",
        "documents": [
            {
                "doc_type": "Outpatient Clinic Note",
                "timestamp": "2026-11-10 10:00",
                "author": "Dr. L. Menon",
                "text": "45M routine checkup. HbA1c is 7.8%. Diagnosed with Type 2 Diabetes Mellitus. Started Metformin 500mg OD. No known allergies."
            },
            {
                "doc_type": "Follow-up Telehealth Note",
                "timestamp": "2026-11-24 16:30",
                "author": "Dr. L. Menon",
                "text": "Patient tolerating Metformin 500mg well with no GI side effects. Fasting blood glucose improved to 118 mg/dL. Continue Metformin 500mg OD and diet control."
            }
        ]
    },
    "Case 4: Dual Anticoagulant & Bleed Risk (CRITICAL HALT)": {
        "patient_id": "PT-6319",
        "documents": [
            {
                "doc_type": "Cardiology Outpatient Record",
                "timestamp": "2026-11-18 11:00",
                "author": "Dr. V. Kulkarni",
                "text": "71M with Atrial Fibrillation on chronic Apixaban 5mg BID. Recent upper GI endoscopy showed healing peptic ulcer; strictly avoid NSAIDs and Aspirin."
            },
            {
                "doc_type": "Orthopedic Urgent Care Note",
                "timestamp": "2026-11-25 09:30",
                "author": "Dr. T. Das",
                "text": "Patient presents with acute knee pain. Prescribed Naproxen 500mg BID and Aspirin 325mg daily for pain relief. Coagulation panel pending."
            }
        ]
    }
}
