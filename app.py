from flask import Flask, render_template, request, redirect, current_app
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid GUI interaction
import io
import base64
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

question_routes = [
    '/show_graph/q1',
    '/show_graph/q2',
    '/show_graph/q3',
    '/show_graph/q4',
    '/show_graph/q5',
    '/show_graph/q6',
    '/show_graph/q7',
    '/show_graph/q8',
    '/show_graph/q9',
    '/show_graph/q10',
    '/show_graph/q11',
    '/show_graph/q12',
    '/show_graph/q13',
    '/show_graph/q14',
    '/show_graph/q15',
    '/show_graph/q16',
    '/show_graph/q17',
    '/show_graph/q18',
    '/show_graph/q19',
    '/show_graph/q20'
]
random.shuffle(question_routes)

def generate_line_graphs():
        # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    # Extracting necessary columns for plotting
    years = df['year']
    countries = df.columns[1:]  # Extract country names from columns (excluding 'year')

    # Create a line graph for each country with markers
    plt.figure(figsize=(30, 20))  # Increase figure size for the line chart

    for country in countries:
        plt.plot(years, df[country], marker='o', markersize=10, label=country, linestyle='-', linewidth=4)  # Add markers and increase size

    plt.title('Medals According to Years for Top 10 Countries (1896-2020)', fontsize=35)
    plt.xlabel('Year', fontsize=25)
    plt.ylabel('Number of Medals', fontsize=25)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=25)  # Adjust legend position
    plt.grid(True)
    plt.xticks(years, rotation=45, fontsize=25)  # Increase x-axis labels font size
    plt.yticks(fontsize=25)  # Larger y-axis labels font size
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot to base64 string
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return chart_url

# Generate graphs when the application starts
global_chart_url = generate_line_graphs()

def generate_area_graphs():
    # Code for generating the area chart (unchanged)
    data = {
        'Country': ['USA', 'RUS', 'GER', 'GBR', 'CHN', 'FRA', 'ITA', 'SWE', 'NOR', 'JPN'],
        'Gold': [1174, 750, 600, 296, 285, 264, 259, 212, 209, 186],
        'Silver': [952, 635, 612, 323, 231, 293, 231, 228, 186, 178],
        'Bronze': [833, 627, 609, 331, 197, 332, 269, 239, 173, 209]
    }
    df_area = pd.DataFrame(data)
    df_area.set_index('Country', inplace=True)

    plt.figure(figsize=(10, 7))
    df_area.plot(kind='area', ax=plt.gca())
    plt.title('Total Medal Counts by Country', fontsize=20)
    plt.xlabel('Country', fontsize=16)
    plt.ylabel('Number of Medals', fontsize=16)
    plt.legend(loc='upper left', fontsize=25)  # Increase legend font size
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    # Save the area chart to a temporary buffer
    img_area = io.BytesIO()
    plt.savefig(img_area, format='png')
    img_area.seek(0)

    # Encode the area chart to base64 string
    area_chart_url = base64.b64encode(img_area.getvalue()).decode()
    plt.close()

    return area_chart_url

# Generate graphs when the application starts
global_chart_url1 = generate_area_graphs()

current_question_index = 0
# Initialize a dictionary to store user answers for each question
user_answers = {}
unasked_questions = list(range(len(question_routes)))
total_response_time = 0

@app.route('/start_random_question')
def start_random_question():
    if not unasked_questions:  # If all questions have been asked
        return redirect('/show_graph/testdone')

    # Randomly select a question from unasked questions
    current_question_index = random.choice(unasked_questions)
    unasked_questions.remove(current_question_index)
    return redirect(question_routes[current_question_index])

# Update the save_answer route to include the question number in the URL and store user answers
@app.route('/save_answer/<int:question_number>', methods=['POST'])
def save_answer(question_number):
    global total_response_time

    if request.method == 'POST':
        # [Existing logic to handle user response]
        user_answer = request.form['answer']
        response_time = request.form.get('responseTime', 0)
        answer_data = {
            'answer': user_answer,
            'time': float(response_time)
        }
        total_response_time += float(response_time)

        if question_number in user_answers:
            user_answers[question_number].append(answer_data)
        else:
            user_answers[question_number] = [answer_data]

    # Redirect to the next question or test completion
    if unasked_questions:
        return redirect('/start_random_question')
    else:
        return redirect('/show_graph/testdone')

