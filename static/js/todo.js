$("#sortable").sortable();
$("#sortable").disableSelection();

countTodos();

// all done btn
$("#checkAll").click(function(){
    var id = $(this).attr('sort-id');
    console.log('id is ' + id);
    AllDone(id);
    autosave();
});

//create todo
$('.add-todo').on('keypress',function (e) {
      e.preventDefault
      if (e.which == 13) {
           if($(this).val() != ''){
           var todo = $(this).val();
           var id = $(this).attr('sort-id');
           console.log("id " + id);
            createTodo(todo, id); 
            countTodos();
           }else{
               // some validation
           }
      }
      autosave();
});
// mark task as done
$('.todolist').on('change','li input[type="checkbox"]',function(){
    if($(this).prop('checked')){
        var doneItem = $(this).parent().parent().find('label').text();
        $(this).parent().parent().parent().addClass('remove');
        done(doneItem);
        countTodos();
    }
    autosave();
});

//delete done task from "already done"
$('.todolist').on('click','.remove-item',function(){
    removeItem(this);
    autosave();
});

$('.autosave').on('click', function(){
    $(".nav li a").removeClass("active");
    $('.tab-content div').removeClass("active show")
    $(this).addClass("active");
    var href = $(this).attr('href');
    console.log('' + href);
    $('' + href).addClass('active');
    $('' + href).addClass('show');
    autosave();
});

// count tasks
function countTodos(){
    var count = $("#sortable li").length;
    $('.count-todos').html(count);
}

//create task
function createTodo(text, id){
    var markup = '<li class="ui-state-default"><div class="checkbox"><label><input type="checkbox" value="" /> '+ text +'</label></div></li>';
    console.log("sort id " + id);
    $('#sortable' + id).append(markup);
    $('.add-todo').val('');
    autosave();
}

//mark task as done
function done(doneItem){
    var done = doneItem;
    var markup = '<li>'+ done +'<button class="btn btn-default btn-xs pull-right remove-item"><span>X</span></button></li>';
    $('#done-items').append(markup);
    $('.remove').remove();
    autosave();
}

//mark all tasks as done
function AllDone(obj){
    var myArray = [];
    var id = $(obj).attr('sortid');

    $('#sortable' + id + ' li').each(function() {
         myArray.push($(this).text());   
    });

    // console.log(myArray);
    
    // add to done
    for (i = 0; i < myArray.length; i++) {
        $('#done-items').append('<li>' + myArray[i] + '<button class="btn btn-default btn-xs pull-right remove-item"><span class="glyphicon glyphicon-remove"></span></button></li>');
    }
    
    // myArray
    $('#sortable' + id + ' li').remove();
    countTodos();
    autosave();
}

//remove done task from list
function removeItem(element){
    $(element).parent().remove();
}

function autosave(){
     // console.log(document.documentElement.innerHTML);
     var instance_id = $("#instance").attr('value');
     var today = new Date();
     var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
     var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
     var dateTime = date + ' '+ time;
     $('#updateTime').html(dateTime);
     console.log(instance_id);
     $.ajax({
         url: '/savedata',
         type: 'post',
         contentType: 'application/json',
         data: JSON.stringify({'newstate' : document.documentElement.innerHTML, 'instance': instance_id}),
         success: function(data) {
            console.log('ok')
         }
     });
}

function update() {
    var instance_id = $("#instance").attr('value');
    $.ajax({
        url: '/updatepage',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({'instance': instance_id}),
        success: function(data) {
            console.log(data)
            var newDoc = document.open("text/html", "replace");
            newDoc.write(data);
            newDoc.close();
            console.log('ok 2');
        }
    });
}
