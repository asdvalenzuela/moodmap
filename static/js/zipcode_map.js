$(document).ready(function () {

    L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map', 'asdv.ka97lo0j', {zoomControl: false, scrollWheelZoom: false});

    new L.Control.Zoom({ position: 'topright' }).addTo(map);

    var removeMarkers = function() {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });
    };

    $("#zipcode-button").click(function(e) {
        removeMarkers();
        markerLayer = new L.FeatureGroup();
        markerLayer.addTo(map);
        var zipcode = $("#zipcode").val();
        var re = /^[0-9]*$/;
        //checks that zipcode is 5 numbers
        if (zipcode.length !== 5 || !re.test(zipcode)) {
            alert("Error: Input must be five numbers.");
            return false;
        }
        else {
            //gets and sets tweets from that zipcode
            $.get("/get_tweets_by_zipcode", {zipcode: zipcode}, function(data) {
                for (i = 0; i < data.length; i++) {
                    newMarker = setMarker(data[i]);
                    markerLayer.addLayer(newMarker);
                }
                newMarker.openPopup();
                map.fitBounds(markerLayer.getBounds());
            });
        }
    });

});