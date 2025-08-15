import gps

# Connect to gpsd
session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

try:
    while True:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                print(f"Latitude: {report.lat}, Longitude: {report.lon}")
except KeyboardInterrupt:
    print("Stopped")
