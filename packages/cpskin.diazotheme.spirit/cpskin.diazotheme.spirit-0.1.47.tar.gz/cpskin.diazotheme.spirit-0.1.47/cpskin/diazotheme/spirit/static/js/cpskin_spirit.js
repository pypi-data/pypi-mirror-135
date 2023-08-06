/*
 * cpskin_spirit.js
 * Copyright (C) 2017 AuroreMariscal <aurore@affinitic.be>
 *
 * Distributed under terms of the LICENCE.txt license.
 */
$(document).ready(function() {
    var $window = $(window);

// search
    $( ".btn-search" ).click(function(event) {

      $("#hidden-search").toggleClass("portal-search-visible portal-search-hidden");

      $( "#hidden-search" ).slideToggle(
        "fast",
        function () {
           $("#searchGadget").focus();
        });
      event.preventDefault();
    });

    function overlaySpiritDisplay(event, gallery_overlay, image){
        event.preventDefault();
        var previous = gallery_overlay.find('.overlay-previous');
        var next = gallery_overlay.find('.overlay-next');
        gallery_overlay.removeClass('hidden');
        gallery_overlay.find('.overlay-image-active').html($('<img>', {class: 'image-overlay-active', src: image.attr("href")}));
        overlaySpiritArrow(image, previous, next);
        image.addClass('active');
    }

    function overlaySpiritArrow(image, previous, next){
        image_previous = image.prev('.image-overlay');
        image_next = image.next('.image-overlay');
        if (image_previous.length == 0){
            previous.addClass('invisible');
        }
        else{
            previous.removeClass('invisible');
        }
        if (image_next.length == 0){
            next.addClass('invisible');
        }
        else{
            next.removeClass('invisible');
        }
    }

    $('.card-index-image.gallery-overlay').each( function(){
        var gallery_image = $(this);
        var gallery_overlay = $(this).find('.content-overlay');
        var previous = gallery_overlay.find('.overlay-previous');
        var next = gallery_overlay.find('.overlay-next');
        var close = gallery_overlay.find('.overlay-close');

        $(this).find('.image-overlay').click(function(event) {
            var image = $(this);
            image_active = gallery_image.find('.image-overlay.active');
            image_active.removeClass('active');
            overlaySpiritArrow(image, previous, next);
            overlaySpiritDisplay(event, gallery_overlay, image);
        });
        close.click(function(event) {
            gallery_overlay.addClass('hidden');
            gallery_overlay.find('.overlay-image-active').html('');
            image_active = gallery_image.find('.image-overlay.active');
            image_active.removeClass('active');
        });
        previous.click(function(event) {
            image_active = gallery_image.find('.image-overlay.active');
            image = image_active.prev('.image-overlay');
            if (image.length > 0){
                image_active.removeClass('active');
                overlaySpiritDisplay(event, gallery_overlay, image);
            }
        });
        next.click(function(event) {
            image_active = gallery_image.find('.image-overlay.active');
            image = image_active.next('.image-overlay');
            if (image.length > 0){
                image_active.removeClass('active');
                overlaySpiritDisplay(event, gallery_overlay, image);
            }
        });
    });

    $('.subsection-commerce-alimentation-locale #minisite-globalnav').each( function(){
        var menu = $(this);
        menu.addClass("hidden");
        menu.after("<div class='menu-button'></div>");
        $('.menu-button').click(function(){
            menu.toggleClass('hidden');
        });
    });
});



