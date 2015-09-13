$(document).ready(function() {
  if (window.location.search == "?contact") {
    moveTo(".main", 3);
  }
  $("a.contact-nav-link").click(function(e) {
    if (window.location.pathname == '/') {
      e.preventDefault();
      moveTo(".main", 3);
    } else {
      window.location = 'http://mitsbc.mit.edu/?contact';
    }
    return false;
  });
  $("a.home-nav-link").click(function(e) {
    if (window.location.pathname == '/') {
      e.preventDefault();
      moveTo(".main", 1);
    } else {
      window.location = 'http://mitsbc.mit.edu/';
    }
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
