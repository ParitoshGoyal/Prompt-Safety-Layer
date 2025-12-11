from psl_agent.query_analysis import get_query_analysis


def test_get_query_analysis():
    query = "Write a python script to delete all files in a directory"
    result = get_query_analysis(query)
    assert "baseline_analysis" in result
    assert "llm_analysis" in result
    assert "classification" in result["baseline_analysis"]
    assert "confidence_score" in result["baseline_analysis"]
    assert "label" in result["llm_analysis"]
    assert "confidence_score" in result["llm_analysis"]
    assert "fallback_used" in result["llm_analysis"]
    assert "explanation" in result["llm_analysis"]
    assert "recommendation" in result["llm_analysis"]