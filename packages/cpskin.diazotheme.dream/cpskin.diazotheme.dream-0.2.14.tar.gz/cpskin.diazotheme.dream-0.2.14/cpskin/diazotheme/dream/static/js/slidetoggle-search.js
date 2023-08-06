// jquery for search button in navigation 

$( document ).ready(function() {
       $( ".btn-search" ).click(function(e) {
        $( "#hidden-search" ).slideToggle(
        "fast",
        function () {
               $("#searchGadget").focus();
           });
         e.preventDefault();
        });
       
       $("#portal-globalnav a[tabindex]").click(function(){
        $("#hidden-search").hide('fast');
       });
});