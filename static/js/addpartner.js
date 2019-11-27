
// $('#addpartner').on('submit', addPartner());

function addpartner() {
    console.log('caught it');
    // get all the inputs into an array.
    var $inputs = $('#addpartner :input');
    var instance_id = $("#instance").attr('value');

    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    var values = {};
    $inputs.each(function() {
        values[this.name] = $(this).val();
    });
    console.log(values);
    $.ajax({
        url: '/addpartner',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({'netid': values['netid'], 'instance': instance_id}),
        success: function(data) {
            if (data != "") {
                alert(data);
                console.log('error' + data);
            }
            else {
                alert("Request to " + values['netid'] + " sent!");
                $('#partnername').html('Partner: ' + values['netid']);
                console.log('success');
            }
        }
    });
}
