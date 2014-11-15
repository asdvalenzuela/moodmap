$(document).ready(function () {

    $( "#slider-range" ).slider({
      orientation: "vertical",
      range: true,
      values: [ 17, 67 ],
      slide: function( event, ui ) {
        console.log("slide!");
        console.log(ui);
      }
    });

    L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map-one', 'asdv.k6h5h7cf', {scrollWheelZoom: false}).setView([37.7516, -122.4477], 9);

    var pusher = new Pusher('998f83412af68dd3edb3');
    var channel = pusher.subscribe('tweet_map');

    var layerlist = [];

    // gets tweet list from database via AJAX, checks for new tweets and displays only new tweets
    // var markers = function() {
    //     console.log("markers");
    //     $.get("/coordinates", function(data) {
    //         console.log(data);
    //         var newmarker = [];
    //         var tweet = data;
    //         if (tweet['score'] == '4') {
    //             newmarker.push(L.marker([tweet['lat_'], tweet['long_']], {
    //             icon: L.mapbox.marker.icon({
    //                 'marker-size': 'small',
    //                 'marker-color': '#FCB514'
    //             })
    //             })
    //             .bindPopup(tweet['text']));
    //             console.log("positive tweet");
    //             }
    //         if (tweet['score'] == '0') {
    //             newmarker.push(L.marker([tweet['lat_'], tweet['long_']], {
    //             icon: L.mapbox.marker.icon({
    //                 'marker-size': 'small',
    //                 'marker-color': '#5F9F9F'
    //             })
    //             })
    //             .bindPopup(tweet['text']));
    //             console.log("negative tweet");
    //         }
    //         marker_layer = L.layerGroup(newmarker);
    //         marker_layer.addTo(map);
    //         layerlist.push(marker_layer);
    //         if (layerlist.length > 50) {
    //             map.removeLayer(layerlist[0]);
    //             console.log("removed");
    //         }
    //       });
    // };


    channel.bind('new_tweet', function(tweet) {
        console.log(tweet);
        var newmarker = [];
        if (tweet['score'] == '4') {
            newmarker.push(L.marker([tweet['loc'][1], tweet['loc'][0]], {
            icon: L.mapbox.marker.icon({
                'marker-size': 'small',
                'marker-color': '#FCB514'
            })
            })
            .bindPopup(tweet['text']));
            console.log("positive tweet");
            }
        if (tweet['score'] == '0') {
            newmarker.push(L.marker([tweet['loc'][1], tweet['loc'][0]], {
            icon: L.mapbox.marker.icon({
                'marker-size': 'small',
                'marker-color': '#5F9F9F'
            })
            })
            .bindPopup(tweet['text']));
            console.log("negative tweet");
        }
        marker_layer = L.layerGroup(newmarker);
        marker_layer.addTo(map);
        layerlist.push(marker_layer);
        if (layerlist.length > 50) {
            map.removeLayer(layerlist[0]);
            console.log("removed");
        }
    });

    // $("body").on("click", function() {
    //     map.eachLayer(function(layer) {
    //         if (layer instanceof L.Marker) {
    //             map.removeLayer(layer);
    //         }
    //     });
    // });

    // makes AJAX call every 3 seconds to display new tweets
//     setInterval(function () {
//         markers();
//         // marker_layer = L.layerGroup(newlist)
//         // marker_layer.clearLayers()
//         }, 10000);
});

    