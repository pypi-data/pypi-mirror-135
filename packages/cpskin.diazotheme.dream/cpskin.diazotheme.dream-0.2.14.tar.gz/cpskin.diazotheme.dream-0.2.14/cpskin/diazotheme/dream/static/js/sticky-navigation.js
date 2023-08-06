jQuery(document).ready(function($) {
 $(window).scroll(function(e) {
   if ($("#portal-column-content").length == 0) return;
   if ($("#mobnav-btn").is(":visible")) return;
   var scroller_anchor = $("#portal-column-content").offset().top;
   if ($(this).scrollTop() >= scroller_anchor && !$('html').hasClass('nav-is-stuck'))
   {   // Fix panel at the top of the screen when users scrolls below anchor.
     $('html').addClass('nav-is-stuck');
     $('html').addClass('nav-is-Substuck');
     top_position = $('#top-navigation').height();
     if ($('body').hasClass('in-minisite-out-portal'))
     top_position = 0;
     $('.container-minisite-globalnav-logo').css({
       'position': 'fixed',
       'top': top_position + 'px'          });      }
     else if ($(this).scrollTop() < scroller_anchor && $('html').hasClass('nav-is-stuck'))
     {   // Put it back to its original position when users scrolls back
       $('html').removeClass('nav-is-stuck');
       $('html').removeClass('nav-is-Substuck');
       $('.container-minisite-globalnav-logo').css({
         'position': 'relative',
         'top': '0px'
         });
       }
       });
 });