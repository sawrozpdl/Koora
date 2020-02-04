const darkSwitch = document.getElementById('darkSwitch');

function initTheme() {
    const e =
        null !== localStorage.getItem('darkSwitch') &&
        'dark' === localStorage.getItem('darkSwitch');
    (darkSwitch.checked = e),
        e
            ? document.body.setAttribute('data-theme', 'dark')
            : document.body.removeAttribute('data-theme');
}

function resetTheme() {
    darkSwitch.checked
        ? (document.body.setAttribute('data-theme', 'dark'),
          localStorage.setItem('darkSwitch', 'dark'))
        : (document.body.removeAttribute('data-theme'), localStorage.removeItem('darkSwitch'));
}

window.addEventListener('load', () => {
    darkSwitch &&
        (initTheme(),
        darkSwitch.addEventListener('change', () => {
            resetTheme();
        }));
});

// --------------- //

let content = document.getElementById('content-article');
let target = document.getElementById('target-article');

if (content)
    content.onkeyup = event => {
        target.innerHTML = marked(event.target.value);
    };

let shareButtons = document.getElementsByClassName('report-button');

for (let button of shareButtons) {
    button.onclick = event => {
        const data = event.target.name.split('$');
        const authorName = data[1];
        const contentTitle = data[0];
        setTimeout(() => {
            $.notify(
                `${authorName || 'User'} has been reported for ${contentTitle || 'the content!'}`,
            );
        }, 500);
    };
}
