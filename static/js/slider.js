document.addEventListener("DOMContentLoaded", () => {

    const length = +document.querySelector('.carousel.slide').dataset.carousellength - 1;

    document.querySelector(".carousel-control-prev").addEventListener('click', (event) => {
        event.preventDefault();
        const el = document.querySelector(".carousel-item.active");
        el.classList.remove('active')
        const num = el.dataset.index;
        if (num == 0) {
            prevEl = document.querySelector(".carousel-item[data-index='2']");
            prevEl.classList.add('active');
        } else {
            prevEl = document.querySelector("[data-index='" + (num - 1) + "']");
            prevEl.classList.add('active');
        }
    });

    document.querySelector(".carousel-control-next").addEventListener('click', (event) => {
        event.preventDefault();
        const el = document.querySelector(".carousel-item.active");
        el.classList.remove('active')
        const num = +el.dataset.index;
        if (num === length) {
            nextEl = document.querySelector(".carousel-item[data-index='0']");
            nextEl.classList.add('active');
        } else {
            nextEl = document.querySelector("[data-index='" + (num + 1) + "']");
            nextEl.classList.add('active');
        }
    });

});