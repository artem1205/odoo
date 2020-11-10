$("#library_list tr").click(function(){
var referenceid = $(this).children().closest("td").html()

    alert( referenceid);
});
