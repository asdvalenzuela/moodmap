//took these out of document ready for testing with Jasmine
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

var setMarker = function(tweet, icon_type) {
    var popup_type;
    if (icon_type == happyIcon) {
        popup_type = "<div class=\"happy-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] + "<br>" + tweet["timestamp"] + "</figcaption></figure></div>";
    }
    if (icon_type == sadIcon) {
        popup_type = "<div class=\"sad-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] +  "<br>" + tweet["timestamp"] + "</figcaption></figure></div>";
    }
    newmarker = L.marker([tweet['loc'][1], tweet['loc'][0]],
        { icon: icon_type, title: tweet['score']+  tweet['id_str']}
    )
    .bindPopup(popup_type);
    return newmarker;
};

$(document).ready(function () {

    L.mapbox.accessToken = 'pk.eyJ1IjoiYXNkdiIsImEiOiJYY3BLVFFJIn0.95ta0d-qxicw8FR70TEJ9w';

    var map = L.mapbox.map('map-one', 'asdv.k6h5h7cf', {zoomControl: false, scrollWheelZoom: false}).setView([37.66, -122], 10);

    new L.Control.Zoom({ position: 'topright' }).addTo(map);
   
    //connects with input from streamTweets.py
    var pusher = new Pusher('998f83412af68dd3edb3');
    var channel = pusher.subscribe('tweet_map');

    var marker_layer = new L.FeatureGroup();
    marker_layer.addTo(map);

    getCurrentTime = function() {
        var currentTime = new Date();
        hour = currentTime.getHours();
        minute = currentTime.getMinutes();
        if (hour === 0 && minute == 1) {
            $.get("/clear_db", function() {
                map.eachLayer(function(layer) {
                    if (layer instanceof L.Marker) {
                        map.removeLayer(layer);
                    }
                });
            });
        }
    };

    getCurrentTime();

    setInterval(function() {
        getCurrentTime();
    }, 60000);

    $.get("/todays_tweets", function(data) {
        for (i = 0; i < data.length; i++) {
            if (data[i]['score'] == '4') {
                newmarker = setMarker(data[i], happyIcon);
            }
            if (data[i]['score'] == '0') {
                newmarker = setMarker(data[i], sadIcon);
            }
        marker_layer.addLayer(newmarker);
        }
    });

    marker_layer.on('layeradd', function(e) {
        map.panTo(e.layer.getLatLng());
    });


    $(function() {
    $( "#slider-range" ).slider({
        orientation: "vertical",
        range: true,
        max: 24,
        values: [ 0, hour ],
        slide: function( event, ui ) {
            if (ui.values[0] === 0) {
                sTime = '12am';
            }
            if (0 < ui.values[0] && ui.values[0] < 12) {
                sTime = ui.values[0] + 'am';
            }
            if (ui.values[0] === 12) {
                sTime = '12pm';
            }
            if (12 < ui.values[0] && ui.values[0] < 24) {
                sTime = ui.values[0] - 12 + 'pm';
            }
            if (ui.values[1] === 24) {
                eTime = '12pm';
            }
            if (0 < ui.values[1] && ui.values[1] < 12) {
                eTime = ui.values[1] + 'am';
            }
            if (ui.values[1] === 12) {
                eTime = '12pm';
            }
            if (12 < ui.values[1] && ui.values[1] < 24) {
                eTime = ui.values[1] - 12 + 'pm';
            }
            $( "#amount" ).val( "(from " + sTime + " to " + eTime + ")" );
        },
        change: function( event, ui) {
            var startTime = ui.values[0];
            var endTime = ui.values[1];
            var time_range_url = "/tweets_by_hour?startTime=" + startTime + "&endTime=" + endTime;
            $.get(time_range_url, function(data){
                var display_list = [];
                for (i = 0; i < data.length; i++) {
                    display_list.push(data[i]['id_str']);
                }
                map.eachLayer(function(layer) {
                    if (layer["options"]) {
                        if ("title" in layer["options"]) {
                            var title = layer["options"]["title"].slice(1);
                                if (display_list.indexOf(title) !== -1) {
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

    var filterTweets = function(tweetType) {
        if (tweetType == 'all-tweets') {
            map.eachLayer(function(layer) {
                if (layer["options"]) {
                    if ("title" in layer["options"]) {
                        if ((layer["options"]["title"].slice(0,1)) == '4') {
                            layer.setOpacity(1);
                        }
                        if ((layer["options"]["title"].slice(0,1)) == '0') {
                            layer.setOpacity(1);
                        }
                    }
                }
            });
        }
        if (tweetType == 'sad-tweets') {
            map.eachLayer(function(layer) {
                if (layer["options"]) {
                    if ("title" in layer["options"]) {
                        if ((layer["options"]["title"].slice(0,1)) == '4') {
                                layer.setOpacity(0);
                        }
                        if ((layer["options"]["title"].slice(0,1)) == '0') {
                                layer.setOpacity(1);
                        }
                    }
                }
            });
        }
        if (tweetType == 'happy-tweets') {
            map.eachLayer(function(layer) {
                if (layer["options"]) {
                    if ("title" in layer["options"]) {
                        if ((layer["options"]["title"].slice(0,1)) == '0') {
                                layer.setOpacity(0);
                        }
                        if ((layer["options"]["title"].slice(0,1)) == '4') {
                                layer.setOpacity(1);
                        }
                    }
                }
            });
        }
    };

    $(function() {
        $("#selectable").selectable({
            selected: function (event, ui) {
                var tweetType = ui.selected.id;
                if (tweetType == 'clear-button') {
                    map.eachLayer(function(layer) {
                        if (layer instanceof L.Marker) {
                            map.removeLayer(layer);
                        }
                        });
                }
                else {
                filterTweets(tweetType);
                }
            }
        });
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

    var setMarker = function(tweet, icon_type) {
        var popup_type;
        if (icon_type == happyIcon) {

            popup_type = "<div class=\"happy-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] + "<br>" + tweet["timestamp"] + "</figcaption></figure></div>";
        }
        if (icon_type == sadIcon) {
            popup_type = "<div class=\"sad-popup\"</div><figure style=\"margin-left:20px\">" + tweet['text'] + "<br><br><img style=\"margin-left:0px;display:inline-block\" src=" + tweet['profile_img'] +" height=40 width=40/><figcaption style=\"font-size:0.75em;display:inline-block;margin-left:10px\">@" + tweet['screen_name'] +  "<br>" + tweet["timestamp"] + "</figcaption></figure></div>";
        }
        newmarker = L.marker([tweet['loc'][1], tweet['loc'][0]],
            { icon: icon_type, title: tweet['score']+  tweet['id_str']}
        )
        .bindPopup(popup_type);
        return newmarker;
    };

    $(function() {
        $( "#radio" ).buttonset();
    });

    var userInteracting = false;

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

    channel.bind('new_tweet', function(tweet) {
        if (!userInteracting) {
            if ($('.ui-selected')[0].id == 'happy-tweets' || $('.ui-selected')[0].id == 'all-tweets') {
                if (tweet['score'] == '4') {
                    newmarker = setMarker(tweet, happyIcon);
                }
            }
            if ($('.ui-selected')[0].id == 'sad-tweets' || $('.ui-selected')[0].id == 'all-tweets') {
                if (tweet['score'] == '0') {
                    newmarker = setMarker(tweet, sadIcon);
                }
            }
        marker_layer.addLayer(newmarker);
        newmarker.openPopup();
        }
    });

});