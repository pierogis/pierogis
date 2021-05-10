function inputHandler(){
    let imageInput = document.getElementById("image-input");
    let inputButton = document.getElementById("input-button");
    inputButton.style.display = 'none';
    var file = imageInput.files[0];

    var reader = new FileReader();
    reader.onload = function () {
        document.getElementById("image").src = reader.result;
    }
    reader.readAsDataURL(file);
}

function dropHandler(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    let image = document.getElementById("image");
    let imageInput = document.getElementById("image-input");
    imageInput.files = files

    image.file = files[0];
    imageInput

    const reader = new FileReader();
    reader.onload = (function(output, input) { return function(e) {
        output.src = e.target.result;
    }; })(image, imageInput);
    reader.readAsDataURL(files[0]);

    inputHandler()
}

function preventDefaults (e) {
    e.preventDefault()
    e.stopPropagation()
}

export function initDropArea() {
    let dropArea = document.getElementById('drop-area');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false)
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(
            eventName, () => dropArea.classList.add('highlight'), false
        );
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(
            eventName, () => dropArea.classList.remove('highlight'), false
        );
    });

    dropArea.addEventListener("drop", dropHandler, false);

    let imageInput = document.getElementById("image-input");
    imageInput.onchange = inputHandler;
}

