/*
 * cpskin_smart.js
 * Copyright (C) 2017 AuroreMariscal <aurore@affinitic.be>
 *
 * Distributed under terms of the LICENCE.txt license.
 */
$(document).ready(function() {
    var $window = $(window);
    var window_height = $window.height();
    var faceted = document.getElementsByClassName('faceted-results');

//    Parallax
   //var lastScrollTop = 0;
   // $( window ).scroll(function() {
   //     var st = $(this).scrollTop();
   //     if (st > lastScrollTop){
   //         scroll = "0";
   //     } else {
   //         scroll = "1";
   //     }
   //     lastScrollTop = st;
   //
   //     var scrolled = $(window).scrollTop();
   //     document.getElementById('portal-header').style.top = scrolled / 12 + "px";
   // });


//    Slide
    $('.actualites').find('.bloc-item').each(function() {
        $(this).find('.pageleadImage, h3, .description').each(function() {
            $(this).addClass('no-view');
        })
        $(this).find('.pageleadImage, h3, .description').each(function() {
            $(this).addClass('in-view');
        })
        
    });
    $('.agenda').each(function() {
        $(this).find('.bloc-item').each(function() {
            $(this).addClass('no-view');
        })

        $(document).scroll(function(){
            $(this).find('.bloc-item').each(function() {
                add_style($(this));
            })
        })
    });
    if (faceted !== null) {
      $(faceted).each(function() {
        $(document).scroll(function(){
            $(this).find('.event-entry').each(function() {
                add_style($(this));
            })
        })
      });
    }
    

    function add_style(el) {
        el_offset_top = el.offset().top;
        el_offset_bottom = (el_offset_top + el.outerHeight());
        var docScroll = $window.scrollTop();
        position = docScroll + (window_height/1.2);
        if( (position >= el_offset_top) && (docScroll <= el_offset_bottom) ){
            el.addClass('in-view');
        }
       
    }
    
// search
    $( ".btn-search" ).click(function(event) {
        $( "#hidden-search" ).slideToggle(
        "fast",
        function () {
               $("#searchGadget").focus();
           });
        event.preventDefault();
        });
       
       $("#portal-globalnav a[tabindex]").click(function(){
        $("#hidden-search").hide('fast');
       });
       
// move to top
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() > 300) {
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
});



