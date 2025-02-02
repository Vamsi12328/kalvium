# -*- coding: utf-8 -*-
"""kalvium.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Oe8w65UHPNefrhzmcnRV1DSD4yvKi9_r
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"

def fetch_results(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def extract_data(soup):
    data = []
    table = soup.find("table")
    if not table:
        raise ValueError("Could not find the results table on the page.")

    rows = table.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 4:
            cols = [col.text.strip() for col in cols]
            data.append(cols[:4])

    return data

def save_to_csv(data, filename="election_results.csv"):
    df = pd.DataFrame(data, columns=["Party", "Won", "Leading", "Total"])
    df.to_csv(filename, index=False)

def main():
    soup = fetch_results(url)
    data = extract_data(soup)
    save_to_csv(data)
    print("Result data saved to election_results.csv")

if __name__ == "__main__":
    main()

import pandas as pd
filename = "election_results.csv"
data = pd.read_csv(filename)

data['Won'] = pd.to_numeric(data['Won'], errors='coerce')
data['Leading'] = pd.to_numeric(data['Leading'], errors='coerce')
data['Total'] = pd.to_numeric(data['Total'], errors='coerce')

total_seats_won = data.groupby('Party')['Won'].sum().reset_index().sort_values(by='Won', ascending=False)
data['Percentage of Total Seats'] = (data['Won'] / data['Won'].sum()) * 100

print("\nParty with the highest number of seats won:")
print(total_seats_won.iloc[0:1])

print("\nTotal number of seats won by the top 5 parties:")
print(total_seats_won.head(5))

print("\nParty with the highest percentage of seats won:")
print(data.loc[data['Percentage of Total Seats'].idxmax()][['Party', 'Percentage of Total Seats']])

print("\nParties with at least 5 seats:")
print(data[data['Won'] >= 5][['Party', 'Won']])

print("\nNumber of parties that won seats:")
print(data['Party'].nunique())

print("\nTotal number of seats contested:")
print(data['Total'].sum())

print("\nDistribution of seats among the top 3 parties:")
print(total_seats_won.head(3))

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("election_results.csv")

df["Winning_Margin"] = df["Won"] - df["Leading"]

top_winners = df.nlargest(10, "Winning_Margin")
plt.bar(top_winners["Party"], top_winners["Winning_Margin"])
plt.xlabel("Party")
plt.ylabel("Winning Margin")
plt.title("Top 10 Winning Margins")
plt.xticks(rotation=45)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("election_results.csv")
total_votes = df["Won"].sum()
df["Vote_Share_Percentage"] = (df["Won"] / total_votes) * 100

top_n_parties = 7

df_sorted = df.sort_values(by="Vote_Share_Percentage", ascending=False)

major_parties = df_sorted.head(top_n_parties)

minor_parties = df_sorted.iloc[top_n_parties:]
other_vote_share = minor_parties["Vote_Share_Percentage"].sum()

other_row = pd.DataFrame([["Other", other_vote_share]], columns=["Party", "Vote_Share_Percentage"])
major_parties = pd.concat([major_parties, other_row], ignore_index=True)

plt.figure(figsize=(10, 8))
plt.pie(major_parties["Vote_Share_Percentage"], labels=major_parties["Party"], autopct="%1.1f%%", startangle=140)
plt.title("Vote Share Distribution")
plt.axis("equal")
plt.show()

import matplotlib.pyplot as plt
years = [2014, 2019, 2024]
nda_seats = [336, 303, 293]
india_seats = [44, 52, 235]

plt.plot(years, nda_seats, marker='o', label='NDA')
plt.plot(years, india_seats, marker='s', label='INDIA')

plt.xlabel('Election Year')
plt.ylabel('Number of Seats')
plt.title('Alliance-wise Seat Trends Over Multiple Elections')
plt.legend()

plt.grid(True)
plt.show()