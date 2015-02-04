$( document ).ready(function() {
  $('[name="choice_field"]' ).change(function() {
     var tp = ($('[name=choice_field]:checked').val());
  if ( tp == 1){$("#alpha").show();}else{$("#alpha").hide();}
});
});