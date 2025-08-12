from datetime import datetime

from erlang import CallCenterPredictions

pred = CallCenterPredictions(
    start_time=datetime(2021, 4, 1, 8),  # Emulating a one hour period
    end_time=datetime(2021, 4, 1, 9),
    calls=200,
    average_handling_time=300,  # In seconds
    target_service_level=0.8,
    target_answer_time=20,
)

agents = pred.raw_agents
print('List with estimated metrics using the agents required (before shinkrage).')
print(f'Agents required (before shinkrage): {agents}')
print(f'Service Level: {100*pred.service_level(agents):.1f}%')
print(f'Average Speed of Snswer: {pred.average_speed_of_answer():.0f}s')
print(f'Occupancy: {100*pred.occupancy():.1f}%')
