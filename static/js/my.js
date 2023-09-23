// $(window).on("scroll", function () {
//     if ($(window).scrollTop()) {
//       $("nav").addClass("black", "shadow-lg");
//     } else {
//       $("nav").removeClass("black", "shadow-lg");
//     }
//   });

var nav = document.querySelector("nav");

window.addEventListener("scroll", function () {
  if (this.window.pageYOffset > 100) {
    nav.classList.add("black", "shadow");
  } else {
    nav.classList.remove("black", "shadow");
  }
});