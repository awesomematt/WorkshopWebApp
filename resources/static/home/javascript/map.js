function initMap() {
        var myLatLng = {lat: 50.292079, lng: 18.669097};

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 17,
          center: myLatLng
        });

        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: 'Warsztat Lakierniczy - Stanisław Kowalski'
        });
      }