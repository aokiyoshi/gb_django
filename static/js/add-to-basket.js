window.onload = function(){

    document.querySelector('.input-number')
        .addEventListener('click', event => {
            event.preventDefault();
            const quantity = document.querySelector('.input-number').value;
            const url = document.querySelector('.add-to-cart').getAttribute('href') + quantity + '/';
            const Http = new XMLHttpRequest();
            Http.open("GET", url);
        })
        
}

