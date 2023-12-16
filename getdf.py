##########################
# Import necessary modules#
##########################

import pandas as pd
from bs4 import BeautifulSoup
import requests

########################
##Initially parameters##
########################

base_url_league = 'https://www.transfermarkt.com/ligat-haal/tabelle/wettbewerb/ISR1/saison_id/'
user_agent = {'User-agent': 'Mozilla/5.0'}

##########################
# Define dataframe columns#
##########################

base_df_struct = pd.DataFrame(
    columns=['Name', 'Year', 'Ranking', 'Total Goals Scored', 'Strikers Goals Scored', 'FW/Total goals', 'Team Code',
             'Name for URL'])
strikers_df_struct = pd.DataFrame(columns=['Name', 'Year', 'Player', 'Strikers Goals Scored'])

team_codes = pd.read_csv('DATA/TeamCodes.csv')


def create_base_df(df):
    for year in range(2007, 2022):
        current_url = f"{base_url_league}{year}"
        response = requests.get(current_url, headers=user_agent)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("div", attrs={"id": "yw1", "class": "grid-view"})
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            data = []
            for i, column in enumerate(columns, start=1):
                text = column.text.strip()
                if i % 10 == 1:
                    data.append(('Ranking', text))
                elif i % 10 == 3:
                    data.append(('Name', text))
                    url = column.find("a").get('href')
                    '''
                    ###To create TeamCodes.csv###
                    data.append(('Name for URL', url.split('/')[1]))
                    data.append(('Team Code', url.split('/')[-3]))
                    '''

                    ###After TeamCodes.csv exists###
                    name_for_url = team_codes.loc[team_codes['Name'] == text, 'Name for URL'].values[0]
                    data.append(('Name for URL', name_for_url))
                    team_code = team_codes.loc[team_codes['Name'] == text, 'Team Code'].values[0]
                    data.append(('Team Code', team_code))

                elif i % 10 == 8:
                    parts = text.split(':')
                    data.append(('Total Goals Scored', int(parts[0])))
                last_2_digits = str(year)[-2:]
                next_last_two_digits = int(last_2_digits) + 1
                if next_last_two_digits < 10:
                    final_year = str(year) + '/0' + str(next_last_two_digits)
                else:
                    final_year = str(year) + '/' + str(next_last_two_digits)
                data.append(('Year', final_year))

            new_df = pd.DataFrame([dict(data)], columns=df.columns)
            df = pd.concat([df, new_df], ignore_index=True)
    df = df.dropna(subset=['Name'])
    df.reset_index(drop=True, inplace=True)
    df = df.sort_values(by=['Name', 'Year'])
    df.to_csv('DATA/SuperStrika.csv', index=False)


def create_strikers_df(team_codes, super_strika):
    for index, row in team_codes.iterrows():
        current_url = 'https://www.transfermarkt.com/' + row['Name for URL'] + '/toptorschuetzensaison/verein/' + str(
            row['Team Code']) + '/plus/0?wettbewerb_id=ISR1&pos=Sturm'
        response = requests.get(current_url, headers=user_agent)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("div", attrs={"id": "yw1", "class": "grid-view"})
        for r in table.find_all('tr'):
            columns = r.find_all('td', class_=['extrarow bg_grey hauptlink img-vat', 'zentriert hauptlink'])
            for column in columns:
                if len(column['class']) == 4:
                    current_year = column.text[-5:]
                else:
                    matching_row = super_strika[
                        (super_strika['Name'] == row['Name']) & (super_strika['Year'] == "20" + current_year)]
                    if not matching_row.empty:
                        if pd.isna(matching_row['Strikers Goals Scored']).any():
                            super_strika.loc[matching_row.index, 'Strikers Goals Scored'] = int(column.text)
                        else:
                            super_strika.loc[matching_row.index, 'Strikers Goals Scored'] += int(column.text)
    super_strika['Strikers Goals Scored'] = super_strika['Strikers Goals Scored'].astype('int')
    super_strika['FW/Total goals'] = (super_strika['Strikers Goals Scored'] / super_strika['Total Goals Scored']).round(
        2)
    super_strika.to_csv('DATA/SuperStrika.csv', index=False)


def create_average_for_year_df():
    df = pd.read_csv('DATA/SuperStrika.csv')
    df_new = df.groupby('Year')['Total Goals Scored', 'Strikers Goals Scored'].sum()
    df_new['FW/Total goals'] = (df_new['Strikers Goals Scored'] / df_new['Total Goals Scored']).round(2)
    df_new.to_csv('DATA/SuperStrikaByYears.csv')


def add_missing_years():
    df = pd.read_csv('DATA/SuperStrika.csv')
    teams = df['Name'].unique()
    years = df['Year'].unique()
    missing_data = []
    for team in teams:
        for year in years:
            if not ((df['Name'] == team) & (df['Year'] == year)).any():
                missing_data.append({'Name': team, 'Year': year, 'Ranking': None, 'Total Goals Scored': None,
                                     'Strikers Goals Scored': None, 'FW/Total goals': None, 'Team Code': None,
                                     'Name for URL': None})
    missing_df = pd.DataFrame(missing_data)

    result_df = pd.concat([df, missing_df], ignore_index=True, sort=False)
    result_df = result_df.sort_values(by=['Name', 'Year'])
    result_df.to_csv('DATA/SuperStrika.csv', index=False)



def main():
    create_base_df(base_df_struct)
    super_strika = pd.read_csv('DATA/SuperStrika.csv')
    create_strikers_df(team_codes,super_strika)
    create_average_for_year_df()
    add_missing_years()

main()