fexception
==========

fexception is designed to provide cleaner useable exceptions. The "f" in fexception represents formatted.

The purpose of fexception is not to replace or remove traceback or exceptions but to act as a companion to increase valuable messages.

fexception allows anyone to create helper/utility/common modules that raise exceptions to get ignored when returning an exception traceback information and add the caller details into the message.

Description
===========

fexception includes every built-in Python exception and adds the ability to wrap a clean formatted structure around the exception. 
Each formatted ("f") exception can add up to five different types of exception input into the formatted exception. fexception has
multiple traceback return options.

fexception's operates like built-in Python exceptions. You raise the exception when needed, and the exception will get formatted. 
All raised exceptions will source and trackback from the original raised location. fexception supports nested formatted messages.

fexception offers five message keys to format the exception to your liking. Three keys provide string or list values to format multiple lines cleanly.
The exception message must be in dictionary format. Use the table below to set the formatted exception message. 

### message_args Usage Table:

| Key           			        | Type          | Optional | Value  									                                                            |
| --------------------------- |:-------------:|:--------:|------------------------------------------------------------------------------------- |
| main_message                | str           | no		   | The main exception message.				                                                  |
| expected_result             | str or list   | yes		   | The expected result message. (str: single line) or (list: individual split lines)    |
| returned_result			        | str or list   | yes      | The returned result message.	(str: single line) or (list: individual split lines)    |
| suggested_resolution		    | str or list   | yes      | A suggested resolution message. (str: single line) or (list: individual split lines) |
| original_exception		      | Exception     | yes      | A caught exception for additional details.                                           |

fexception includes a custom exception class that is not part of the built-in Python exceptions. This exception is called FCustomException. This exception is unique because it can add custom exceptions to the formatted message. When the exception is returned, the exception will return as your custom exception class. This class is the only class that has a possibility of six keys. The required key for this custom class is called custom_type.

Optional Features
=================
fexception offers two custom argument options to adjust the traceback output. These two options are optional and are not required to create formatted exceptions.

tb_limit: <br />
  - The first option allows the traceback to be limited by the index point. If you want no traceback, you can set it to 0, or if you wish to see the first two lines, you can select the value to 2. The default value is None, which prints all available traceback detail.
  - Setting the tb_limit to zero will remove the "Trace Details" from the exception message. Nested exceptions will still contain "Trace Details". This option may be ideal for an end user-facing message for a specific error.


caller_override: <br />
  - The second option allows you complete control over the returned formatted message and traceback. This is useful if you choose to create sub-modules to perform validation checks, but you do not want those sub-modules to show up in the traceback details.
  - This option is less common but powerful when you have nested helper modules. 
  - The adjusted traceback detail will return to the console when raised, but the back-end traceback will still know the original calls to all modules. Any inspection of the trackback directly will show all calls.
  - A tb_limit value needs to be set when enabling caller_override. Set the value to None for all output or a number to limit the returned traceback lines.

The caller_overide option must be in dictionary format. Use the table below to set option. 

### caller_override Usage Table:

| Key           			        | Type          | Optional | Value  									                                                            |
| --------------------------- |:-------------:|:--------:|------------------------------------------------------------------------------------- |
| module                      | str           | no		   | The override module.			                                                            |
| name                        | str           | no		   | The override name.    		                                                            |
| line                        | int           | no		   | The override line number.                                                            |
| tb_remove                   | str           | no		   | The traceback module name that needs to be removed.			                            |

Usage Examples
============
### Example1:
Normal exception raise.

    exc_args = {
      'main_message': 'Incorrect value was sent.',
      'expected_result': '5',
      'returned_result': '2',
      'suggested_resolution': 'Check the input source.',
    }
    raise FValueError(exc_args)

### Example2:
Exception raise with a custom exception class.<br />

    exc_args = {
      'main_message': 'Incorrect value was sent.',
      'expected_result': '5',
      'returned_result': '2',
      'suggested_resolution': 'Check the input source.',
      'custom_type': MySampleException,
    }
    raise FCustomException(exc_args)

### Example3:
Exception raise with adjusted traceback.

    exc_args = {
      'main_message': 'Incorrect value was sent.',
      'expected_result': '5',
      'returned_result': '2',
      'suggested_resolution': 'Check the input source.',
    }
    caller_override = {
      'module': 'my_module',
      'name': 'get_type,
      'line': 90,
      'tb_remove': 'helpers',
    }
    raise FValueError(exc_args, None, caller_override)

