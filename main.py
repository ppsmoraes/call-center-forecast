import matplotlib.pyplot as plt  # type: ignore[import-not-found]
from pandas import DataFrame, read_excel, to_datetime

df: DataFrame = read_excel('data/01 Call-Center-Dataset.xlsx')

dayly: DataFrame = df[['Call Id', 'Date']].groupby('Date').count()
dayly.rename(columns={'Call Id': 'Calls'}, inplace=True)
dayly.index = to_datetime(dayly.index)
dayly['Day Name'] = dayly.index.day_name()
dayly['Week'] = dayly.index.isocalendar().week

day_names: list[str] = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
]

plt.figure(figsize=(10, 6))
plt.boxplot(
    [dayly[dayly['Day Name'] == day]['Calls'] for day in day_names],
    tick_labels=day_names,
)
plt.xlabel('Dias da Semana')
plt.ylabel('Ligações Recebidas')
plt.title('Distribuição de Ligações por Dia da Semana')
plt.xticks(rotation=45)
plt.show()

# plt.plot(dayly.index, dayly['Calls'])
# plt.xlabel('Data')
# plt.ylabel('Quantidade de Chamadas')
# plt.title('Chamadas por Dia')
# plt.xticks(dayly.index[::8])
# plt.show()
