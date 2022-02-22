document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#land-view').style.display = 'none';
    document.querySelector('#lands-view').style.display = 'block';

    document.querySelectorAll('.see').forEach(e => {
        e.onclick = () => load_land(e.dataset.id)
    })
})


function load_land(land_id) {

    fetch(terrain_url + land_id)
        .then(res => res.json())
        .then(land => {
            // LAND INFORMATION
            document.querySelector('#title').innerHTML = land.title;
            document.querySelector('#landlord').innerHTML = land.landlord.username;
            document.querySelector('#tenant').innerHTML = land.tenant.username;
            // document.querySelector('#contract').href = land.contract;
            document.querySelector('#description').innerHTML = land.description;
            document.querySelector('#location').innerHTML = land.location;
            document.querySelector('#hectares').innerHTML = `${land.hectares} ha`;
            document.querySelector('#map').href = land.map;

            // Add Weather Html
            document.querySelector("#weather").innerHTML = land.html

            // BILLING INFORMATION
            document.querySelector('#method').innerHTML = land.billing.method;
            document.querySelector('#amount').innerHTML = land.billing.amount;
            document.querySelector('#payed').innerHTML = land.billing.payed;
            document.querySelector('#pending').innerHTML = land.billing.pending;
            document.querySelector('#deadline').innerHTML = land.billing.deadline;

            statusPill = document.querySelector('#status')
            if (land.billing.pending == 0 || land.billing.daysleft > 100) {
                statusPill.style.backgroundColor = "green";
                statusPill.innerHTML = "No hurry";
            } else if (land.billing.daysleft > 30) {
                statusPill.style.backgroundColor = "yellow";
                statusPill.style.color = "black";
                statusPill.innerHTML = "Near deadline";
            } else {
                statusPill.style.backgroundColor = "red";
                statusPill.innerHTML = "Pay Time!";
            }

            // Show view
            document.querySelector('#land-view').style.display = 'block';
            document.querySelector('#lands-view').style.display = 'none';
            document.querySelector('#land-view').style.animationPlayState = "running";

            // Weather API fetch
            // const lat = land.coord.lat
            // const lon = land.coord.long

            // fetch(`http://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${APIkey}&mode=html`)
            //     .then(res => res.text())
            //     .then(res => {
            //         document.querySelector('#weather').innerHTML = res;
            //     })
            //     .catch(err => console.log(err))


        })
        .catch(err => {
            console.log(err)
        }
        );

}