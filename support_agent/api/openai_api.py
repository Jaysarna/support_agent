import frappe
import requests
import json
from frappe.utils.password import get_decrypted_password

def validate_issue(doc, method):
    agent_settings = frappe.get_single("Support Agent Settings")
    prompt = f"""
    Subject: {doc.subject}
    Description: {doc.description}

    {agent_settings.context}
    """

    # Decrypt the model_token field (assuming it's a Password field)
    decrypted_token = get_decrypted_password(
        "Support Agent Settings", agent_settings.name, "model_token"
    )
    if agent_settings.disable == False:
        response = requests.post(
            url=agent_settings.model_url,
            headers={
                "Authorization": f"Bearer {decrypted_token}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "ERPNext Helper",
            },
            data=json.dumps({
                "model": agent_settings.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": agent_settings.max_token,  # keep response short
                "temperature": agent_settings.temperature,  # creativity level
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
                    "<p><b>AI Suggestion:</b></p><br>"
                    f"<div style='margin-left:10px;'>{formatted_ai_text}</div>"
                    "</div>"
                )

                doc.custom_ai_response = formatted_text  # your Text Editor field
            except Exception as e:
                frappe.throw(f"AI response could not be parsed: {e}")

        else:
            frappe.throw(f"API error: {response.status_code} - {response.text}")
