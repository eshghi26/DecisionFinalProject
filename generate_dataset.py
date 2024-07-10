import pandas as pd
import numpy as np
import random
def generate_data():
    rand = random.randint(1,100)
    np.random.seed(rand)  # For reproducibility

    num_schools = 25

    data = {
        'School_ID': [f'SCH_{i:03d}' for i in range(1, num_schools + 1)],
        'Performance_Score': np.random.uniform(50, 95, num_schools),
        'Student_Teacher_Ratio': np.random.uniform(10, 25, num_schools),
        'Educational_Needs_Percent': np.random.uniform(5, 20, num_schools),
        'Disable_Student_Percent': np.random.uniform(0, 30, num_schools),
        'Tech_Access_Score': np.random.uniform(40, 90, num_schools),
        'Free_Reduced_Lunch_Percent': np.random.uniform(20, 80, num_schools),
    }

    df = pd.DataFrame(data)
    df.to_csv('output/school_dataset_generated.csv', index=False)