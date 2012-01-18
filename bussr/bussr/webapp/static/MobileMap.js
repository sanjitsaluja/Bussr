/*global YUI, ZILLOW */
/*jslint browser: true, white: true */
/*
 * @description : supporting JS code for mobile maps.
 * @date 5/13/2011
 * @author scotts 
 */

YUI.add('zillow-mobile-map', function (Y) {
	
	// TODO/NOTE: this is run every time YUI().use('zillow-mobile-map')... is called, which
	// can lead to bugs if it's "use"d more than once.
	
	var MobileMap = {
	    activeMarkers : {},   // holds map marker objects currently active on map.
	    ajaxObj : null,          // holds YUI.io object, so we can abort the ajax call if needed.
	    ajaxTimeout : null,   // holds ajax callback, to control overzealous event firing
	    boundsTimeout : null, // stores bounds_changed handler, to control overzealous event firing  
	    bubbleClickHandler: null, // saves the bubble handler so we can detach later.
	    bubbleOn : false,	  // flag telling if the bubble is currently shown; quicker to check a flag since it's checked on every bounds_changed
	    locationBarTimeout: null, // stores hideLocationBar timeout event, to control overzealous firing
	    locationMarker : null,// marker displaying user's current location
	    mapLoaded: false,	  // flag to tell if the initial map is loaded on page load.
	    mapObj : null,        // holds Google Map object.
	    resultHandler: null,  // reference to the most-recent resultHandler object.
	    selectedMarker: null, // ref to the selected/active/green marker on the map (its bubble is being shown)
	    viewport : {x: 0, y: 0}, // holds viewport dimensions
	    DEVICE_PERF : true,   // whether the device is performant enough to display prices on map, etc.
	    SHOW_LOCATION_ACCURACY : 100, // minimum geolocation accuracy (meters) to show user's location on map.
	    ZOOM_IN_LIMIT : 16,   // most we will zoom in when we locate user.
	    ZOOM_OUT_LIMIT : 5,   // most we will zoom out when we locate user.
	    ZOOM_START : 3,       // level when no location found (for whole USA)
	    
	    // resizes map div and triggers the Google Map API's resize event 
	    resizeMap : function (mapDivId) {
	    	Y.on("domready", function () {
	    		var oldVP = Y.clone(MobileMap.viewport),
		        // get coords of element on page
	                el = Y.one('#' + mapDivId),
	                top = el.getY();
	            // YUI winHeight returns wrong value on iOS, so we'll try 
	            // native JavaScript first
	            MobileMap.viewport.x = (typeof window.innerWidth != 'undefined')
        				? window.innerWidth
        				: el.get('winWidth');
	            MobileMap.viewport.y = (typeof window.innerHeight != 'undefined')
	            		? window.innerHeight
	            		: el.get('winHeight');
	            el.setStyle('height', MobileMap.viewport.y - top);
	            // manually call the map resize trigger, if it exists yet.
	            if(MobileMap.mapObj && (oldVP.x != MobileMap.viewport.x || oldVP.y != MobileMap.viewport.y)) {
	                google.maps.event.trigger(MobileMap.mapObj, 'resize');
	            }
	    	});
	    },
	    
	    preMapLoad: function (mapDivId) {
	    	// effectively turns off scrolling
	    	Y.one("body").setStyle('overflow', 'hidden');
	    	
	    	// turns "refine search" into a floating element on top of map
	        var imw = Y.one('#info-message-wrapper'); 
	        if (imw) {
	        	var pos = imw.getXY(),
	        	    // listener for click -- will hide info box.
	        	    ds = Y.one('#primaryCandidate');
	        	// get absolute position
	        	imw.setStyle('top', pos[1]);
	        	imw.setStyle('zIndex', 2);
	        	imw.setStyle('position', 'absolute');
	        	
	        	if (ds) {
	        		ds.on('click', function (e) {
	        			return this.closeInfoMessage();
	        		});
	        	}
	        }
	    },
	    
	    closeInfoMessage: function () {
	    	var imw = Y.one('#info-message-wrapper'); 
	        if (imw) {
	        	imw.setStyle('display', 'none');
	        	return false;
	        }
	    },
	    
	    postMapLoad: function (mapDivId) {
	    	if (ZILLOW.loc.length) {
	        	var loc = ZILLOW.loc.split(',');
	        	this.placeCurrentMarker(loc[0], loc[1]);
	        }
    		// set up event listeners
    		var currentLink = Y.one('#current_location_link'),
    		    resizeMapHandler;
    		if (currentLink) {
    			currentLink.on("click", function (e) {
    				e.preventDefault();
    				MobileMap.locate();
    			}, this);
    		}
    		
    		resizeMapHandler = function(mapDivId) {
    			if(this.locatinBarTimeout) {
    				clearTimeout(this.locationBarTimeout);
    			}
    			this.locationBarTimeout = setTimeout(function () {
    				MobileMap.resizeMap(mapDivId);	
    			}, 100);
    		} 
    		
    		// set up window resize listener
    		Y.one('window').on('resize',function (e){
    			resizeMapHandler(mapDivId);
    		});
    		// orientation listener
    		Y.one('window').on('orientationchange',function (e) {
    			Y.Z.Border.hideLocationBar();
    			resizeMapHandler(mapDivId);
    		});
    		
    		// scroll listener
    		Y.one('window').on('scroll', function (e) {
    			// if we're actually scrolling, and not just opening the 
    			// location bar, scroll back to the top.
	    		if (window.top.scrollY > 0) {
		    		//alert(window.top.scrollY + ',' + window.top.screenY + ',' + window.top.screenTop);
	    			Y.Z.Border.hideLocationBar();
	    		}
    		});
    		
    		Y.Z.Border.hideLocationBar();
	    },
	    
	    // creates the Google map
	    createMap: function (mapId) {
	    	this.createMapWithType(mapId, google.maps.MapTypeId.ROADMAP);
	    },
	    
	    createMapWithType: function (mapId, mapType) {
	        this.resizeMap(mapId);
	        
	        // set defaults
	        var zoomLevel = this.ZOOM_START,
	            defaultCoords = { lat: 35.12, lon: -96.85 }, // center of USA.
	            coords,
	            relocate = false, // flag to find location and re-center/re-zoom map
	            box = {},
	        	boxArr, 
	        	bounds;
	        
	        // if previous rect is present, load it at appropriate zoom level
	        try {
	        	// n, e, s, w
	        	boxArr = ZILLOW.rect.split(',');
	        	// empty string or default rectangle
	        	if( ! boxArr.length || ZILLOW.rect == '50.62214,-68.327143,23.705962,-125.374896') {
	        		throw new Error( 'No location' );
	        	}
	        	//console.debug('ZILLOW.rect', ZILLOW.rect );
	        	box.n = boxArr[0];
	        	box.e = boxArr[1];
	        	box.s = boxArr[2];
	        	box.w = boxArr[3];
	        	coords = { lat: ( parseFloat( box.n ) + parseFloat( box.s ) ) / 2, 
	        			lon: ( parseFloat( box.e ) + parseFloat( box.w ) ) / 2 };
	            if( this.isLat( coords.lat ) && this.isLon( coords.lon ) ) {
	                //console.debug( 'Saved location found', coords );
	            } else {
	                throw new Error( 'No location' );
	            }
	        } catch( e ) {
	            //console.debug( e, 'No location saved in session' );
	            coords = defaultCoords;
	            relocate = true;
	            box = null;
	        }
	        // else show united states zoomed out.
	        
	        var latlng = new google.maps.LatLng( coords.lat, coords.lon );
	        var mapOptions = {
	            zoom: zoomLevel,
	            zoomControlOptions: { position: google.maps.ControlPosition.LEFT_BOTTOM },
	            //zoomControl: MobileUtil.isTouchDevice() ? false : true,
	            zoomControl: true,
	            center: latlng,
	            mapTypeId: mapType,
	            mapTypeControl: false, // terrain, satellite, etc
	            streetViewControl: false,
	            mapTypeControlOptions: {
	                style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
	            },
	            navigationControlOptions: {
	                style: google.maps.NavigationControlStyle.SMALL
	            }
	        };
	        this.mapObj = new google.maps.Map(document.getElementById(mapId), mapOptions);
	       
	        if( box ) {
	        	// reduce the bounds by 20% to ensure reloads fit at same zoom level.
	        	var nsAdj = ( parseFloat( box.n ) - parseFloat( box.s ) ) * .2;
	        	var ewAdj = ( parseFloat( box.e ) - parseFloat( box.w ) ) * .2;
	        	var bounds = new google.maps.LatLngBounds(
	                    new google.maps.LatLng( parseFloat( box.s ) + nsAdj, parseFloat( box.w ) + ewAdj ),   // sw
	                    new google.maps.LatLng( parseFloat( box.n ) - nsAdj, parseFloat( box.e ) - ewAdj ) ); // ne
		        this.mapObj.fitBounds( bounds );
	        }
	        
	        // Add listener for zoom/pan events, so we can adjust displayed properties.
	        // This is also usually called when the orientation changes.
	        google.maps.event.addListener(this.mapObj, 'bounds_changed', function() {
	        	if( this.boundsTimeout ) {
	                clearTimeout( this.boundsTimeout );
	            }
	        	// wrapped in a timeout to prevent over-zealous firing.
	        	this.boundsTimeout = setTimeout( function() {
	        		//MobileMap.hideMarkers();
		        	MobileMap.hideBubble();
	    			MobileMap.resizeMap( 'map_canvas');
		            var bounds = MobileMap.mapObj.getBounds();
		            Y.Global.fire('mobileMap:panMap', {
		            	zoomLevel: MobileMap.mapObj.getZoom(),
		            	bounds: {
			            	n: bounds.getNorthEast().lat(),
			            	e: bounds.getNorthEast().lng(),
		    				s: bounds.getSouthWest().lat(),
		    				w: bounds.getSouthWest().lng()
			            }
		            });
	        	}, 100 );
	        });
	        
	        google.maps.event.addListener(this.mapObj, 'dragstart', function() {
	        	MobileMap.abortAjax();
		    	MobileMap.abortResultHandler();
	        	MobileMap.hideMarkers();
	        	MobileMap.hideBubble();
	        	MobileMap.changeStatus( "Loading...", true );
	        	Y.Z.Border.hideLocationBar();
	        	MobileMap.closeInfoMessage();
	        });	        

	        /*
	         * zoom_changed could either by an explicit zoom in/out by user, 
	         * or the result of a "Find Me" request, or an initial zoom level
	         * change when looking up the user's last location on a return to the map.
	         */
	        google.maps.event.addListener(this.mapObj, 'zoom_changed', function() {
	        	MobileMap.abortAjax();
		    	MobileMap.abortResultHandler();
	        	MobileMap.clearMarkers();
	        	MobileMap.hideBubble();
	        	MobileMap.changeStatus( "Loading...", true );
	        	Y.Z.Border.hideLocationBar();
	        });
	        
	        google.maps.event.addListener(this.mapObj, 'idle', function() {
	        	MobileMap.getResults();
	        	MobileMap.showMarkers();
	        });
	        
	        // click on map will hide bubble & disamb. message
	        google.maps.event.addListener(this.mapObj, 'click', function() { 
	        	MobileMap.hideBubble(); 
	        	MobileMap.closeInfoMessage();
	        });
	        
	        if( relocate ) {
	            this.locate();
	        }
	    },
	    
	    recenterMap : function( lat, lon, accuracyBox ) {
	        // determines zoom level by centering point and creating a radius from the accuracy. 
	        if( accuracyBox ) {
	            var bounds = new google.maps.LatLngBounds(
	                    new google.maps.LatLng( accuracyBox.s, accuracyBox.w ),   // sw
	                    new google.maps.LatLng( accuracyBox.n, accuracyBox.e ) ); // ne
	            this.mapObj.fitBounds( bounds );
	            var zoom = this.mapObj.getZoom();
	            if( zoom > this.ZOOM_IN_LIMIT) {
	            	console.debug( 'decreasing zoom limit from ' + zoom + ' to ' + this.ZOOM_IN_LIMIT );
	                this.mapObj.setZoom(this.ZOOM_IN_LIMIT);
	            } else if( zoom < this.ZOOM_OUT_LIMIT) {
	            	console.debug( 'increasing zoom limit from ' + zoom + ' to ' + this.ZOOM_OUT_LIMIT );
	                this.mapObj.setZoom(this.ZOOM_OUT_LIMIT);
	            }
	        } else {
	            var latlng = new google.maps.LatLng( lat, lon );
	            this.mapObj.panTo( latlng );
	        }
	    },
	    
	    // adds a marker to the map
	    addMarker : function( /* obj */ propObj ) {
	        var zpid = propObj.id;
	        
	        // add marker to map, if it's not already there
	        if( this.activeMarkers[zpid] === undefined ) {
	        	var lat = propObj.ad.la;
		        var lon = propObj.ad.lo;
		        var price = propObj.pr ? '$' + MobileUtil.priceRound(propObj.pr) : '';
		        var LatLng = new google.maps.LatLng(parseFloat(lat), parseFloat(lon));
		        // create marker
		        var hs = this.getHomeStatusInfo(propObj.hs, null, propObj.so);
		        var markerOptions = {
		            clickable: true,
		            icon: hs.img,
		            map: this.mapObj,
		            position: LatLng,
		            zIndex: 3
		        };
	            var marker = new google.maps.Marker(markerOptions);
	            google.maps.event.addListener(marker, 'click', function() { 
	            	MobileMap.displayBubble(zpid); 
	            });
	            
	            // add to activeMarkers
	            this.activeMarkers[zpid] = { 'zpid': zpid, 'lat': lat, 'lon': lon, 
	                    'markerObj': marker, 'propObj': propObj, 
	                    zoom: this.mapObj.getZoom() };
	        }
	    },

	    // add price overlay text label ("475k")
	    addPriceOverlay : function( propObj ) {
	    	if(propObj && propObj.id) {
	    		var zpid = propObj.id,
	    	    lat = propObj.ad.la,
		        lon = propObj.ad.lo,
		        price = propObj.pr ? '$' + MobileUtil.priceRound(propObj.pr) : '';
	            if(this.DEVICE_PERF && price && ! this.activeMarkers[zpid].priceOverlay) {
	            	this.activeMarkers[zpid].priceOverlay = new priceOverlay(MobileMap.mapObj, lat, lon, price);
	            }
	    	}
	    },
	    
	    clearPriceOverlay : function( zpid ) {
	    	if( this.activeMarkers[zpid].priceOverlay ) {
	    		this.activeMarkers[zpid].priceOverlay.setMap(null);
		    	this.activeMarkers[zpid].priceOverlay = null;
	    	}
	    },
	    
	    // clears any markers that have panned out of view
	    clearMarker : function( /* int */ markerKey ) {
	    	if(this.activeMarkers[markerKey].markerObj) {
	    		this.activeMarkers[markerKey].markerObj.setMap(null);
	    	}
	        if( this.DEVICE_PERF && this.activeMarkers[markerKey] && this.activeMarkers[markerKey].priceOverlay ) {
	            this.activeMarkers[markerKey].priceOverlay.setMap(null);    
	        }
	        this.activeMarkers[markerKey] = null; // TODO: doesn't delete unless we first nullify.
	        delete this.activeMarkers[markerKey];
	    },
	    
	    hideMarkers : function() {
	    	for( i in this.activeMarkers ) {
	    		if(this.activeMarkers[i].markerObj) {
	    			this.activeMarkers[i].markerObj.setVisible(false);
	    		}
	    		this.clearPriceOverlay(i);
	    	}
	    },
	    
	    clearMarkers : function() {
	    	for( i in this.activeMarkers ) {
	    		this.clearMarker(i);
	        }
	    },
	    
	    showMarkers : function() {
	    	for( i in this.activeMarkers ) {
	    		if(this.activeMarkers[i].markerObj) {
	    			this.activeMarkers[i].markerObj.setVisible(true);
	    		}
	    		this.addPriceOverlay(this.activeMarkers[i].propObj);
	        }
	    },
	    
	    // Determines if the activeMarker object is within the current map bounds.
	    isInView : function( AMObj ) {
	        var bounds = this.mapObj.getBounds();
	        return ( AMObj.lon >= bounds.getSouthWest().lng()
	           && AMObj.lon <= bounds.getNorthEast().lng()
	           && AMObj.lat <= bounds.getNorthEast().lat()
	           && AMObj.lat >= bounds.getSouthWest().lat()
	        ) ? true : false;
	    },
	    
	    // clear markers that have panned out of view.
	    clearPannedProps: function() {
	    	for( i in this.activeMarkers ) {
	            if( ! this.isInView( this.activeMarkers[ i ] ) ) {
	            	this.clearMarker(i);
	            }
	        }
	    },
	    
	    // clear markers that were plotted on a higher (zoomed-in) zoomLevel
	    // send a property list of new markers so we won't delete them (so they'll have to be immediately re-created).
	    clearZoomedProps: function( propList ) {
	    	if(!propList) {
	    		return false;
	    	}
	    	var i, 
	    		aM = {},
	    		zL = this.mapObj.getZoom();
	    	for( i = 0; i < propList.length; i++ ) {
	        	aM[ propList[i].id ] = 1;
	        }
	    	for( i in this.activeMarkers ) {
	        	if( this.activeMarkers[i].zoom > zL && ! aM[i] ) {
	            	this.clearMarker(i);	
	            // set to current zoom level if marker is loaded on new zoom level, too.
	            } else if( this.activeMarkers[i].zoom > zL ) {
	            	this.activeMarkers[i] = zL;
	            }
	        }
	    },
	    
	    // Removes zoomed-out markers, adds new markers; fired from ajax callback.
	    plotProperties : function( delegate, propList ) {
	    	if(! delegate.status || !propList) {
	    		return;
	    	}
	        var i;
	        this.clearPannedProps();
	        this.clearZoomedProps(propList);
	        for( i = 0; i < propList.length; i++ ) {
	        	if( delegate.status ) {
	        	    // See if the property is mappable before mapping it
	        	    if (propList[i].ma) {
    	        		this.addMarker( propList[i] );
    	        		this.addPriceOverlay( propList[i] );
	        		}
	        	} else {
	        		return;
	        	}
	        }
	    },
	    
	    /**
	     * Displays the status (locating user, loading results, 1-20 of 587).
	     * @status - string -- status
	     * @progress - boolean -- show progress indicator
	     */
	    changeStatus : function( status, progress ) {
	        YUI({
	            filter: 'raw'
	        }).use("node", function(Y) {
	            var str = ( progress ? '<img src="' + ZILLOW.vstatic.base + '/images/m/loader_trans.gif" style="margin:-4px 0;" alt="Loading" /> ' : ' ' )
	                    + status;
	            Y.one( "#map-status" ).insert( str, 'replace');
	        });
	    },
	    
	    /**
	     * The public getResults() has a timer and other features, which calls 
	     * the private _getResults().
	     */
	    getResults : function() {
	    	this.changeStatus( "Loading...", true );
	    	MobileMap.abortAjax();
	    	MobileMap.abortResultHandler();
	    	if( this.ajaxTimeout ) {
                clearTimeout( this.ajaxTimeout );
            }
        	// XHR call, wrapped in a timeout to prevent over-zealous firing.
        	this.ajaxTimeout = setTimeout( function() {
      	        MobileMap._getResults();
        	}, 300 );
	    },
	    
	    // Don't call this private method directly, use the public getResults() instead.
	    _getResults : function() {
            var bounds = this.mapObj.getBounds();
            var zoomLevel = this.mapObj.getZoom();

            // Create the io callback/configuration
            var callback = {
                timeout: 10000,
                context: this,
                on: {
                    success: function(x, o) {
                    	this.abortResultHandler();
                    	this.resultHandler = new resultHandler(x, o);
                    },
                    failure: function(x, o) {
                        if( o.statusText !== 'abort' ) {
                        	this.changeStatus( "Error", false );
                            console.error("Ajax call failed!", x, o.statusText, o );
                        } else {
                        	this.applyResultStatus();
                        }
                    }
                }
            };
            /*
            var url = '/webservice/GetZRectResultsJson.htm?zws-id=X1-ZWz1c2fz2pfk7f_6r0dc' 
                    + '&southWest=' + bounds.getSouthWest().lng() + ',' + bounds.getSouthWest().lat()
                    + '&northEast=' + bounds.getNorthEast().lng() + ',' + bounds.getNorthEast().lat()
                    + '&zoomLevel=' + ( zoomLevel < 19 ? zoomLevel : 18 ) + '&res=20';
            */
            // get current URL, add rect stuff
            var zurl = new Y.Z.ZURL();

            zurl.setPathParam('rect', bounds.getNorthEast().lat() + ',' + bounds.getNorthEast().lng() + ','
    				+ bounds.getSouthWest().lat() + ',' + bounds.getSouthWest().lng() );
            zurl.setPathParam('rb');
            zurl.setParam('isJson', 'true');
            zurl.setParam('isList', 'false');
            zurl.setParam('isMapView', 'true');
            var url = zurl.exportURL({exportAnchor:false});
            
            this.abortAjax();
            //console.debug('ajax url', url);
            this.ajaxObj = Y.io(url, callback);    
	    },
	    	    
	    abortResultHandler : function() {
	    	if( this.resultHandler ) {
        		this.resultHandler.cancel()
        	}
	    },
	    
	    abortAjax : function() {
	    	if( this.ajaxObj && this.ajaxObj.abort && this.ajaxObj.isInProgress() ) {
            	console.warn('ABORT!');
                this.ajaxObj.abort();
            }
	    },
	    
	    displayBubble : function( zpid ) {
	    	var prop = this.activeMarkers[zpid].propObj;
	        //console.debug( this.activeMarkers[zpid].propObj );
	    
	        // make whole bubble clickable
	        var aTag = '/m/homedetails/' + zpid + '_zpid/';
	        var hdb = Y.one( "#home_details_bubble" );
            this.bubbleClickHandler = hdb.on('click', function( e ) {
            	window.location = aTag;
            });
            
            // insert address, price, beds, sqft, baths, lot size
            var hs = this.getHomeStatusInfo( prop.hs, null, prop.so );
            var html = '<div class="bubble-head"><a href="' + aTag +  '">'  
            			+ (( prop.pt != '' ) ? Y.Lang.trim( prop.pt ) : (Y.Lang.trim( prop.ad.st ) + ', ' + Y.Lang.trim( prop.ad.cy ) + ', ' + Y.Lang.trim( prop.ad.et )))
            		+ '</a></div>'
                    + '<table class="bubble-table">'
                    + '<tr><td colspan="2"><img src="' + hs.img + '" alt="' + hs.txt + '" />'
                    + hs.txt + ': $' + Y.DataType.Number.format( parseInt(prop.pr), {thousandsSeparator: ','}) + prop.au + '</td></tr>'
                    + '<tr><td>Beds: ' + ( ! prop.be ? 'n/a' : prop.be ) + '</td>'
                    + '<td class="bubble-second-column bubble-second-column-top">Sqft: ' + ( ! prop.sf ? 'n/a' : prop.sf ) + '</td></tr>'
                    + '<tr><td>Baths: ' + ( ! prop.ba ? 'n/a' : prop.ba ) + '</td>'
                    + '<td class="bubble-second-column">Lot:  ' + ( ! prop.ls ? 'n/a' : prop.ls ) + '</td></tr>'
                    + '</table>';
            
            var offerText = prop.so ? '<strong>Zillow Special Offer:</strong> ' + prop.st : '';
            
            // Transition fade from one to another
            if(this.bubbleOn) {
            	// fade old contents out
            	var bw = Y.one("#bubble_wrap");
            	bw.transition({
                	easing: 'ease-out',
                    duration: 0.15, // seconds
                    opacity: 0
                }, function(){ // callback
                	//hdb.setStyle('visibility','hidden');
                    
                	Y.one( "#bubble-details" ).insert(html, 'replace');
                	var bo = Y.one( "#bubble-offer" );
                	bo.insert(offerText, 'replace');
                	if(prop.so) {
                		bo.addClass('special-listing-info');
                	} else {
                		bo.removeClass('special-listing-info');
                	}
                	Y.one( "#bubble-img" ).setAttribute( 'src', prop.il);
                	
                	// get fully rendered height
            		hdb.setStyle('height','auto');
                    hdb.setStyle('overflow','visible');
                    var height = hdb.get('region').height;
                    
                    hdb.setStyle('overflow','hidden');
                    //hdb.setStyle('visibility','visible');
                	
                	// fade new contents in
                    bw.transition({
                    	easing: 'ease-in',
                        duration: 0.15, // seconds
                        opacity: 1
                    }, function() {
                    	hdb.setStyle('height', height + 'px');
                    });
                });
                
            // Transition bubble open
            } else {
            	Y.one( "#bubble-details" ).insert(html, 'replace');
            	var bo = Y.one( "#bubble-offer" ); 
            	bo.insert(offerText, 'replace');
            	if(prop.so) {
            		bo.addClass('special-listing-info');
            	} else {
            		bo.removeClass('special-listing-info');
            	}            	
            	Y.one( "#bubble-img" ).setAttribute( 'src', prop.il);
            	
            	// get fully rendered height
                hdb.setStyle('height','auto');
                hdb.setStyle('overflow','hidden');
                var height = hdb.get('region').height;
                
                // then hide before transition starts
                hdb.setStyle('height','0px');
                hdb.setStyle('overflow','hidden');
                hdb.setStyle('visibility','visible');
                
                hdb.transition({
                	easing: 'ease-in',
                    duration: 0.25, // seconds
                    height: height + 'px'
                });
            }
            
            this.bubbleOn = true;
            
            // if a marker is already selected (green), revert it to its original icon.
            if(this.selectedMarker) {
	            this.unselectMarker(this.selectedMarker);
            }
            // set this property's map icon to active (green).
            var offer = this.activeMarkers[zpid].propObj.so;
            this.activeMarkers[zpid].markerObj.setIcon(ZILLOW.vstatic.base + 'images/m/home_active' + (offer ? '_offer' : '') + '.png');
            this.selectedMarker = this.activeMarkers[zpid];
            this.closeInfoMessage();
	    },
	    
	    hideBubble : function() {
	    	if( this.bubbleOn ) {
	    		// start transition
	    		Y.one('#home_details_bubble').transition({
	            	easing: 'ease-out',
	                duration: 0.25, // seconds
	                height: '0px'
	            }, function() {
	            	this.setStyle('visibility','hidden');
	            });
		        if(this.selectedMarker) {
		            this.unselectMarker(this.selectedMarker);
		            this.selectedMarker = null;
	            }
		        this.bubbleClickHandler.detach();
		        this.bubbleOn = false;
	    	}
	    },
	    
	    unselectMarker: function(m) {
	    	var hs = this.getHomeStatusInfo(m.propObj.hs, null, m.propObj.so);
            m.markerObj.setIcon(hs.img);
	    },
	    
	    // returns text and icon location for all home statuses.
	    getHomeStatusInfo: function(key, favorite, offer) {
	    	favorite = !!favorite;
	    	offer = !!offer;
	    	var s = {
    			pending :           {t:"Pending",           i:'sale'},
	            sold :              {t:"Sold",              i:'sold'},
	            forRent :           {t:"For Rent",          i:'rent'},
	            forSale :           {t:"For Sale",          i:'sale'},
	            forSaleByOwner:     {t:"For Sale by Owner", i:'sale'},
	            forSaleBankOwned:   {t:"Bank Owned",        i:'sale'},
	            forSaleForeclosure: {t:"Foreclosure",       i:'sale'},
	            forSaleAuction:     {t:"Auction",           i:'sale'},
	            other :         	{t:"Zestimate",         i:'zestimate'},
	            recentlySold :  	{t:"Recently Sold",     i:'sold'},
	            MMM:            	{t:"Make Me Move",      i:'mmm'},
	            newConstruction:	{t:"New Construction",  i:'sale'},
	            foreclosure:    	{t:"Foreclosure",       i:'sale'},
	            auction:        	{t:"Auction",           i:'sale'},
	            bankOwned:      	{t:"Bank Owned",        i:'sale'},
	            foreclosure:    	{t:"Foreclosure",       i:'sale'},
	            unknown:        	{t:"Property",          i:'sale'}
	    	};
	    	if(!s[key]) {
	    		key = 'unknown';
	    	}
	    	var extra = '';
	    	if(favorite) {
	    		extra = '_fav';
	    	} else if(offer) {
	    		extra = '_offer';
	    	}
	    	return {txt:s[key].t, img: ZILLOW.vstatic.base + 'images/m/home_' 
	    			+ s[key].i + extra + '.png'};
	    },
	    
	    // Locates a user, if it finds a location, redirects to map. Otherwise displays error message.
	    locate : function() {
	    	var elapsed = new Date();
	        this.changeStatus( "Locating...", true );
	        
	        Y.Z.Geo.locate(
	                // success callback
	                function(position) {
	        		MobileMap.foundLocationCallback(position, elapsed);
	                },
	                // fail callback
	            function(e) {
	                MobileMap.noLocationCallback(e);
	                }
	            );
	    },
	    
	    // device found location
	    foundLocationCallback : function(position, elapsed) {
	    	//console.debug( 'foundLocationCallback()' );
	        var lat = position.coords.latitude;
	        var lon = position.coords.longitude;
	        var accuracy = position.coords.accuracy;
	        if( ! this.isLat( lat ) || ! this.isLon( lon ) ) {
	            this.noLocationCallback();
	            return;
	        }
	        /*
	        console.debug( 'Found location: ' + lat + ', ' + lon);
	        console.debug( 'Accuracy: ' + accuracy + 'm (' + ( Math.round( accuracy * 0.000621371192 * 100 ) / 100 ) + ' mi)');
	        console.debug( 'Age: ' + ((+new Date() - position.timestamp) / 1000) + 's');
	        console.debug( 'Elapsed: ' + ((new Date() - elapsed) / 1000 ) + 's');
	        */
	        
	        this.placeCurrentMarker( lat, lon );
	        var accuracyBox = Y.Z.Geo.getBoxFromPoint( lat, lon, accuracy );
	        this.recenterMap(lat, lon, accuracyBox);
	        MobileMap.getResults();
	    },
	    
	    // place current location marker/icon
    	placeCurrentMarker : function( lat, lon) {
	    	lat = parseFloat(lat);
	        lon = parseFloat(lon);
	    	if(this.locationMarker) {
	    		this.locationMarker.setMap(null);
	    	}
	        var markerLatLng = new google.maps.LatLng( lat, lon );
	        var markerOptions = {
	            clickable: false,
	            icon: ZILLOW.vstatic.base + '/images/m/gps.png',
	            map: this.mapObj,
	            position: markerLatLng,
	            zIndex: 3
	        };
	        this.locationMarker = new google.maps.Marker(markerOptions);
	    },
	    	    
	    // couldn't determine location
	    // passing true means device has GPS support
	    noLocationCallback : function(e) {
    		var code = ! e || typeof e.code == 'undefined' ? 0 : e.code;
			alert( Y.Z.Geo.ERROR_MESSAGES[ code ] );
	    	this.applyResultStatus();
	    },
	    
	    isLat : function( lat ) {
	        return lat <= 90 && lat >= -90 ? true : false;
	    },

	    isLon : function( lon ) {
	        return lon <= 180 && lon >= -180 ? true : false;
	    },
	    
	    applyResultStatus : function() {
	    	var s = this.resultHandler
	    			? this.resultHandler.getResultStatus()
	    			: 'No results';
	    	this.changeStatus(s);
	    }
	    
	};
	Y.namespace("Z").MobileMap = MobileMap;
	
	/**
	 * The resultHandler class.
	 */

	// This is instantiated for each AJAX _getResults() callback method.
	var resultHandler = function(x, o) {
		var jsonObj;
		this.total = 0;
		this.results = null;
		this.status = 1; // 1 == running/finished, 0 == aborted
	    try {
	        jsonObj = Y.JSON.parse(o.responseText);
	        if(jsonObj.Response !== 'Success' && jsonObj.Response !== 'No Results') {
        		throw new Error('Server error');
        	}
    		this.results = jsonObj.Results ? jsonObj.Results : [];
        	this.total = jsonObj.to ? parseInt(jsonObj.to) : 0;
	    } 
	    catch(e) {
	    	MobileMap.changeStatus( "Error", false );
	        console.error("AJAX/server error", e);
	        return;
	    }
    	MobileMap.plotProperties( this, this.results );
	    MobileMap.changeStatus(this.getResultStatus());
	};
	
	// Sets the status as, e.g., "1-20 of 492 Results".
	resultHandler.prototype.getResultStatus = function() {
    	var str = '',
			c = 0,
			newTotal,
			am = MobileMap.activeMarkers;
    	for(var i in am) {
    		if(am[i].propObj.hs !== 'other') {
    			c++;
    		}
    	}
	    if( c === 0 ) {
	        str = 'No results';
	    } else if( c === 1 ) {
	        str = '1 result';
	    } else if( c === parseInt( this.total ) ) { // showing all results
	        str = c + ' results';
	    } else { // too many results; only showing some
	    	newTotal = this.total < c ? c : this.total; 
	        str = "1-" + c + " of " + Y.DataType.Number.format( newTotal, {thousandsSeparator: ','});
	    }
	    return str;
	}
	
	resultHandler.prototype.cancel = function() {
		this.status = 0;
	}
	

	/*
	 * Price overlay creates the gray textboxes that attach to property markers 
	 * that contain price info ("475k").
	 * 
	 * Google Maps Overlay Docs: http://code.google.com/apis/maps/documentation/javascript/overlays.html#OverlaysOverview
	 * 
	 * We remove the priceOverlays whenever the map is panned or zoomed for 
	 * performance reasons and recreate them when the map is idle. Since they 
	 * are moved relative to the icons they're "attached" to, moving them kills 
	 * performance on mobile devices.
	 */

	priceOverlay = function(map, lat, lon, content) {
	  // We define a property to hold the image's
	  // div. We'll actually create this div
	  // upon receipt of the add() method so we'll
	  // leave it null for now.
	  this._div = null;
	  this._lat = lat;
	  this._lon = lon;
	  this._content = content;

	  // Explicitly call setMap() on this overlay
	  this.setMap(map);
	};

	priceOverlay.prototype = new google.maps.OverlayView();

	priceOverlay.prototype.onAdd = function() {

	  // Note: an overlay's receipt of onAdd() indicates that
	  // the map's panes are now available for attaching
	  // the overlay to the map via the DOM.

	  // Create the DIV and set some basic attributes.
	  var div = document.createElement('DIV');
	  div.style.border = "none";
	  div.style.borderWidth = "0px";
	  div.style.position = "absolute";
	  div.style.width = "auto"; // so it's set to something, so we can grab it later.
	  div.className += ' marker-label';

	  var txt = document.createTextNode(this._content);
	  div.appendChild(txt);
	  
	  
	  // Set the overlay's _div property to this DIV
	  this._div = div;

	  // We add an overlay to a map via one of the map's panes.
	  // We'll add this overlay to the overlayImage pane.
	  var panes = this.getPanes();
	  panes.overlayLayer.appendChild(div);
	};

	// This is called automatically when overlay's map property set to null.
	priceOverlay.prototype.onRemove = function() {
	    //console.debug( 'onRemove', this._div);
	    this._div.parentNode.removeChild(this._div);
	    this._div = null;
	};

	priceOverlay.prototype.draw = function() {
	      var overlayProjection = this.getProjection();
	      var point = overlayProjection.fromLatLngToDivPixel( new google.maps.LatLng(this._lat, this._lon) );
	      // Resize the image's DIV to fit the indicated dimensions.
	      var d = this._div;
	      var width = d.clientWidth ? d.clientWidth : 35;
	      d.style.left = point.x - ( width / 2 ) + 'px';
	      d.style.top = point.y + 1 + 'px';
	};

	// TODO: is this method used?
	priceOverlay.prototype.show = function() {
	    if (this._div) {
	        this._div.style.visibility = "visible";
	    }
	};
	
    //add handlers to professional radio buttons
    function attachRadioButtonHandlers() {
            var form = Y.one('.auth-form');
            console.debug(form);
            if (form) {
                form.all('input[name="proRadioGroup"]').on('click', function() {

                }, form);
            }
    }
    // expose globally
    Y.config.win.attachRadioButtonHandlers = attachRadioButtonHandlers;


}, '3.3.0', {
    requires: [
        'datatype-number',
        'datatype-xml',
        'io-base',
        'json-parse',
        'transition',
        'node-screen',
        'zillow-mobile-url', 'zillow-mobile-geo', 'zillow-mobile-border'
    ]
});




/***** Mobile Utilities *****/

var MobileUtil = {
    // determines if device has a touch screen for hiding things like map zoom buttons
    isTouchDevice : function() {
        try {
            document.createEvent("TouchEvent");  
            return true;  
        } catch (e) {  
            return false;  
        }
    },
    
    priceRound : function( price ) {
        if( price >= 10000000 ) {
            return Math.round(price / 1000000) + 'M'; // 15M
        } else if( price >= 1000000 ) {
            return Math.round(price * 10 / 1000000) / 10 + 'M'; // 1.6M
        } else if( price >= 10000 ) {
            return Math.round(price / 1000) + 'K';     // 350K
        } else if(price >= 1000) {
        	return Math.round(price * 10 / 1000) / 10 + 'K';     // 350K
        } else {
            return price;                       // 1500
        }
    }
};

/*******************************************/







/*
 * Utility functions
 */
var util = {
    countProps : function( obj ) {
        var i;
        var c = 0;
        for( i in obj ) {
            c++;
        }
        return c;
    }
};
