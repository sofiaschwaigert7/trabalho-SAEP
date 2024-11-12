function api (endpoint, body, callback=(data)=>{}) {
    return fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {
                Swal.fire({
                    title: "Erro!",
                    text: data.error,
                    icon: 'error',
                }).then(() => location.reload());
            } else {

                Swal.fire({
                    title: "Sucesso!",
                    text: data.message,
                }).then(() => callback(data))
            }
        })
        .catch(error => {
            console.log(error);
            // Lida com erros, caso algo dê errado
            Swal.fire({
                title: "Erro!",
                text: "Erro desconhecido.",
                icon: 'error'
            }).then(() => location.reload());
        });
}

function _loading_btn (btn) {
    btn.disabled = true;
    btn.innerHTML = `<img src="/static/loading.svg" id="icon-loading">`;
}
