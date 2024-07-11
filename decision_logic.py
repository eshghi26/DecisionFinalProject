def rank(data):
    weights = {
        'Academic_Performance_Score': -0.25,
        'Graduation_Rate': 0.20,
        'Educational_Needs_Percent': 0.15,
        'Disable_Student_Percent': 0.15,
        'Technology_Access_Score': -0.10,
        'Total_Students': 0.15
    }

    def zero_to_one_convertor(factor):
        return (factor.max() - factor) / (factor.max() - factor.min())

    converted_data = data.copy()
    for column, weight in weights.items():
        if weight < 0:
            converted_data[column] = zero_to_one_convertor(data[column])
        else:
            converted_data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())

    converted_data['rank_score'] = sum(converted_data[column] * abs(weight) for column, weight in weights.items())
    return converted_data['rank_score']