cli
===

All of the cli commands look like this.

.. code-block:: console

   $ pyrogis {filling/subcommand} {path} [-o output] [..common options] [..order options] [..togo options]

A ``filling`` is a set of ingredients that will be used to cook.
Often it just represents the named :py:class:`~pyrogis.ingredients.ingredient.Ingredient`.
A directory can be used for ``path``, in which case the program will try to cook each file in the directory.
If an ``output`` filename or dir is provided, it should match the expected output.

The following options are common to each ``filling``.
In addition, each ``filling`` or has its own set of options, seen in :doc:`menu/index`.

.. toctree::

    menu/index

*common options*
~~~~~~~~~~~~~~~~

==================== ============================================= ========== =======
arg                  description                                   default    valid
==================== ============================================= ========== =======
``filling``          define filling/ingredients to cook with       required   see menu
``path``             path to input media                           required   dir, image, animation
``-o``, ``--output`` name of the output file                       depends    ``int``
``--presave``        flag to indicate frames should be saved from  ``False``  flag
                     animations
``--async``          flag to indicate frames should be cooked      ``False``  flag
                     in an async process pool
``--processes``      number of processes to use for pool^          ``None``   ``int``
``--resume``         skip cooked frames to finish a cook task      ``False``  flag
``--frames-filter``  provide a python expression to identify       ``True``   ``bool``
                     frames to be cooked
==================== ============================================= ========== =======

If the input file is a directory or a movie file (anything animated),
the output will be an animation as well. Artifact "cooked" folder will contain frames.
If you don't understand what output type to expect from your command, don't provide ``output``.

auto pilot
""""""""""

There is an "auto pilot" preprocessing step where the program will try to determine an
effective way to cook the order.
By default, it will cook a batch of frames using ``multiprocessing``
and a batch where each frame is first saved as it's own png for input to cooking.
It compares the time these batches took to the time it took to cook without tricks.

Usually, animations will find multiprocessing to be beneficial.
In some cases, presave is used;
the file has to take a long time to open for it to be worth presaving frames

``presave``, and ``async`` skip their respective tests.

``presave`` will be ignored if dir ``path``.
If ``processes`` is provided, ``async`` is set to ``True``.
If ``async`` is provided without ``processes``, ``processes`` wil be ``os.cpu_count()``.

resume
""""""

With ``resume`` present, frames that are already in the cooked directory
and generated from the given input filename
will not be overwritten by the outputs of this command.

Three uses:
- "Pause" the program with Ctrl-c and resume with the same command
- Change the ``filling`` in the animation for any frames that weren't finished
- Recover errors if a frame failed to cook.

frames filtering
""""""""""""""""

The variables ``i`` and ``frames`` can be used in the ``frames-filter`` expression.
They represent the **index** of the frame in question and the total number of frames.
They should evaluate to ``True`` or ``False``.
Where ``True`` means the frame in question will be cooked

.. code-block:: python

   # only the frame with index 5
   i==5
   # frames indices greater than 50
   i>50
   # only even indexed frames
   i%2==0
   # frames beyond the halfway point
   i>=frames/2

Keep in mind python is 0 indexed -> frame index 5 is the 6 frame in the sequence.

*togo options*
~~~~~~~~~~~~~~

==================== ============================================= ========== =======
arg                  description                                   default    valid
==================== ============================================= ========== =======
``--fps``            fps to output an animation at                 ``25``     ``int``
                     (ignored if single frame)
``--frame-duration`` ms frame duration to output an animation with
                     (overrides fps)                               ``None``   ``float``
``--no-optimize``    if present and output would be .gif,
                     the gif is not optimized using gifsicle       ``False``  ``float``
==================== ============================================= ========== =======

Togo options apply when cooking an animation and when directly bundling frames with :ref:`togo` subcommand.

.. _togo:

togo
~~~~

*bundle a directory of frames into an animation*

.. code-block:: console

   $ pyrogis togo ./cooked --fps 50

``togo`` can be used to take this input directory and compile into a movie file.
This happens automatically for other subcommands

Doesn't work as an input in ``custom`` ``filling``.

``duration`` will override ``fps``.

The options for this can be provided to any ``filling`` if the output would be an animation.
