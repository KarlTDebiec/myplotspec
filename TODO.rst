Planned Changes
===============

Modest Updates
--------------
- Use add_partner_subplot in draw_subplot rather current than draw_dataset hack

Major Rewrite
-------------
- Restructure how the specification is built, making it less insane

- Current implementation:

    - Maintains a source specification (read from a yaml file)
    - Every time a function is run, 
    - Hardcoded for working with matplotlib; not resusable

- Planned implementation:

    - Build entire specification before doing anything else
    - Use plugin system to allow a series of functions to read the source
      specification sequentially 
    - Move generic parts to new submodule 'YSpec'

- YSpec plugins
    - Starts with spec = {}

    - INITIALIZE looks at source, builds structure of figures, subplots,
      and datasets, but includes nothing else

      - Plugins in general should be able to look at entire source spec and
        pull out the parts in which they are interested
      - INITIALIZE may be generic and accept arguments concerning which
        portion of the source spec to use
      - For MyPlotSpec, INITIALIZE should be told that the structure of
        interest has the form {figures: {subplots: {datasets}}}
      - Should understand slices in indexes
      - May also need to know about nrows and ncols
        - MyPlotSpec may therefore have its own initialize plugin`

    - DEFAULTS adds default arguments for each figure, subplot, and dataset

      - Loops over figures, subplots, and datasets, and adds default
        arguments to each instance
      - Actually, should not need to know about the level structure as
        INITIALIZE does, just maps names to default arguments. Levels are
        included within the defaults dictionary
      - Needs some way to inspect dataset classes to look for their own
        defaults
    - PRESETS looks at source, identifies selected presets, and applies
      them to each figure, subplot, and dataset

      - Must find some way to reconcile the ability of presets to influence
        the number and organization of figures, subplots, and datasets
      - Needs some way to inspect dataset classes to look for their own
        presets
    - MULTIPLE looks for MULTIPLE settings within each figure; applies
      appropriate arguments
    - MANUAL applies remaining specs from source

      - Reads entire source spec and applies all arguments other than those
        marked by 
    - WRITE outputs complete spec, optionally retaining PRESETS, MULTIPLE

- MyPlotSpec plugins

- DEFAULTS and PRESETS must support inheritance from superclasses

- How to layer, such that defaults and preset may be read from a CLASS that
  represents dataset x (or subplot t or figure z)?

  - Write Dataset classes to support this NOW, later work into broader
    FigureManager class
  - Dataset 
- Should dataset classes be extended (i.e. 'draw' method added?) to allow
  drawing? Perhaps use function_to_method_wrapper on a staticmethod of the
  FigureManager class

  - Probably not a good idea to modify classes, as in the long term I may
    want the same cahced dataset to be fed into multiple FigureManagers
- Should each node on the spec tree be associated with an object?
