from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import decision_logic as dl
import os
import generate_dataset as gd


app= Flask(__name__)

def allocate_resources(df, total_budget):
    df['Allocated_Budget'] = df['Priority_Score'] / df['Priority_Score'].sum() * total_budget
    return df


def visualize_results_priority(df):
    plt.figure(figsize=(12, 6))
    plt.bar(df['School_ID'], df['Priority_Score'])
    plt.title('School Priority Scores')
    plt.xlabel('School ID')
    plt.ylabel('Priority Score')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save the plot as a PNG file
    output_dir = 'static'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'priority_scores.png')
    plt.savefig(output_path)
    plt.close()  # Close the figure to free up memory

def visualize_results_budget(df, totalbudget):
    allocated_df = allocate_resources(df, totalbudget)
    plt.figure(figsize=(12, 6))
    plt.bar(allocated_df['School_ID'], allocated_df['Allocated_Budget'])
    plt.title('School Budget Allocation')
    plt.xlabel('School ID')
    plt.ylabel('Budget Allocation')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save the plot as a PNG file
    output_dir = 'static'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'budget_allocation.png')
    plt.savefig(output_path)
    plt.close()  # Close the figure to free up memory


@app.get('/')
def home():
    return render_template('index.html')

@app.route('/gendata')
def gendata():
    gd.generate_data()
    generate= "Dataset generated successfully"
    return render_template('index.html', generate=generate)

@app.route('/showgendata')
def showgendata():
    generated = pd.read_csv('output/school_dataset_generated.csv')
    showgen = generated[['School_ID', 'Performance_Score', 'Student_Teacher_Ratio', 'Educational_Needs_Percent', 'Disable_Student_Percent', 'Tech_Access_Score', 'Free_Reduced_Lunch_Percent']].to_string(index=False)
    return render_template('showgendata.html', showgen=showgen)

@app.route('/setbudget', methods= ['GET', 'POST'])
def setbudget():
    if request.method == 'POST':
        budget = request.form.get("budget")
        totalbudget = {
            'Total_Budget': [budget]
        }
        export = pd.DataFrame(totalbudget)
        export.to_csv('output/totalbudget.csv', index=False)
        info= "Total budget successfully set"
        return render_template('index.html', info=info)
    return render_template('setbudget.html')

@app.route('/allores')
def allores():
    # Load data
    df = pd.read_csv('output/school_dataset_generated.csv')

    # Calculate priority scores (using the function from Step 3)
    df['Priority_Score'] = dl.calculate_priority_score(df)
    df = df.sort_values('Priority_Score', ascending=False).reset_index(drop=True)
    total_budget_csv = pd.read_csv('output/totalbudget.csv')
    total_budget = int(total_budget_csv['Total_Budget'].to_string(index=False))
    allocated_df = allocate_resources(df, total_budget)
    allores= allocated_df[['School_ID', 'Priority_Score', 'Allocated_Budget']].to_string(index=False)
    return render_template('allores.html', allores=allores)

@app.route('/visual')
def visual():
    # Load data
    df = pd.read_csv('output/school_dataset_generated.csv')

    # Calculate priority scores (using the function from Step 3)
    df['Priority_Score'] = dl.calculate_priority_score(df)
    df = df.sort_values('Priority_Score', ascending=False).reset_index(drop=True)
    total_budget_csv = pd.read_csv('output/totalbudget.csv')
    total_budget = int(total_budget_csv['Total_Budget'].to_string(index=False))
    visualize_results_priority(df)
    visualize_results_budget(df, total_budget)
    return render_template('visual.html')

app.run(debug=True, host="0.0.0.0")