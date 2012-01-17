var BusStopFetcher = function (resultHandler) {
    return {
        ajaxObj: null,

        // get fetch url
        getStopUrl : function (lat, lng) {
            return '/ws/stops/' + lat + ',' + lng + '/';
        },

        abortAjax : function() {
            if (this.ajaxObj) {
                this.ajaxObj.abort();
            }
        },

        getStopsForLatLng : function(lat, lng) {
            url = this.getStopUrl(lat, lng);
            this.abortAjax();
            this.ajaxObj = $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
            });

            this.ajaxObj.done(function(msg) {
                if (resultHandler && resultHandler.stopFetcherGotStops) {
                    resultHandler.stopFetcherGotStops(msg["stops"]);
                }
            });

            this.ajaxObj.fail(function(jqXHR, textStatus) {
                // TODO: handle error
                console.log('ajax failed', jqXHR, textStatus);
            });
        },
    }
};


var earthQuakeMap = {
    map : null,
    markers : [],
    stopFetcher : null,

    stopFetcherGotStops : function(stops) {
		this.clearAllMarkers();
        for (var j = 0; j < stops.length; j++) {
            stop = stops[j];
            this.addMarker(stop["lat"], stop["lng"]);
        }
    },
    
    searchAroundMapCenter : function () {
		this.searchForStopsAroundCenter(this.map.getCenter());
	},
    
    searchForStopsAroundCenter : function(center) {
		this.stopFetcher.getStopsForLatLng(center.lat(), center.lng());
	},

    initializeMap : function() {
		this.stopFetcher = BusStopFetcher(earthQuakeMap);
		
		var initialMapCenter = new google.maps.LatLng(41.87811, -87.62980);
        var myOptions = {
            zoom: 15,
            center: initialMapCenter,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        this.map = new google.maps.Map(
                    document.getElementById('map_canvas'), 
                    myOptions
                   );
        var that = this;
        google.maps.event.addListener(this.map, 'bounds_changed', 
			function() {
				that.searchAroundMapCenter();
			});
        
		this.searchForStopsAroundCenter(initialMapCenter);
    },

	clearAllMarkers  : function() {
		if (this.markers) {
			for (var i = 0; i < this.markers.length; i++ ) {
				this.markers[i].setMap(null);
			}
		}
	},

    addMarker : function(lat, lng) {
        position = new google.maps.LatLng(lat, lng);
        this.markers.push(new google.maps.Marker({
            position: position, 
            map: this.map,
            draggable: false
        }));
        return this.markers[this.markers.length-1];
    },
};

$(document).ready(function() {
    earthQuakeMap.initializeMap();
});
