$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: 'absolute'});
  });