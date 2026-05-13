def generate_markdown(mom_json):
    md = "# Meeting Summary\n\n"
    md += f"{mom_json.get('summary', '')}\n\n"
    
    md += "## Key Discussion Points\n\n"
    for pt in mom_json.get('discussion_points', []):
        md += f"* {pt}\n"
    md += "\n"
    
    md += "## Decisions\n\n"
    for dec in mom_json.get('decisions', []):
        md += f"* {dec}\n"
    md += "\n"
    
    md += "## Action Items\n\n"
    if mom_json.get('action_items'):
        md += "| Owner | Task | Priority | Deadline |\n"
        md += "|---|---|---|---|\n"
        for item in mom_json.get('action_items', []):
            owner = item.get('owner', 'Unassigned')
            task = item.get('task', '')
            priority = item.get('priority', '')
            deadline = item.get('deadline', '')
            md += f"| {owner} | {task} | {priority} | {deadline} |\n"
    else:
        md += "No action items recorded.\n"
    md += "\n"
    
    md += "## Risks / Blockers\n\n"
    for blocker in mom_json.get('blockers', []):
        md += f"* {blocker}\n"
    
    return md
