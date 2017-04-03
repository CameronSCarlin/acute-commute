function hideFormCard(){
  $(this).hide();
  var cc = $('#calculating-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn')

  hCC = hideCalculatingCard.bind(cc)
  setTimeout(hCC, 5000);
}

function hideCalculatingCard(){
  $(this).addClass('animated fadeOut')
  $(this).hide();
  $('#results-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn');
}

$('#directions-form').submit(function(e) {
  $('#form-card')
    .addClass('animated fadeOut')

  $('#form-card')
  .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', hideFormCard);

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
