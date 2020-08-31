$(document).ready(function () {
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.modal').modal();
  $('.tabs').tabs();
  $('.datepicker').datepicker();
  $('.timepicker').timepicker();
  /*
  This line enables validation on materialize selects by displaying the otherwise hidden select element.
  The idea was taken from stackoverflow user "Imran Saleem."
  */
  $("select[required]").css({ display: "block", height: 0, padding: 0, width: 0, position: 'absolute' });
});