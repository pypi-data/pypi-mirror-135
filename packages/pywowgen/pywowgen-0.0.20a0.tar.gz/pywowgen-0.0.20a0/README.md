# pywowgen

Create Workadventure maps and worlds (set of interconnected maps) suitable for "rc3" or "vanilla" Workadventure
instances

- Generate Maps from templates and generator scripts
- Check maps for errors and missing resources and display this in an interactive graph view
- Fix map errors using the graph view
- Apply some overwrites and fixes to generate maps which will run in default workadventure and / or the community / rc3
  edition.
- Merge resources metadata (licenses, ...) into a single file info to be used in maps

## Use the CLI

    # optionally set the env WOWGEN_EXTRA prior execution to define where all the resources go. If not set, its will be set to the operating systems temp dir
    # e.g. WOWGEN_EXTRA=/tmp/wowgen_extra

    # load external resources from git and verify installation
    pywowgen test

    # run the api
    pywowgen api --res ${WOWGEN_EXTRA}\wowgen.git\res --tmp ${WOWGEN_EXTRA}\TMP --fin ${WOWGEN_EXTRA}\sites --force True
    
    # check a resource folder
    pywowgen overview --path ${WOWGEN_EXTRA}\wowgen.git\res 
    
    # run a world build
    pywowgen world --file . ${WOWGEN_EXTRA}\wowgen.git\examples\default_pipeline.json --res ${WOWGEN_EXTRA}\wowgen.git\res --tmp .${WOWGEN_EXTRA}\wowgen.git\sites\default_pipeline --fin ${WOWGEN_EXTRA}
    
    # analyze a world build
    pywowgen check --path  ${WOWGEN_EXTRA}\wowgen.git\sites\default_pipeline

    
    