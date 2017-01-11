
$('.form-control').on('change invalid', function() {
    var textfield = $(this).get(0);

    // 'setCustomValidity not only sets the message, but also marks
    // the field as invalid. In order to see whether the field really is
    // invalid, we have to remove the message first
    textfield.setCustomValidity('');

    if (!textfield.validity.valid) {
      textfield.setCustomValidity('Please fill out this field.');
    }
});

