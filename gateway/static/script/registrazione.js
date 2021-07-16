var lnkSubmit = document.forms.formregistrazione;
function formSubmit_registrazione() {
    // Se e' stato fatto l'inserimento verra' effettuato il submit
    if (lnkSubmit.password.value != lnkSubmit.password_confirm.value) {
        alert("password non corrispondente")
        return false;
    }
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
    var nome = lnkSubmit.nome.value;
    var cognome = lnkSubmit.cognome.value;
    var codiceFiscale = lnkSubmit.codiceFiscale.value;
    var tesseraSanitaria = lnkSubmit.tesseraSanitaria.value;
    var dataNascita = lnkSubmit.dataNascita.value;
    var luogoNascita = lnkSubmit.luogoNascita.value;
    var luogoResidenza = lnkSubmit.luogoResidenza.value;
    var email = lnkSubmit.email.value;
    var telefono = lnkSubmit.telefono.value;
    var password = lnkSubmit.password.value;
    var data = {nome, cognome, dataNascita, luogoNascita, email, telefono, password, codiceFiscale, tesseraSanitaria, luogoResidenza}
    var json = JSON.stringify(data);

    xhr.open('POST', '/api/users/register');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(json);
}
