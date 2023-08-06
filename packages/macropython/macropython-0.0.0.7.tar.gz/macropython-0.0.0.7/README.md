    # macropython

    class RecordMacro

        args:
            _filename : ``str`` - the file to output to.
            _startup_delay : ``float`` - the delay before recording inputs
            _enable_output : ``bool`` - should print debug info

        methods:

            logic() - the function for saving macro data
                ~ note: this method should not be used manually, it is used my the class itself

            start(startup_delay : ``float``) - use this method is called to start recording input
            args:
                startup_delay : ``float`` - this args is optional, dont pass anything to skip
            ~ note: after the recording is started, use the ESC or Escape key to stop recording

    class RecordMacro

        args:

            _filename : ``str`` - the file to load the macro from
            _startup_delay : ``float`` - the delay before recording inputs
            _enable_output : ``bool`` - should print debug info

        methods:

            start(startup_delay : ``float``) - use this function to play the macro
            args:
                startup_delay : ``float`` - this args is optional, dont pass anything to skip
            ~ note: after the recording is started, close the python program to quit playing

    class HotKeyMacro

        args:

            _data_ : ``list`` - this is a ``list`` of ``dict``
                info:

                    the ``dict``s inside the ``list`` are structured as shown below
                    {
                        'trigger' : ``str`` - the key that starts the macro

                        'file' : ``str`` - the location of the macro

                        'repeat' : ``bool`` - repeat the macro forever until the trigger is released
                            ~ note: if set to False, the macro will only once when the trigger is pressed

                        'delay' : ``float`` - time to wait before repeating the macro again
                            ~ note: will only wait if repeat is set to True
                    }


            _startup_delay : ``float`` - the delay before recording inputs
            _enable_output : ``bool`` - should print debug info
