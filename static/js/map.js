$(document).ready(function () {
  L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map-one', 'asdv.k6h5h7cf', {scrollWheelZoom: false}).setView([37.7516, -122.4477], 9);

    markerlist = [];
    layerlist = [];

    // gets tweet list from database via AJAX, checks for new tweets and displays only new tweets
    var markers = function() {
        console.log("markers");
        $.get("/coordinates", function(data) {
            console.log(data);
            newlist = [];
            for (i = 0; i < data.length; i++) {
                var id_str = data[i]['id_str'];
                var in_list = markerlist.indexOf(id_str);
                if (in_list == -1) {
                    if (data[i]['score'] == '4') {
                        newmarker = L.marker([data[i]['lat_'], data[i]['long_']], {
                        icon: L.mapbox.marker.icon({
                            'marker-size': 'small',
                            'marker-color': '#FCB514'
                        })
                        })
                        .bindPopup(data[i]['text']);
                        markerlist.push(id_str);
                        newlist.push(newmarker);
                    }
                    if (data[i]['score'] == '0') {
                        newmarker = L.marker([data[i]['lat_'], data[i]['long_']], {
                        icon: L.mapbox.marker.icon({
                            'marker-size': 'small',
                            'marker-color': '#5F9F9F'
                        })
                        })
                        .bindPopup(data[i]['text']);
                        markerlist.push(id_str);
                        newlist.push(newmarker);
                    }
            }}
            marker_layer = L.layerGroup(newlist);
            layerlist.push(marker_layer);
            if (layerlist.length > 10) {
                map.removeLayer(layerlist[0]);
                console.log("removed");
            }
            marker_layer.addTo(map);
          });
    };

    // $("body").on("click", function() {
    //     map.eachLayer(function(layer) {
    //         if (layer instanceof L.Marker) {
    //             map.removeLayer(layer);
    //         }
    //     });
    // });

    // makes AJAX call every 3 seconds to display new tweets
    setInterval(function () {
        markers();
        // marker_layer = L.layerGroup(newlist)
        // marker_layer.clearLayers()
        }, 3000);
});

    