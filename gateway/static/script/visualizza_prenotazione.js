function visualizza_prenotazione(){

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
        var data = document.getElementById("Data");
        var luogo = document.getElementById("Luogo");
        var codiceFiscale = document.getElementById("CodiceFiscale");
        res = res['data'];
        data.innerHTML = res.dataVaccino;
        luogo.innerHTML = res.luogoVaccino;
        codiceFiscale.innerHTML = res.codiceFiscale;

        /*Il messaggio inizialmente è display="block" e una volta recuperate le info
        cambia in display="none"*/

        var messaggio = document.getElementById("messaggio_no_prenotazione");
        messaggio.style.display="none";

        /*La tabella inizialmente è display="none" e una volta recuperate le info
        cambia in display="block"*/
        
        var tableObject = document.getElementById("tabella_prenotazione");
        tableObject.style.display="block";
        return true;
    });

    xhr.open('GET', '/api/bookings/view');
    xhr.send();
    
}
