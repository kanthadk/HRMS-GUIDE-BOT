import frappe
from hrms_guide_bot.hrms_guide_bot.doctype.bot_telemetry.bot_telemetry import log_event

class PolicyEngine:
	def __init__(self, user=None):
		self.user = user or frappe.session.user

	def resolve(self, query):
		"""
		Retrieve policy information using semantic search (stubbed).
		"""
		# 1. Embed query (Stub)
		# embedding = get_embedding(query)
		
		# 2. Vector Search implementation
		# This requires PGVector or similar. 
		# For the prototype, we can use a basic keyword search on PolicyChunk.
		
		chunks = frappe.db.get_all("PolicyChunk",
			filters={
				"chunk_text": ["like", f"%{query}%"]
			},
			fields=["chunk_text", "section_label", "policy_version"],
			limit=3
		)
		
		# Filter by Approved PolicyVersion
		# Logic: Join with PolicyVersion where status = 'Approved'
		# Doing this efficiently in Frappe ORM:
		
		valid_chunks = []
		for chunk in chunks:
			version = frappe.get_doc("PolicyVersion", chunk.policy_version)
			if version.status == "Approved":
				valid_chunks.append({
					"text": chunk.chunk_text,
					"source": f"{version.policy_document} - {version.version_name} ({chunk.section_label})"
				})
		
		if not valid_chunks:
			return {
				"message": "I couldn't find any specific policy regarding that."
			}

		# 3. Generate Answer using LLM
		context_text = "\n\n".join([f"Source ({c['source']}): {c['text']}" for c in valid_chunks])
		prompt = f"Answer the user query based on the following policy text:\n\n{context_text}\n\nQuery: {query}"
		
		from hrms_guide_bot.hrms_guide_bot.utils.llm import get_chat_response
		answer_text = get_chat_response(prompt)
		
		log_event("policy_used", self.user, {"query": query, "chunks_found": len(valid_chunks)})

		return {
			"answer": answer_text,
			"citations": [c["source"] for c in valid_chunks]
		}
