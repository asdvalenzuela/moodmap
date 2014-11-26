$(document).ready(function () {

    L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map', 'asdv.ka97lo0j', {zoomControl: false, scrollWheelZoom: false});

    new L.Control.Zoom({ position: 'topright' }).addTo(map);

    var layerlist = [];
    var newmarker = 'x';
    var data = [];

    $("#zipcode-button").click(function(e) {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });
        marker_layer = new L.FeatureGroup();
        marker_layer.addTo(map);
        var zipcode = $("#zipcode").val();
        if (zipcode.length !== 5) {
            alert("Error: Input must be five numbers.");
            return false;
        }
        var re = /^[0-9]*$/;
        if (!re.test(zipcode)) {
            alert("Error: Input must be five numbers.");
            return false;
        }
        else {
            $.get("/get_tweets_by_zipcode", {zipcode: zipcode}, function(data) {
                for (i = 0; i < data.length; i++) {
                    if (data[i]['score'] == '4') {
                        setMarker(data[i], happyIcon, "Happy Tweet");
                    }
                    if (data[i]['score'] == '0') {
                        setMarker(data[i], sadIcon, "Sad Tweet");
                    }
                    marker_layer.addLayer(newmarker);
                }
                newmarker.openPopup();
                map.fitBounds(marker_layer.getBounds());
            });
        }
    });

    var sadIcon = L.icon({
        iconUrl: '../static/img/sad.png',
        iconSize: [16, 24],
        iconAnchor: [8, 12],
        popupAnchor: [0, -20]
    });

    var happyIcon = L.icon({

        iconUrl: '../static/img/happy.png',
        iconSize: [16, 24],
        iconAnchor: [8, 12],
        popupAnchor: [0, -20]
    });

    var setMarker = function(tweet, icon_type, sentiment) {
        var popup_type = null;
        if (icon_type == happyIcon) {
            popup_type = "<div class=\"happy-popup\"</div><b>" + sentiment + " from</b><figure style=\"margin-left: 0px\"><img src=" + tweet['profile_img'] +" height=30 width=30/><figcaption>@" + tweet['screen_name'] + "</figcaption></figure><br>" + tweet['text'];
        }
        if (icon_type == sadIcon) {
            popup_type = "<div class=\"sad-popup\"</div><b>" + sentiment + " from</b><figure style=\"margin-left: 0px\"><img src=" + tweet['profile_img'] +" height=30 width=30/><figcaption>@" + tweet['screen_name'] +  "</figcaption></figure><br>" + tweet['text'];
        }
        newmarker = L.marker([tweet['loc'][1], tweet['loc'][0]],
            { icon: icon_type, title: tweet['score']+  tweet['id_str']}
        )
        .bindPopup(popup_type);
    };

});