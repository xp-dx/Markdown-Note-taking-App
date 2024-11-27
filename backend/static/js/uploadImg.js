const fileInput = document.getElementById('fileInput');
const addFileButton = document.getElementById('addFileButton');
const sendFilesButton = document.getElementById('sendFilesButton');
const filesList = document.getElementById('filesList');
const files = [];

addFileButton.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  files.push(file);
  const fileListHTML = files.map((file, index) => {
    return `<div>Файл ${index + 1}: ${file.name}</div>`;
  }).join('');
  filesList.innerHTML = fileListHTML;
  sendFilesButton.disabled = false;
});

sendFilesButton.addEventListener('click', () => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files[]', file);
  });
  // Отправка файлов на сервер
  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
  .then((response) => response.text())
  .then((message) => console.log(message))
  .catch((error) => console.error(error));
});