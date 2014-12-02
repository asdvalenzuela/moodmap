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
