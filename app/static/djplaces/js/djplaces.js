var dj = jQuery.noConflict();

dj(function () {

    var options = {
            map: "#map_location",
            mapOptions: {zoom: 10},
            markerOptions: {draggable: false},
            types: ["geocode", "establishment"]
        },
        geocomplete = dj("#id_place");

    // NB, this results in updating the Location name based on the coordinates.
    // For example, this means that "London, United Kingdom" will be changed to some specific address.
    if (dj('#id_location').val()) {
        options.location = dj('#id_location').val()
    }

    geocomplete
        .geocomplete(options)
        .bind("geocode:result", function (event, result) {
            dj('#id_location').val(result.geometry.location.lat() + ',' + result.geometry.location.lng());
        })
        .bind("geocode:error", function (event, status) {
            console.log("ERROR: " + status);
        })
        .bind("geocode:multiple", function (event, results) {
            console.log("Multiple: " + results.length + " results found");
        });

});
