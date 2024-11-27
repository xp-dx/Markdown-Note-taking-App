const form = document.querySelector('form');
const titleInput = document.querySelector('.title');
const contentInput = document.querySelector('.content');

form.addEventListener('submit', (e) => {
e.preventDefault();

const title = titleInput.value;
const content = contentInput.value;

fetch('/write-note', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `title=${title}&content=${content}`,
})
.then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })

.then((data) => {
    alert('Article created successfully!');
    console.log(data);
  })
.catch((error) => {
    alert('Error creating article. More details in the console.');
    console.error(error);
  });
});