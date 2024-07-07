const newBookForm = document.querySelector(".new-book-form-cont form");
newBookForm.addEventListener("submit", e => {
    e.preventDefault();
});

const newBookFormSubmitBtn = document.querySelector(".new-book-form-cont form .submit");
newBookFormSubmitBtn.addEventListener("click", e => {
    e.preventDefault();
    newBookForm.submit();
});

const bookImg = document.querySelector(".book-img img");
const bookImgInput = document.querySelector(".book-img input");
bookImgInput.addEventListener("change", e => {
    const reader = new FileReader();
    reader.onload = function() {
        bookImg.src = reader.result;
    }
    reader.readAsDataURL(e.target.files[0]);
});

const newBookBtn = document.querySelector(".new-book-btn");
const newBookFormCont = document.querySelector(".new-book-form-cont");
const closeBookForm = document.querySelector(".new-book-form-cont .title img");
newBookBtn.addEventListener("click", e => {
    newBookFormCont.classList.remove("hidden");
});

closeBookForm.addEventListener("click", e => {
    newBookFormCont.classList.add("hidden");
});


