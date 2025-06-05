const successButton = document.querySelector('#successButton');
const errorButton = document.querySelector('#errorButton');
const toastNotification = document.querySelector('#toastNotification');

const showToast = (message, isError = false) => {
    let toast = document.createElement('div');
    toast.classList.add('toast');
    if (isError) toast.classList.add('error');

    toast.innerHTML = message;
    toastNotification.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

successButton?.addEventListener('click', () => {
    showToast('<i class="fa-solid fa-circle-check"></i> Successfully submitted!');
});

errorButton?.addEventListener('click', () => {
    showToast('<i class="fa-solid fa-circle-exclamation"></i> An error occurred!', true);
});
