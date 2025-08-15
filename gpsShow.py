from flask import Flask, render_template_string, jsonify
from gps3 import gps3
import threading

gps_data = {"lat": 0, "lon": 0}

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time GPS Tracker</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="width: 100%; height: 100vh;"></div>
    <script>
        var map = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
        }).addTo(map);
        var marker = L.marker([0, 0]).addTo(map);

        async function updateGPS() {
            const res = await fetch('/gps');
            const data = await res.json();
            marker.setLatLng([data.lat, data.lon]);
            map.setView([data.lat, data.lon], 18);
        }

        setInterval(updateGPS, 2000);
    </script>
</body>
</html>
"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/gps')
def gps_endpoint():
    return jsonify(gps_data)

def read_gps():
    global gps_data
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            if data_stream.TPV['lat'] != 'n/a' and data_stream.TPV['lon'] != 'n/a':
                gps_data["lat"] = data_stream.TPV['lat']
                gps_data["lon"] = data_stream.TPV['lon']

if __name__ == "__main__":
    threading.Thread(target=read_gps, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
