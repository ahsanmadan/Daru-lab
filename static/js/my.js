$(window).on("scroll", function () {
  if ($(window).scrollTop()) {
    $("nav").addClass("black", "shadow");
  } else {
    $("nav").removeClass("black", "shadow");
  }
});

let count = 0;
function toast() {
  count += 1;
  if (count % 2 === 1) {
    $("#toastv").show;
  } else {
    $("#toastv").hide;
  }
}
