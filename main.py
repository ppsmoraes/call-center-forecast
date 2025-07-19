import pandas as pd
import matplotlib.pyplot as plt

df: pd.DataFrame = pd.read_excel('data/01 Call-Center-Dataset.xlsx')

df_dayly: pd.DataFrame = df[['Call Id', 'Date']].groupby('Date').count()

print(df_dayly)

# plt.figure(figsize=(12, 6))
# plt.plot(df_dayly.index, df_dayly['Call Id'])
# plt.xlabel('Data')
# plt.ylabel('Quantidade de Chamadas')
# plt.title('Chamadas por Dia')
# plt.xticks(rotation=45)
# plt.show()