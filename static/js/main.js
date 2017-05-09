// function

var jeopardy = new Audio('./static/jeopardy.mp3');
jeopardy.addEventListener('ended', function() {
    this.currentTime = 0;
    this.play();
}, false);

function hideFormCard(formData){
  // form-card -> calculating-card
  $(this).hide();
  var cc = $('#calculating-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn')

  hCC = hideCalculatingCard.bind(cc)

  var endPoint = '/trip'

  $.ajax({
    type: 'POST',
    url: endPoint,
    data: formData,
    dataType: 'json',
    success: function(data){
      hCC(data);
    },
    error: function(){
      console.log('functionality not implemented');
    }
  })

}

function hideCalculatingCard(data){
  // calculating-card -> results-card
  $(this).addClass('animated fadeOut')
  $(this).hide();

  // add the data to the results card
  // debugger;
  var legs = data.legs;
  legs.forEach(function(leg, index){
    var appendStr = '<div>'
    appendStr += '<h4>' + 'Leg #' + (index + 1) + '</h4>'
    appendStr += '<ul id="leg-metadata">'
    appendStr += '<li>' + 'mode: '+ leg.mode + '</li>'
    appendStr += '<li>' + 'duration: '+ leg.duration + '</li>'
    appendStr += '<li>' + 'price_range: '+ leg.price_range + '</li>'
    appendStr += '</ul>'
    appendStr += '</div>'
    $('#results-card .card-action').append(appendStr);
  })

  $('#results-card')
    .removeAttr('hidden')
    .addClass('animated fadeIn');
  jeopardy.stop();
}

$('#directions-form').submit(function(e) {
  // override behavior of form
  $('#form-card')
    .addClass('animated fadeOut')

  var formData = $(this).serialize();
  hideFormCardPartial = hideFormCard.bind(this, formData)
  $('#form-card')
  .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', hideFormCardPartial);

  e.preventDefault();
  jeopardy.play();
});
