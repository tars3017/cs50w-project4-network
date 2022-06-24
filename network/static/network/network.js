document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#next').addEventListener('click', load_next_page);
    // document.querySelector('#index').addEventListener('click', () => load_post('index'));
    // document.querySelector('#personal').addEventListener('click', () => load_post('personal'));
    // document.querySelector('#following').addEventListener('click', () => load_post('following'));
});

function load_next_page() {
    let post_area = document.querySelector('#post-area');
    var first = post_area.firstElementChild;
    while (first) {
        first.remove();
        first = post_area.firstElementChild;
    }
    console.log('here');
    fetch('/next', {
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
        });
    });
}
// function load_post(load_target) {
//     if (load_target === 'index') {
//         fetch('/index/0', {
//             method: 'GET'
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
            // data.forEach(post => {
            //     const poster = post.poster;
            //     const content = post.content;
            //     const like_num = post.like_num;
            //     const timestamp = post.post_time;

            //     const post_area = document.querySelector('#post-area');
            //     let element = document.createElement('h6');
                
            //     element.innerHTML = poster;
            //     post_area.appendChild(element);

            //     element = document.createElement('p');
            //     element.innerHTML = 'edit not develp ye';
            //     post_area.appendChild(element);

            //     element.innerHTML = content;
            //     post_area.appendChild(element);
                
            //     element = innerHTML = timestamp;
            //     post_area.appendChild(element);

            //     if (like_num !== 0) {
            //         element.innerHTML = `${like_num}&#10084;`;
            //     }
            //     else {
            //         element.innerHTML = '0&#9825';
            //     }
            //     post_area.appendChild(element);
            // })
//         });
        
//     }
//     else if (load_target === 'following') {
//         TODO
//     }
//     else {
//         TODO
//     }
// }