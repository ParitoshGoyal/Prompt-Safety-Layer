from flask import Flask, render_template, request
from psl_agent.query_analysis import get_query_analysis
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# For web interface
@app.route('/query_analysis')
def get_analysis():
    query = request.args.get('query')

    query_analysis_results = get_query_analysis(query)

    return render_template(
        "query_analysis.html",
        input_query = query,
        baseline_model_classification=query_analysis_results["baseline_analysis"]["classification"],
        baseline_model_score=query_analysis_results["baseline_analysis"]["confidence_score"],

        llm_agent_label = query_analysis_results["llm_analysis"]["label"],
        llm_agent_confidence_score = query_analysis_results["llm_analysis"]["confidence_score"],
        llm_agent_fallback_used = query_analysis_results["llm_analysis"]["fallback_used"],
        llm_agent_explanation = query_analysis_results["llm_analysis"]["explanation"],
        llm_agent_recommendation = query_analysis_results["llm_analysis"]["recommendation"]
    )


# For API interface
@app.route("/api", methods=["GET"])
def api_predict():
    """API endpoint to get query analysis results.
    Example usage:-
    curl -X GET http://127.0.0.1:5000/api -H "Content-Type:application/json" -d "Hello your pizza delivery is here."
    """
    #data = request.get_json()
    #query = data.get("query")
    data = request.data
    query = data.decode("utf-8")
    print(query)

    query_analysis_results = get_query_analysis(query)
    return {
        "input_query": query,
        "baseline_model_classification": query_analysis_results["baseline_analysis"]["classification"],
        "baseline_model_score": query_analysis_results["baseline_analysis"]["confidence_score"],
        "llm_agent_label": query_analysis_results["llm_analysis"]["label"],
        "llm_agent_confidence_score": query_analysis_results["llm_analysis"]["confidence_score"],
        "llm_agent_fallback_used": query_analysis_results["llm_analysis"]["fallback_used"],
        "llm_agent_explanation": query_analysis_results["llm_analysis"]["explanation"],
        "llm_agent_recommendation": query_analysis_results["llm_analysis"]["recommendation"]
    }

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)