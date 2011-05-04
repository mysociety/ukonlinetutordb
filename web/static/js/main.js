// Adapted from the jQuery entry on http://css-tricks.com/perfect-full-page-background-image/
$(window).load(function() {    

    var theWindow   = $(window);
    var bg          = $("#bg");
    var aspectRatio = bg.width() / bg.height();
    
    var resizeBg = function () {
        if ( (theWindow.width() / theWindow.height()) < aspectRatio ) {
            bg
              .removeClass()
              .addClass('bgheight');
        } else {
            bg
              .removeClass()
              .addClass('bgwidth');
        }
    }
    
    theWindow
      .resize( resizeBg )
      .trigger("resize");
    
});