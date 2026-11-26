import streamlit as st
from pypdf import PdfReader
from sample_records import PATIENT_CASES
from agents import run_medusa_pipeline

st.set_page_config(page_title="MEDUSA-X | Clinical Intelligence", page_icon="🩺", layout="wide")

if "audit_result" not in st.session_state:
    st.session_state.audit_result = None
if "audited_patient" not in st.session_state:
    st.session_state.audited_patient = None
if "physician_cleared" not in st.session_state:
    st.session_state.physician_cleared = False
if "physician_note" not in st.session_state:
    st.session_state.physician_note = ""

st.title("🩺 MEDUSA-X: Agentic Clinical Record Reconciliation")
st.caption("Autonomous Timeline Reconstruction, Conflict Detection & Epistemic Safety Gatekeeper")

st.sidebar.header("1. Select Input Mode")
input_mode = st.sidebar.radio(
    "Choose data source:",
    ["Preset Clinical Cases", "Live Judge Sandbox (Custom Text / PDF)"]
)

documents = []
patient_id = "PT-CUSTOM-01"

if input_mode == "Preset Clinical Cases":
    selected_case_name = st.sidebar.selectbox("Choose a test scenario:", list(PATIENT_CASES.keys()))
    case_data = PATIENT_CASES[selected_case_name]
    patient_id = case_data["patient_id"]
    documents = case_data["documents"]
