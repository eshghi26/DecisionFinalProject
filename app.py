from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import decision_logic as dl
import os
import generate_dataset as gd


app= Flask(__name__)

def budget_allocation(instance, total_budget):
    instance['Allocated_Budget'] = instance['rank_score'] / instance['rank_score'].sum() * total_budget
    return instance


def ranking_chart(instance):
    plt.figure(figsize=(12, 6))
    plt.plot(instance['School_ID'], instance['rank_score'], marker='o')
    # plt.bar(instance['School_ID'], instance['rank_score'])
    plt.title('School Ranking')
    plt.xlabel('School ID')
    plt.ylabel('Ranking Score')
    plt.xticks(rotation=90)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Save the plot as a PNG file
    output_dir = 'static'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'priority_scores.png')
    plt.savefig(output_path)
    plt.close()

def budget_chart(instance, totalbudget):
    allocated_instance = budget_allocation(instance, totalbudget)
    plt.figure(figsize=(12, 6))
    plt.plot(allocated_instance['School_ID'], allocated_instance['Allocated_Budget'], marker='o')
    # plt.bar(allocated_instance['School_ID'], allocated_instance['Allocated_Budget'])
    plt.title('School Budget Allocation')
    plt.xlabel('School ID')
    plt.ylabel('Budget Allocation')
    plt.xticks(rotation=90)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
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
    gd.dataset_generation()
    generate= "Dataset generated successfully"
    return render_template('index.html', generate=generate)

@app.route('/showgendata')
def showgendata():
    generated = pd.read_csv('output/school_dataset_generated.csv')
    showgen = generated[['School_ID', 'Academic_Performance_Score', 'Graduation_Rate', 'Educational_Needs_Percent', 'Disable_Student_Percent', 'Technology_Access_Score', 'Total_Students']].to_string(index=False)
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
    data = pd.read_csv('output/school_dataset_generated.csv')

    # Calculate priority scores (using the function from Step 3)
    data['rank_score'] = dl.rank(data)
    data = data.sort_values('rank_score', ascending=False).reset_index(drop=True)
    total_budget_csv = pd.read_csv('output/totalbudget.csv')
    total_budget = int(total_budget_csv['Total_Budget'].to_string(index=False))
    allocated_df = budget_allocation(data, total_budget)
    allores= allocated_df[['School_ID', 'rank_score', 'Allocated_Budget']].to_string(index=False)
    return render_template('allores.html', allores=allores)

@app.route('/visual')
def visual():
    # Load data
    data = pd.read_csv('output/school_dataset_generated.csv')

    # Calculate priority scores (using the function from Step 3)
    data['rank_score'] = dl.rank(data)
    data = data.sort_values('rank_score', ascending=False).reset_index(drop=True)
    total_budget_csv = pd.read_csv('output/totalbudget.csv')
    total_budget = int(total_budget_csv['Total_Budget'].to_string(index=False))
    ranking_chart(data)
    budget_chart(data, total_budget)
    return render_template('visual.html')

app.run(debug=True, host="0.0.0.0")