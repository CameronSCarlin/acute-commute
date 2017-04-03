function hide_element(){
  $(this).hide();
  $('#calculating-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn');
}

$('#directions-form').submit(function(e) {
  $('#directions-card')
    .addClass('animated fadeOut')

  $('#directions-card')
  .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', hide_element);

  var formData = $(this).serialize();
  $.ajax({
    type: 'POST',
    url: '<api-endpoint>',
    data: formData,
    dataType: 'json',
    success: function(data){
      console.log(data);
    },
    error: function(){
      console.log('functionality not implemented');
    }
  })
  e.preventDefault();
});
