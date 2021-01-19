$(document).ready(function(){
 
    function ajax_login(){
        $.ajax({
        url:'/ajaxlogin',
        data:$('form').serialize(),
        type:'POST',
        success:function(response){
            console.log(response)
        },
        error:function(error){
            console.log(error)
        }
        })
}

   $("#loginForm").submit(function(event){
   
     
    ajax_login()
   })
   
 
});