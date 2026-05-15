from workflow.models import LearnedDraftRule
from .retrieval import retrieve_relevant_chunks


def build_query_for_task(task_type):
    queries = {
        "case_fact_summary": "facts parties dates obligations dispute events claims evidence",
        "notice_summary": "notice deadline breach demand response obligation",
        "document_checklist": "documents missing required signature date party evidence",
        "internal_memo": "legal facts issue background evidence recommendation",
    }

    return queries.get(task_type, queries["case_fact_summary"])


def get_learned_rules_text():
    rules = LearnedDraftRule.objects.order_by("-frequency")[:10]
    return "\n".join([f"- {r.rule}" for r in rules])


def summarize_evidence(evidence):
    if not evidence:
        return "No reliable evidence was retrieved from the uploaded document."

    bullets = []

    for item in evidence[:5]:
        short_text = item["text"][:350].strip()
        bullets.append(
            f"- Chunk {item['chunk_index']} says: {short_text}..."
        )

    return "\n".join(bullets)


def format_evidence(evidence):
    if not evidence:
        return "No evidence available."

    rows = []

    for i, item in enumerate(evidence, start=1):
        rows.append(
            f"""
### Evidence {i}
Source: {item['source']}
Chunk: {item['chunk_index']}
Relevance Score: {item['score']}

{item['text']}
"""
        )

    return "\n".join(rows)


def format_unclear_sections(unclear):
    if not unclear:
        return "- No major unclear sections detected."

    return "\n".join([f"- {u}" for u in unclear])


def build_draft_from_evidence(document, evidence, task_type, learned_rules=""):
    unclear = document.structured_data.get("unclear_sections", [])

    draft = f"""
# First-Pass Internal Legal Memo

## Draft Type
{task_type.replace("_", " ").title()}

## Source Document
{document.original_name}

## Important Extracted Fields
Possible Parties: {document.structured_data.get("possible_parties", [])}
Dates: {document.structured_data.get("dates", [])}
Monetary Amounts: {document.structured_data.get("monetary_amounts", [])}

## Summary
Based only on retrieved evidence:

{summarize_evidence(evidence)}

## Key Evidence
{format_evidence(evidence)}

## Unclear or Low-Confidence Areas
{format_unclear_sections(unclear)}

## Operator Notes
- This is a grounded first-pass draft.
- Unsupported legal conclusions should be manually reviewed.
- If a fact is not present in the evidence section, it should not be treated as confirmed.

## Learned Drafting Preferences Applied
{learned_rules if learned_rules else "- No learned operator preferences yet."}
"""

    return draft.strip()


def generate_grounded_draft(document, task_type="case_fact_summary"):
    query = build_query_for_task(task_type)
    evidence = retrieve_relevant_chunks(document, query)
    learned_rules = get_learned_rules_text()

    draft = build_draft_from_evidence(
        document=document,
        evidence=evidence,
        task_type=task_type,
        learned_rules=learned_rules,
    )

    return draft, evidence