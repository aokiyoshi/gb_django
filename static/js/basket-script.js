function basketTotalUpdate() {
    const basketTotal = document.querySelector(".basket-total");
    if (document.querySelectorAll("[class^=basket-element]").length == 0) {
        basketTotal.remove();
        return;
    } 

    const url = "/basket/basket_total/";

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(basketTotal, data.total)
            basketTotal.innerHTML = data.total;
        });

}

window.onload = function(){

    document.addEventListener('click', event => {

        if (event.target.nodeName == "INPUT") {
            
            const url = "/basket/edit/" + event.target.name + "/" + event.target.value + "/";

            const basketEl = document.querySelector(".basket-element" + event.target.name);

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    basketEl.innerHTML = data.result;
                    if (data.result === "") {
                        basketEl.remove()
                    }
                    basketTotalUpdate();
                });
            
            
        }

        
    })

    document.querySelector('.basket-delete')
        .addEventListener('click', event => {
            const url = "/basket/remove/" + event.target.name + "/";
            const basketEl = document.querySelector(".basket-element" + event.target.name);
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    basketEl.remove()
                    basketTotalUpdate();
                });
            
            }

    )
}
