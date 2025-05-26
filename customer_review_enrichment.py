import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER Lexicon for sentiment analysis 
nltk.download('vader_lexicon')


# define a fun to fetch data from a sql database using a sql query 
def fetch_data_from_sql():
    conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-M1VM1S2\\SQLEXPRESS;"
    "DATABASE=PortfolioProject_MarketingAnalytics;"
    "Trusted_Connection=yes;"
)

    conn = pyodbc.connect(conn_str)

    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText from dbo.customer_reviews"

    df = pd.read_sql(query,conn)

    conn.close()

    return df

# fetch the customer review data from sql database 
customer_reviews_df = fetch_data_from_sql()

# Intialize the VADER sentiment intensity analyzer for analysing the sentiment of text data
sia = SentimentIntensityAnalyzer()

# fuction to calculate sentiment score 
def calculate_sentiment(review):
    sentiment = sia.polarity_scores(review)
    # return the compound score, which is a normalised score between -1 and 1
    return sentiment['compound']

# function to categorize sentiment using both the sectiment score and the rating
def categorize_sentiment(score, rating):
    if score > 0.05:
        if rating >=4:
            return 'Positive'
        elif rating ==3:
            return 'Mixed Positive'
        else:
            return 'Mixed Negative'
        
    elif score< -0.05:
        if rating <= 2:
            return 'Negative'
        elif rating ==3:
            return 'Mixed Negative'
        else:
            return 'Mixed Positive'
    
    else:
        if rating >=4:
            return 'Positive'
        if rating <=2:
            return 'Negative'

# function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'
    else:
        return '-1.0 to -0.5'


customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis =1
)

customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

print(customer_reviews_df.head())

customer_reviews_df.to_csv('fact_customer-reviews_with_sentiment.csv', index=False)
