var BusStopFetcher = function (resultHandler) {
    return {
        ajaxObj: null,

        // get fetch url
        getStopUrl : function (lat, lng) {
            return '/ws/stops/' + lat + ',' + lng + '/';
        },
        
        getStopUrlForRect : function(lat1, lng1, lat2, lng2) {
        	return '/ws/stopsrect/' + Math.min(lat1,lat2) + ',' + Math.min(lng1, lng2) + '/' + Math.max(lat1, lat2) + ',' + Math.max(lng1, lng2) + '/';
        },

		// abort the pending ajax operation
        abortAjax : function() {
            if (this.ajaxObj) {
				this.ajaxObj.abort();
            }
        },

        getStopsForLatLng : function(lat, lng) {
            var url = this.getStopUrl(lat, lng);
            this.abortAjax();
            this.ajaxObj = $.ajax({
                url: url,
                type: "GET",
                dataType: "json"
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
        
        getStopsForRect : function(lat1, lng1, lat2, lng2) {
            var url = this.getStopUrlForRect(lat1, lng1, lat2, lng2);
            this.abortAjax();
            this.ajaxObj = $.ajax({
                url: url,
                type: "GET",
                dataType: "json"
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
        }
    }
};


var earthQuakeMap = {
	map: null,							// google map object
	activeMarkers: [],					// hold active markers
	busStopFetcher: null,				// ajax fetcher
	searchDelay: null,					// delay the search, prevent overzealous searching
	viewport : {x: 0, y: 0},			// holds viewport dimensions
	
    // resizes map div and triggers the Google Map API's resize event 
    resizeMap : function (mapDivId) {
    	$("#" + mapDivId).css('height', 300);
    	
        /*var that = this;
        $(document).ready(function () {
    		console.log('resizeMap');
    		var oldVP = jQuery.extend(true, {}, that.viewport);
    		var h = $(window).height();
    	    var w = $(window).width();
    	    var top = $("#"+mapDivId).position().top;
    	    $("#"+mapDivId).css('height',h-top);
    	    google.maps.event.trigger(that.mapObj, 'resize');
    	});*/
    },
	
	stopFetcherGotStops: function(stops) {
    	this.plotStops(stops);
	},
	
	searchAroundMapCenter: function() {
		this.searchForStopsAroundCenter(this.map.getCenter());
	},
	
	searchMapBounds : function() {
		bounds = this.map.getBounds();
		this.searchMapBoundsHelper(bounds.getNorthEast(), bounds.getSouthWest());
	},
	
	searchMapBoundsHelper : function(corner1, corner2) {
		this.busStopFetcher.getStopsForRect(corner1.lat(), corner1.lng(), corner2.lat(), corner2.lng());
	},
	
	searchForStopsAroundCenter: function(center) {
		this.busStopFetcher.getStopsForLatLng(center.lat(), center.lng());
	},
	
	initializeGoogleMapHelper : function() {
		var that = this;
		var initialMapCenter = new google.maps.LatLng(41.87811, -87.62980);
		var myOptions = {
			zoom: 15,
			center: initialMapCenter, 
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		this.map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
		var that = this;
		
		google.maps.event.addListener(this.map, 'bounds_changed', function() {
			that.handleBoundsChanged();
		});
		
		google.maps.event.addListener(this.map, 'dragstart', function() {
			that.handleDragStart();
		});
	},
	
	initializeMap : function() {
		// Create the bus stop fetcher with ourselves as the delegate
		this.busStopFetcher = BusStopFetcher(earthQuakeMap);
		this.initializeGoogleMapHelper();
	},
	
	plotStops : function(stops) {
		this.deleteAllMarkers();
		for (var j = 0; j < stops.length; j++) {
			stop = stops[j];
			console.log(stop);
			this.addMarker(stop);
		}
	},

	//+----------------------------------------------------------------
	// Delete all marker from the map and our local set
	//-----------------------------------------------------------------		
	deleteAllMarkers : function() {
		if (this.activeMarkers) {
			for (var i in this.activeMarkers) {
				if (this.activeMarkers[i]) {
					this.deleteMarker(i);
				}
			}
		}
	},
	
	displayBubble: function(marker) {
		console.log(marker)
	},
	//+----------------------------------------------------------------
	// Delete a marker from the map and our local set
	//-----------------------------------------------------------------
	deleteMarker: function(stopId){
		console.log(this.activeMarkers.length);
		if (this.activeMarkers[stopId]) {
			if(this.activeMarkers[stopId].marker) {
	    		this.activeMarkers[stopId].marker.setMap(null);
	    	}
			
	        this.activeMarkers[stopId] = null;
	        delete this.activeMarkers[stopId];
		}
		console.log(this.activeMarkers.length);
	},
	
	//+----------------------------------------------------------------
	// Add a marker to the map. Add a click event to the marker to 
	// display a bubble.
	//-----------------------------------------------------------------
    addMarker : function(stop) {
		var stopId = stop.stopId;
		var mapMarker;
		var marker;
		var lat, lng;
		var position;
		var that = this;
		
		if (this.activeMarkers[stopId] === undefined) {
			lat = parseFloat(stop["lat"]);
			lng = parseFloat(stop["lng"]);
			position = new google.maps.LatLng(lat, lng);
			
			marker = new google.maps.Marker({
				position: position,
				map: this.map,
				draggable: false,
				clickable: true
			});

			// add a marker to the map. also add it to our ivar set
			mapMarker = this.activeMarkers[stopId] = {
				'stopId': stopId,
				'lat': lat,
				'lng': lng,
				'stop': stop,
				'marker': marker
			};
			
			// display the bubble on click
			google.maps.event.addListener(marker, 'click', function(){
				that.displayBubble(mapMarker);
			});
		}
    },
	
	// Private methods
	// Abort the pending ajax fetch
	abortPendingFetch : function() {
		if(this.busStopFetcher) {
	        this.busStopFetcher.abortAjax();
	    }
	},
	
	//+-----------------------------------------------------------
	// event handlers
	//------------------------------------------------------------
	// Prevent overzealous firing
	handleBoundsChanged : function() {
		if (this.searchTimeout) {
			clearTimeout(this.searchTimeout);
		}	
		var that = this;
		this.searchTimeout = setTimeout(
								function() { that.searchMapBounds(); },
								500);
	},
	
	// Handle the dragging of the map
	handleDragStart : function () {
		this.abortPendingFetch();
//		this.abortResultHandler();
//		this.hideMarkers();
//		this.hideBubble();
//		this.changeStatus( "Loading...", true );
	}
};

// When the document is ready initialize the map.
$(document).ready(function() {
    earthQuakeMap.initializeMap();
    var mapDivId = 'map_canvas';
    earthQuakeMap.resizeMap(mapDivId);
    
    $(window).resize(function() {
        var mapDivId = 'map_canvas';
        earthQuakeMap.resizeMap(mapDivId);
    });
});

