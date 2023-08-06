Validate Field
=======================

This is a project that is used to validate fields which is empty or it contain accurate values. Before touching the database we can check and raise appropriate error message if any mistmatch on it, else return True.

.. code-block:: bash

    1)  Check value is missed or empty
    2)  Check wether the datatype is correct or not
        2.1)    int = Specifies the integer 
        2.2)    str = Specifies the string  
        2.3)    email = Specifies the email  
        2.4)    phone = Specifies the phone number  
        2.5)    alpha = Specifies the alphabetes  
        2.6)    '' = Specifies the null value, is equal to str

Installing
=======================

.. code-block:: bash
    
    pip install validate-field

Usage
=======================
Enter received_field(values that comes from the front-end side) and required_field(list of values that need to be check in th back-end)

.. code-block:: bash

    from validate_field.validation import validate_field
    
    received_field = {
        'id':1,
        'name':"testuser",
        'email':'testmail@gmail.com',
        'mobile':'+918330069872',
        'password':"testpass@122#"
    }
    required_field = [
        ['id','int'],
        ['name','alpha'],
        ['email','email'],
        ['mobile','phone'],
        ['password','str']
    ]
   
    validation_result = validate_field(received_field, required_field)
    print(validation_result)
