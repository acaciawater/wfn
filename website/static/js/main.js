//@codekit-prepend "library.js";
Shadowbox.init({
    skipSetup: true,
        handleOversize: "drag",
        modal: false
});
$(document).ready(function(){

  $('#tab1').addClass('tab-active');

  $('.full-width-slider').iosSlider({
    snapToChildren: true,
    desktopClickDrag: true,

    scrollbarDrag: true,
    scrollbarContainer: '.drag-scrollbar-scroll-container',
    scrollbarMargin: 0,
    scrollbarHeight: '5px',
    scrollbarBackground: '#301948',
    scrollbarBorderRadius: 0,
    scrollbarOpacity: 1,

    onSlideChange: bannerChange

  });


  $('input[name="next"]').each(function(){
      var self = this;
      var formContainer = $(self).parents('.login-form');
      var download = $(self).val().split('download-prep=');
      if(download.length > 1){
          if(formContainer.length > 0) {
              $('h1 a', formContainer).attr('href',$('h1 a', formContainer).attr('href') + '#download-prep=' + download[1]);
          }
      }
  });

  function bannerChange(args) {
    var currentSlideNumber = args.currentSlideNumber;

    $('.tab-active').removeClass('tab-active');
    $("#tab"+currentSlideNumber).addClass('tab-active');

  }

  $('.banner-tab').click(function() {

    var tab_id = $(this).attr('id');
    var lastChar = tab_id.substr(tab_id.length - 1);

    $('.full-width-slider').iosSlider('goToSlide', lastChar);

  });

  $('.next-btn').click(function(event) {
    event.preventDefault();
    $('.full-width-slider').iosSlider('nextSlide');
  });
  $('.last-btn').click(function(event) {
    event.preventDefault();
    $('.full-width-slider').iosSlider('goToSlide', 1);
  });

  // WRAP ORDER LIST
  $( "ol li" ).wrapInner( "<span></span>");

  // SHADOWBOX
  Shadowbox.setup();

  // External links
  $("a[href^='http']:not([href^='http://www.waterfootprint.org']):not([href^='http://www.production.wfp.fabriquehq.nl']), a[href$='.pdf']").attr("target", "_blank");


  $('.sb-overlay').one('click',Shadowbox.close);

  // SELECT DROPDOWN
  $("select").simpleselect().bind("change.simpleselect", function(){
    $(".placeholder").append( "<span class='icon icon-arrow-dropdown'></span>" );
  });

  $(".placeholder").append( "<span class='icon icon-arrow-dropdown'></span>" );

  // GOOGLE CSE
  (function() {
    var cx = '009044456670657422827:epit2kjddks';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//www.google.com/cse/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();

});

$(window).load(function() {
    $(window).hashchange( function(){
        var hash = location.hash.substr(1);
        var navigate = (hash.split('navigate-prep=').length > 1) ? '#navigate-prep=' + hash.split('navigate-prep=')[1].split('&')[0] : '';
        if(hash.split('partner-login=').length > 1 && parent === window){
            Shadowbox.open({
                content: '/accounts/partner-login/' + navigate,
                player: 'iframe',
                height:     500,
                width:      555
            });
            location.hash = '';
        }
        if(hash.split('register-login').length > 1 && parent === window){
            Shadowbox.open({
                content: '/accounts/register/' + navigate,
                player: 'iframe',
                height:     550,
                width:      555
            });
            location.hash = '';
        }
        if(hash.split('navigate=').length > 1 && parent === window){
            window.location = hash.split('navigate=')[1].split('&')[0]
        }
        if(hash.split('download=').length > 1 && parent === window){
            window.open(window.location.toString().split(window.location.pathname)[0] + hash.split('download=')[1].split('&')[0], '_blank');
            location.hash = '';
            window.location.reload();
        }
        if(hash.split('success=1').length > 1 && parent != window){
            var params = '';
            if(hash.split('download-prep=').length > 1) {
                params = '#download=' + hash.split('download-prep=')[1].split('&')[0];
            }else if(hash.split('navigate-prep=').length > 1) {
                params = '#navigate=' + hash.split('navigate-prep=')[1].split('&')[0]
            }
            parent.location = parent.location.toString().split(window.location.pathname)[0] + params;
        }
        if(hash.split('download-prep=').length > 1){
            $('input[name="next"]').each(function(){
              var self = this;
              if($(self).val() === "")
                $(self).val('/accounts/logged-in/#success=1' + (hash.split('download-prep=').length > 1 ? '&download-prep=' + hash.split('download-prep=')[1].split('&')[0] : ''));
              var formContainer = $(self).parents('.login-form');
              var download = $(self).val().split('download-prep=');
              if(download.length > 1){
                  if(formContainer.length > 0) {
                      $('h1 a', formContainer).attr('href',$('h1 a', formContainer).attr('href') + '#download-prep=' + download[1].split('&')[0]);
                  }
              }
            })
        }
        if(hash.split('navigate-prep=').length > 1){
            $('input[name="next"]').each(function(){
              var self = this;
              if($(self).val() === "")
                $(self).val('/accounts/logged-in/#success=1' + (hash.split('navigate-prep=').length > 1 ? '&navigate-prep=' + hash.split('navigate-prep=')[1].split('&')[0] : ''));
              var formContainer = $(self).parents('.login-form');
              var download = $(self).val().split('navigate-prep=');
              if(download.length > 1){
                  if(formContainer.length > 0) {
                      $('h1 a', formContainer).attr('href',$('h1 a', formContainer).attr('href') + '#navigate-prep=' + download[1].split('&')[0]);
                  }
              }
            })
        }

        if(hash === 'reload'){
            window.location = window.location.toString();
        }
    });
    $(window).hashchange();
});

