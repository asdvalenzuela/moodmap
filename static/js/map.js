$(document).ready(function () {

    var getCurrentTime = function() {
        var currentTime = new Date();
        hour = currentTime.getHours();
        minute = currentTime.getMinutes();
    };

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

    //defines look of icon and popup depending on sentiment of tweet, creates marker object
    var setMarker = function(tweet) {
        if (tweet['score'] === '4') {
            iconType = happyIcon;
            popupType = "<div class=\"happy-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] + "<br>" + tweet["timestamp"] + "</figcaption></figure></div>";
        }
        if (tweet['score'] === '0') {
            iconType = sadIcon;
            popupType = "<div class=\"sad-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] +  "<br>" + tweet["timestamp"] + "</figcaption></figure></div>";
        }
        newMarker = L.marker([tweet['loc'][1], tweet['loc'][0]],
            { icon: iconType, title: tweet['score'] + tweet['id_str']}
        )
        .bindPopup(popupType);
        return newMarker;
    };

    L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map-one', 'asdv.k6h5h7cf', {zoomControl: false, scrollWheelZoom: false}).setView([37.66, -122], 10);

    new L.Control.Zoom({ position: 'topright' }).addTo(map);
   
    //connection to Twitter Stream API through receiveTweets.py
    var pusher = new Pusher('998f83412af68dd3edb3');
    var channel = pusher.subscribe('tweet_map');

    //creates initial layer and adds to map
    var markerLayer = new L.FeatureGroup();
    markerLayer.addTo(map);

    getCurrentTime();

    var removeMarkers = function() {
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });
    };

    //displays all tweets from today up to the current hour
    $.get("/todays_tweets", function(data) {
        for (i = 0; i < data.length; i++) {
            newMarker = setMarker(data[i]);
            markerLayer.addLayer(newMarker);
        }
    });
    
    //pans to each marker as it is placed
    markerLayer.on('layeradd', function(e) {
        map.panTo(e.layer.getLatLng());
    });

    //Jquery UI radiobuttons
    $(function() {
        $( "#radio" ).buttonset();
    });

    //Jquery UI slider
    $(function() {
    $( "#slider-range" ).slider({
        orientation: "vertical",
        range: true,
        max: 24,
        values: [ 0, hour ],
        slide: function( event, ui ) {
            if (ui.values[0] === 0) {
                startHour = '12am';
            }
            if (0 < ui.values[0] && ui.values[0] < 12) {
                startHour = ui.values[0] + 'am';
            }
            if (ui.values[0] === 12) {
                startHour = '12pm';
            }
            if (12 < ui.values[0] && ui.values[0] < 24) {
                startHour = ui.values[0] - 12 + 'pm';
            }
            if (ui.values[1] === 24) {
                endHour = '12pm';
            }
            if (0 < ui.values[1] && ui.values[1] < 12) {
                endHour = ui.values[1] + 'am';
            }
            if (ui.values[1] === 12) {
                endHour = '12pm';
            }
            if (12 < ui.values[1] && ui.values[1] < 24) {
                endHour = ui.values[1] - 12 + 'pm';
            }
            $( "#amount" ).val( "(from " + startHour + " to " + endHour + ")" );
        },
        //displays only the tweets from the hour range specified by the slider
        change: function( event, ui) {
            var startTime = ui.values[0];
            var endTime = ui.values[1];
            var timeRangeURL = "/tweets_by_hour?startTime=" + startTime + "&endTime=" + endTime;
            $.get(timeRangeURL, function(data){
                var displayList = [];
                for (i = 0; i < data.length; i++) {
                    displayList.push(data[i]['id_str']);
                }
                map.eachLayer(function(layer) {
                    if (layer["options"]) {
                        if ("title" in layer["options"]) {
                            var title = layer["options"]["title"].slice(1);
                                if (displayList.indexOf(title) !== -1) {
                                    layer.setOpacity(1);
                                }
                                else {
                                    layer.setOpacity(0);
                                }
                            
                        }
                    }
                });
            });
        }
    });
    $( "#amount" ).val( "(from 12am to now)");
    });

    //Jquery UI selectables
    //displays happy, sad, or all tweets based on active selectable
    //clears map if clear is selected
    $(function() {
        $("#selectable").selectable({
            selected: function (event, ui) {
                var tweetType = ui.selected.id;
                if (tweetType === 'clear-button') {
                    removeMarkers();
                    $('.ui-selected')[0].id = 'all-tweets';
                }
                else {
                filterTweets(tweetType);
                }
            }
        });
    });

    //changes opacity scores based on active selectable
    var filterTweets = function(tweetType) {
        if (tweetType === 'all-tweets') {
            setOpacity(1, 1);
        }
        if (tweetType === 'sad-tweets') {
            setOpacity(0, 1);
        }
        if (tweetType === 'happy-tweets') {
            setOpacity(1, 0);
        }
    };

    //changes opacity of markers based on active selectable
    var setOpacity = function(happyOpacity, sadOpacity) {
        map.eachLayer(function(layer) {
            if (layer["options"]) {
                if ("title" in layer["options"]) {
                    if ((layer["options"]["title"].slice(0,1)) === '4') {
                        layer.setOpacity(happyOpacity);
                    }
                    if ((layer["options"]["title"].slice(0,1)) === '0') {
                        layer.setOpacity(sadOpacity);
                    }
                }
            }
        });
    };

    var userInteracting = false;

    //toggles visibility of slider based on selected radio button
    //changes variable userInteracting to stop/start Pusher Websocket API
    $('input').on('click', function() {
        if ($('input')[0].checked  === true) {
            userInteracting = false;
            $('.slider-content').css('visibility', 'hidden');

        }
        if ($('input')[0].checked  === false) {
            userInteracting = true;
            $('.slider-content').css('visibility', 'visible');
        }
    });

    //places happy, sad, or all tweets received from Pusher Websocket API based on active selectable
    //stops Pusher if 'By Hour' is selected
    channel.bind('new_tweet', function(tweet) {
        if (!userInteracting) {
            if ($('.ui-selected')[0].id === 'happy-tweets' || $('.ui-selected')[0].id === 'all-tweets') {
                if (tweet['score'] === '4') {
                    newMarker = setMarker(tweet);
                }
            }
            if ($('.ui-selected')[0].id === 'sad-tweets' || $('.ui-selected')[0].id === 'all-tweets') {
                if (tweet['score'] === '0') {
                    newMarker = setMarker(tweet);
                }
            }
        markerLayer.addLayer(newMarker);
        newMarker.openPopup();
        }
    });

});