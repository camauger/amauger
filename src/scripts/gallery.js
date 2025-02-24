export function initGallery() {
  document.addEventListener("DOMContentLoaded", function () {
    var images = document.querySelectorAll(".gallery-item img");
    images.forEach(function (img) {
      img.addEventListener("click", function () {
        console.log("Image cliquée : " + this.alt);
      });
    });
  });
}
