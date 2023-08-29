import oomlout_footprint_src as oom_f_s
import kiutils


def main():

    #test()


    #oom_f_s.make_footprint_yaml()
    oom_f_s.clone_and_copy_footprints()
    #oom_f_s.documment_footprints()


def test():
    #yaml load test
    import yaml
    file = 'footprints_folder/1Bitsy/1bitsy-hardware-lib/1bitsy-basic-sl-1xx-xx-19.kicad_mod/working/working.yaml'
    with open(file, 'r') as yaml_file:
        yaml_dict = oom_f_s.yaml.load(yaml_file, Loader=oom_f_s.yaml.FullLoader)
    pass




if __name__ == '__main__':
    main()