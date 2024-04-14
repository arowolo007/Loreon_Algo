import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
import ssl
# from forex_python.converter import CurrencyRates
import yfinance as yf
import time

# Function to send email notification
def send_email(subject, body):
    sender_email = "loreon.damilola@gmail.com"
    receiver_email = ["arowolodamilola5@gmail.com", "loreon.bimbola@gmail.com", "loreon.ilerioluwa@gmail.com "]

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()




def calculate_sma_support_resistance(data, sma_period=50):
    # Calculate Simple Moving Average (SMA)
    data['SMA'] = data['Close'].rolling(window=sma_period).mean()

    # Calculate Support and Resistance Levels
    data['Support'] = data['Low'].rolling(window=sma_period).min()
    data['Resistance'] = data['High'].rolling(window=sma_period).max()

    return data

# Function to check for buy/sell opportunity
def check_trade(currency_pair, sma_period):
    
    asset = yf.Ticker(currency_pair)
    # get all stock info
    current_rate = asset.info['ask']
    
    # Calculate SMA
    historical_rates = yf.download('EURUSD=X', interval='1h', start='2024-3-20')

    refined_data = calculate_sma_support_resistance(historical_rates, sma_period)

    sma = refined_data['SMA'][-1]
    resistance_level = refined_data['Resistance'][-1]
    support_level = refined_data['Support'][-1]

    print(f'Current_rate : {current_rate}, SMA : {sma}, Resistance_level : {resistance_level}, Support_level : {support_level} ')

    # Check for buy/sell opportunity
    if current_rate > resistance_level and current_rate > sma:
        send_email(f"Loreon Forex Trade Buy Alert : {currency_pair} ", f"Opportunity to buy {currency_pair} at {current_rate}\n\n\nAdditional Info : Current_rate : {current_rate}, SMA : {sma}, Resistance_level : {resistance_level}, Support_level : {support_level} ")
    elif current_rate < support_level and current_rate < sma:
        send_email(f"Loreon Forex Trade Sell Alert : {currency_pair} ", f"Opportunity to sell {currency_pair} at {current_rate}\n\n\nAdditional Info : Current_rate : {current_rate}, SMA : {sma}, Resistance_level : {resistance_level}, Support_level : {support_level} ")
    else:
        send_email(f"Loreon Forex No Trade Alert : {currency_pair} ", f"No Opportunity for action {currency_pair} at {current_rate}\n\n\nAdditional Info : Current_rate : {current_rate}, SMA : {sma}, Resistance_level : {resistance_level}, Support_level : {support_level} ")
    print('mail sent')
# Main function to monitor trades
def main():
    currency_pairs = ["EURUSD=X", "GBPUSD=X","AUDUSD=X"]  # Currency pairs to monitor
    sma_period = 24  # Period for SMA calculation (in hours)

    
    while True:
        for pair in currency_pairs:
            check_trade(pair, sma_period)
        time.sleep(300)  # Check every hour

if __name__ == "__main__":
    main()
