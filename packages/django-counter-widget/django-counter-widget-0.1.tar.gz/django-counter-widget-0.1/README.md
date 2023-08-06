# Counter Widget
Counter Widget is a simple widget made up of two buttons and a number input. Two buttons are used to increase and decrease the input value.

## Installation
In terminal:

    pip install django-counter-widget

Add the app in your INSTALLED_APPS settings

    INSTALLED_APPS = [
        ...
        'counter_widgets',
    ]

## How To Use
You can use the CounterWidget for your forms IntegerField.

    from counter_widgets import CounterWidget

    class YourForm(forms.Form):
        counter_field = forms.IntegerField(widget=CounterWidget)

In the template where you are rendering YourForm, include the following line

    {% include "counter_widgets/counter_script.html" %}

If you don't include the above line in the template where you are rendering the widget, the increment (+) and decrement (-) buttons will not work.

## Customising the Widget
You can create your own customized widget from Counterwidget. You can change increment text, decrement text, delta (increment/decrement amount default is 1), you can have different values ​​for increment and decrement.
In the following we have customized counter widget increment_text, decrement_text, increment_value, decrement_value

    class CustomCounterWidget(CounterWidget):
        increment_text = "Add 100"
        decrement_text = "Subtract 50"
        increment_value = 100
        decrement_value = 50
    
    class TestForm(forms.Form):
        count = forms.IntegerField(widget=CustomCounterWidget)

Another example

    class AnotherCustomCounterWidget(CounterWidget):
        increment_text = "Add Century"
        decrement_text = "Subtract Century"
        delta = 100
