# oomlout_oomp_footprint_src

## name

### composition

1. owner - the github / lab name of the owner
2. library - library name (.pretty folder name)
3. footprint_name - the name of the footprint (kicad_mod filename)

* note - repo name and location of .pretty in the repo are not tracked

## notes

### mirroring kicad footprints

gitlab source https://gitlab.com/kicad/libraries/kicad-footprints



### extra bits

* file -- this is the location in the repo, with both .pretty folder and .kicad_mod name
* repo -- the github json repo verbatum, the kicad repo has some gitlab things done

### oomp_key

* oomp_key -- oomp{owner}{library}{footprint_name} 
* oomp_key_extra -- oomp_footprint{owner}{library}{footprint_name} 
* oomp_key_full -- oomp_footprint{owner}{library}{footprint_name}{md5_6}
* oomp_key_simple -- {owner}{library}{footprint_name}  

## actions

* action_setup -- pulls the folder details from kitspaces directory and adds all the found repos to repo.yaml. Then clones all the repos one by one and copys the footprints to various directory structures. Then adds a yaml file for each with details and puts a readme.md in the folder with the details printed out.