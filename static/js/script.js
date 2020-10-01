$(document).ready(function () {
  "use strict";

  $('.sidenav').sidenav();
  $('select').formSelect();
  $('.modal').modal();
  $('.tabs').tabs();
  $('.datepicker').datepicker({
    autoClose: true,
    minDate: new Date()
  });
  $('.timepicker').timepicker();
  $('.collapsible').collapsible();
  $('textarea').characterCounter();
  $('.tooltipped').tooltip();
  /*
  This line enables validation on materialize selects by displaying the otherwise hidden select element.
  The idea was taken from stackoverflow user "Imran Saleem."
  */
  $("select[required]").css({ display: "block", height: 0, padding: 0, width: 0, position: 'absolute' });
  $('.select-wrapper ul.select-dropdown li').off('touchend').on('touchend', function() { $(this).click(); });
  /*
  This function iterates through all the progressbars, gets its data-value, and
  sets a width and class(color) to the progressbar according to the data-value.
  */
  function setProgBar() {
    let i = 0;
    let progBar = document.getElementsByClassName("determinate");
    while (i < progBar.length) {

      let progBar = document.getElementsByClassName("determinate")[i];
      let progValue = progBar.getAttribute("data-value");
      if (progValue == "Very High") {
        $(progBar).addClass("light-green accent-3").width("100%");
      }
      else if (progValue == "High") {
        $(progBar).addClass("light-green accent-2").width("80%");
      }
      else if (progValue == "Medium") {
        $(progBar).addClass("light-blue lighten-1").width("60%");
      }
      else if (progValue == "Low") {
        $(progBar).addClass("light-blue lighten-3").width("40%");
      }
      else {
        $(progBar).addClass("orange lighten-2").width("20%");
      }
      i++;
    }
  }
  setProgBar();
  setTimeout(function () {
    $(".flashes").fadeOut('slow');
  }, 5000);


  /*
  Code for displaying/hiding back-to-top button. Taken from 
  https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
  */
  let mybutton = document.getElementById("back-to-top");

  // When the user scrolls down 500px from the top of the document, show the button
  window.onscroll = function () {
    scrollFunction();
  };

  function scrollFunction() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }

  // When the user clicks on the button, scroll to the top of the document
  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }

  $("#back-to-top").click(function () {
    topFunction();
  });
});