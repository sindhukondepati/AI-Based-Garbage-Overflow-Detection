const fileInput = document.getElementById("fileInput");
const fileText = document.getElementById("fileText");

function openFilePicker() {
    fileInput.click();
}

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileText.innerText = fileInput.files[0].name;
    } else {
        fileText.innerText = "Click to upload image or video";
    }
});
