from workflow.models import LearnedDraftRule


def learn_from_operator_edit(original_text, edited_text):
    rules = []

    if len(edited_text) > len(original_text) * 1.15:
        rules.append("Operator prefers more detailed explanations.")

    if edited_text.count("- ") > original_text.count("- "):
        rules.append("Operator prefers more bullet-point structure.")

    if "unclear" in edited_text.lower() or "not confirmed" in edited_text.lower():
        rules.append("Operator prefers explicit uncertainty and low-confidence notes.")

    if "evidence" in edited_text.lower():
        rules.append("Operator prefers stronger evidence references in drafts.")

    if not rules:
        rules.append("Operator made wording/style refinements; keep future drafts concise and editable.")

    for rule in rules:
        obj, created = LearnedDraftRule.objects.get_or_create(rule=rule)

        if not created:
            obj.frequency += 1
            obj.save()

    return rules