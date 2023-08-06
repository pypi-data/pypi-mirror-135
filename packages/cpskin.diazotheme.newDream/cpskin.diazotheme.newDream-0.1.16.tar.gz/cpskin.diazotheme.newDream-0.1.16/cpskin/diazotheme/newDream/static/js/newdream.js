// jquery for search button in navigation 

$( document ).ready(function() {

  $(function () {
      $(window).scroll(function () {
          if ($(this).scrollTop() > 600) {
              $('#scroll-to-top').fadeIn();
          } else {
              $('#scroll-to-top').fadeOut();
          }
      });

      $('#scroll-to-top a').click(function () {
          $('body,html').animate({
              scrollTop: 0
          }, 700);
          return false;
      });
  });
  $("#scroll-to-top").hide();

  // Toggle search

    $( ".btn-search , #search-btn" ).click(function(e) {
        e.stopPropagation();
        $("#hidden-search").slideToggle("fast"
        , function () {$("#searchGadget").focus(); $('#hidden-search').css('overflow','visible')}
        );
        e.preventDefault();
    });

    $("#hidden-search , #LSResult").on("click", function (event) {
        event.stopPropagation();
    });

    $(document).on("click", function () {
        $("#hidden-search").hide();
    });

  $(".toggle-button").click(function(event){
    var toggle_button_id = this.id;
    var toggle_block_id = toggle_button_id.replace("-button", "-block");
    $("#" + toggle_block_id).toggleClass("active desactive");
    event.stopImmediatePropagation()
  });

});


$(document).ready(function(){
  $(".navigation-1 #portal-globalnav ul li a:first-child").click(function(){
      var position = $(this).offset();
      $(".navTreeLevel0").css("left", "10");
  });
});


//parallax Newdream

 $(document).ready(function(){
   var controller = new ScrollMagic.Controller();
   new ScrollMagic.Scene({
     triggerElement: "#cpskin-banner",
     triggerHook: "0",
   })
   .duration('200%')
   .setTween(".banner-container >  img", {
     y: "80%", 
     ease: Linear.easeNone
   })
   .addTo(controller);

  });

  //Pause video 

 $(document).ready(function(){
  video = document.getElementById("banner-video");
  $('#toggle-video').click(function() {
    if (video.paused == false) {
        video.pause();
        $( "#toggle-video" ).removeClass( "video-play" );
        $( "#toggle-video" ).addClass( "video-pause" ).html("Pause");
    } else {
        video.play();
        $( "#toggle-video" ).removeClass( "video-pause" );
        $( "#toggle-video" ).addClass( "video-play" ).html("Play");
    }
  });
 });