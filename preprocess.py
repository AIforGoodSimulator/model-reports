import pandas as pd
import glob
from pathlib import Path
import os

def read_preprocess_file(path,camp_name):
    raw_data = pd.read_csv(os.path.join('camp_info','camp_params.csv'))
    population_frame = raw_data[raw_data.Camp==camp_name].reset_index()
    total_population = population_frame['Total_population'][0]
    df=pd.read_csv(path,index_col=0)
    df.R0=df.R0.apply(lambda x: round(complex(x).real,1))
    df_temp=df.drop(['Time','R0','latentRate','removalRate','hospRate','deathRateICU','deathRateNoIcu'], axis=1)
    df_temp=df_temp*total_population
    df.update(df_temp)
    return df

def load_interventions(folder_path,camp_name,prefix=None,suffix=None):
    intervention_files=[]
    for file in glob.glob(os.path.join(folder_path,"*.csv")):
        intervention_files.append(file)
    selectedInterventions={}
    for file in intervention_files:
        path=Path(file)
        if prefix is not None:
            if suffix is not None:
                if path.stem.startswith(prefix) and path.stem.endswith(suffix):
                    selectedInterventions[path.stem]=read_preprocess_file(file,camp_name)
            else:
                if path.stem.startswith(prefix):
                    selectedInterventions[path.stem]=read_preprocess_file(file,camp_name)
        elif suffix is not None:
            if path.stem.endswith(suffix):
                selectedInterventions[path.stem]=read_preprocess_file(file,camp_name)
        else:
            selectedInterventions[path.stem]=read_preprocess_file(file,camp_name)
    return selectedInterventions

def load_intervention_dict(camp_name):
    if camp_name=='Moria':
        intervention_dict={
            'highrisk20-30':'remove 20 high-risk residents from day 0 to day 30',
            'highrisk50-12':'remove 50 high-risk residents from day 0 to day 12',
            'highrisk100-6':'remove 100 high-risk residents from day 0 to day 6',
            'hygiene0.7-30':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 30',
            'hygiene0.7-60':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 60',
            'hygiene0.7-90':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 90',
            'hygiene0.7-200':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 200',
            'hygiene0.8-200':'reduce transmission by 20% by social distancing/mask/handwashing from day 0 to day 200',
            'hygiene0.9-200':'reduce transmission by 10% by social distancing/mask/handwashing from day 0 to day 200',
            'icu12-200':'increase ICU capacity from 6 to 12',
            'icu24-200':'increase ICU capacity from 6 to 24',
            'icu48-200':'increase ICU capacity from 6 to 48',
            'isolate10-100':'isolate symptomatically infected people at 10 people per day for 100 days',
            'isolate10-200':'isolate symptomatically infected people at 10 people per day for 200 days',
            'isolate50-20':'isolate symptomatically infected people at 50 people per day for 20 days',
            'isolate50-40':'isolate symptomatically infected people at 50 people per day for 40 days',
            'isolate50-80':'isolate symptomatically infected people at 50 people per day for 80 days',
            'isolate50-120':'isolate symptomatically infected people at 50 people per day for 120 days',
            'isolate100-20':'isolate symptomatically infected people at 100 people per day for 20 days',
            'isolate100-30':'isolate symptomatically infected people at 100 people per day for 30 days',
            'isolate100-60':'isolate symptomatically infected people at 100 people per day for 60 days',
            'shielding':'shielding'
        }
    if camp_name=='Haman-al-Alil':
        intervention_dict={
            'highrisk50-5':'remove 50 high-risk residents from day 0 to day 5',
            'highrisk10-25':'remove 10 high-risk residents from day 0 to day 25',
            'hygiene0.7-30':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 30',
            'hygiene0.7-60':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 60',
            'hygiene0.7-90':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 90',
            'hygiene0.7-180':'reduce transmission by 30% by social distancing/mask/handwashing from day 0 to day 180',
            'hygiene0.8-180':'reduce transmission by 20% by social distancing/mask/handwashing from day 0 to day 180',
            'hygiene0.9-180':'reduce transmission by 10% by social distancing/mask/handwashing from day 0 to day 180',
            'hygiene0.8-90':'reduce transmission by 20% by social distancing/mask/handwashing from day 0 to day 90',
            'hygiene0.9-90':'reduce transmission by 10% by social distancing/mask/handwashing from day 0 to day 90',
            'isolate20-30':'isolate symptomatically infected people at 20 people per day for 30 days',
            'isolate20-90':'isolate symptomatically infected people at 20 people per day for 90 days',
            'isolate20-180':'isolate symptomatically infected people at 20 people per day for 180 days',
            'isolate50-30':'isolate symptomatically infected people at 50 people per day for 30 days',
            'isolate50-90':'isolate symptomatically infected people at 50 people per day for 90 days',
            'shielding':'shielding'
        }
    return intervention_dict
