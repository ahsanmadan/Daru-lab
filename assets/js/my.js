$(window).on("scroll", function () {
    if ($(window).scrollTop()) {
      $("nav").addClass("black", "shadow-lg");
    } else {
      $("nav").removeClass("black", "shadow-lg");
    }
  });