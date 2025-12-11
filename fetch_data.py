# Use if data needs to be re-downloaded and saved locally
from pathlib import Path
import pandas as pd



def download_data():
        
    splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
    df_train = pd.read_parquet("hf://datasets/xTRam1/safe-guard-prompt-injection/" + splits["train"])
    df_test = pd.read_parquet("hf://datasets/xTRam1/safe-guard-prompt-injection/" + splits["test"])


    df_train['fold'] = 'train'
    df_test['fold'] = 'test'

    df = pd.concat([df_train, df_test], ignore_index=True, axis=0)


    # Save the Dataset
    # folder path
    folder =Path('data')
    # create folder if it doesn't exist
    folder.mkdir(exist_ok=True)
    # save to csv
    df.to_csv('data/dataset.csv', index=False)


if __name__ == "__main__":
    download_data()