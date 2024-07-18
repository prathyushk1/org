$(document).ready(function () {
alert("hiiii");
   $("#inc").click(function (e) {
   e.preventDefault();
   $count = { count }
    if ($count == 1){
         $item_id = {{ cart_item.item_id }}
         }
    else if ($count > 1){
        $item_id = {{ i.item_id }}
        }
    else{
        $item_id =0
        }
      $.ajax({
        url: '/inc_qty/',
        data: { 'item_id':$item_id },
        type: 'get',
        datatype: 'json',
        success: function (d) {
            if (d.status) {
            alert("helloooo")
            if(d.qty == 5){
            alert(d.qty)
                 $("#inc").prop('disabled', true);
                 }
            else{
            alert(d.qty)
                 $("#qty").val(d.qty)
                 }
                }
            }, error: function (d1) {
            console.log(d1)
        }

    });
    });

    $("#dsc").click(function () {
       $count = {{ count }}
    if ($count == 1){
    $item_id = {{ cart_item.item_id }}
    }
    else
        $item_id = $("#dnc").val(d.qty)

      $.ajax({
        url: '/dnc_qty/',
        data: { 'item_id':$item_id },
        type: 'get',
        datatype: 'json',
        success: function (d) {
            if (d.status) {
            if(d.qty == 1){
                 $("#dnc").prop('disabled', true);
                 }
            else{
                 $("#qty").val(d.qty);
                 }
                }
            }, error: function (d1) {
            console.log(d1)
        }
    });
    });
    });