import os
import json
from typing import Dict, Any
from groq import Groq

class AnswerGenerator:
    def __init__(self, api_key: str = None):
        """
        Initialize AnswerGenerator with Groq API
        Get your free API key from: https://console.groq.com
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Get one free at https://console.groq.com")

        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Free Llama 3.3 70B model

    def generate_answer(self, query: str, query_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a natural language answer from query results with citations
        """

        system_prompt = """You are an agricultural and climate data analyst. Your job is to:
1. Analyze the data provided
2. Generate a clear, accurate answer to the user's question
3. Include specific numbers and statistics
4. Cite data sources for every claim
5. Provide insights and context

Format your response as:
- Start with a direct answer to the question
- Support with specific data points
- Add relevant context or insights
- End with data source citations

Be precise, professional, and data-driven."""

        user_prompt = f"""User Question: {query}

Data Retrieved:
{json.dumps(query_results, indent=2)}

Please provide a comprehensive answer to the user's question based on this data. Include:
1. Direct answer with specific numbers
2. Key insights and comparisons
3. Data source citations (mention districts, specific metrics)
4. Any limitations of the analysis

Keep the answer concise but informative."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=2048
            )

            answer = chat_completion.choices[0].message.content.strip()

            return {
                "success": True,
                "query": query,
                "answer": answer,
                "raw_data": query_results,
                "sources": self._extract_sources(query_results)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Answer generation failed: {str(e)}",
                "query": query
            }

    def _extract_sources(self, query_results: Dict[str, Any]) -> list:
        """Extract data sources from query results"""
        sources = []

        query_type = query_results.get("query_type", "")

        if "crop" in str(query_results):
            sources.append({
                "dataset": "Crop Production Data",
                "region": "Karnataka",
                "file": "crop_production.csv",
                "description": "District-level crop production data for Kharif, Rabi, and Summer seasons"
            })

        if "rainfall" in str(query_results):
            sources.append({
                "dataset": "Rainfall Data",
                "region": "Tamil Nadu",
                "file": "rainfall_data.csv.csv",
                "period": "June 2017 to May 2018",
                "description": "District-level seasonal rainfall data"
            })

        return sources
