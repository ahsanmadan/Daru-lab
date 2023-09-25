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
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
  toastTrigger.addEventListener("click", () => {
    toastBootstrap.show();
  });
}

const homenav = `
<div class="container d-flex">
<ul class="flex-column">
<li class="me-3"><a href="">Produk</a></li>
<li class="nav-item dropdown">
  <a
    class="nav-link dropdown-toggle"
    href=""
    role="button"
    data-bs-toggle="dropdown"
    aria-expanded="false"
  >
    Tentang
  </a>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="/dampak">Dampak</a></li>
    <li><a class="dropdown-item" href="/us">Tentang Kami</a></li>
    <li><a class="dropdown-item" href="/faq">FAQ</a></li>
  </ul>
</li>
</ul>
<a href="/" class="logo" style="margin: 15px; float: none; text-align: center">
<img src="static/img/logo.png" alt="" height="40px" />
</a>
<ul></ul>
<a
style="margin-top: 27px; float: none; text-align: center"
class="cart fs-5"
href=""
><i class="fa-solid fa-cart-shopping" style="color: #ffffff"></i
></a>
</div>
  `;
