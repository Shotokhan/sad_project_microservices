var lnkSubmit = document.forms.formlogin;
function formSubmit_login() {

    if (lnkSubmit.username.value == "" || lnkSubmit.password.value == "") {
      alert("Submit non effettuato. Completa tutti i campi");
      return false;
    }
    else {
        //Se è stato fatto l'inserimento verrà effettuato il submit
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
        var is_operatore = lnkSubmit.operatore.checked;
        var password = lnkSubmit.password.value;
        if (is_operatore == true) {
            var idAslOperatore = lnkSubmit.username.value;
            var data = { idAslOperatore, password, is_operatore };
        } else {
            var codiceFiscale = lnkSubmit.username.value;
            var data = { codiceFiscale, password, is_operatore };
        }

        var json = JSON.stringify(data);

        xhr.open('POST', '/api/users/login');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(json);
    }
}



