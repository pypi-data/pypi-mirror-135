/*
 * cpskin_spirit.js
 * Copyright (C) 2017 AuroreMariscal <aurore@affinitic.be>
 *
 * Distributed under terms of the LICENCE.txt license.
 */
$(document).ready (function() {
    var $window = $(window);
// search
  if(window.innerWidth >= 600){
     $( ".btn-search" ).click(function(event) {
    
      $("#hidden-search").toggleClass("portal-search-visible portal-search-hidden");
    
      event.preventDefault();
    });
    }
    
  var logo_url = $('#portal-logo-desktop img').attr('src');

  $(window).scroll(function(e) {
    if ($("#portal-column-content").length == 0) return;
    if ($("#mobnav-btn").is(":visible")) return;
    var scroller_anchor = $("#portal-column-content").offset().top;
    if ($(this).scrollTop() >= scroller_anchor && !$('html').hasClass('nav-is-stuck'))
    {   // Fix panel at the top of the screen when users scrolls below anchor.
      $('html').addClass('nav-is-stuck');
      $('html').addClass('nav-is-Substuck');
      top_position = 0;
      if ($('body').hasClass('in-minisite-out-portal'))
        top_position = 0;
      $('#navWrapper').css({
        'position': 'fixed',
        'top': top_position + 'px'
      });
      base_url = logo_url.split('cpskinlogo.png')[0]
      sticky_logo_url = base_url + 'cpskinlogo-sticky.png';
      $('#portal-logo-desktop img').attr('src', sticky_logo_url);
    }
    else if ($(this).scrollTop() < scroller_anchor && $('html').hasClass('nav-is-stuck'))
    {   // Put it back to its original position when users scrolls back
      $('html').removeClass('nav-is-stuck');
      $('html').removeClass('nav-is-Substuck');
      $('#navWrapper').css({
        'position': 'relative',
        'top': '0px'
        });
      if (!$('body').hasClass('in-minisite-in-portal'))
      {
        $('#portal-logo-desktop img').attr('src', logo_url);
      }
      
    }
  });
  // logo in mini site
  if ($('body').hasClass('in-minisite-in-portal')){
      base_url = logo_url.split('cpskinlogo.png')[0]
      sticky_logo_url = base_url + 'cpskinlogo-sticky.png';
      $('#portal-logo-desktop img').attr('src', sticky_logo_url);
      $('#navWrapper').addClass('minisite-collapsable');
    }
});



