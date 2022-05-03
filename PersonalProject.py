# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import smtplib
import imghdr
from email.message import EmailMessage

import time
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pd

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

msg=EmailMessage()

yf.pdr_override() 
start=dt.datetime(2022,5,03)
now=dt.datetime.now()

stock="TGT"
TargetPrice=280

msg['Subject'] = 'Alert on '+ stock
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'rczamora@uark.edu'

alerted=False
While 1:
	df = pdr.get_data_yahoo(stock, start, now)
	currentClose=df["Adj Close"][-1]
    
	condition=currentClose>TargetPrice
    
	if(condition and alerted==False):
		alerted=True
        message=stock +" Has activated the alert price of "+ str(TargetPrice) +\
		 "\nCurrent Price: "+ str(currentClose)

		print(message)
  
		msg.set_content(message)

		files=[r"C:\\\\uem.walton.uark.edu\\UEMProfiles_Lab$\\rczamora\\RedirectedFolders\\Documents\\Finn510\\FundamentalList.xlsx"]

		for file in files:
			with open(file,'rb') as f:
				file_data=f.read()
				file_name="FundamentalList.xlsx"

				msg.add_attachment(file_data, maintype="application",
					subtype='ocetet-stream', filename=file_name)

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
		    smtp.send_message(msg)

		    print("completed")
	else:
		print("No new alerts")
     
	time.sleep(60)
    
    
    
    df = yf.Ticker("TGT-USD").history(period="max").reset_index()[["Open"]]


df.shape

dataset_train = np.array(df[:int(df.shape[0]*0.8)])
dataset_test = np.array(df[int(df.shape[0]*0.8):])
print(dataset_train.shape)
print(dataset_test.shape)

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

scaler = MinMaxScaler(feature_range=(0,1))
dataset_train = scaler.fit_transform(dataset_train)
dataset_train[:5]

dataset_test = scaler.transform(dataset_test)
dataset_test[:5]

def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x,y 

x_train, y_train = create_dataset(dataset_train)
x_test, y_test = create_dataset(dataset_test)

model = Sequential()
model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96))
model.add(Dropout(0.2))
model.add(Dense(units=1))

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(x_train, y_train, epochs=50, batch_size=32)
model.save('stock_prediction.h5')

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))

fig, ax = plt.subplots(figsize=(16,8))
ax.set_facecolor('white')
ax.plot(y_test_scaled, color='red', label='Original price')
plt.plot(predictions, color='cyan', label='Predicted price')
plt.legend()
