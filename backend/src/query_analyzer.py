import os
import json
from typing import Dict, Any
from groq import Groq

class QueryAnalyzer:
    def __init__(self, api_key: str = None):
        """
        Initialize QueryAnalyzer with Groq API
        Get your free API key from: https://console.groq.com
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Get one free at https://console.groq.com")

        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  # Free Llama 3.3 70B model

    def analyze_query(self, query: str, available_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a natural language query and extract:
        - Query type (comparison, trend, ranking, correlation, recommendation)
        - Entities (states, districts, crops, years, seasons)
        - Parameters (time periods, metrics)
        """

        system_prompt = """You are a query analyzer for an agricultural and climate data system.

Available data:
- Crop Production Data (Karnataka): Contains district-level data for Kharif, Rabi, and Summer seasons with Area, Yield, and Production metrics
- Rainfall Data (Tamil Nadu): Contains district-level rainfall data for South West Monsoon, North East Monsoon, Winter, and Hot Weather seasons

Your task is to analyze the user's natural language query and extract structured information.

Return ONLY a JSON object with the following structure (no additional text):
{
    "query_type": "comparison|trend|ranking|correlation|recommendation",
    "data_sources": ["crop"|"rainfall"],
    "entities": {
        "districts": ["list of districts mentioned"],
        "states": ["list of states mentioned"],
        "crops": ["list of crops mentioned if any"],
        "seasons": ["list of seasons mentioned"]
    },
    "metrics": ["list of metrics to analyze: production, yield, area, rainfall"],
    "time_period": "description of time period if mentioned",
    "analysis_type": "description of what analysis to perform"
}

Examples:
Query: "Compare rainfall in Chennai vs Coimbatore"
Response: {
    "query_type": "comparison",
    "data_sources": ["rainfall"],
    "entities": {
        "districts": ["Chennai", "Coimbatore"],
        "states": ["Tamil Nadu"],
        "crops": [],
        "seasons": []
    },
    "metrics": ["rainfall"],
    "time_period": "all available",
    "analysis_type": "Compare total and seasonal rainfall between two districts"
}

Query: "Which district has highest crop production in Karnataka?"
Response: {
    "query_type": "ranking",
    "data_sources": ["crop"],
    "entities": {
        "districts": [],
        "states": ["Karnataka"],
        "crops": [],
        "seasons": []
    },
    "metrics": ["production"],
    "time_period": "all available",
    "analysis_type": "Find district with maximum total crop production"
}"""

        user_prompt = f"Query: {query}\n\nProvide ONLY the JSON response:"

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
                temperature=0.1,
                max_tokens=1024,
                response_format={"type": "json_object"}
            )

            response_text = chat_completion.choices[0].message.content

            # Try to parse JSON from response
            try:
                # Clean the response text
                response_text = response_text.strip()

                # Find JSON in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1

                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                    return analysis
                else:
                    # If no JSON found, return error
                    return {"error": "Could not parse query analysis", "raw_response": response_text}

            except json.JSONDecodeError as e:
                return {"error": f"JSON parsing error: {str(e)}", "raw_response": response_text}

        except Exception as e:
            return {"error": f"Query analysis failed: {str(e)}"}
