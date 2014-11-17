$(document).ready(function () {

    L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map-one', 'asdv.k6h5h7cf', {scrollWheelZoom: false}).setView([37.66, -121.57], 9);

    var pusher = new Pusher('998f83412af68dd3edb3');
    var channel = pusher.subscribe('tweet_map');

    var marker_layer = new L.FeatureGroup();
    marker_layer.addTo(map);

    var layerlist = [];
    var newmarker = 'x';

    $.get("/coordinates", function(data) {
        for (i = 0; i < data.length; i++) {
            console.log(data[i]);
        if (data[i]['score'] == '4') {
            setMarker(data[i], '#FCB514');
        }
        if (data[i]['score'] == '0') {
            setMarker(data[i], '#5F9F9F');
        }
        marker_layer.addLayer(newmarker);
    }});

    marker_layer.on('layeradd', function(e) {
        map.panTo(e.layer.getLatLng());
    });

    // marker_layer.on('click', function(e) {
    //     map.panTo(e.layer.getLatLng());
    // });

    // $( "#slider-range" ).slider({
    //   orientation: "vertical",
    //   range: true,
    //   values: [ 17, 67 ],
    //   slide: function( event, ui ) {
    //     console.log("slide!");
    //     console.log(ui);
    //   }
    // });

    $(function() {
    $( "#slider-range" ).slider({
      orientation: "vertical",
      range: true,
      max: 24,
      values: [ 8, 16 ],
      slide: function( event, ui ) {
        $( "#amount" ).val(ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      }
    });

    $( "#amount" ).val($( "#slider-range" ).slider( "values", 0 ) +
      " - " + $( "#slider-range" ).slider( "values", 1 ) );
    });

    $(function() {
    $( "#selectable" ).selectable();
    });

    var setMarker = function(tweet, color) {
        newmarker = L.marker([tweet['loc'][1], tweet['loc'][0]], {
            icon: L.mapbox.marker.icon({
                'title': tweet['text'],
                'marker-size': 'small',
                'marker-color': color
        })
        })
        .bindPopup(tweet['text']);
    };

    channel.bind('new_tweet', function(tweet) {
        if (tweet['score'] == '4') {
            setMarker(tweet, '#F7E699');
        }
        if (tweet['score'] == '0') {
            setMarker(tweet, '#BDE0F2');
        }
        marker_layer.addLayer(newmarker);
        newmarker.openPopup();
        // layerlist.push(marker_layer);
        // if (layerlist.length > 50) {
        //     map.removeLayer(layerlist[0]);
        //     console.log("removed");
        // }
    });

    // $("body").on("click", function() {
    //     map.eachLayer(function(layer) {
    //         if (layer instanceof L.Marker) {
    //             map.removeLayer(layer);
    //         }
    //     });
    // });

});
