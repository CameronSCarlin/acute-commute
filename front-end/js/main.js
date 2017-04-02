function hide_element(){
  // hide element
  $(this).hide();
  $('#calculating')
    .removeAttr('hidden')
    .addClass('animated fadeIn');
}

$('#directions-form').on('submit', function(e) {
  e.preventDefault();
  $('#directions-card')
    .addClass('animated fadeOut')
  $('#directions-card').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', hide_element);
});