@app.route('/show_graph')
def show_graph():
    return render_template('show_graph.html', chart_url=global_chart_url, area_chart_url=global_chart_url1)

def generate_usa_most_medals_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    # Extracting necessary columns for plotting
    years = df['year']

    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    # Plotting the specific graph for the United States
    plt.plot(years, df['USA'], marker='o', color='b', linestyle='-', label='United States')
    
    plt.title('Medals Won by the United States Each Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_usa = io.BytesIO()
    plt.savefig(img_usa, format='png')
    img_usa.seek(0)

    # Encode the plot to base64 string
    usa_chart_url = base64.b64encode(img_usa.getvalue()).decode()
    plt.close()

    return usa_chart_url

# Generate graph for the United States when the application starts
global_chart_url_usa = generate_usa_most_medals_graph()

@app.route('/show_graph/q1')
def show_question_1():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'
    # Question and answer choices
    question = 'Which year did the United States win the most medals?'
    answer_choices = ['1904', '1984', '2016', '2020']
    return render_template('show_graph.html', next_question_route=next_question_route, question_number='Which year did the United States won the medals the most?', usa_chart_url=global_chart_url_usa, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_country_comparison_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    # Clean column names to remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Extracting necessary columns for plotting
    years = df['year']

    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    # Plotting the comparison graph for China and Russia/Soviet Union/ROC
    plt.plot(years, df['CHN'], marker='o', color='m', label='China', linestyle='-')
    plt.plot(years, df['RUSS'], marker='o', color='orange', label='Russia/Soviet Union/ROC', linestyle='-')
    
    plt.title('Medals Comparison: China vs Russia/Soviet Union/ROC')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_comparison = io.BytesIO()
    plt.savefig(img_comparison, format='png')
    img_comparison.seek(0)

    # Encode the plot to base64 string
    comparison_chart_url = base64.b64encode(img_comparison.getvalue()).decode()
    plt.close()

    return comparison_chart_url

# Generate comparison graph when the application starts
global_chart_url_comparison = generate_country_comparison_graph()

@app.route('/show_graph/q2')
def show_question_2():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'
    # Question and answer choices
    question = 'Which country got more medals over the years: Russia or China?'
    answer_choices = ['Russia', 'China', 'The number of medals won by both countries is the same.', 'Cannot be determined from the given data.']
    return render_template('show_graph.html',next_question_route=next_question_route,question_number='Which country got more medals over the years: Russia or China?', comparison_chart_url=global_chart_url_comparison, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)


@app.route('/show_graph/q3')
def show_question_3():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Which country won the medals the most in 1980?'
    answer_choices = ['USA', 'Germany', 'Russia', 'Great Britain']
    return render_template('show_graph.html', next_question_route=next_question_route,question_number='Which country won the medals the most in 1980?', chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_sweden_norway_medals_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    years = df['year']

    # Plot the graphs for Sweden and Norway
    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    plt.plot(years, df['SWE'], marker='o', color='blue', label='Sweden', linestyle='-')
    plt.plot(years, df['NOR'], marker='o', color='olive', label='Norway', linestyle='-')

    plt.title('Medals Comparison: Sweden vs Norway')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_sweden_norway = io.BytesIO()
    plt.savefig(img_sweden_norway, format='png')
    img_sweden_norway.seek(0)

    # Encode the plot to base64 string
    sweden_norway_chart_url = base64.b64encode(img_sweden_norway.getvalue()).decode()
    plt.close()

    return sweden_norway_chart_url

# Generate graph for Sweden and Norway when the application starts
global_chart_url_sweden_norway = generate_sweden_norway_medals_graph()

@app.route('/show_graph/q4')
def show_question_4():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Which country got more medals over the years: Sweden or Norway?'
    answer_choices = ['Sweden', 'Norway', 'The number of medals won by both countries is the same.', 'Cannot be determined from the given data.']
    return render_template('show_graph.html',  next_question_route=next_question_route,question_number='Which country got more medals over the years: Sweden or Norway?',
                           sweden_norway_chart_url=global_chart_url_sweden_norway, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_medals_comparison_1908_1936():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    years = df['year']

    # Plot the graphs for Great Britain and Italy between 1908 and 1936
    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    plt.plot(years[(years >= 1908) & (years <= 1936)], df['GBR'][(years >= 1908) & (years <= 1936)], marker='o', color='red', linestyle='-', label='Great Britain')
    plt.plot(years[(years >= 1908) & (years <= 1936)], df['ITA'][(years >= 1908) & (years <= 1936)], marker='o', color='purple', linestyle='-', label='Italy')

    plt.title('Medals Comparison: Great Britain vs Italy (1908-1936)')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_medals_comparison = io.BytesIO()
    plt.savefig(img_medals_comparison, format='png')
    img_medals_comparison.seek(0)

    # Encode the plot to base64 string
    medals_comparison_chart_url = base64.b64encode(img_medals_comparison.getvalue()).decode()
    plt.close()

    return medals_comparison_chart_url

# Generate graph for Great Britain and Italy between 1908 and 1936 when the application starts
global_chart_url_medals_comparison = generate_medals_comparison_1908_1936()

@app.route('/show_graph/q5')
def show_question_5():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Which country decreased in the number of medals between 1908 to 1936 overall: Great Britain or Italy?'
    answer_choices = ['Great Britain', 'Italy', 'Both Great Britain and Italy had a decrease in medals', 'Neither Great Britain nor Italy had a decrease in medals']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Which country decreased in the number of medals between 1908 to 1936 overall: Great Britain or Italy?',
                           medals_comparison_chart_url=global_chart_url_medals_comparison, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

# Modify the code in the generate_most_medals_1980_graph function to generate a graph for a specific country for a specific year (in this case, France for the year it won the most medals)
def generate_most_medals_country_year_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    # Plotting the graph for France to identify the year it won the most medals
    plt.plot(df['year'], df['FRA'], marker='o', color='brown', linestyle='-', label='France')

    plt.title('Medals Won by France Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_france = io.BytesIO()
    plt.savefig(img_france, format='png')
    img_france.seek(0)

    # Encode the plot to base64 string
    france_chart_url = base64.b64encode(img_france.getvalue()).decode()
    plt.close()

    return france_chart_url

# Generate graph for France over the years when the application starts
global_chart_url_france = generate_most_medals_country_year_graph()

@app.route('/show_graph/q6')
def show_question_6():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Which year did France win the most medals?'
    answer_choices = ['1900', '1984', '2012', '2016']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Which year did France win the most medals?', france_chart_url=global_chart_url_france, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_japan_fewest_medals_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    years = df['year']
    japan_medals = df['JPN']

    # Plot the graph for Japan's medals each year
    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    plt.plot(years, japan_medals, marker='o', color='blue', linestyle='-', label='Japan')

    plt.title('Medals Won by Japan Each Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.xticks(years, rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_japan_medals = io.BytesIO()
    plt.savefig(img_japan_medals, format='png')
    img_japan_medals.seek(0)

    # Encode the plot to base64 string
    japan_medals_chart_url = base64.b64encode(img_japan_medals.getvalue()).decode()
    plt.close()

    return japan_medals_chart_url

# Generate graph for Japan when the application starts
global_chart_url_japan = generate_japan_fewest_medals_graph()

@app.route('/show_graph/q7')
def show_question_7():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'In which year did Japan get the fewest medals?'
    answer_choices = ['1948', '1976', '1980', '2020']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='In which year did Japan get the fewest medals?',
                           japan_medals_chart_url=global_chart_url_japan, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_fastest_increase_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    years = df['year']
    countries = df.columns[1:]

    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    max_increase_country = ''
    max_increase_rate = 0

    # Calculate the increase rate for each country between 1968 and 1980
    for country in countries:
        mask = (years >= 1968) & (years <= 1980)
        medals_1968 = df.loc[years == 1968, country].values[0]
        medals_1980 = df.loc[years == 1980, country].values[0]
        increase_rate = (medals_1980 - medals_1968) / medals_1968

        # Plot the graph for each country for the specified years
        plt.plot(years[mask], df[country][mask], marker='o', linestyle='-', label=country)

        # Find the country with the highest increase rate
        if increase_rate > max_increase_rate:
            max_increase_rate = increase_rate
            max_increase_country = country

    plt.title('Medals Change Rate between 1968 and 1980')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.grid(True)
    
    # Move the legend to the bottom, adjust its appearance, and arrange entries vertically
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), shadow=True, ncol=1, prop={'size': 7})

    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_fastest_increase = io.BytesIO()
    plt.savefig(img_fastest_increase, format='png')
    img_fastest_increase.seek(0)

    # Encode the plot to base64 string
    fastest_increase_chart_url = base64.b64encode(img_fastest_increase.getvalue()).decode()
    plt.close()

    return fastest_increase_chart_url, max_increase_country


# Generate the fastest increase graph and determine the country with the fastest increase when the application starts
global_chart_url_fastest_increase, country_fastest_increase = generate_fastest_increase_graph()

@app.route('/show_graph/q8')
def show_question_8():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'   # Question and answer choices
    question = 'Which country has the fastest increase in the number of medals between 1968 to 1980?'
    answer_choices = ['Russia', 'Germany', 'Great Britain', 'USA']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Which country has the fastest increase in the number of medals between 1968 to 1980?', fastest_increase_chart_url=global_chart_url_fastest_increase, country_fastest_increase=country_fastest_increase, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_russia_participation_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    years = df['year']
    russia_participation = df['RUSS']

    # Plot the graph for Russia's participation in the Olympics each year
    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    plt.plot(years, russia_participation, marker='o', color='green', linestyle='-', label='Russia')

    plt.title('Russia Participation in the Olympics Each Year')
    plt.xlabel('Year')
    plt.ylabel('Participation Status')
    plt.legend()
    plt.grid(True)
    plt.xticks(years, rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_russia_participation = io.BytesIO()
    plt.savefig(img_russia_participation, format='png')
    img_russia_participation.seek(0)

    # Encode the plot to base64 string
    russia_participation_chart_url = base64.b64encode(img_russia_participation.getvalue()).decode()
    plt.close()

    return russia_participation_chart_url

# Generate graph for Russia's participation when the application starts
global_chart_url_russia_participation = generate_russia_participation_graph()

@app.route('/show_graph/q9')
def show_question_9():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'
    # Question and answer choices
    question = 'From when to when did Russia not participate in the Olympics?'
    answer_choices = ['1980 to 1984 and 1988 to 1992', '1976 to 1980 and 1984 to 1988', '1972 to 1980 and 1984 to 1992', '1976 to 1980 and 1988 to 1996']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='From when to when did Russia not participate in the Olympics?',
                           russia_participation_chart_url=global_chart_url_russia_participation, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)


def generate_germany_most_medals_graph():
    # Load the data from the Excel file
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'
    df = pd.read_excel(file_path)

    years = df['year']

    plt.figure(figsize=(7, 5))  # Modify figure size as needed

    # Plotting the graph for Germany for every 4 years
    plt.plot(years[::4], df['Germany (GER) (Includes east and west along with unified)'][::4], marker='o', color='green', linestyle='-', label='Germany')

    plt.title('Medals Won by Germany Every 4 Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a temporary buffer
    img_germany = io.BytesIO()
    plt.savefig(img_germany, format='png')
    img_germany.seek(0)

    # Encode the plot to base64 string
    germany_chart_url = base64.b64encode(img_germany.getvalue()).decode()
    plt.close()

    return germany_chart_url

# Generate graph for Germany when the application starts
global_chart_url_germany = generate_germany_most_medals_graph()

@app.route('/show_graph/q10')
def show_question_10():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Which year did Germany win the medals the most?'
    answer_choices = ['1896', '1936', '1988', '1992']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Which year did Germany win the medals the most?', germany_chart_url=global_chart_url_germany, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_usa_gold_silver_graph():
    data = {
        'Year': [
            1896, 1900, 1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 
            1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020
        ],
        'Gold': [
            11, 19, 76, 23, 25, 0, 41, 45, 22, 41, 24, 0, 0, 38, 40, 32, 34, 36, 45, 33, 34, 0, 83, 36, 37, 44, 37, 36, 36, 48, 46, 39
        ],
        'Silver': [
            7, 14, 78, 12, 19, 0, 27, 27, 18, 32, 20, 0, 0, 27, 19, 25, 21, 26, 28, 31, 35, 0, 61, 41, 34, 32, 24, 39, 39, 26, 37, 41
        ],
        'Bronze': [
            2, 15, 77, 12, 19, 0, 27, 27, 16, 30, 12, 0, 0, 19, 17, 17, 16, 28, 34, 30, 25, 0, 30, 27, 37, 25, 32, 26, 37, 30, 38, 33
        ]
    }

    # Convert the updated dataset into a DataFrame and set 'Year' as the index
    df = pd.DataFrame(data)
    df.set_index('Year', inplace=True)

    # Define the colors for the medals
    colors = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze

    df.plot(kind='area', color=colors, figsize=(7, 5))

    # Set the title and labels
    plt.title('USA Summer Olympic Medals from 1896 to 2020')
    plt.xlabel('Year')
    plt.ylabel('Total number of Medals')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    plt.xticks(df.index)
    plt.legend(loc='upper left')
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_usa_s = io.BytesIO()
    plt.savefig(img_usa_s, format='png')
    img_usa_s.seek(0)

    # Encode the plot to base64 string
    usa_gold_silver_chart_url = base64.b64encode(img_usa_s.getvalue()).decode()
    plt.close()

    return usa_gold_silver_chart_url

@app.route('/show_graph/q11')
def show_question_11():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'  
    usa_gold_silver_chart_url = generate_usa_gold_silver_graph()
    question = 'In which year did the USA win the most gold and silver medals combined?'
    answer_choices = ['1984', '1904', '2020']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='In which year did the USA win the most gold and silver medals combined?', usa_gold_silver_chart_url=usa_gold_silver_chart_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)


def generate_russia_graph():
    data = {
    'Year': [
        1900, 1908, 1912, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020
    ],
    'Gold': [
        0, 1, 0, 22, 37, 43, 30, 29, 50, 49, 80, 55, 45, 26, 32, 28, 24, 18, 19, 20
    ],
    'Silver': [
        0, 2, 2, 30, 29, 29, 31, 32, 27, 41, 69, 31, 38, 21, 28, 26, 13, 21, 17, 28
    ],
    'Bronze': [
        0, 0, 3, 19, 32, 31, 35, 30, 22, 35, 46, 46, 29, 16, 29, 36, 23, 27, 20, 23
    ]
    }

    df = pd.DataFrame(data)
    df.set_index('Year', inplace=True)

    # Define the colors for the medals
    colors = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze

    df.plot(kind='area', color=colors, figsize=(7, 5))

    # Set the title and labels
    plt.title('Russia Summer Olympic Medals from 1896 to 2020')
    plt.xlabel('Year')
    plt.ylabel('Total number of Medals')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)


    plt.xticks(df.index)
    plt.legend(loc='upper left')
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_r_s = io.BytesIO()
    plt.savefig(img_r_s, format='png')
    img_r_s.seek(0)

    # Encode the plot to base64 string
    russia_graph_url = base64.b64encode(img_r_s.getvalue()).decode()
    plt.close()
    return russia_graph_url

@app.route('/show_graph/q12')
def show_question_12():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    
    russia_graph_url = generate_russia_graph()
    question = 'In which year has Russia been the most consistent in winning medals across all categories?'
    answer_choices = ['1980(Gold: 80, Silver: 69, Bronze: 46)', '1988(Gold: 55, Silver: 54, Bronze: 26)', '1996(Gold: 26, Silver: 21, Bronze: 28)']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='In which year has Russia been the most consistent in winning medals across all categories?', russia_graph_url=russia_graph_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_uk_graph():
    data = {
    'Year': [
        1896, 1900, 1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 
        1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020
    ],
    'Gold': [
        2, 15, 1, 56, 10, 0, 14, 9, 3, 4, 4, 0, 0, 3, 1, 6, 2, 4, 5, 4, 3, 5, 5, 5, 5, 1, 11, 9, 19, 29, 27, 22
    ],
    'Silver': [
        3, 8, 1, 51, 15, 0, 15, 13, 10, 7, 7, 0, 0, 14, 2, 7, 6, 12, 5, 5, 5, 7, 11, 10, 3, 8, 10, 9, 13, 18, 23, 20
    ],
    'Bronze': [
        2, 9, 0, 39, 16, 0, 13, 12, 7, 5, 3, 0, 0, 6, 8, 11, 12, 2, 3, 9, 5, 9, 21, 9, 12, 6, 7, 12, 19, 18, 27, 22
    ]
}

    df = pd.DataFrame(data)
    df.set_index('Year', inplace=True)

    colors = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze

    df.plot(kind='area', color=colors, figsize=(7, 5))

    plt.title('UK SUmmer Olympic Medals from 1896 to 2020')
    plt.xlabel('Year')
    plt.ylabel('Total number of Medals')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.xticks(df.index)
    plt.legend(loc='upper left')
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_uk_s = io.BytesIO()
    plt.savefig(img_uk_s, format='png')
    img_uk_s.seek(0)

    # Encode the plot to base64 string
    uk_graph_url = base64.b64encode(img_uk_s.getvalue()).decode()
    plt.close()
    return uk_graph_url

@app.route('/show_graph/q13')
def show_question_13():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'
    uk_graph_url = generate_uk_graph()
    question = 'Did the UK have a significant improvement in performance during a specific period?'
    answer_choices = ['No, the UKs performance remained consistent throughout the years.', 'Yes, the UKs performance improved significantly from 1976 to 1984.', 'Yes, the UK had a significant improvement in performance during the period from 2012 to 2020.']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Did the UK have a significant improvement in performance during a specific period?', uk_graph_url=uk_graph_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_germany_graph():
    data = {
        'Year': [
            1896, 1900, 1904, 1908, 1912, 1928, 1932, 1936, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020
        ],
        'Gold': [
            6, 4, 4, 3, 5, 10, 3, 33, 0, 6, 12, 10, 14, 33, 50, 47, 17, 48, 33, 20, 13, 13, 16, 11, 17, 10
        ],
        'Silver': [
            5, 3, 5, 5, 13, 7, 12, 26, 7, 13, 19, 22, 20, 34, 37, 37, 19, 49, 21, 18, 17, 16, 11, 20, 10, 11
        ],
        'Bronze': [
            2, 2, 6, 5, 7, 14, 5, 30, 17, 7, 11, 18, 33, 39, 42, 42, 23, 35, 28, 27, 26, 20, 14, 13, 15, 16
        ]
    }

    # Convert the updated dataset into a DataFrame and set 'Year' as the index
    df = pd.DataFrame(data)
    df.set_index('Year', inplace=True)

    # Define the colors for the medals
    colors = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze

    df.plot(kind='area', color=colors, figsize=(7, 5))

    # Set the title and labels
    plt.title('Germany Summer Olympic Medals from 1896 to 2020')
    plt.xlabel('Year')
    plt.ylabel('Total number of Medals')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    plt.xticks(df.index)
    plt.legend(loc='upper left')
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_g_s = io.BytesIO()
    plt.savefig(img_g_s, format='png')
    img_g_s.seek(0)

    # Encode the plot to base64 string
    germany_graph_url = base64.b64encode(img_g_s.getvalue()).decode()
    plt.close()
    return germany_graph_url

@app.route('/show_graph/q14')
def show_question_14():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    
    germany_graph_url = generate_germany_graph()
    question = 'Which Olympic Games saw the biggest decline in Germany’s medal count?'
    answer_choices = ['1952', '1984', '2008']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Which Olympic Games saw the biggest decline in Germany’s medal count?', germany_graph_url= germany_graph_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_china_graph():
    data = {
    'Year': [
        1932, 1936, 1948, 1952, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020
    ],
    'Gold': [
        0, 0, 0, 0, 15, 5, 16, 16, 28, 32, 48, 39, 26, 38
    ],
    'Silver': [
        0, 0, 0, 0, 8, 11, 22, 22, 16, 17, 22, 31, 18, 32
    ],
    'Bronze': [
        0, 0, 0, 0, 9, 12, 16, 12, 14, 14, 30, 22, 26, 19
    ]
    }

    # Convert the updated dataset into a DataFrame and set 'Year' as the index
    df = pd.DataFrame(data)
    df.set_index('Year', inplace=True)

    # Define the colors for the medals
    colors = ['#FFD700', '#C0C0C0', '#CD7F32']  # Gold, Silver, Bronze

    df.plot(kind='area', color=colors, figsize=(7, 5))

    # Set the title and labels
    plt.title('China Summer Olympic Medals from 1932 to 2020')
    plt.xlabel('Year')
    plt.ylabel('Total number of Medals')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    plt.xticks(df.index)
    plt.legend(loc='upper left')
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_c_s = io.BytesIO()
    plt.savefig(img_c_s, format='png')
    img_c_s.seek(0)

    # Encode the plot to base64 string
    china_graph_url = base64.b64encode(img_c_s.getvalue()).decode()
    plt.close()
    return china_graph_url

@app.route('/show_graph/q15')
def show_question_15():
    global current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    # Determine the next question based on current_question_index
    china_graph_url = generate_china_graph()
    question = 'How did China’s medal performance in the 2008 Olympic Games, when they were the host nation, compare to other years?'
    answer_choices = ['In 2008, China won 80.06% of the total medals it achieved from 1984 to 2020.', 'In 2008, China won 47.06% of the total medals it achieved from 1984 to 2020.', 'In 2008, Chinas medal success was at 47.06%, but the pattern was not uniform, as the victories were exclusively in the silver medal category.']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='How did China’s medal performance in the 2008 Olympic Games, when they were the host nation, compare to other years?', china_graph_url= china_graph_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

@app.route('/show_graph/q16')
def show_question_16():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Which country had the highest number of silver medals in the Summer Olympics from 1896 to 2020?'
    answer_choices = ['Russia', 'The United States', 'Great Britain', 'Germany']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Which country had the highest number of silver medals in the Summer Olympics from 1896 to 2020?', chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

@app.route('/show_graph/q17')
def show_question_17():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'How many silver medals did Germany win in total over the years?'
    answer_choices = ['415', '923', '305']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='How many silver medals did Germany win in total over the years?', chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

def generate_d_graph():
    file_path = 'Medals According to Years for top 10 countries (1896-2020).xlsx'

    # Read data starting from row 2 for both columns
    df = pd.read_excel(file_path, header=None, skiprows=1, names=['Year', 'Medals'], usecols=[0, 1])

    # Plotting the area chart
    plt.figure(figsize=(7, 5))
    df.plot(kind='area', x='Year', y='Medals', color=['gold', 'silver', 'brown'])

    # Title and labels
    plt.title('USA Medals Over the Years (1896-2020)')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.grid(True)
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_d_s = io.BytesIO()
    plt.savefig(img_d_s, format='png')
    img_d_s.seek(0)

    # Encode the plot to base64 string
    d_graph_url = base64.b64encode(img_d_s.getvalue()).decode()
    plt.close()
    return d_graph_url

@app.route('/show_graph/q18')
def show_question_18():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    # Question and answer choices
    question = 'Has China won at least 150 medals of each type (gold, silver, bronze) over the years?'
    answer_choices = ['Yes', 'No']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number='Has China won at least 150 medals of each type (gold, silver, bronze) over the years?', chart_url=global_chart_url, area_chart_url=global_chart_url1, question=question, answer_choices=answer_choices)

@app.route('/show_graph/q19')
def show_question_19():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    
    d_graph_url = generate_d_graph()  # Call the function to generate the graph
    question = 'Which year did the USA experience a significant increase in the number of medals, considering the gold, silver, and bronze categories combined?'
    answer_choices = ['1896', '1936','1968','2008']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number=question, d_graph_url=d_graph_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, answer_choices=answer_choices)

def generate_e_graph():
    data = {
        'Country': ['United States (USA)', 'Russia (RUS)', 'Germany (GER)', 'Great Britain (GBR)', 'China (CHN)'],
        'Gold': [1061, 608, 305, 296, 285],
        'Silver': [840, 515, 305, 323, 231],
        'Bronze': [738, 502, 312, 331, 197],
        'Total': [2639, 1625, 922, 950, 713]
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    df.set_index('Country', inplace=True)

    # Plotting the area chart
    plt.figure(figsize=(7, 5))
    df.T.plot(kind='area', stacked=True, colormap='jet', alpha=0.7)

    # Title and labels
    plt.title('Medals Distribution Over Countries (1896-2020)')
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend(title='Country', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    # Save the plot to a temporary buffer
    img_e_s = io.BytesIO()
    plt.savefig(img_e_s, format='png')
    img_e_s.seek(0)

    # Encode the plot to base64 string
    e_graph_url = base64.b64encode(img_e_s.getvalue()).decode()
    plt.close()
    return e_graph_url

@app.route('/show_graph/q20')
def show_question_20():
    global current_question_index
    # Determine the next question based on current_question_index
    next_question_route = question_routes[current_question_index + 1] if current_question_index + 1 < len(question_routes) else '/show_graph/testdone'    
    e_graph_url = generate_e_graph()  # Call the function to generate the graph
    question = 'Which country had the 3rd highest total number of medals (Gold, Silver, Bronze combined) in the Summer Olympics from 1896 to 2020?'
    answer_choices = ['United States (USA)', 'Russia (RUS)','Germany (GER)','Great Britain (GBR)']
    return render_template('show_graph.html',next_question_route=next_question_route, question_number=question, e_graph_url=e_graph_url, chart_url=global_chart_url, area_chart_url=global_chart_url1, answer_choices=answer_choices)

@app.route('/reset_test')
def reset_test():
    global user_answers, total_response_time, unasked_questions

    # Reset user answers and total response time
    user_answers = {}
    total_response_time = 0

    # Reset the unasked questions list
    unasked_questions = list(range(len(question_routes)))

    # Optionally shuffle the question routes again
    random.shuffle(question_routes)

    # Redirect to the start of the quiz
    return redirect('/')

# Update the testdone route to include a link to reset the test
@app.route('/show_graph/testdone')
def testdone():
    total_score = 0
    for question_number, answers in user_answers.items():
        if correct_answers.get(question_number) == answers[0]['answer']:
            total_score += 1

    return render_template('testdone.html', user_answers=user_answers, 
                           correct_answers=correct_answers, 
                           total_score=total_score,
                           total_response_time=total_response_time,
                           reset_link="/reset_test")  # Add a link to reset the test


correct_answers = {
    1: '1904',
    2: 'Russia',
    3: 'Russia',
    4: 'Sweden',
    5: 'Great Britain',
    6: '2016',
    7: '1980',
    8: 'Russia',
    9: '1980 to 1984 and 1988 to 1992',
    10: '1936',
    11: '1904',
    12: '1980 (Gold: 80, Silver: 69, Bronze: 46)',
    13: 'Yes, the UK had a significant improvement in performance during the period from 2012 to 2020.',
    14: '1984',
    15: 'In 2008, China won 47.06% of the total medals it achieved from 1984 to 2020.',
    16: 'The United States',
    17: '305',
    18: 'Yes',
    19: '1936',
    20: 'Germany (GER)'
}

if __name__ == '__main__':
    app.run(debug=True)
