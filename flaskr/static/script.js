const toastNotification = document.querySelector('#toastNotification');

document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.remove();
        }, 5000);
    });
});