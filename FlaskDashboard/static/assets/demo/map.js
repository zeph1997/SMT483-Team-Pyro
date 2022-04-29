
    var map = L.map('map').setView([1.3521, 103.8198], 13);
    L.tileLayer('https://api.maptiler.com/maps/toner/{z}/{x}/{y}.png?key=ZXDj7dd61PS9sxJFlOol', {
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
    }).addTo(map);

    var SIcon = L.Icon.extend({
    options: {
        iconSize:     [20, 20],
        shadowSize:   [50, 64],
        iconAnchor:   [22, 94],
        shadowAnchor: [4, 62],
        popupAnchor:  [-3, -76]
    }
    });

var BIcon = L.Icon.extend({
    options: {
        iconSize:     [40, 40],
        shadowSize:   [50, 64],
        iconAnchor:   [22, 94],
        shadowAnchor: [4, 62],
        popupAnchor:  [-3, -76]
    }
});
greenIcon = new SIcon({iconUrl: 'assets/img/green_marker.png'}),
redIcon = new BIcon({iconUrl: 'assets/img/red_marker.png'}),
orangeIcon = new SIcon({iconUrl: 'assets/img/orange_marker.png'});

L.marker([1.296568, 103.852119], {icon: greenIcon}).addTo(map).bindPopup("I am a green leaf. ");
L.marker([1.293942, 103.849996], {icon: redIcon}).addTo(map).bindPopup("I am a green leaf.");
L.marker([1.295332, 103.849324], {icon: orangeIcon}).addTo(map).bindPopup("I am a green leaf.");


// for location in locations:
//     if thermalfire ==1 and camerafire==1: 
//         redIcon
//         L.marker([.lat, .long], icon: red).addtom(map).bindPopup("")
//     else if thermalfire==1 or camerafire==1:
//         orangeIcon
//     else:
//         greenIcon 
