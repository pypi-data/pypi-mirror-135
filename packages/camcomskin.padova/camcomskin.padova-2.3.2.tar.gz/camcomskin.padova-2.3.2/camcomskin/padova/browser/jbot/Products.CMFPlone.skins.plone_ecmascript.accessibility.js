// accessibility.js
// provides global function setBaseFontSize, which is used on the
// accessibility page to set small, normal or large type.
//
// font size is stored in a "fontsize" cookie, which is read on each pageload.

/*global createCookie, readCookie */

function setBaseFontSize($fontsize, $reset) {
  var $body = jQuery('body');
  if ($reset) {
    $body.removeClass('smallText').removeClass('largeText');
    createCookie('fontsize', $fontsize, 365);
  }
  $body.addClass($fontsize);
}

function setFontHandler(e) {
  e.preventDefault();

  switch ($(this).text()) {
    case 'Normale':
      setBaseFontSize('', 1);
      break;

    case 'Piccolo':
      setBaseFontSize('smallText', 1);
      break;

    case 'Grande':
      setBaseFontSize('largeText', 1);
      break;
  }
}

jQuery(function($) {
  var $fontsize = readCookie('fontsize');
  if ($fontsize) {
    setBaseFontSize($fontsize, 0);
  }

  if ($('body.section-accessibilita')) {
    $('body.section-accessibilita ul li a:not([href])').each(function() {
      $(this).attr('href', '#');
      $(this).on('click', setFontHandler);
    });
  }
});
