$(document).ready(function() {
  $("a.contact-nav-link").click(function() {
    moveTo(".main", 3);
    // $('html, body').animate({
    //   scrollTop: $("div.contact").offset().top
    // }, 1000, 'easeInOutExpo', function() {});
    return false;
  });
  $("a.contact-nav-link-redirect").click(function() {
    window.location = 'index.html';
    moveTo(".main", 3);
    // $('html, body').animate({
    //   scrollTop: $("div.contact").offset().top
    // }, 1000, 'easeInOutExpo', function() {});
    return false;
  });
  $("a.home-nav-link").click(function() {
    window.location = 'index.html';
    moveTo(".main", 1);
    // $('html, body').animate({
    //   scrollTop: $("div.home").offset().top
    // }, 1000, 'easeInOutExpo', function() {});
    return false;
  });

  $("div.picture-nav").hover(
    function() {
      $(this).find("div.dark-overlay").stop().fadeTo("fast", 0.0);
    }, 
    function() {
      $(this).find("div.dark-overlay").stop().fadeTo("fast", 0.5);
    });

  $("div.exec-photo").hover(
    function() {
      $(this).find("div.dark-overlay").stop().fadeTo("fast", 0.0);
      $(this).find("div.exec-name").stop().fadeTo("fast", 0.0);
      $(this).find("div.exec-position").stop().fadeTo("fast", 0.0);
    },
    function() {
      $(this).find("div.dark-overlay").stop().fadeTo("fast", 0.5);
      $(this).find("div.exec-name").stop().fadeTo("fast", 1.0);
      $(this).find("div.exec-position").stop().fadeTo("fast", 1.0);
    });

  $("div.event-photo").hover(
    function() {
      $(this).find("div.dark-overlay").stop().fadeTo("fast", 0.3);
    },
    function() {
      $(this).find("div.dark-overlay").stop().fadeTo("fast", 0.5);
    });
});