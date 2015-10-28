$(document).ready(function(){

  $('a.sidemenu-item#sidemenu-user').click(function() {
    if ($('li.dropdown#sidemenu-user').hasClass('open')) {
        $('li.dropdown#sidemenu-user').removeClass('open');
    } else {
        $('li.dropdown#sidemenu-user').addClass('open');
    }
  });
  $('i.pull-right.fa.fa-angle-left').click(function() { 
    if ($('body').hasClass('sidemenu-open')) {
      $('body').removeClass('sidemenu-open'); 
      $('i.pull-right.fa.fa-angle-left').toggleClass('fa-angle-left fa-angle-right');
      $(".logo-icon").rotate({ angle:0,animateTo:270, duration: 2000, easing: $.easing.easeOutBounce })
    } else {
      $('body').addClass('sidemenu-open');
      $('i.pull-right.fa.fa-angle-right').toggleClass('fa-angle-right fa-angle-left');
      $(".logo-icon").rotate({ angle:270,animateTo:0, duration: 2000, easing: $.easing.easeOutBounce })
    }
  });
});
