const toastNotification = document.querySelector('#toastNotification');

// const showToast = (message, isError = false) => {
//     let toast = document.createElement('div');
//     toast.classList.add('toast');
//     if (isError) toast.classList.add('error');

//     toast.innerHTML = message;
//     toastNotification.appendChild(toast);

//     setTimeout(() => {
//         toast.remove();
//     }, 5000);
// }

document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.remove();
        }, 5000);
    });
});