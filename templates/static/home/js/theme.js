$('.page-scroll').bind('click', function(event) {
  var $anchor = $(this);
  $('html, body').stop().animate({
      scrollTop: $($anchor.attr('href')).offset().top - 64
  }, 1500, 'easeInOutExpo');
  event.preventDefault();
});

var cbpAnimatedHeader = (function() {
 var docElem = document.documentElement,
 header = document.querySelector( '.navbar-fixed-top' ),
 didScroll = false,
 changeHeaderOn = 10;
 function init() {
  window.addEventListener( 'scroll', function( event ) {
   if( !didScroll ) {
    didScroll = true;
    setTimeout( scrollPage, 250 );
   }
  }, false );
 }
 function scrollPage() {
  var sy = scrollY();
  if ( sy >= changeHeaderOn ) {
   classie.add( header, 'navbar-shrink' );
  } else {
    classie.remove( header, 'navbar-shrink' );
  }
  didScroll = false;
 }
 function scrollY() {
  return window.pageYOffset || docElem.scrollTop;
 }
 init();
})();

$('body').scrollspy({
 target: '.navbar',
 offset: 65
})

$(window).load(function() {
 $(".page-loader").fadeOut("slow");
});

$("#owl-intro-text").owlCarousel({
 singleItem : true,
 autoPlay : 6000,
 stopOnHover : true,
 navigation : false,
 navigationText : false,
 pagination : true
})

$("#owl-partners").owlCarousel({
 items : 4,
 itemsDesktop : [1199,3],
 itemsDesktopSmall : [980,2],
 itemsTablet: [768,2],
 autoPlay : 5000,
 stopOnHover : true,
 pagination : false
})

$("#owl-testimonial").owlCarousel({
 singleItem : true,
 pagination : true,
 autoHeight : true
})

$.stellar({
 horizontalScrolling: false,
 verticalScrolling: true,
});

new WOW().init();

$('.counter').counterUp({
 delay: 10,
 time: 2000
});

$(window).load(function() {
$('.portfolio_menu ul li').click(function(){
 $('.portfolio_menu ul li').removeClass('active_prot_menu');
 $(this).addClass('active_prot_menu');
});

var $container = $('#portfolio');
$container.isotope({
 itemSelector: '.col-sm-4',
 layoutMode: 'fitRows'
});

$('#filters').on( 'click', 'a', function() {
 var filterValue = $(this).attr('data-filter');
 $container.isotope({ filter: filterValue });
 return false;
});
});

$(window).scroll(function(){
 if ($(this).scrollTop() > 100) {
  $('.scrolltotop').fadeIn();
 } else {
   $('.scrolltotop').fadeOut();
 }
});

$('.scrolltotop').click(function(){
 $('html, body').animate({scrollTop : 0}, 1500, 'easeInOutExpo');
 return false;
});

$(document).on('click','.navbar-collapse.in',function(e) {
 if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
  $(this).collapse('hide');
 }
});