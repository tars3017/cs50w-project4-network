document.addEventListener('DOMContentLoaded', function() {
    checkHasNextPrev();
    document.querySelector('#next').addEventListener('click', () => load_another_page('next'));
    document.querySelector('#prev').addEventListener('click', () => load_another_page('prev'));
    window.onload = updateCheck();
    
});

// window.addEventListener('haschange', function () {
//     console.log('location changed!');
//     updateCheck();
// });
function updateCheck() {
    console.log('post change!');
    checkHasNextPrev();
    update_heart();
}
function update_heart() {
    // console.log('run update_heart');
    document.querySelectorAll('.heart').forEach(heart => {
        heart.onclick = () =>{
            console.log(heart.parentElement.dataset.id);
            chang_like_status(heart.parentElement.dataset.id);
            console.log(heart.innerHTML);
            let re = /^[0-9]+/;
            let found = heart.innerHTML.match(re);
            console.log("found", Number(found)+1);
            if (heart.innerHTML.includes('❤')) {
                heart.innerHTML = heart.innerHTML.replace('❤', '♡');
                heart.innerHTML = heart.innerHTML.replace(found, Number(found)-1);
            }
            else {
                // console.log(heart.innerHTML.replace('♡', '❤'));
                heart.innerHTML = heart.innerHTML.replace('♡', '❤');
                heart.innerHTML = heart.innerHTML.replace(found, Number(found)+1);
            }
        }
    });
}
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
            const id = post.id;
            const poster = post.poster;
            const content = post.content;
            const like_num = post.like_num;
            const timestamp = post.post_time;
            const like_or_not = post.is_like;
            
            let this_post = document.createElement('div');
            this_post.className = "post round text-light bg-dark border-primary";
            this_post.setAttribute("data-id", id);
            let element = document.createElement('h6');
            
            element.innerHTML = poster;
            this_post.appendChild(element);

            // console.log(poster, document.querySelector('#personal'))
            if (document.querySelector('#personal') !== null && `<strong>${poster}</strong>` == document.querySelector('#personal').innerHTML) {
                element = document.createElement('button');
                element.className = "edit-place round text-light bg-secondary border-primary"
                // element.value = id;
                element.innerHTML = 'Edit';
                this_post.appendChild(element);
            }  

            element = document.createElement('p');
            element.innerHTML = content;
            this_post.appendChild(element);
            
            element = document.createElement('p');
            element.innerHTML = timestamp;
            this_post.appendChild(element);

            element = document.createElement('p');
            element.className = 'heart';
            if (like_or_not) {
                element.innerHTML = `${like_num}&#10084;`;
            }
            else {
                element.innerHTML = `${like_num}&#9825`;
            }
            this_post.appendChild(element);

            post_area.appendChild(this_post);

            checkHasNextPrev();
            update_heart();
        });
    })

    
}

function checkHasNextPrev() {
    // console.log("run checkHasNextPrev");
    fetch('/has_another', {
        method: 'GET'
    })
    .then(response => response.json())
    // .then(tmp => console.log(tmp.json()));
    .then(data => {
        console.log(data);
        if (!data["has_next"]) {
            // console.log("has next");
            // console.log("disabled next");
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
            // console.log("disabled prev");
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

function chang_like_status(id) {
    console.log("click hear no", id);
    fetch('/like_unlike', {
        method: 'POST',
        body: JSON.stringify({
            now_id: id
        })
    });
    // .then(tmp => {
    //     console.log(tmp);
    // });
    // .then(response => response.json)
    // .then(result => {
    //     console.log(result);
    // });
}