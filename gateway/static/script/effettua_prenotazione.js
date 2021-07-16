var lnkSubmit = document.forms.formprenotazione;
function Submit_prenotazione() {

    var xhr = new XMLHttpRequest();

    xhr.addEventListener('error', function (event) {
        window.location.href = "/errorPage";
        return false;
    });
    xhr.addEventListener('load', function (event) {
        let res = JSON.parse(xhr.responseText);
        if ("error" in res) {
            window.location.href = "/errorPage?error_msg=" + encodeURI(res["error"]);
            return false;
        }
        window.location.href = "/";
        return true;
    });

    xhr.open('POST', '/api/bookings/newBooking');
    xhr.send();
}

function Back_Home() {
    window.location.href = "/";
}
