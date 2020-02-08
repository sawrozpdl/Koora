let content = document.getElementById('content-article');
let target = document.getElementById('target-article');

if (content)
    content.onkeyup = event => {
        target.innerHTML = marked(event.target.value);
    };


let markdown_items = document.getElementsByClassName('to-markdown')

for (let item of markdown_items) {
    item.innerHTML = marked(item.innerText)
}