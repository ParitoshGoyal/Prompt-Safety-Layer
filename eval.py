from psl_agent.query_analysis import get_query_analysis, baseline_model_analysis, llm_model_analysis
import pandas as pd
from matplotlib import pyplot as plt
import json
import sys

def evaluate_models(start_count=0, end_count=100):
    errors = []
    count = 0
    skip_count = start_count
    df_data = pd.read_csv("data/dataset.csv")
    df_test_data = df_data[df_data["fold"]=='test']
    # df_sampled = pd.read_csv('data/df_sampled_results.csv')
    for idx, row in df_test_data.iterrows():
        text = row['text']

        if count < skip_count: # > 0:
            skip_count -= 1
            print(f"skipping processed")
            continue

        try:
        # Call baseline model analysis
            baseline_result = baseline_model_analysis(text)
            llm_result = llm_model_analysis(text)

            df_test_data.at[idx, 'baseline_label'] = baseline_result['classification']
            df_test_data.at[idx, 'baseline_confidence'] = baseline_result['confidence_score']

            df_test_data.at[idx, 'agent_label'] = llm_result['label']
            df_test_data.at[idx, 'agent_confidence'] = llm_result['confidence_score']
            df_test_data.at[idx, 'agent_fallback'] = llm_result['fallback_used']
            df_test_data.at[idx, 'agent_explanation'] = llm_result['explanation']
            df_test_data.at[idx, 'agent_recommendation'] = llm_result['recommendation']

        except Exception as e:
            errors.append({'error':e, 'index':idx})
            with open(f'eval_logs/errors_{start_count}_{end_count}.json', 'w') as f:
                json.dump(errors, f, indent=4, default=str)

            continue


        # Save df_sampled to CSV
        df_test_data.to_csv(f'eval_logs/df_sampled_results_{start_count}_{end_count}.csv', index=False)
        #print("df_sampled saved to data/df_sampled_results.csv")

        count +=1
        print(f"Count:{count}, idx:{idx}, baseline:{baseline_result}, llm_agent:{llm_result}")

        if end_count-start_count + 1 == count:
            break



    print("Analysis complete. df_sampled updated with results.")

    # Save df_sampled to CSV
    # df_sampled.to_csv('data/df_sampled_results.csv', index=False)
    print("df_sampled saved to data/df_sampled_results.csv")


if __name__ == "__main__":
    # Example:- python eval.py --start_count 0 --end_count 5
    if len(sys.argv)>1:
        print(sys.argv)
        start_count = int(sys.argv[2])
        end_count = int(sys.argv[4])

    evaluate_models(start_count, end_count)