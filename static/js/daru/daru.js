// bagian add user

function sign_up() {
  let username = $("#username-input").val();
  let nama = $("#nama-input").val();
  let pass = $("#pass-input").val();
  console.log(username, nama, pass);
  if ((username, nama, pass == "")) {
    alert("Fill in the blanks");
    return;
  }
  $.ajax({
    type: "POST",
    url: "/save",
    data: {
      username_give: username,
      nama_give: nama,
      password_give: pass,
    },
    success: function (response) {
      if (response["result"] === "success") {
        let token = response["token"];
        $.cookie("mytoken", token, { path: "/" });
        alert("Your are signed up! Nice!");
        window.location.replace("/admin");
      } else {
        alert(response[msg]);
      }
    },
  });
}
function save_user() {
  let username = $("#username-input").val();
  let nama = $("#nama-input").val();
  let pass = $("#pass-input").val();
  console.log(username, nama, pass);
  if ((username, nama, pass == "")) {
    alert("Fill in the blanks");
    return;
  }
  $.ajax({
    type: "POST",
    url: "/save",
    data: {
      username_give: username,
      nama_give: nama,
      password_give: pass,
    },
    success: function (response) {
      if (response["result"] === "success") {
        window.location.replace("/admin/user");
        alert("user added successfully");
      } else {
        alert("user was not successfully added");
      }
    },
  });
}
// bagian login
function sign_in() {
  let username = $("#log-username").val();
  let password = $("#log-pw").val();
  $.ajax({
    type: "POST",
    url: "/sign_in",
    data: {
      username_give: username,
      password_give: password,
    },
    success: function (response) {
      if (response["result"] === "success") {
        let token = response["token"];
        $.cookie("mytoken", token, { path: "/" });
        alert("Login Sucessful!");
        window.location.href = "/admin";
      } else {
        alert(response["msg"]);
      }
    },
  });
}
function sign_out() {
  $.removeCookie("mytoken", { path: "/" });
  alert("Signed out!");
  window.location.href = "/";
}

// function listUsers() {
//   $.ajax({
//     type: "GET",
//     url: "/getUsers",
//     data: {},
//     success: function (response) {
//       let userRows = response["users"];
//       for (let i = 0; i < userRows.length; i++) {
//         let username = userRows[i]["username"];
//         let nama = userRows[i]["nama_lengkap"];

//         let temp_html = `
//         <tr>
//         <td>
//           <label class="users-table__checkbox">
//             <input type="checkbox" class="check" />
//             ${username}
//           </label>
//         </td>
//         <td>${nama}</td>
//         <td>
//           <span class="p-relative">
//           <a href=""><i class="fa-solid fa-ellipsis" style="color: #b9b9b9;"></i></a>
//             <ul class="users-item-dropdown dropdown">
//               <li><a href="##">Edit</a></li>
//               <li><a href="##">Delete</a></li>
//             </ul>
//           </span>
//         </td>
//       </tr>
//                   `;
//         $("#tableUsers").append(temp_html);
//       }
//     },
//   });
// }

function deleteUser() {
  $.ajax({
    type: "GET",
    url: "/deleteUser",
    data: {},
    success: function (response) {
      if (response["result"] === "success") {
        alert("User data successfully deleted");
        window.location.href = "/admin/user";
      } else {
        alert(response["something wrong"]);
      }
    },
  });
}

function save_product() {
  let pname = $("#pname-input").val().trim();
  let ppic = $("#ppic-input").prop("files")[0];
  let price = $("#price-input").val();
  let desc = $("#desc-input").val();
  if (!pname || !ppic || !price) {
    alert("Fill in the blanks!");
    return;
  }

  // Validasi tipe file (hanya menerima gambar)
  if (!ppic.type.startsWith("image/") || ppic.type === "image/gif") {
    alert("Files allowed are only of the image type!");
    return;
  }

  // Validasi kapasitas gambar (maksimum  megabyte)
  if (ppic.size > 2 * 1024 * 1024) {
    alert("image size exceeds the limit(Max 2 MB)");
    return;
  }

  let image = new Image();
  image.src = URL.createObjectURL(ppic);
  image.onload = function () {
    // Validasi ukuran width dan height
    if (image.width >= 500 && image.height >= 400) {
      // Gambar memenuhi syarat, lanjutkan dengan pengiriman data
      let form_data = new FormData();
      form_data.append("pname_give", pname);
      form_data.append("ppic_give", ppic);
      form_data.append("price_give", price);
      form_data.append("desc_give", desc);

      $.ajax({
        type: "POST",
        url: "/save_product",
        data: form_data,
        contentType: false,
        processData: false,
        success: function (response) {
          alert(response["msg"]);
          window.location.reload();
        },
      });
    } else {
      alert("Width size must exceed 500px and height size must exceed 400px");
    }
  };
}

// bagian delete produk
function deleteProduk(id) {
  var result = confirm("Apakah anda yakin ingin menghapus produk ini?");
  if (result) {
    $.ajax({
      type: "POST",
      url: "/deleteProduk",
      data: { id_give: id },
      success: function (response) {
        alert(response["msg"]);
        window.location.reload();
      },
    });
  }
}
function removeDecimalPoint(numString) {
  // Menghapus titik (.)
  return numString.replace(/\./g, "");
}
function editProduk(id) {
  $.ajax({
    type: "GET",
    url: `/admin/fill-edit/${id}`,
    success: function (response) {
      if (response.result === "success") {
        let post = response.post;
        $("#pname-edit").val(post.pname);
        $("#desc-edit").val(post.desc);
        $("#price-edit").val(removeDecimalPoint(post.price));

        // Set nomor posting pada tombol "Simpan Perubahan"
        $("#editProduk-button").attr("onclick", `prosesEdit(${id})`);
      } else {
        alert(response.msg);
      }
    },
  });
}
function prosesEdit(id) {
  let name= $("#pname-edit").val();
  let desc = $("#desc-edit").val();
  let price = $("#price-edit").val();
  let newPpic = $("#ppic-edit")[0].files[0];
  console.log(name,desc,price)
  // let formData = new FormData();
  // formData.append("pname-give", name);
  // formData.append("desc-give", desc);
  // formData.append("price-give", price);

  // if (newPpic) {
  //   formData.append("ppic-give", newPpic);
  // }

  // $.ajax({
  //   type: "POST",
  //   url: `/admin/prosesEdit/${id}`,
  //   data: formData,
  //   contentType: false,
  //   processData: false,
  //   success: function (response) {
  //     if (response.result === "success") {
  //       window.location.reload();
  //     } else {
  //       alert(response.msg);
  //     }
  //   },
  // });
}

function produkDetail(folder) {
  $.ajax({
    type: "GET",
    url: `/produk/${folder}`,
    success: function (response) {},
  });
}
