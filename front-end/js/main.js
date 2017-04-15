function hideFormCard(){
  // form-card -> calculating-card
  $(this).hide();
  var cc = $('#calculating-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn')

  hCC = hideCalculatingCard.bind(cc)
  setTimeout(hCC, 5000);
}

function hideCalculatingCard(){
  // calculating-card -> results-card
  $(this).addClass('animated fadeOut')
  $(this).hide();
  $('#results-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn');
}

$('#directions-form').submit(function(e) {
  // override behavior of form
  $('#form-card')
    .addClass('animated fadeOut')

  $('#form-card')
  .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', hideFormCard);

  endPoint = 'http://127.0.0.1:5000/trip'

  var formData = $(this).serialize();
  $.ajax({
    type: 'POST',
    url: endPoint,
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
