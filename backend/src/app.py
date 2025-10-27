from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from data_loader import DataLoader
from query_analyzer import QueryAnalyzer
from query_processor import QueryProcessor
from answer_generator import AnswerGenerator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
print("Initializing Samarth Q&A System...")
data_loader = DataLoader(data_dir="../data")
query_analyzer = QueryAnalyzer()
query_processor = QueryProcessor(data_loader)
answer_generator = AnswerGenerator()
print("System initialized successfully!")

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Samarth - Intelligent Q&A System for Government Data",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Submit a natural language query",
            "/data-summary": "GET - Get summary of available data",
            "/health": "GET - Health check"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Samarth API is running"})

@app.route('/data-summary')
def data_summary():
    """Get summary of available datasets"""
    try:
        summary = data_loader.get_data_summary()
        return jsonify({
            "success": True,
            "data": summary
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/query', methods=['POST'])
def query():
    """
    Main endpoint for processing natural language queries

    Expected JSON body:
    {
        "query": "Your natural language question here"
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'query' field in request body"
            }), 400

        user_query = data['query']

        if not user_query or len(user_query.strip()) == 0:
            return jsonify({
                "success": False,
                "error": "Query cannot be empty"
            }), 400

        print(f"\n=== Processing Query ===")
        print(f"Query: {user_query}")

        # Step 1: Analyze the query
        print("Step 1: Analyzing query...")
        available_data = data_loader.get_data_summary()
        query_analysis = query_analyzer.analyze_query(user_query, available_data)

        if "error" in query_analysis:
            return jsonify({
                "success": False,
                "error": query_analysis["error"],
                "stage": "query_analysis"
            }), 500

        print(f"Query Analysis: {query_analysis}")

        # Step 2: Process the query and retrieve data
        print("Step 2: Processing query and retrieving data...")
        query_results = query_processor.process_query(query_analysis)

        if "error" in query_results:
            return jsonify({
                "success": False,
                "error": query_results["error"],
                "stage": "query_processing"
            }), 500

        print(f"Query Results: {query_results}")

        # Step 3: Generate natural language answer
        print("Step 3: Generating answer...")
        answer = answer_generator.generate_answer(user_query, query_results)

        print(f"Answer generated successfully!")
        print("=" * 50)

        return jsonify(answer)

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/example-queries')
def example_queries():
    """Get example queries users can try"""
    return jsonify({
        "examples": [
            {
                "category": "Comparison",
                "queries": [
                    "Compare rainfall in Chennai vs Coimbatore",
                    "Compare crop production between Raichur and Belagavi districts",
                    "Which district has more rainfall: Nagapattinam or Kanniyakumari?"
                ]
            },
            {
                "category": "Ranking",
                "queries": [
                    "Which district has the highest crop production in Karnataka?",
                    "Top 5 districts by rainfall in Tamil Nadu",
                    "Districts with lowest crop yield",
                    "Rank districts by total crop area"
                ]
            },
            {
                "category": "Analysis",
                "queries": [
                    "What is the average rainfall across Tamil Nadu?",
                    "Total crop production in Karnataka",
                    "Which season contributes most to crop production?",
                    "Seasonal rainfall patterns in Tamil Nadu"
                ]
            },
            {
                "category": "Specific Data",
                "queries": [
                    "Crop production data for Mysuru district",
                    "Rainfall data for Salem district",
                    "How much area is under cultivation in Ballari?",
                    "What is the yield in Hassan district?"
                ]
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
