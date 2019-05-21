from datetime import datetime, time

today = datetime.today()
tim = time(hour=today.hour, minute=today.minute+1)
print(tim)