Formatted Exception Message Examples
====================================

### Example1 (tb_limit=0):

    FValueError: A problem occurred while checking the variable type.
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    -----------------------------------------------------------------Additional Information---------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    Expected Result:
      - A <class 'str'>.

    Returned Result:
      - A <class 'int'> was sent.

    Suggested Resolution:
      - Check input variable.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------

### Example2 (tb_limit=None or tb_limit=1):

    Traceback (most recent call last):
      File "C:\fexception\tests\test_fexceptions.py", line 26, in <module>
        raise FValueError(exc_args)
    FValueError: A problem occurred while checking the variable type.
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    -----------------------------------------------------------------Additional Information---------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    Expected Result:
      - A <class 'str'>.

    Returned Result:
      - A <class 'int'> was sent.

    Suggested Resolution:
      - Check input variable.

    Trace Details:
      - Exception: FValueError
      - Module: test_fexceptions
      - Name: __main__
      - Line: 26
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------

### Nested Example1 (tb_limit=0):

    FValueError: A problem occurred in the nested example.
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    -----------------------------------------------------------------Additional Information---------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    Nested Exception:

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start Original Exception~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                A problem occurred while checking the variable type.
                ------------------------------------------------------------------------------------------------------------------------------------------------------
                -----------------------------------------------------------------Additional Information---------------------------------------------------------------
                ------------------------------------------------------------------------------------------------------------------------------------------------------
                Expected Result:
                  - A <class 'str'>.

                Returned Result:
                  - A <class 'int'> was sent.

                Suggested Resolution:
                  - Check input variable.

                Trace Details:
                  - Exception: FValueError
                  - Module: test_fexceptions
                  - Name: __main__
                  - Line: 27
                ------------------------------------------------------------------------------------------------------------------------------------------------------
                ------------------------------------------------------------------------------------------------------------------------------------------------------

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End Original Exception~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Suggested Resolution:
      - Please check that you entered the correct input variable.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------

### Nested Example2 (tb_limit=None):

    Traceback (most recent call last):
      File "C:\GitHub_Repositories\fexception\tests\test_fexceptions.py", line 27, in <module>
        raise FValueError(exc_args)
    FValueError: A problem occurred while checking the variable type.
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    -----------------------------------------------------------------Additional Information---------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    Expected Result:
      - A <class 'str'>.

    Returned Result:
      - A <class 'int'> was sent.

    Suggested Resolution:
      - Check input variable.

    Trace Details:
      - Exception: FValueError
      - Module: test_fexceptions
      - Name: __main__
      - Line: 27
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------


    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "C:\GitHub_Repositories\fexception\tests\test_fexceptions.py", line 34, in <module>
        raise FValueError(exc_args)
    FValueError: A problem occurred in the nested example.
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    -----------------------------------------------------------------Additional Information---------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    Nested Exception:

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Start Original Exception~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                A problem occurred while checking the variable type.
                ------------------------------------------------------------------------------------------------------------------------------------------------------
                -----------------------------------------------------------------Additional Information---------------------------------------------------------------
                ------------------------------------------------------------------------------------------------------------------------------------------------------
                Expected Result:
                  - A <class 'str'>.

                Returned Result:
                  - A <class 'int'> was sent.

                Suggested Resolution:
                  - Check input variable.

                Trace Details:
                  - Exception: FValueError
                  - Module: test_fexceptions
                  - Name: __main__
                  - Line: 27
                ------------------------------------------------------------------------------------------------------------------------------------------------------
                ------------------------------------------------------------------------------------------------------------------------------------------------------

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~End Original Exception~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Suggested Resolution:
      - Please check that you entered the correct input variable.

    Trace Details:
      - Exception: FValueError
      - Module: test_fexceptions
      - Name: __main__
      - Line: 34
    ------------------------------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------------------------------------
  
Installation
============

From PyPI
-------------------
You can find fexception on PyPI. https://pypi.org/project/fexception/ 

Usage
=====
Once installed, add fexception as a module and select the formatted
exception option from the import.

Note: You can use * to import all formatted exception options.
