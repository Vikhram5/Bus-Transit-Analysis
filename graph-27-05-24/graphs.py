import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('04-02-19.csv')
#df=pd.read_csv('analysis-up.csv')

bus_no=int(input("Enter Bus Number: "))
df = df[df['Schedule Name'].str.contains(rf'\b{bus_no}\b')]

cols =['Schedule Name','Ticket Issued Time','Adult','From Stage','To Stage','Source','Destination']
df = df[cols]
df =df[(df['Source']=='T.NAGAR') & (df['Destination']=='THIRUPORUR')]


# from_stages=df['From Stage'].unique()
# to_stages=df['To Stage'].unique()
# print("The list of from stages are: ")
# print(from_stages)
# print("")
# print("The list of to stages are: ")
# print(to_stages)


from_stage=input("Enter From Stage: ").upper()
to_stage=input("Enter To Stage: ").upper()

df=df[(df['From Stage']==from_stage) & (df['To Stage']==to_stage)]
df['Ticket Issued Time'] = pd.to_datetime(df['Ticket Issued Time'], format='%H:%M:%S', errors='coerce')

df['Hour']=df['Ticket Issued Time'].dt.hour

df= df.groupby('Hour')['Schedule Name'].count().reset_index()
df.columns = ['Hour', 'Bus Count']

#All hours
hours= pd.DataFrame({'Hour': range(24)})
df=hours.merge(df, on='Hour', how='left').fillna(0)

df['Bus Count'] = df['Bus Count'].astype(int)
df['Cumulative Boarding'] = df['Bus Count'].cumsum()
df['10 Mins Headway']=(df['Cumulative Boarding']/6).round(1)
df['20 Mins Headway']=(df['Cumulative Boarding']/3).round(1)

#store in excel file
file_name=input("Enter File name to store: ")
df.to_excel(f"{file_name}.xlsx")

plt.figure(figsize=(10, 6))
plt.plot(df['Hour'], df['Cumulative Boarding'], linestyle='-', color='b', linewidth=2)
plt.title(f"{from_stage} - {to_stage}",fontsize=16)
plt.xlabel('Hour', fontsize=14)
plt.ylabel('Passenger Count', fontsize=14)
plt.xticks(range(24), fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
