document.addEventListener('DOMContentLoaded', function () {

    if (document.querySelector('#deleteButton') !== null) {
        // only for editing
        handleDelete();
    }

})

function handleDelete() {


    document.querySelector('#deleteButton').onclick = () => {
        warning = document.querySelector('#warningToast')
        warning.className = "toast show";
        document.querySelector('#dismiss').onclick = () => {
            warning.className = "toast hide";
        }
        document.querySelector('#delete').onclick = () => {
            warning.className = "toast hide"

            // get csrf_token
            const csrftoken = getCookie('csrftoken');

            // make request
            const request = new Request(
                url,
                { headers: { 'X-CSRFToken': csrftoken } }
            );


            //delete land async -> insert csrf_token
            fetch(request, {
                method: 'PUT',
                mode: "same-origin",
                body: JSON.stringify({
                    deleting: true,
                    land_id: id,
                })
            })
                .then(res => {
                    if (res.status === 204) {
                        // go back to index
                        window.location.replace(index);
                    } else {
                        res.json()
                            .then(res => alert(res.message))
                    }
                })
                .catch(err => console.log(err))
        }
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