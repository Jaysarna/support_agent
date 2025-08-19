import frappe
import requests
import json

def validate_issue(doc, method):
    prompt = f"""
    Subject: {doc.subject}
    Description: {doc.description}

    Provide a short suggestion (max 100 words) based on ERPNext/Frappe documentation and general logic.
    Avoid long reasoning, just give concise helpful guidance.
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer",  # replace with valid key
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-site.com",
            "X-Title": "ERPNext Helper",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150,  # keep response short
            "temperature": 0.7
        })
    )

    if response.status_code == 200:
        try:
            ai_text = (
                response.json()
                .get("choices")[0]
                .get("message")
                .get("content")
                .strip()
            )

            # Format newlines first
            formatted_ai_text = ai_text.replace("\n", "<br>")

            # Wrap nicely for Text Editor field
            formatted_text = (
                "<div style='font-size:14px; line-height:1.6;'>"
                "<p><b>AI Suggestion:</b></p>"
                f"<div style='margin-left:10px;'>{formatted_ai_text}</div>"
                "</div>"
            )

            doc.custom_ai_response = formatted_text  # your Text Editor field
        except Exception:
            doc.custom_ai_response = "<p><i>AI response could not be parsed.</i></p>"
    else:
        doc.custom_ai_response = f"<p><i>API error: {response.status_code}</i></p>"
