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
  $('textarea, .count').characterCounter();
  $('.tooltipped').tooltip();
  $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
  });
  
  //Set background to indicators on carousel to make them more visible.
  $(".indicators").css("background-color", "rgba(0, 0, 0, .6)");
  
  /*
  This line enables validation on materialize selects by displaying the otherwise hidden select element.
  The idea was taken from stackoverflow user "Imran Saleem."
  */
  $("select[required]").css({ display: "block", height: 0, padding: 0, width: 0, position: 'absolute' });

  /*
  This function iterates through all the progressbars, gets its data-value, and
  sets a width and class(color) to the progressbar according to the data-value.
  */
  function setProgBar() {
    let i = 0;
    let progBars = document.getElementsByClassName("determinate");
    while (i < progBars.length) {
      let progBar = progBars[i];
      let progValue = progBar.getAttribute("data-value");
      if (progValue == "Very High") {
        $(progBar).addClass("light-green accent-3").width("100%");
      }
      else if (progValue == "High") {
        $(progBar).addClass("light-green").width("80%");
      }
      else if (progValue == "Medium") {
        $(progBar).addClass("light-blue lighten-2").width("60%");
      }
      else if (progValue == "Low") {
        $(progBar).addClass("yellow accent-2").width("40%");
      }
      else {
        $(progBar).addClass("orange lighten-1").width("20%");
      }
      i++;
    }
  }
  /*
  Set background image for carousel items
  */
  function setCarouselImage() {
    let i = 0;
    let carouselImgs = document.getElementsByClassName("carousel-item");
    while (i < carouselImgs.length) {
      let carouselImg = carouselImgs[i];
      let url = carouselImg.getAttribute("data-img");
      $(carouselImg).css({ "background-image": "url(" + url + ")", "background-repeat": "no-repeat", "background-size": "cover" });
      i++;
    }
  }
  setProgBar();
  setCarouselImage();
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
  
  // Enable admin rights via function in app.py.
  $("#admin").click(function () {
    $.getJSON($SCRIPT_ROOT + '/toggle_admin',
      function (data) {
        $("#footer-heading").text(data.admin);
        $("#footer-info").text(data.info)
        setTimeout(function() {
          $("#footer-heading").text("We're on social media!");
        $("#footer-info").text("Don't forget to keep in touch with your team mates on social media.");
        }, 4000)
      });
    return false
  });
});