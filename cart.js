document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.add-to-cart');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            btn.innerText = '✔ Добавлено';
            btn.disabled = true;
        });
    });
});
