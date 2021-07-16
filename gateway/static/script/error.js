function logout_error() {

    var xhr = new XMLHttpRequest();

    xhr.addEventListener('error', function (event) {
        return false;
    });

    xhr.addEventListener('load', function (event) {
        return true;
    });

    xhr.open('GET', '/api/users/logout');
    xhr.send();

}
