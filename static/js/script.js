$(document).ready(function () {
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.modal').modal();
  $('.tabs').tabs();
  $('.datepicker').datepicker({
    autoClose: true
  });
  $('.timepicker').timepicker();
  /*
  This line enables validation on materialize selects by displaying the otherwise hidden select element.
  The idea was taken from stackoverflow user "Imran Saleem."
  */
  $("select[required]").css({ display: "block", height: 0, padding: 0, width: 0, position: 'absolute' });

  /*
  This function iterates through all the progressbars, gets its data-value, and
  sets a class(color) to the progressbar according to the data-value.
  */
  function setProgBarColor() {
    let i = 0;
    let progBar = document.getElementsByClassName("determinate")
    while (i < progBar.length) {

      let progBar = document.getElementsByClassName("determinate")[i];
      let progValue = progBar.getAttribute("data-value");
      console.log(progValue);
      if (progValue == "100%") {
        console.log("setting color")
        $(progBar).addClass("light-blue darken-4");
      }
      else if (progValue == "80%") {
        console.log("setting color")
        $(progBar).addClass("light-blue darken-3");
      }
      else if (progValue == "60%") {
        console.log("setting color")
        $(progBar).addClass("light-blue ligthen-1");
      }
      else if (progValue == "40%") {
        console.log("setting color")
        $(progBar).addClass("light-blue ligthen-3");
      }
      else {
        $(progBar).addClass("light-blue ligthen-4");
      }
      i++;
    }
  }
  setProgBarColor();
});