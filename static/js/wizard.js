$('.prev').click(function(){

    var prevId = $(this).parents('.tab-pane').prev().attr("id");
    $('[href=#'+prevId+']').tab('show');
    return false;
    
  })
  
  $('.next').click(function(){
  
    var nextId = $(this).parents('.tab-pane').next().attr("id");
    $('[href=#'+nextId+']').tab('show');
    return false;
    
  })
  
  // $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    
  //   //update progress
  //   var step = $(e.target).data('step');
  //   console.log(step);
  //   var percent = (parseInt(step) / 6) * 100;
  //   console.log(e.attr('weight'));
    
  //   $('.progress-bar').css({width: percent + '%'});
  //   $('.progress-bar').text("Step " + step + " of 7");
    
  //   //e.relatedTarget // previous tab
    
  // })
  $('.nav li a').on('click', function(e){
    console.log('activate');
    var step = $(e.target).data('step');
    // console.log(step);
    var weight = $(this).attr('weight');
    var steps = $(this).attr('num-steps');

    $('.progress-bar').css({width: weight + '%'});
    $('.progress-bar').text("Step " + step + " of " + steps + ": " + weight + "%");
    
  });
  
  $('.first').click(function(){
  
    $('#myWizard a:first').tab('show')
  
  })