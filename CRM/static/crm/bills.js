document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.bill-dropdown').forEach((e) => {
        e.style.display = 'none';
    })
    document.querySelectorAll('.bill-content-wrapper').forEach((e) => {
        e.onclick = () => toggle_dropdown(document.querySelector(`#bill-dropdown-${e.id}`))
    })
})

function toggle_dropdown(e) {
    // play animation and show dropdown
    e.style.animationPlayState = 'paused';
    e.style.display = e.style.display === 'block' ? 'none' : 'block';
    e.style.animationPlayState = 'running';
}