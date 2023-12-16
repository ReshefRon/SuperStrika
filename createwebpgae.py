from flask import Flask, render_template, request, jsonify
import pandas as pd
import getgraph

app = Flask(__name__)

df_1 = pd.read_csv('DATA/SuperStrika.csv')
df_2 = pd.read_csv('DATA/SuperStrikaByYears.csv')

@app.route('/')
def index():
    teams = list(df_1['Name'].unique())  # List of teams from your DataFrame
    return render_template('index.html',teams=teams)

@app.route('/get_graph', methods=['POST'])
def get_graph():
    selected_team = request.json['team']
    graph_data = getgraph.create_scatter_for_team(selected_team, df_1, df_2)
    return graph_data.getvalue(), 200, {'Content-Type': 'image/png'}


if __name__ == '__main__':
    app.run(debug=True)