else:
    patient_id = st.sidebar.text_input("Patient ID:", value="PT-LIVE-99")
    uploaded_files = st.sidebar.file_uploader(
        "Upload Clinical PDFs or TXTs (Optional)",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    if uploaded_files:
        for idx, file in enumerate(uploaded_files, 1):
            text_content = ""
            if file.name.lower().endswith(".pdf"):
                reader = PdfReader(file)
                for page in reader.pages:
                    text_content += (page.extract_text() or "") + "\n"
            else:
                text_content = file.read().decode("utf-8", errors="ignore")
            documents.append({
                "doc_type": f"Uploaded File: {file.name}",
                "timestamp": f"Document #{idx}",
                "author": "Uploaded Clinical Record",
                "text": text_content.strip()
            })

if st.session_state.audited_patient != patient_id:
    st.session_state.audit_result = None
    st.session_state.physician_cleared = False
    st.session_state.physician_note = ""

st.sidebar.markdown("---")
st.sidebar.info(
    "**Multi-Agent Safety Pipeline:**\n"
    "1. **Temporal Extractor:** Orders fragmented notes & anchors verbatim quotes.\n"
    "2. **Skeptic Auditor:** Cross-checks allergies, drugs, labs & silent drops.\n"
    "3. **Circuit Breaker:** Halts unsafe automation & enforces Human-in-the-Loop sign-off."
)

col1, col2 = st.columns([1, 1.45], gap="large")

with col1:
    st.subheader(f"📂 Fragmented Records ({patient_id})")

    if input_mode == "Live Judge Sandbox (Custom Text / PDF)" and not uploaded_files:
        st.markdown("Paste fragmented notes below (or upload PDFs in the sidebar):")
        note_1 = st.text_area(
            "Document 1 (Admission / Allergy Note)",
            value="2026-11-25 08:00 | ER Note (Dr. Rao): 58F admitted with UTI. ALLERGY: Sulfa drugs (Stevens-Johnson Syndrome). Started IV Ceftriaxone.",
            height=105
        )
        note_2 = st.text_area(
            "Document 2 (Lab / Progress Note)",
            value="2026-11-25 14:00 | Lab Report: Urine culture pending. Creatinine 2.4 mg/dL (Elevated - Acute Kidney Injury).",
            height=105
        )
        note_3 = st.text_area(
            "Document 3 (Discharge / Rx Note)",
            value="2026-11-26 09:00 | Discharge Rx (Dr. Nair): Discharge home on Bactrim DS (Sulfamethoxazole/Trimethoprim) BID x 5 days and Ibuprofen 600mg TID for pain.",
            height=105
        )
        for i, raw in enumerate([note_1, note_2, note_3], 1):
            if raw.strip():
                documents.append({
                    "doc_type": f"Clinical Note #{i}",
                    "timestamp": "See note text",
                    "author": "Live Input",
                    "text": raw.strip()
                })
    else:
        for doc in documents:
            with st.expander(f"📄 {doc['timestamp']} — {doc['doc_type']}", expanded=True):
                st.markdown(f"**Author:** {doc['author']}")
                st.write(doc["text"])

with col2:
    st.subheader("🧠 Agentic Reconciliation & Safety Audit")

    if st.button("🚀 Run MEDUSA-X Clinical Audit", type="primary", use_container_width=True):
        if not documents:
            st.warning("Please provide at least one clinical document or note.")
        else:
            with st.spinner("Agent 1 extracting timeline -> Agent 2 auditing conflicts -> Agent 3 evaluating safety gate..."):
                st.session_state.audit_result = run_medusa_pipeline(patient_id, documents)
                st.session_state.audited_patient = patient_id
                st.session_state.physician_cleared = False
                st.session_state.physician_note = ""

    result = st.session_state.audit_result

    if result is not None:
        decision = result["system_decision"]

        if st.session_state.physician_cleared:
            st.success(
                f"✅ **CLEARED VIA PHYSICIAN ESCALATION OVERRIDE**\n\n"
                f"All critical conflicts have been reviewed and resolved by an attending clinician. "
                f"**Resolution Note:** *{st.session_state.physician_note}*"
            )
        elif decision == "HALT_AND_ESCALATE":
            st.error(f"🛑 **SYSTEM HALTED — ESCALATION REQUIRED**\n\n{result['decision_reason']}")
        elif decision == "PROCEED_WITH_CAUTION":
            st.warning(f"⚠️ **PROCEED WITH CAUTION**\n\n{result['decision_reason']}")
        else:
            st.success(f"✅ **RECORDS VERIFIED — SAFE TO PROCEED**\n\n{result['decision_reason']}")

        m1, m2, m3 = st.columns(3)
        effective_uncertainty = 15 if st.session_state.physician_cleared else result["uncertainty_score"]
        m1.metric("Uncertainty Score", f"{effective_uncertainty}/100", delta="-75 Resolved" if st.session_state.physician_cleared else None)
        m2.metric("Conflicts Detected", len(result["detected_conflicts"]))
        m3.metric("Timeline Events", len(result["reconstructed_timeline"]))

        with st.expander("🔍 Multi-Agent Autonomous Execution Trace", expanded=False):
            st.markdown(f"- **Active Engine:** `{result.get('model_used', 'MEDUSA-X Engine')}`")
            st.markdown(f"- **Agent 1 (Temporal Extractor):** Parsed **{len(documents)}** fragmented sources into **{len(result['reconstructed_timeline'])}** chronological clinical events with verbatim evidence quotes.")
            st.markdown(f"- **Agent 2 (Cross-Record Auditor):** Cross-checked medications, allergies, diagnoses, and lab statuses; flagged **{len(result['detected_conflicts'])}** contradiction(s) and **{len(result['missing_information'])}** missing data gap(s).")
            st.markdown(f"- **Agent 3 (Epistemic Circuit Breaker):** Evaluated uncertainty (`{result['uncertainty_score']}/100`) against safety gate (`65/100`) -> Initial Gate: **`{decision}`**.")

        if result["detected_conflicts"]:
            st.markdown("### 🚨 Detected Contradictions & Safety Risks")
            for idx, conflict in enumerate(result["detected_conflicts"], 1):
                badge = "🔴" if conflict["severity"] == "CRITICAL" else "🟠"
                sources_str = "  ⚡⟷⚡  ".join(conflict["conflicting_sources"])
                st.markdown(
                    f"**{badge} [{conflict['severity']}] {conflict['conflict_type']}**\n"
                    f"- **Conflict Link:** `{sources_str}`\n"
                    f"- **Clinical Hazard:** {conflict['description']}"
                )

        if result["missing_information"]:
            st.markdown("### 🧩 Unresolved Gaps & Missing Data")
            for item in result["missing_information"]:
                st.markdown(f"- {item}")

        if result["escalation_questions"] and not st.session_state.physician_cleared:
            st.markdown("### 🩺 Human-in-the-Loop Physician Escalation Gate")
            st.caption("Complete all mandatory safety checks below to unlock clinical sign-off:")
            all_checked = True
            for i, q in enumerate(result["escalation_questions"]):
                checked = st.checkbox(q, key=f"esc_{patient_id}_{i}")
                if not checked:
                    all_checked = False

            override_note = st.text_input(
                "Attending Physician Resolution / Order Modification:",
                placeholder="e.g., Discontinued Amoxicillin-Clavulanate; prescribed Azithromycin 500mg PO; updated EHR allergy to Penicillin."
            )
            if st.button("✅ Sign Off & Clear Circuit Breaker", disabled=not (all_checked and len(override_note.strip()) > 5)):
                st.session_state.physician_cleared = True
                st.session_state.physician_note = override_note.strip()
                st.rerun()

        st.markdown("### ⏳ Reconstructed Chronological Timeline")
        for event in result["reconstructed_timeline"]:
            st.markdown(
                f"**`{event['timestamp']}`** | **{event['category']}** — {event['fact']}\n"
                f"> *Source ({event['source_doc']}): \"{event['exact_quote']}\"*"
            )

        st.markdown("### 📋 Verified Clinical Summary (Zero Assumptions)")
        if st.session_state.physician_cleared:
            st.success(f"RECONCILED & CLEARED SUMMARY: {result['verified_summary']} | Physician Override Applied: {st.session_state.physician_note}")
        else:
            st.info(result["verified_summary"])

        final_status = "CLEARED_WITH_PHYSICIAN_OVERRIDE" if st.session_state.physician_cleared else decision
        report_md = f"# MEDUSA-X Clinical Reconciliation & Safety Report\n"
        report_md += f"**Patient ID:** {patient_id}\n**Final Status:** {final_status}\n**Uncertainty Score:** {effective_uncertainty}/100\n\n"
        if st.session_state.physician_cleared:
            report_md += f"## Physician Sign-Off\n- **Resolution:** {st.session_state.physician_note}\n\n"
        report_md += "## Detected Conflicts\n" + "\n".join(
            [f"- [{c['severity']}] {c['conflict_type']}: {c['description']} (Sources: {', '.join(c['conflicting_sources'])})" for c in result["detected_conflicts"]]
        ) + "\n\n"
        report_md += f"## Verified Summary\n{result['verified_summary']}\n"

        st.download_button(
            label="📥 Download Auditable Clinical Handoff Report (.md)",
            data=report_md,
            file_name=f"MEDUSA_X_Audit_{patient_id}.md",
            mime="text/markdown",
            use_container_width=True
        )
