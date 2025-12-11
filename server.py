from flask import Flask, render_template, request
from psl_agent.query_analysis import get_query_analysis
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)