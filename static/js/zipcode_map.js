var happyIcon = L.icon({
    iconUrl: '../static/img/happy.png',
    iconSize: [16, 24],
    iconAnchor: [8, 12],
    popupAnchor: [0, -20]
});

var sadIcon = L.icon({
    iconUrl: '../static/img/sad.png',
    iconSize: [16, 24],
    iconAnchor: [8, 12],
    popupAnchor: [0, -20]
});

var setMarker = function(tweet) {
    if (tweet['score'] === '4') {
        iconType = happyIcon;
        popupType = "<div class=\"happy-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] + "<br></figcaption></figure></div>";
    }
    if (tweet['score'] === '0') {
        iconType = sadIcon;
        popupType = "<div class=\"sad-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] +  "<br></figcaption></figure></div>";
    }
    newMarker = L.marker([tweet['loc'][1], tweet['loc'][0]],
        { icon: iconType, title: tweet['score'] + tweet['id_str']}
    )
    .bindPopup(popupType);
    return newMarker;
};

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
        var re = /^\d{5}$/;
        //checks that zipcode is 5 numbers
        if (!re.test(zipcode)) {
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