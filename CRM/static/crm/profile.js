document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#new-message').onclick = () => new_message('#message-form');

    // for adding landlords or tenants
    document.querySelector('#addUser').onclick = () => new_message('#addForm');
    document.querySelectorAll('.accept-request').forEach((e) => accept_request(e));
    document.querySelectorAll('.delete-request').forEach((e) => delete_message(e));
})

function new_message(form_id) {

    form = document.querySelector(form_id);
    form.style.animationPlayState = "running";
    form.style.display = form.style.display === 'block' ? 'none' : 'block';

}

function accept_request(e) {

    // fetch url with request to accept
    e.onclick = () => {

        // get csrf_token
        const csrftoken = getCookie('csrftoken');

        const request = new Request(
            message_url,
            { headers: { 'X-CSRFToken': csrftoken } }
        );

        fetch(request, {
            method: 'PUT',
            mode: "same-origin",
            body: JSON.stringify({
                "message_id": e.dataset.id
            })
        })
            .then(res => {
                if (res.status === 200) {
                    alert("New Business Relation Created!")
                    location.reload()
                } else {
                    res.json()
                        .then(res => {
                            alert(res.error)
                        })
                }

            })
            .catch(err => {
                console.log(err)
                err.json()
                    .then(err => {
                        console.log(err)
                    })
            })
    }
}

function delete_message(e) {

    // fetch route with message to delete
    e.onclick = () => {

        // get csrf_token
        const csrftoken = getCookie('csrftoken');

        // make request
        const request = new Request(
            message_url,
            { headers: { 'X-CSRFToken': csrftoken } }
        );


        fetch(request, {
            method: 'PUT',
            mode: "same-origin",
            body: JSON.stringify({
                "deleting": true,
                "message_id": e.dataset.id
            })
        })
            .then(res => {
                if (res.status === 200) {
                    location.reload()
                } else {
                    res.json()
                        .then(res => {
                            alert(res.error)
                        })
                }
            })
            .catch(err => {
                console.log(err)
                err.json()
                    .then(err => {
                        console.log(err)
                    })
            })
    }
}


// function to get csrf cookie taken from django documentation -> https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}