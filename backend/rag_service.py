import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class RagService:
    def __init__(self):
        # Load mock data
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, "mock_data.json")
            with open(data_path, "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}
            print(f"Warning: mock_data.json not found at {data_path}")

        # Initialize Azure OpenAI Client
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo") # Default or set in env
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")

        if self.api_key and self.endpoint:
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=self.api_version,
                azure_endpoint=self.endpoint
            )
        else:
            self.client = None
            print("Warning: Azure OpenAI credentials not found. AI features will respond with static fallback.")

    def find_context(self, query):
        """Simple keyword search to find relevant context from mock_data."""
        query = query.lower()
        context_parts = []
        
        # Flatten the nested json for search
        for category, items in self.data.items():
            for key, info in items.items():
                # Check if key or category is in query
                if key in query or category in query or query in info['content'].lower():
                    context_parts.append(f"[{category.upper()} - {key.capitalize()}]: {info['content']} (Source: {info['url']})")
        
        # If specific match is found via direct key mapping (from buttons)
        # e.g. "fees_tuition_in_state" -> data['fees']['tuition_in_state']
        if "_" in query:
             parts = query.split("_", 1)
             if len(parts) == 2:
                 cat, sub = parts
                 if cat in self.data and sub in self.data[cat]:
                     return f"[{cat.upper()} - {sub.capitalize()}]: {self.data[cat][sub]['content']} (Source: {self.data[cat][sub]['url']})"

        if not context_parts:
            # Return a broad context if nothing specific found, or empty
            return "No specific internal data found."
            
        return "\n".join(context_parts[:3]) # Limit to top 3 matches to save tokens

    def get_response(self, query):
        context = self.find_context(query)
        
        system_prompt = f"""You are a helpful University Assistant. 
        Use the following context to answer the student's question. 
        If the answer is in the context, always include the source link provided.
        If the answer is NOT in the context, politely say you only have information about specific university topics.
        
        Context:
        {context}
        """

        if not self.client:
            return f"[System]: Azure OpenAI not configured. \n\n**Context found:**\n{context}"

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error contacting AI service: {str(e)}"
