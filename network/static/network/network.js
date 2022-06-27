document.addEventListener('DOMContentLoaded', function() {
    // checkHasNextPrev();
    document.querySelector('#next').addEventListener('click', () => load_another_page('next'));
    document.querySelector('#prev').addEventListener('click', () => load_another_page('prev'));
    window.onload = checkHasNextPrev;
});

// window.addEventListener('haschange', function () {
//     console.log('location changed!');
// });
function load_another_page(opt) {
    console.log('click detect', opt);
    checkHasNextPrev();
    let post_area = document.querySelector('#post-area');
    let first = post_area.firstElementChild;
    while (first) {
        first.remove();
        first = post_area.firstElementChild;
    }
    console.log('here');
    fetch(`/${opt}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.forEach(post => {
            const poster = post.poster;
            const content = post.content;
            const like_num = post.like_num;
            const timestamp = post.post_time;

            
            let this_post = document.createElement('div');
            this_post.className = "post round text-light bg-dark border-primary";
            let element = document.createElement('h6');
            
            element.innerHTML = poster;
            this_post.appendChild(element);

            element = document.createElement('p');
            element.innerHTML = 'edit not develp ye';
            this_post.appendChild(element);

            element = document.createElement('p');
            element.innerHTML = content;
            this_post.appendChild(element);
            
            element = document.createElement('p');
            element.innerHTML = timestamp;
            this_post.appendChild(element);

            element = document.createElement('p');
            if (like_num !== 0) {
                element.innerHTML = `${like_num}&#10084;`;
            }
            else {
                element.innerHTML = '0&#9825';
            }
            this_post.appendChild(element);

            post_area.appendChild(this_post);

            checkHasNextPrev();
        });
    })

    
}

function checkHasNextPrev() {
    console.log("run checkHasNextPrev");
    fetch('/has_another', {
        method: 'GET'
    })
    .then(response => response.json())
    // .then(tmp => console.log(tmp.json()));
    .then(data => {
        console.log(data);
        if (!data["has_next"]) {
            console.log("has next");
            console.log("disabled next");
            document.querySelector('#next').setAttribute('disabled', '');
            document.querySelector('#next').classList.remove("bg-dark");
            document.querySelector('#next').classList.remove("text-light");
            document.querySelector('#next').classList.add("bg-secondary");
            document.querySelector('#next').classList.add("text-dark");
        }
        else {
            document.querySelector('#next').removeAttribute('disabled', '');
            document.querySelector('#next').classList.remove("bg-secondary");
            document.querySelector('#next').classList.remove("text-dark");
            document.querySelector('#next').classList.add("text-light");
            document.querySelector('#next').classList.add("bg-dark");
            
        }
        if (!data["has_prev"]) {
            console.log("disabled prev");
            document.querySelector('#prev').setAttribute('disabled', '');
            document.querySelector('#prev').classList.remove("bg-dark");
            document.querySelector('#prev').classList.remove("text-light");
            document.querySelector('#prev').classList.add("text-dark");
            document.querySelector('#prev').classList.add("bg-secondary");
        }
        else {
            document.querySelector('#prev').removeAttribute('disabled', '');
            document.querySelector('#prev').classList.remove("bg-secondary");
            document.querySelector('#prev').classList.remove("text-dark");
            document.querySelector('#prev').classList.add("text-light");
            document.querySelector('#prev').classList.add("bg-dark");
            
        }
    });
}