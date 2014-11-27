describe("setMarker", function() {
    tweet = { "loc" : [ -122.12993, 37.681463 ], "screen_name" : "analphadies", "hour" : 17, "text" : "@shanstinator @softlycanthropy @halesknot -500% surprised", "score" : "4", "profile_img" : "https://pbs.twimg.com/profile_images/534637314136616960/FJFeSB8S_normal.jpeg", "id_str" : "537424145433501696", "date" : "11 25 14" };
    newmarker = setMarker(tweet, happyIcon, "Happy Tweet");
    var check_string = newmarker._popup._content;
    if (check_string.indexOf('happy-popup') > 0) {
        result = true;
    }
    else {
        result = false;
    }
    it("should place happy marker", function() {
        expect(result).toBe(true);
  });
});

describe("setMarker", function() {
    tweet = { "loc" : [ -121.916328, 37.439005 ], "screen_name" : "xo_leena", "hour" : 17, "text" : "My neighborhood is fucking gorgeous. 🚘🍂🌳🍂 http://t.co/ioQiAVKhR0", "score" : "0", "profile_img" : "https://pbs.twimg.com/profile_images/537016007986917376/6r6iW1I6_normal.jpeg", "id_str" : "537424162927542274", "date" : "11 25 14" };
    newmarker = setMarker(tweet, sadIcon, "Sad Tweet");
    var check_string = newmarker._popup._content;
    if (check_string.indexOf('sad-popup') > 0) {
        result = true;
    }
    else {
        result = false;
    }
    it("should place sad marker", function() {
        expect(result).toBe(true);
  });
});


