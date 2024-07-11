import pandas as pd
import numpy as np
import random
def dataset_generation():
    school_id = 15
    rand = random.randint(1,100)
    np.random.seed(rand)  # Changing the seed for randomize range

    data = {
        'School_ID': [f'SCH_{i:03d}' for i in range(1, school_id + 1)],
        'Academic_Performance_Score': np.random.uniform(60, 98, school_id),
        'Graduation_Rate': np.random.uniform(75, 100, school_id),
        'Educational_Needs_Percent': np.random.uniform(5, 20, school_id),
        'Disable_Student_Percent': np.random.uniform(0, 30, school_id),
        'Technology_Access_Score': np.random.uniform(50, 95, school_id),
        'Total_Students': np.random.randint(300, 1500, school_id),
    }

    dataset = pd.DataFrame(data)
    dataset.to_csv('output/school_dataset_generated.csv', index=False)