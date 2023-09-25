$(window).on("scroll", function () {
  if ($(window).scrollTop()) {
    $("nav").addClass("black", "shadow");
  } else {
    $("nav").removeClass("black", "shadow");
  }
});

const toastTrigger = document.getElementById("liveToastBtn");
    const toastLiveExample = document.getElementById("liveToast");

    if (toastTrigger) {
      const toastBootstrap =
        bootstrap.Toast.getOrCreateInstance(toastLiveExample);
      toastTrigger.addEventListener("click", () => {
        toastBootstrap.show();
      });
    }
