const textArea = document.getElementById("text");
const charCount = document.getElementById("charCount");
const form = document.getElementById("translateForm");
const button = document.getElementById("translateButton");


textArea.addEventListener("input", function () {

    charCount.textContent =
        `${textArea.value.length} / 1000`;

});


function clearText() {

    textArea.value = "";

    charCount.textContent = "0 / 1000";

    textArea.focus();

}


function copyTranslation() {

    const translation =
        document.getElementById("translation");

    if (!translation) {
        return;
    }

    navigator.clipboard.writeText(
        translation.innerText
    );

}


form.addEventListener("submit", function () {

    button.disabled = true;

    button.innerHTML = "Translating...";

});
