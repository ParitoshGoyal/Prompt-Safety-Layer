from pprint import pprint
import joblib
import pandas as pd
from psl_agent.agent import PromptSafetyClassifier
# import agent

baseline_loaded_model = joblib.load('models/baseline_model.pkl')

llm_model = PromptSafetyClassifier()

# load_agent = agent.load_agent()

# get per query analysis
def get_query_analysis(query: str) -> dict:
    baseline_analysis = baseline_model_analysis(query)

    llm_analysis= llm_model_analysis(query) #{"classification":"unsafe"}
    return {
        "baseline_analysis": baseline_analysis,
        "llm_analysis": llm_analysis
    }

def baseline_model_analysis(query: str) -> dict:
    y_proba = baseline_loaded_model.predict_proba(pd.Series(query))
    label = y_proba[0].argmax()
    classification = "safe" if label == 0 else "unsafe"

    return {"classification":classification, "confidence_score":y_proba[0].max()}



def llm_model_analysis(query: str) -> dict:



    output = llm_model.analyze(query)
    return output