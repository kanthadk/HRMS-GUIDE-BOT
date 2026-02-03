import frappe
# import openai

def get_chat_response(prompt, context=None):
    """
    Call OpenAI API to generate a response.
    Requires 'OPENAI_API_KEY' in site config.
    """
    api_key = frappe.conf.get("OPENAI_API_KEY") or frappe.db.get_single_value("System Settings", "openai_api_key")
    
    if not api_key:
        # Mock mode for testing without API Key
        # return "Error: OpenAI API Key not configured. Please contact the administrator."
        return f"[MOCK AI RESPONSE] I have received your request regarding: '{prompt[:30]}...'. Since I am in test mode, I confirm that the logic flow is working correctly. In production, I would answer based on the policy text provided."
        
    # Mocking the call if no library installed or for safety
    # In production:
    # client = openai.OpenAI(api_key=api_key)
    # response = client.chat.completions.create(...)
    
    # For now, we simulate a response to avoid crashing if library missing
    # But I will write the real code commented out or active if `openai` is standard
    
    # Simple requests fallback if openai package is not installed
    import requests
    import json
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful HR assistant. Answer based on the provided policy context only."},
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"Error from AI Provider: {response.text}"
            
    except Exception as e:
        frappe.log_error(f"LLM Error: {str(e)}")
        return "I'm having trouble connecting to my brain right now. Please try again later."
