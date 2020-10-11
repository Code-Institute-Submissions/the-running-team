# Testing

The app has two main views. One for when the user is logged in, and another for when the user is not logged in. The following tables shows all the manual testing executed in both views.

## Non-logged in user views

### Navigation

**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Title|click|Display events page| |x
Events|click|Display events page| |x
The Team|click|Display team member page| |x
Log In|click|Display log in page| |x
Register|click|Display register page| |x


### Footer

**Item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Facebook icon|click|Open in new tab| |x
Twitter icon|click|Open in new tab| |x
Snapchat icon|click|Open in new tab| |x
LinkedIn icon|click|Open in new tab| |x


### Team members page
**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Member card|click|Display member details| |x
Member card|click|Hide member details| |x
Back to top button|on scroll|Display back to top button| |x

### Log in page

**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Username field|Not valid input|Red underline, unable to submit| |x
Password field|Not valid input|Red underline, unable to submit| |x
Form|Submit|Redirect to profile page| |x

### Register page 

**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Text input fields with 'required' attribute|Not valid input|Red underline, unable to submit| |x
Selects|None chosen|Error message on submit, unable to submit| |x
Image url|Non valid input|Red underline, display error message, unable to submit| |x
Form|Submit|Redirect to profile page| |x


### New workout form

**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Text input fields with 'required' attribute|Not valid input|Red underline, unable to submit| |x
Selects|None chosen|Error message on submit, unable to submit| |x
Date|Click|Display materialize date picker| |x
Time|Click|Display materialize time picker| |x
Form|Submit|Redirect to displaying workout tab| |x 

### New blog post form 

**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Title field|Not valid input|Red underline, unable to submit, display error message| |x
Content field|Not valid input|Red underline, unable to submit, display error message| |x
Form|Submit|Redirect to displaying blog posts tab| |x

### Delete workout/blogpost

**item**|**action**|**expected result**|**Fail**|**Pass**
:-----:|:-----:|:-----:|:-----:|:-----:
Delete button|click|Open modal, prompt user to double check| |x