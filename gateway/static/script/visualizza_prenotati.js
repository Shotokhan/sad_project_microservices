function addCell(tr, val) {
    var td = document.createElement('td');

    td.innerHTML = val;

    tr.appendChild(td)
}


function addRow(tbl, val_1, val_2, val_3, val_4, val_5) {
    var tr = document.createElement('tr');
    addCell(tr, val_1);
    addCell(tr, val_2);
    addCell(tr, val_3);
    addCell(tr, val_4);
    addCell(tr, val_5);
    tbl.appendChild(tr)
}



function visualizza_prenotati() {

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
        /*Il messaggio inizialmente � display="block" e una volta recuperate le info
        cambia in display="none"*/

        var messaggio = document.getElementById("messaggio_no_prenotazione");
        messaggio.style.display = "none";
        res = res['data'];
        /*La tabella inizialmente � display="none" e una volta recuperate le info
        cambia in display="block"*/
        var tbl = document.getElementById('tabella_prenotati');
        tbl.style.display = "block";
        var len = res.length;
        addRow(tbl, "Nome", "Cognome", "Codice Fiscale", "Luogo Vaccino", "Data Vaccino");
        for (var i = 0; i < len; i++) {
            addRow(tbl, res[i].nome, res[i].cognome, res[i].codiceFiscale, res[i].luogoVaccino, res[i].dataVaccino);
        }
        return true;
    });

    xhr.open('GET', '/api/bookings/view');
    xhr.send();

}


function logout_operatore() {

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

    xhr.open('GET', '/api/users/logout');
    xhr.send();

}
