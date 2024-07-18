$(document).ready(function () {
  alert("hello");
    $.ajax({
        url: 'https://dummyjson.com/products/categories',
        type: 'get',
        success: function (data) {
        console.log(data);
        }, error: function (d1) {
            console.log(d1)
        }

    });
});