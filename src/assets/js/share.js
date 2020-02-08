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
