def normalize_inverse(series):
    return (series.max() - series) / (series.max() - series.min())


def calculate_priority_score(df):
    weights = {
        'Performance_Score': -0.25,
        'Student_Teacher_Ratio': 0.20,
        'Educational_Needs_Percent': 0.15,
        'Disable_Student_Percent': 0.15,
        'Tech_Access_Score': -0.10,
        'Free_Reduced_Lunch_Percent': 0.15
    }

    normalized_df = df.copy()
    for column, weight in weights.items():
        if weight < 0:
            normalized_df[column] = normalize_inverse(df[column])
        else:
            normalized_df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())

    normalized_df['Priority_Score'] = sum(normalized_df[column] * abs(weight) for column, weight in weights.items())
    return normalized_df['Priority_Score']