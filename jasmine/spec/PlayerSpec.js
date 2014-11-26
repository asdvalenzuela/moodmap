describe("dummy", function() {
  it("should pass", function() {
	return true;
  });
});

describe("setMarker", function () {
  it("should place happy marker", function() {
	newmarker = setMarker({ "loc" : [ -122.12993, 37.681463 ], "screen_name" : "analphadies", "text" : "@shanstinator @softlycanthropy @halesknot -500% surprised", "entities" : { "user_mentions" : [ { "indices" : [ 0, 13 ], "id_str" : "2460018415", "screen_name" : "shanstinator", "name" : "shannon (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧" }, { "indices" : [ 14, 30 ], "id_str" : "2546557103", "screen_name" : "softlycanthropy", "name" : "Kay" }, { "id" : 410732889, "indices" : [ 31, 41 ], "id_str" : "410732889", "screen_name" : "halesknot", "name" : "potato queen" } ], "symbols" : [ ], "trends" : [ ], "hashtags" : [ ],"urls" : [ ] }, "score" : "4", "profile_img" : "https://pbs.twimg.com/profile_images/534637314136616960/FJFeSB8S_normal.jpeg", "id_str" : "537424145433501696", "date" : "11 25 14"}, L.icon({
		iconUrl: '../static/img/happy.png',
		iconSize: [16, 24],
		iconAnchor: [8, 12],
		popupAnchor: [0, -20]
	}), "Happy");
  });
});

// describe("Player", function() {
//   var player;
//   var song;

//   beforeEach(function() {
//     player = new Player();
//     song = new Song();
//   });

//   it("should be able to play a Song", function() {
//     player.play(song);
//     expect(player.currentlyPlayingSong).toEqual(song);

//     //demonstrates use of custom matcher
//     expect(player).toBePlaying(song);
//   });

//   describe("when song has been paused", function() {
//     beforeEach(function() {
//       player.play(song);
//       player.pause();
//     });

//     it("should indicate that the song is currently paused", function() {
//       expect(player.isPlaying).toBeFalsy();

//       // demonstrates use of 'not' with a custom matcher
//       expect(player).not.toBePlaying(song);
//     });

//     it("should be possible to resume", function() {
//       player.resume();
//       expect(player.isPlaying).toBeTruthy();
//       expect(player.currentlyPlayingSong).toEqual(song);
//     });
//   });

//   // demonstrates use of spies to intercept and test method calls
//   it("tells the current song if the user has made it a favorite", function() {
//     spyOn(song, 'persistFavoriteStatus');

//     player.play(song);
//     player.makeFavorite();

//     expect(song.persistFavoriteStatus).toHaveBeenCalledWith(true);
//   });

//   //demonstrates use of expected exceptions
//   describe("#resume", function() {
//     it("should throw an exception if song is already playing", function() {
//       player.play(song);

//       expect(function() {
//         player.resume();
//       }).toThrowError("song is already playing");
//     });
//   });
// });
